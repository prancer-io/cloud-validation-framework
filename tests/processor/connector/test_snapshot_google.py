""" Tests for snapshot azure"""
from unittest.mock import Mock

snapshot =  {
    "source": "googleStructure",
    "type": "google",
    "testUser": "ajeybk",
    "project-id": "liquproj",
    "nodes": [
        {
            "snapshotId": "71",
            "type": "instances.get",
            "collection": "instances",
            "path":"/compute/v1/projects/liquproj/zones/us-west1-b/instances/proxy-6103b668-6761-494d-b6ac-fbc2bca4fe55"
        }
    ]
}

master_snapshot = {
    "source": "googleStructure",
    "type": "google",
    "testUser": "testuser",
    "project-id": "project-id",
    "nodes": [
        {
            "masterSnapshotId": "1",
            "type": "instances.aggregatedList",
            "collection": "instances"
        }
    ]
}

connector = {
    "organization": "company1",
    "type": "google",
    "fileType": "structure",
    "organization-unit": [
        {
            "name": "ABC",
            "accounts": [
                {
                    "account-name": "<Account Name>",
                    "account-description": "Google Cloud Engine details",
                    "project-id": "<Project Name>",
                    "account-user": "kbajey@gmail.com",
                    "users": [
                        {
                            "name": "ajeybk",
                            "gce": {
                                "type": "service_account",
                                "project_id": "<Project Id>",
                                "private_key_id": "Private Key Id",
                                "private_key": "<Actual Private Key>",
                                "client_email": "<acc>@<project>.iam.gserviceaccount.com",
                                "client_id": "<client id>",
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "client_x509_cert_url": "<As in from google.json file>"
                            },
                            "project":"<Project Name>",
                            "zone":"us-west1-b",
                            "client": "Compute"
                        }
                    ]
                }
            ]
        }
    ]
}

instanse_data = {
    "selfLink": "https://www.googleapis.com/compute/v1/projects/",
    "name": "instance-1",
    "id": "1234567890",
    "kind": "compute#instance",
    "status": "RUNNING"
}

def mock_google_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [
      {
        'json': connector
      }
    ]

def mock_read_connector_file(filepath):
    return connector

def mock_config_value(section, key, default=None):
    if key == 'structure':
        return 'structure'
    elif key == 'dbname':
        return 'dbname'
    elif section == "GOOGLE" and key == 'params':
        return 'hello'
    return 'pytestdb'

def mock_get_test_json_dir():
    return ""


def mock_error_get_checksum(data):
    raise Exception


def mock_get_dbtests_false():
    return False


def mock_make_snapshots_dir(container):
    return True


def mock_store_snapshot(snapshot_dir, data):
    pass


def mock_insert_one_document(doc, collection, dbname):
    pass


def mock_fs_json_source():
    return False


def mock_db_json_source():
    return True


def mock_file_exist(path):
  return True

def mock_get_collection_size(collection_name):
    return 100

class MyMockCompute:
  
    def mock_compute_method(self, param={}):
        return MyMockCompute()

    def get(self):
        return MyMockCompute()

    def aggregatedList(self):
        return MyMockCompute()

    def execute(self):
        return {'hello': 'world'}

class MyMockComputeNoData:
  
    def mock_compute_method(self):
        return MyMockComputeNoData()

    def get(self):
        return MyMockComputeNoData()

    def execute(self):
        return None

class MyMockServiceAccountCredentials:

    @staticmethod
    def from_json_keyfile_name(path, scopes):
        return None


class MyMockDiscovery:

  @staticmethod
  def build(service, version, credentials='', cache_discovery=False):
      return MyMockCompute()


def validate_negative_snapshot_nodes(snapshot_source):
    return None, None


def mock_negative_get_google_client_data(sub_data, snapshot_user, node_type):
    return None


def mock_get_google_client_data(sub_data, snapshot_user, node_type):
    return MyMockCompute()


def mock_save_json_to_file(object, path):
    pass


def mock_get_node(compute, node, snapshot_source, connector):
    return {
        'hello': 'world',
        'collection': 'dummy'
    }


def mock_get_google_call_function(node):
    return ["mock_compute_method"], {"params" : {}}

def mock_get_google_call_function_for_crawler(node, project_id):
    return ["mock_compute_method"], {"param" : "project-id"}

def mock_exception_get_google_call_function(node):
    return None, {}


def mock_exception_get_google_call_function2(node):
    return "hello", {}

