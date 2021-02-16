import json
import ast
import hashlib
import time
from datetime import datetime
from openapi_schema_to_json_schema import to_json_schema
from processor.helper.json.json_utils import get_field_value,json_from_file,save_json_to_file,\
    make_snapshots_dir,store_snapshot
from processor.logging.log_handler import getlogger
from processor.helper.config.config_utils import config_value, get_test_json_dir,framework_dir
from kubernetes import client,config
import kubernetes.client
from kubernetes.client.rest import ApiException
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.database.database import COLLECTION



logger = getlogger()
def populate_snapshot_kubernetes(snapshot, container=None):
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_serviceAccount = get_field_value(snapshot,'serviceAccount')
    snapshot_namespace = get_field_value(snapshot,'namespace')
    snapshot_nodes = get_field_value(snapshot,'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    if valid_snapshotids  and snapshot_nodes:
        logger.debug(valid_snapshotids)
        try :
            for node in snapshot_nodes:
                node_paths = get_field_value(node,'paths')
                node_type = get_field_value(node,'type')
                for node_path in node_paths:
                    kubernetes_structure_data = get_kubernetes_structure_data(snapshot_source)
                    print(node)
                    kubernetes_snapshot_data = get_kubernetes_snapshot_data(kubernetes_structure_data,node_path,node_type,snapshot_serviceAccount,snapshot_namespace) 

                    if kubernetes_snapshot_data :
                        error_str = kubernetes_snapshot_data.pop('error', None)
                        snapshot_dir = make_snapshots_dir(container)
                        node_db_record_data= node_db_record(node,node_path,snapshot)
                        node_db_record_data['json']=kubernetes_snapshot_data

                        snapshot_data[node['snapshotId']] = False if error_str else True
                        if snapshot_dir:
                            store_snapshot(snapshot_dir, node_db_record_data)

                get_kube_apiserver_info(node_paths,snapshot_source)
        except Exception as ex:
                logger.info('can not connect to kubernetes cluster: %s', ex)
                raise ex
    return snapshot_data
    # print(snapshot_nodes)


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



def get_kube_apiserver_info(path,snapshot_source):
    container_path = get_test_json_dir()
    # print(container_path)

def get_kubernetes_snapshot_data(kubernetes_structure_data,path,node_type,snapshot_serviceAccount,snapshot_namespace):
    api_response = None
    if node_type == "pod":
        pod_name = path.split("/")[-1]
        namespace = path.split("/")[3]
        api_instance = create_kube_apiserver_instance(kubernetes_structure_data,path,snapshot_serviceAccount,snapshot_namespace)
        try : 
            api_response = api_instance.read_namespaced_pod(name=pod_name,namespace=namespace)
        except Exception as ex:
                logger.info('error in calling api: %s', ex)
                raise ex
        api_response_dict = todict(api_response)
    return api_response_dict

def create_kube_apiserver_instance(kubernetes_structure_data,path,snapshot_serviceAccount,snapshot_namespace):
    api_instance = None
    service_account_secret = get_client_secret(kubernetes_structure_data,snapshot_serviceAccount,snapshot_namespace)

    if service_account_secret == "" :
        logger.error("\t\t ERROR : service account token can not find for service account : %s" % (snapshot_serviceAccount))
        # return api_instance
    cluster_url = get_field_value(kubernetes_structure_data,'clusterUrl')
    api_instance = create_kube_apiserver_instance_client(cluster_url,service_account_secret,path)
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

def create_kube_apiserver_instance_client(cluster_url,service_account_secret,path):
    configuration = kubernetes.client.Configuration()
    token = '%s' % (service_account_secret)
    configuration.api_key={"authorization":"Bearer "+ token}
    configuration.host = cluster_url
    configuration.verify_ssl=False 
    configuration.debug = False
    client.Configuration.set_default(configuration)
    api_client = client.CoreV1Api()
    return api_client

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