import json
import ast
import sys
import hashlib
import time
import os
import pymongo
from datetime import datetime
from processor.helper.config.rundata_utils import get_dbtests, get_from_currentdata
from processor.helper.json.json_utils import get_field_value,json_from_file,\
    make_snapshots_dir,store_snapshot,get_field_value_with_default,STRUCTURE,\
    collectiontypes
from processor.logging.log_handler import getlogger
from processor.helper.config.config_utils import config_value,framework_dir, EXCLUSION
from kubernetes import client,config
import kubernetes.client
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.database.database import insert_one_document,\
    COLLECTION, DATABASE, DBNAME, get_collection_size, create_indexes,sort_field,\
    get_documents
import traceback
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.snapshot_base import Snapshot
from processor.connector.vault import get_vault_data

Cache_secret = ""
Cache_namespace = ""


logger = getlogger()



def get_kubernetes_structure_path(snapshot_source):
    """
    get_kubernetes_structure_path will get kubernetes connector file path
    from configuration file.
    """
    folder = config_value('KUBERNETES','kubernetesStructureFolder')
    if folder:
        connector_path = '%s/%s/%s.json' % (framework_dir(), folder, snapshot_source)
    else:
        connector_path = '%s/%s.json' % (framework_dir(), snapshot_source)
    return connector_path

def get_kubernetes_structure_data(snapshot_source):
    """
    get_kubernetes_structure_data going to get structure data from connector 
    file which specified in snapshot as source field.
    Return structure data as json dictionary
    """
    kubernetes_structure_data = {}
    if json_source():
        qry = {'name': snapshot_source}
        dbname = config_value('MONGODB', 'dbname')
        sort = [sort_field('timestamp', False)]
        collection =config_value(DATABASE, collectiontypes[STRUCTURE])
        structure_docs = get_documents(collection=collection , dbname=dbname, sort= sort, query=qry, limit=1)
        logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, STRUCTURE, len(structure_docs))
        if structure_docs and len(structure_docs):
            kubernetes_structure_data = structure_docs[0]['json']
    else:
        kubernetes_structure_path = get_kubernetes_structure_path(snapshot_source)
        kubernetes_structure_data = json_from_file(kubernetes_structure_path)

    return kubernetes_structure_data

def make_kubernetes_snapshot_template(snapshot,node,kubernetes_snapshot_data):
    """
    make_kubernetes_snapshot_template prepare the data for db records and add data which got from 
    kubernetes cluster.
    This function is required  if we need to add kubernetes data to mongo db 
    """
    node_db_record_data= node_db_record(snapshot,node)
    node_db_record_data['json']=kubernetes_snapshot_data

    return node_db_record_data



def create_kube_apiserver_instance(snapshot,node):
    """
    create_kube_apiserver_instance creating kubernetes apiserver instance to have 
    communication and get response kubernetes apiserver 
    """
    snapshot_serviceAccount = get_field_value(snapshot,'serviceAccount')
    snapshot_namespace = get_field_value(snapshot,'namespace')
    node_type =  get_field_value(node,'type')
    snapshot_source = get_field_value(snapshot,'source')
    kubernetes_structure_data = get_kubernetes_structure_data(snapshot_source)
    api_instance = None
    service_account_secret = get_client_secret(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace)

    cluster_url = get_field_value(kubernetes_structure_data,'clusterUrl')
    api_instance = create_kube_apiserver_instance_client(cluster_url,service_account_secret,node_type)
    return api_instance

def get_client_secret(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace):
    """
    get_client_secret get service account from master snapshot and will 
    compare with other service accounts which allocated in kubernetes
    structure file and get secret of service account if it’s exist in
    structure file. Also check environment variables if service account
    secret isn’t exist in structure file with the name got from snap shot file.
    This function return secret as string which will use to get connection with 
    kubernetes cluster.

    """
    global Cache_namespace,Cache_secret
    if snapshot_namespace  == Cache_namespace:
        return Cache_secret


    namespaces = get_field_value(kubernetes_structure_data,'namespaces')
    service_account_secret = ""
    for namespace in namespaces :
        service_accounts = get_field_value(namespace,'serviceAccounts')
        for service_account in service_accounts :
            if snapshot_serviceAccount == service_account['name'] and namespace['namespace'] in snapshot_namespace :
                service_account_secret = get_field_value(service_account,'secret')
                if service_account_secret is not None:
                    Cache_secret= service_account_secret
                    Cache_namespace = snapshot_namespace
                    return service_account_secret
                else :
                    service_account_secret = get_vault_data(service_account['id'])
                    if  service_account_secret is not None:
                        Cache_secret= service_account_secret
                        Cache_namespace = snapshot_namespace
            

    
   
            

    
    if service_account_secret == "" :
        logger.error("\t\t ERROR : can not find secret for service account : %s" % (snapshot_serviceAccount))

    return service_account_secret 