def mock_google_param_version(path):
    return {
        "instances": ["project", "zone", "instance"],
        "projects": ["project"],
        "zones": ["project", "zone"],
        "disks": ["project", "zone", "disk"],
        "firewalls": ["project", "firewall"],
        "fileType": "structure",
        "type": "others",
        "crawlerMethods" : {
            "aggregatedList" : [
                "acceleratorTypes", "addresses", "autoscalers", "backendServices", "diskTypes", "disks", 
                "forwardingRules", "operations", "healthChecks", "instanceGroupManagers","instanceGroups", 
                "instances","interconnectAttachments","machineTypes", "networkEndpointGroups","nodeGroups","nodeTemplates",
                "nodeTypes","commitments","reservations", "resourcePolicies","routers","sslCertificates", 
                "subnetworks","targetHttpProxies","targetHttpsProxies", "targetInstances","targetPools",
                "targetVpnGateways","urlMaps","vpnGateways","vpnTunnels"
            ],
            "globalList" : [
                "backendBuckets", "externalVpnGateways", "firewalls", "httpHealthChecks", "httpsHealthChecks", 
                "images", "instanceTemplates", "interconnectLocations", "interconnects", "licenses", "networks", 
                "routes", "securityPolicies", "snapshots", "sslPolicies", "targetSslProxies", "targetTcpProxies"
            ],
            "getIamPolicy" : [
                "organizations", "projects"
            ]
        },
        "queryprameters" : {
            "firewalls.get" : {
            "project" : "projects",
                "firewall" : "firewalls"
            },
            "instances.get" : {
                "project" : "projects",
                "zone" : "zones",
                "instance" : "instances"
            },
            "projects.zones.clusters.get" : {
                "projectId" : "projects",
                "zone" : "zones",
                "clusterId" : "clusters"
            }
        },
        "crawler_queryprameters" : [
            {
                "params" : ["project"],
                "services" : [
                    "firewalls.list", "instances.aggregatedList"
                ]
            },
            {
                "params" : ["projectId", "zone"],
                "services" : ["projects.zones.clusters.list"]
            }
        ],
        "serviceName" : {
            "cloudresourcemanager" : [
                "organizations", "projects", "folders", "liens", "operations"
            ],
            "compute" : [
                "firewalls", "instances"
            ],
            "container" : [
                "projects.zones.clusters"
            ]
        }
    }



def mock_google_param_version_document(collection, query=None, dbname=None, sort=None, limit=10):
    return [
        {
            "json": mock_google_param_version(None)
        }
    ]


def test_exception_populate_google_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.validate_snapshot_nodes', validate_negative_snapshot_nodes)
    monkeypatch.setattr('processor.connector.snapshot_google.get_documents', mock_google_get_documents)
    from processor.connector.snapshot_google import populate_google_snapshot
    val = populate_google_snapshot(snapshot)
    assert val == None


