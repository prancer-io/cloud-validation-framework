import json
import ast
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



logger = getlogger()
def populate_snapshot_kubernetes(snapshot, container=None):
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_serviceAccount = get_field_value(snapshot,'serviceAccount')
    snapshot_namespace_array = get_field_value(snapshot,'namespace')
    snapshot_nodes = get_field_value(snapshot,'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    print("$%$$#$%#$%#$%#1111 : ",snapshot_data)
    try :
        for node in snapshot_nodes:
            node_paths = get_field_value(node,'paths')
            node_type = get_field_value(node,'type')
            # print(container)
            for num,node_path in enumerate(node_paths):
                kubernetes_structure_data = get_kubernetes_structure_data(snapshot_source)
                kubernetes_snapshot_data = get_kubernetes_snapshot_data(kubernetes_structure_data,node_path,node_type) 
                snapshot_dir = make_snapshots_dir(container)
                if snapshot_dir:
                    store_snapshot(snapshot_dir, node)
                # snapshot_data.append(kubernetes_snapshot_data)
                # print(kubernetes_snapshot_data)
                # save_json_to_file(kubernetes_snapshot_data,"/tmp/mehrad.json")

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

def get_kubernetes_snapshot_data(kubernetes_structure_data,path,node_type):
    if node_type == "pod":
        pod_name = path.split("/")[-1]
        namespace = path.split("/")[3]
        api_instance = create_kube_apiserver_instance(kubernetes_structure_data,path)
        api_response = api_instance.read_namespaced_pod(name=pod_name,namespace=namespace)
        # options = {"supportPatternProperties": True}
        api_response_dict = todict(api_response)
        # print(converted)
        # api_response_json = eval(api_response)
    return api_response_dict

def create_kube_apiserver_instance(kubernetes_structure_data,path):
    service_account_secret = get_client_secret(kubernetes_structure_data)
    cluster_url = get_field_value(kubernetes_structure_data,'clusterUrl')
    api_instance = create_kube_apiserver_instance_client(cluster_url,service_account_secret,path)
    return api_instance

def get_client_secret(kubernetes_structure_data):
    namespaces = get_field_value(kubernetes_structure_data,'namespaces')
    for namespace in namespaces :
        service_accounts = get_field_value(namespace,'serviceAccounts')
        for service_account in service_accounts :
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