def create_kube_apiserver_instance_client(cluster_url,service_account_secret,node_type):
    """ 
    Kubernetes library have several core kinds for getting data with cluster api server.
    For each Object type we have different core and we should use those function to get
    correct and reliable result. create_kube_apiserver_instance_client function pass 
    core instance due to node type.
    """
    node_type=node_type.lower()
    configuration = kubernetes.client.Configuration()
    token = '%s' % (service_account_secret)
    configuration.api_key={"authorization":"Bearer "+ token}
    configuration.host = cluster_url
    configuration.verify_ssl=False 
    configuration.debug = False
    client.Configuration.set_default(configuration)
    if node_type in ["pod","service","serviceaccount"]:
        api_client = client.CoreV1Api()
    if node_type in ["deployment","replicaset"]:
        api_client = client.AppsV1Api()
    if node_type in ["networkpolicy"]:
        api_client = client.NetworkingV1Api()
    if node_type in ["podsecuritypolicy"]:
        api_client = client.PolicyV1beta1Api()
    if node_type in ["rolebinding","role","clusterrole","clusterrolebinding"]:
        api_client = client.RbacAuthorizationV1beta1Api()
    return api_client

def get_kubernetes_snapshot_data(snapshot,node):
    """
    get_kubernetes_snapshot_data get api instance and due to snapshot and
    node and will request the data from kubernetes cluster.
    Snapshot file should have path in nodes so get_kubernetes_snapshot_data
    can use it here to find out which kind of object in which name space we need to get. 
    Also this function can use path to request the data from kubernetes apiserver.
    Some of the objects does not have any namespace so this function should 
    be able find out the  name space from path.
    In this function also kubernetes library exception are handled to find if
    any error happened.
    """
    path=  get_field_value(node,'paths')[0]
    node_type = get_field_value(node,'type')
    api_response = None
    object_name = path.split("/")[-1]
    snapshot_namespace = path.split("/")[3]
    api_instance = create_kube_apiserver_instance(snapshot,node)
    try:
        if node_type == "pod":
            snapshot_namespace = path.split("/")[3]
            api_response = api_instance.read_namespaced_pod(name=object_name,namespace=snapshot_namespace)

        if node_type == "deployment":
            snapshot_namespace = path.split("/")[4]
            api_response = api_instance.read_namespaced_deployment(name=object_name,namespace=snapshot_namespace)

        if node_type == "replicaset":
            snapshot_namespace = path.split("/")[4]
            api_response = api_instance.read_namespaced_replica_set(name=object_name,namespace=snapshot_namespace)

        if node_type == "service":
            snapshot_namespace = path.split("/")[3]
            api_response = api_instance.read_namespaced_service(name=object_name,namespace=snapshot_namespace)

        if node_type == "networkpolicy":
            snapshot_namespace = path.split("/")[4]
            api_response = api_instance.read_namespaced_network_policy(name=object_name,namespace=snapshot_namespace)

        if node_type == "podsecuritypolicy":
            api_response = api_instance.read_pod_security_policy(name=object_name)

        if node_type == "rolebinding":
            snapshot_namespace = path.split("/")[4]
            api_response = api_instance.read_namespaced_role_binding(name=object_name,namespace=snapshot_namespace)

        if node_type == "role":
            snapshot_namespace = path.split("/")[4]
            api_response = api_instance.read_namespaced_role(name=object_name,namespace=snapshot_namespace)
        
        if node_type == "clusterrolebinding":
            api_response = api_instance.read_cluster_role_binding(name=object_name)
        
        if node_type == "clusterrole":
            api_response = api_instance.read_cluster_role(name=object_name)
        
        if node_type == "serviceaccount":
            snapshot_namespace = path.split("/")[3]
            api_response = api_instance.read_namespaced_service_account(name=object_name,namespace=snapshot_namespace)

    except Exception as ex :
        logger.info('\t\tERROR : error in calling api for getting information %s : %s',node_type, object_name)
        logger.info('\t\tERROR : %s',ex)
        print(traceback.format_exc())

        
    api_response_dict = todict(api_response)  
    return api_response_dict

def todict(obj):
    """
    todict function convert data to serialized json.
    """
    if hasattr(obj, 'attribute_map'):
        result = {}
        for k,v in getattr(obj, 'attribute_map').items():
            val = getattr(obj, k)
            if val is not None:
                result[v] = todict(val)
        return result
    elif type(obj) == list:
        return [todict(x) for x in obj]
    elif type(obj) == datetime:
        return str(obj)
    else:
        return obj