def test_populate_google_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_google.get_documents', mock_google_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_google.get_google_client_data', mock_get_google_client_data)
    monkeypatch.setattr('processor.connector.snapshot_google.get_node', mock_get_node)
    monkeypatch.setattr('processor.connector.snapshot_google.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_google import populate_google_snapshot
    val = populate_google_snapshot(snapshot)
    assert val == {'71': True}
    monkeypatch.setattr('processor.connector.snapshot_google.get_google_client_data', mock_negative_get_google_client_data)
    val = populate_google_snapshot(snapshot)
    assert val == {'71': False}


def test_populate_google_snapshot_with_exception(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_google.get_documents', mock_google_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_google.get_google_client_data', mock_get_google_client_data)
    monkeypatch.setattr('processor.connector.snapshot_google.get_node', mock_get_node)
    monkeypatch.setattr('processor.connector.snapshot_google.get_dbtests', mock_get_dbtests_false)
    monkeypatch.setattr('processor.connector.snapshot_google.make_snapshots_dir', mock_make_snapshots_dir)
    monkeypatch.setattr('processor.connector.snapshot_google.store_snapshot', mock_store_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_google.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_google import populate_google_snapshot
    val = populate_google_snapshot(snapshot)


def test_get_google_client_data(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.save_json_to_file', mock_save_json_to_file)
    monkeypatch.setattr('processor.connector.snapshot_google.ServiceAccountCredentials', MyMockServiceAccountCredentials)
    monkeypatch.setattr('processor.connector.snapshot_google.discovery', MyMockDiscovery)
    test_user = snapshot['testUser']
    from processor.connector.snapshot_google import get_google_client_data
    val = get_google_client_data(connector, test_user, "instances.get")
    assert isinstance(val, MyMockCompute)


def test_get_node(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.get_google_call_function', mock_get_google_call_function)
    from processor.connector.snapshot_google import get_node
    node = snapshot['nodes'][0]
    val = get_node(MyMockCompute(), node, "file.file", snapshot)
    assert val['json'] == {'hello': 'world'}
    val = get_node(MyMockComputeNoData(), node, "file.file", snapshot)
    assert val['json'] == {}
    monkeypatch.setattr('processor.connector.snapshot_google.get_checksum', mock_error_get_checksum)
    val = get_node(MyMockCompute(), node, "file.file", snapshot)
    assert val['error'] != ''
    monkeypatch.delattr('processor.connector.snapshot_google.get_checksum')

    monkeypatch.setattr('processor.connector.snapshot_google.get_google_call_function', mock_exception_get_google_call_function)
    val = get_node(MyMockCompute(), node, "file.file", snapshot)
    assert val['json'] == {}
    monkeypatch.setattr('processor.connector.snapshot_google.get_google_call_function', mock_exception_get_google_call_function2)
    val = get_node(MyMockCompute(), node, "file.file", snapshot)
    assert val['json'] == {}

def test_get_all_nodes(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.get_google_call_function_for_crawler', mock_get_google_call_function_for_crawler)
    from processor.connector.snapshot_google import get_all_nodes
    node = master_snapshot['nodes'][0]
    val = get_all_nodes(MyMockCompute(), node, "file.file", snapshot, {})
    assert val['json'] == {'hello': 'world'}
    val = get_all_nodes(MyMockComputeNoData(), node, "file.file", snapshot, {})
    assert val['json'] == {}

def test_set_snapshot_data(monkeypatch):
    from processor.connector.snapshot_google import set_snapshot_data
    node = master_snapshot['nodes'][0]
    items = [instanse_data, instanse_data]
    snapshot_data = set_snapshot_data(node, items, {})
    print(snapshot_data)
    assert len(snapshot_data[node['masterSnapshotId']]) == 1
    assert snapshot_data[node['masterSnapshotId']][0]["masterSnapshotId"] == [node['masterSnapshotId']]

    
def test_get_call_kwargs(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_fs_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.json_from_file', mock_google_param_version)
    monkeypatch.setattr('processor.connector.snapshot_google.exists_file', mock_file_exist)
    from processor.connector.snapshot_google import get_call_kwargs
    node = snapshot['nodes'][0]
    val = get_call_kwargs(node)
    assert val == {'params': {'zone': 'us-west1-b', 'project': 'liquproj', 'instance': 'proxy-6103b668-6761-494d-b6ac-fbc2bca4fe55'}}

    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.get_documents', mock_google_param_version)
    monkeypatch.setattr('processor.connector.snapshot_google.get_documents', mock_google_param_version_document)
    from processor.connector.snapshot_google import get_call_kwargs
    node = snapshot['nodes'][0]
    val = get_call_kwargs(node)
    assert val == {'params': {'zone': 'us-west1-b', 'project': 'liquproj', 'instance': 'proxy-6103b668-6761-494d-b6ac-fbc2bca4fe55'}}

    from processor.connector.snapshot_google import get_google_call_function
    fn_str_list, kwargs = get_google_call_function(node)
    assert kwargs == {'params': {'zone': 'us-west1-b', 'project': 'liquproj', 'instance': 'proxy-6103b668-6761-494d-b6ac-fbc2bca4fe55'}}
    assert fn_str_list == ["instances", "get"]

def test_get_call_kwargs_for_crawler(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_fs_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.json_from_file', mock_google_param_version)
    monkeypatch.setattr('processor.connector.snapshot_google.exists_file', mock_file_exist)
    from processor.connector.snapshot_google import get_call_kwargs_for_crawler
    node = master_snapshot['nodes'][0]
    projectId = master_snapshot['project-id']
    val = get_call_kwargs_for_crawler(node, projectId)
    assert val == {'project': 'project-id'}

    from processor.connector.snapshot_google import get_google_call_function_for_crawler
    fn_str_list, kwargs = get_google_call_function_for_crawler(node, projectId)
    assert fn_str_list ==  ["instances", "aggregatedList"]
    assert kwargs ==  {'project': 'project-id'}

def test_get_google_data(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_google.json_source', mock_fs_json_source)
    monkeypatch.setattr('processor.connector.snapshot_google.get_test_json_dir', mock_get_test_json_dir)
    monkeypatch.setattr('processor.connector.snapshot_google.exists_file', mock_file_exist)
    monkeypatch.setattr('processor.connector.snapshot_google.json_from_file', mock_read_connector_file)

    from processor.connector.snapshot_google import get_google_data
    val = get_google_data("file.file")
    assert val == connector
