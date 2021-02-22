import json
import ast
import hashlib
import time
from datetime import datetime
from openapi_schema_to_json_schema import to_json_schema
from processor.helper.json.json_utils import get_field_value,json_from_file,save_json_to_file,\
    make_snapshots_dir,store_snapshot,get_field_value_with_default
from processor.logging.log_handler import getlogger
from processor.helper.config.config_utils import config_value, get_test_json_dir,framework_dir
from kubernetes import client,config
import kubernetes.client
from kubernetes.client.rest import ApiException
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.database.database import COLLECTION



logger = getlogger()


def get_kubernetes_structure_path(snapshot_source):
    """
    get_kubernetes_structure_path will get kubernetes connector file path
    from configuration file.
    """
    connector_path = '%s/%s/%s.json' % \
                 (framework_dir(),config_value('KUBERNETES','kubernetsStructureFolder'),snapshot_source)
    return connector_path

def get_kubernetes_structure_data(snapshot_source):
    kubernetes_structure_path = get_kubernetes_structure_path(snapshot_source)
    return json_from_file(kubernetes_structure_path)



def get_kube_apiserver_info():
    container_path = get_test_json_dir()
    return container_path

def make_kubernetes_snapshot_template(node,node_path,snapshot,kubernetes_snapshot_data):
    node_db_record_data= node_db_record(node,node_path,snapshot)
    node_db_record_data['json']=kubernetes_snapshot_data

    return node_db_record_data



def create_kube_apiserver_instance(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace,node_type):
    api_instance = None
    service_account_secret = get_client_secret(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace)

    if service_account_secret == "" :
        logger.error("\t\t ERROR : service account token can not find for service account : %s" % (snapshot_serviceAccount))
        # return api_instance
    cluster_url = get_field_value(kubernetes_structure_data,'clusterUrl')
    api_instance = create_kube_apiserver_instance_client(cluster_url,service_account_secret,node_type)
    return api_instance

def get_client_secret(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace):
    namespaces = get_field_value(kubernetes_structure_data,'namespaces')
    service_account_secret = ""
    for namespace in namespaces :
        service_accounts = get_field_value(namespace,'serviceAccounts')
        for service_account in service_accounts :
            if snapshot_serviceAccount == service_account['name'] and snapshot_namespace == namespace['namespace']:
                service_account_secret = get_field_value(service_account,'token')
    return service_account_secret 

def create_kube_apiserver_instance_client(cluster_url,service_account_secret,node_type):
    configuration = kubernetes.client.Configuration()
    token = '%s' % (service_account_secret)
    configuration.api_key={"authorization":"Bearer "+ token}
    configuration.host = cluster_url
    configuration.verify_ssl=False 
    configuration.debug = False
    client.Configuration.set_default(configuration)
    if node_type in ["pod","service"]:
        api_client = client.CoreV1Api()
    if node_type in ["deployment","replicaset"]:
        api_client = client.AppsV1Api()
    if node_type in ["networkpolicy"]:
        api_client = client.NetworkingV1Api()
    if node_type in ["podsecuritypolicy"]:
        api_client = client.PolicyV1beta1Api()
    if node_type in ["rolebinding"]:
        api_client = client.RbacAuthorizationV1beta1Api()
    return api_client

def get_kubernetes_snapshot_data(kubernetes_structure_data,path,node_type,snapshot_serviceAccount,snapshot_namespace):
    api_response = None
    object_name = path.split("/")[-1]
    api_instance = create_kube_apiserver_instance(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace,node_type)

    if node_type == "pod":
        api_response = api_instance.read_namespaced_pod(name=object_name,namespace=snapshot_namespace)
        # logger.info('error in calling api for getting information pod : %s', object_name)
        
    if node_type == "deployment":
        api_response = api_instance.read_namespaced_deployment(name=object_name,namespace=snapshot_namespace)
        # logger.info('error in calling api for getting information deployment : %s', object_name)
    
    if node_type == "replicaset":
        api_response = api_instance.read_namespaced_replica_set(name=object_name,namespace=snapshot_namespace)
        # logger.info('error in calling api for getting information replicaset : %s', object_name)
    
    if node_type == "service":
        api_response = api_instance.read_namespaced_service(name=object_name,namespace=snapshot_namespace)
        # logger.info('error in calling api for getting information replicaset : %s', object_name)

    if node_type == "networkpolicy":
        api_response = api_instance.read_namespaced_network_policy(name=object_name,namespace=snapshot_namespace)
        # logger.info('error in calling api for getting information networkPolicy : %s', object_name)

    if node_type == "podsecuritypolicy":
        api_response = api_instance.read_pod_security_policy(name=object_name)
        # logger.info('error in calling api for getting information  podSecurityPolicy: %s', object_name)
    
    if node_type == "rolebinding":
        api_response = api_instance.read_namespaced_role_binding(name=object_name,namespace=snapshot_namespace)
        # logger.info('error in calling api for getting information  roleBinding: %s', object_name)

    api_response_dict = todict(api_response)  
    return api_response_dict