def node_db_record(snapshot,node): 
    """
    node_db_record add additional fields to prepare the data for inserting 
    in database.
    """
    collection = node['collection'] if 'collection' in node else COLLECTION
    data = {
    "structure":"kubernetes",
    "reference": snapshot['namespace'],
    "contentType": "json",
    "source": snapshot['source'],
    "paths": get_field_value(node,"paths"),
    "timestamp": int(time.time() * 1000),
    "queryuser": snapshot['serviceAccount'],
    "checksum":hashlib.md5("{}".encode('utf-8')).hexdigest(),
    "node": node,
    "snapshotId":node['snapshotId'],
    "collection": collection.replace('.', '').lower(),
    "json": {}
    }

    return data

def get_lits(snapshot,node):
    node_type = get_field_value(node,'type')
    master_snapshot_func = {
        'pod' : get_list_namespaced_pods,
        'networkpolicy' : get_list_namespaced_network_policy,
        'podsecuritypolicy' : get_list_namespaced_pod_security_policy,
        'role':get_list_namespaced_role,
        'rolebinding' : get_list_namespaced_role_binding,
        'clusterrole':get_list_cluster_role,
        'clusterrolebinding' : get_list_cluster_role_binding,
        'serviceaccount' : get_list_namespaced_service_account,
    }
    list_item=[]
    try:
         return master_snapshot_func[node_type](snapshot,node)

    except Exception as ex :
        logger.info('\t\tERROR : error in calling api for getting information %s ',node_type)
        logger.info('\t\tERROR : %s',ex)
        print(traceback.format_exc())

    return list_item

def get_list_namespaced_pods(snapshot,node):

    snapshot_namespaces = get_field_value(snapshot,'namespace')
    pod_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_namespaced_pod(namespace=snapshot_namespace)
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            pod_name = get_field_value(api_response_dict_item,'metadata.name')
            pod_path = "api/v1/namespaces/%s/pods/%s" % (snapshot_namespace,pod_name)
            pod_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    pod_path
                ]
            })
    return pod_items

def get_list_namespaced_network_policy(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    network_policy_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_namespaced_network_policy(namespace=snapshot_namespace)
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            network_policy_name = get_field_value(api_response_dict_item,'metadata.name')
            network_policy_path = "apis/networking.k8s.io/v1/namespaces/%s/networkpolicies/%s" % (snapshot_namespace,network_policy_name)
            network_policy_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    network_policy_path
                ]
            })
    return network_policy_items

def get_list_namespaced_pod_security_policy(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    pod_security_policy_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_pod_security_policy()
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            pod_security_policy_name = get_field_value(api_response_dict_item,'metadata.name')
            pod_security_policy_path = "apis/policy/v1beta1/podsecuritypolicies/%s" % (pod_security_policy_name)
            pod_security_policy_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    pod_security_policy_path
                ]
            })
    return pod_security_policy_items

def get_list_namespaced_role(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    role_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_namespaced_role(namespace=snapshot_namespace)
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            role_binding_name = get_field_value(api_response_dict_item,'metadata.name')
            role_binding_path = "apis/rbac.authorization.k8s.io/v1beta1/namespaces/%s/roles/%s" % (snapshot_namespace,role_binding_name)
            role_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    role_binding_path
                ]
            })
    return role_items


def get_list_namespaced_role_binding(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    role_binding_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_namespaced_role_binding(namespace=snapshot_namespace)
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            role_binding_name = get_field_value(api_response_dict_item,'metadata.name')
            role_binding_path = "apis/rbac.authorization.k8s.io/v1beta1/namespaces/%s/rolebindings/%s" % (snapshot_namespace,role_binding_name)
            role_binding_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    role_binding_path
                ]
            })
    return role_binding_items

def get_list_cluster_role(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    cluster_role_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_cluster_role()
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            cluster_role_name = get_field_value(api_response_dict_item,'metadata.name')
            cluster_role_path = "apis/rbac.authorization.k8s.io/v1beta1/clusterroles/%s" % (cluster_role_name)
            cluster_role_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    cluster_role_path
                ]
            })
    return cluster_role_items

def get_list_cluster_role_binding(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    cluster_role_binding_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_cluster_role()
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            cluster_role_binding_name = get_field_value(api_response_dict_item,'metadata.name')
            cluster_role_binding_path = "apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindings/%s" % (cluster_role_binding_name)
            cluster_role_binding_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    cluster_role_binding_path
                ]
            })
    return cluster_role_binding_items