def todict(obj):
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

def node_db_record(node,node_path,snapshot):
    collection = node['collection'] if 'collection' in node else COLLECTION
    data = {
    "structure":"kubernetes",
    "refrence": snapshot['namespace'],
    "source": snapshot['source'],
    "path":node_path,
    "timestamp": int(time.time() * 1000),
    "queryuser": snapshot['serviceAccount'],
    "checksum":hashlib.md5("{}".encode('utf-8')).hexdigest(),
    "node": node,
    "snapshotId":node['snapshotId'],
    "collection": collection.replace('.', '').lower(),
    "json": {}
    }
    return data

def get_lits(node_type,namespaces,kubernetes_structure_data,snapshot_serviceAccount):
    list_items = []
    if node_type == 'pod':
        for namespace in namespaces :
            list_item = get_list_namespaced_pods(
                namespace,
                kubernetes_structure_data,
                snapshot_serviceAccount,
                namespace,
                'pod')
            list_items.append(list_item)
    return list_items

def get_list_namespaced_pods(namespace,kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace,node_type):
        pod_items = []
        api_instance = create_kube_apiserver_instance(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace,node_type)
        api_response = api_instance.list_namespaced_pod(namespace=namespace)
        api_response_dict = todict(api_response) 
        api_response_dict_items = get_field_value(api_response_dict,'items')
        for api_response_dict_item in api_response_dict_items :
            pod_name = get_field_value(api_response_dict_item,'metadata.name')
            pod_path = "api/v1/namespaces/%s/pods/%s" % (namespace,pod_name)
            pod_items.append({
                'namespace': namespace,
                'paths':[
                    pod_path
                ]
            })
        return pod_items


def generate_crawler_snapshot(snapshot,container,node,node_type,node_path,snapshot_data,kubernetes_structure_data,snapshot_serviceAccount):
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_serviceAccount =  get_field_value(snapshot,'serviceAccount')
    snapshot_namespaces = get_field_value(snapshot,'namespace')
    snapshot_nodes = get_field_value(snapshot,'nodes')
    snapshot_masterSnapshotId = get_field_value(node,'masterSnapshotId')
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    namespace = get_field_value_with_default(snapshot,'namespace',"")
    node_type = get_field_value_with_default(node, 'type',"")

    resource_items = get_lits(
        node_type=node_type,
        namespaces=snapshot_namespaces,
        kubernetes_structure_data=kubernetes_structure_data,
        snapshot_serviceAccount=snapshot_serviceAccount)
    
    snapshot_data[node['masterSnapshotId']] = []
    for masterSnapshotId,snapshot_list in snapshot_data.items() :
        old_record = None
        if isinstance(snapshot_list, list):
            for item in snapshot_list:
                if item["path"] == node_path:
                    old_record = item
            if old_record:
                found_old_record = True
                if node['masterSnapshotId'] not in old_record['masterSnapshotId']:
                    old_record['masterSnapshotId'].append(
                        node['masterSnapshotId'])        
    for resource_item in resource_items :
        for index,resource_namespaced_item in enumerate(resource_item):
            snapshot_data[node['masterSnapshotId']].append(               {
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
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_serviceAccount = get_field_value(snapshot,'serviceAccount')
    snapshot_namespace = get_field_value(snapshot,'namespace')
    snapshot_nodes = get_field_value(snapshot,'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    kubernetes_structure_data = get_kubernetes_structure_data(snapshot_source)

    if valid_snapshotids  and snapshot_nodes:
        logger.debug(valid_snapshotids)
        try :
            for node in snapshot_nodes:
                validate = node['validate'] if 'validate' in node else True
                logger.info(node)
                node_paths = get_field_value(node,'paths')
                node_type = get_field_value(node,'type')
                for node_path in node_paths:
                    if 'snapshotId' in node:
                        if validate:
                            kubernetes_snapshot_data = get_kubernetes_snapshot_data(
                            kubernetes_structure_data,
                            node_path,node_type,
                            snapshot_serviceAccount,
                            snapshot_namespace) 
                            if kubernetes_snapshot_data :
                                error_str = kubernetes_snapshot_data.pop('error', None)
                                kubernetes_snapshot_template = make_kubernetes_snapshot_template(
                                    node,
                                    node_path,
                                    snapshot,
                                    kubernetes_snapshot_data
                                )
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
                        snapshot_data = generate_crawler_snapshot(
                            snapshot,
                            container,
                            node,
                            node_type,
                            node_path,
                            snapshot_data,
                            kubernetes_structure_data,
                            snapshot_serviceAccount)
                    


        except Exception as ex:
                logger.info('can not connect to kubernetes cluster: %s', ex)
                raise ex
    return snapshot_data