def get_list_namespaced_service_account(snapshot,node):
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    service_account_items = []
    api_instance = create_kube_apiserver_instance(snapshot,node)
    for snapshot_namespace in snapshot_namespaces:
        api_response = api_instance.list_namespaced_service_account(namespace=snapshot_namespace)
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            service_account_name = get_field_value(api_response_dict_item,'metadata.name')
            service_account_path = "api/v1/namespaces/%s/serviceaccounts/%s" % (snapshot_namespace,service_account_name)
            service_account_items.append({
                'namespace': snapshot_namespace,
                'paths':[
                    service_account_path
                ]
            })
    return service_account_items

def generate_crawler_snapshot(snapshot,node,snapshot_data):
    node_type= get_field_value(node,'type')
    node_type = get_field_value_with_default(node, 'type',"")
    resource_items = []
    resource_items=get_lits(snapshot=snapshot,node=node)

    exclusions = get_from_currentdata(EXCLUSION).get('exclusions', [])
    resourceExclusions = {}
    for exclusion in exclusions:
        if 'exclusionType' in exclusion and exclusion['exclusionType'] and exclusion['exclusionType'] == 'resource':
            if 'paths' in exclusion and isinstance(exclusion['paths'], list):
                resourceExclusions[tuple(exclusion['paths'])] = exclusion

    snapshot_data[node['masterSnapshotId']] = []
    for index,resource_namespaced_item in enumerate(resource_items) :
        if isinstance(resource_namespaced_item['paths'], str):
            key = tuple([resource_namespaced_item['paths']])
        elif isinstance(resource_namespaced_item['paths'], list):
            key = tuple(resource_namespaced_item['paths'])
        else:
            key = None
        if key and key in resourceExclusions:
            logger.warning("Excluded from resource exclusions: %s", resource_namespaced_item['paths'])
            continue
        snapshot_data[node['masterSnapshotId']].append({
                        "masterSnapshotId" : [node['masterSnapshotId']],
                        "snapshotId": '%s%s_%s' % (node['masterSnapshotId'],resource_namespaced_item['namespace'], str(index)),
                        "type": node_type,
                        "collection": node['collection'],
                        "paths": resource_namespaced_item['paths'],
                        "status" : "active",
                        "validate" : node['validate'] if 'validate' in node else True
                    })
    return snapshot_data



def populate_kubernetes_snapshot(snapshot, container=None):
    snapshot_nodes = get_field_value(snapshot,'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    dbname = config_value('MONGODB', 'dbname')
    if valid_snapshotids  and snapshot_nodes:
        logger.debug(valid_snapshotids)
        try :
            for node in snapshot_nodes:
                validate = node['validate'] if 'validate' in node else True
                logger.info(node)
                if 'snapshotId' in node:
                    if validate:
                        kubernetes_snapshot_data = get_kubernetes_snapshot_data(snapshot,node) 
                        if kubernetes_snapshot_data :
                            error_str = kubernetes_snapshot_data.pop('error', None)
                            kubernetes_snapshot_template = make_kubernetes_snapshot_template(
                                snapshot,
                                node,
                                kubernetes_snapshot_data
                            )
                            if get_dbtests():
                                if get_collection_size(kubernetes_snapshot_template['collection']) == 0:
                                    #Creating indexes for collection
                                    create_indexes(
                                        kubernetes_snapshot_template['collection'], 
                                        config_value(DATABASE, DBNAME), 
                                        [
                                            ('snapshotId', pymongo.ASCENDING),
                                            ('timestamp', pymongo.DESCENDING)
                                        ]
                                    )
                                    create_indexes(
                                        kubernetes_snapshot_template['collection'], 
                                        config_value(DATABASE, DBNAME), 
                                        [
                                            ('_id', pymongo.DESCENDING),
                                            ('timestamp', pymongo.DESCENDING),
                                            ('snapshotId', pymongo.ASCENDING)
                                        ]
                                    )
                                insert_one_document(kubernetes_snapshot_template, kubernetes_snapshot_template['collection'], dbname,check_keys=False)
                            
                            snapshot_dir = make_snapshots_dir(container)
                            if snapshot_dir:
                                store_snapshot(snapshot_dir, kubernetes_snapshot_template)                                
                            if "masterSnapshotId" in node :
                                snapshot_data[node['snapshotId']] = node['masterSnapshotId']
                            elif "snapshotId" in node :
                                snapshot_data[node['snapshotId']] = False if error_str else True
                        else:
                            node['status'] = 'inactive'
                elif 'masterSnapshotId' in node:
                    snapshot_data = generate_crawler_snapshot(snapshot,node,snapshot_data)
                


        except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error('can not connect to kubernetes cluster: %s ', ex )
                logger.error('\t ERROR INFO : \n \tfile name : %s\n \tline : %s\n \ttype : %s\n \tobject : %s',fname,exc_tb.tb_lineno,exc_type,exc_obj)
                print(traceback.format_exc())
                raise ex
    return snapshot_data
