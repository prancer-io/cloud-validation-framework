""" Tests for snapshot azure"""
import pytest

snapshot = {
    "source": "azureStructure.json",
    "testUser": "ajeybk1@kbajeygmail.onmicrosoft.com",
    "subscriptionId": "37f11aaf-0b72-44ef-a173-308e990279da",
    "nodes": [
        {
            "snapshotId": "1",
            "type": "Microsoft.Compute/availabilitySets",
            "collection": "Microsoft.Compute",
            "path":"/resourceGroups/mno-nonprod-shared-cet-eastus2-networkWatcher/providers/Microsoft.Compute/availabilitySets/mno-nonprod-shared-cet-eastus2-tab-as03"
        }
    ]
}

snapshot_crawler =     {
      "source": "azureStructure1",
      "type": "azure",
      "testUser": "ajey.khanapuri@liquware.com",
      "subscriptionId": [
        "d34d6141-7a19-4458-b0dd-f038bb7760c1"
      ],
      "nodes": [
        {
          "masterSnapshotId": "31",
          "type": "Microsoft.Compute/availabilitySets",
          "collection": "Microsoft.Compute"
        }
      ]
    }

def mock_insert_one_document(doc, collection, dbname, check_keys=True):
    pass

def mock_get_access_token():
    return 'clientsecret'


def mock_empty_get_access_token():
    return None

def mock_get_vault_data(client_id=None):
    return None

def mock_get_web_client_data(snapshot_type, snapshot_source, snapshot_user):
    return 'client_id', None, 'sub_name', 'sub_id', 'tenant_id'

def mock1_get_web_client_data(snapshot_type, snapshot_source, snapshot_user):
    if snapshot_user =='abcd':
        return 'client_id', None, 'sub_name', 'sub_id', 'tenant_id'
    return 'client_id', 'client_secret', 'sub_name', 'sub_id', 'tenant_id'

def mock_http_get_request_happy(url, headers=None, name=""):
    data = {'a': 'b'}
    return 200, data


def mock_http_get_crawler_request(url, headers=None, name=""):
    data = {'value': [
            {
                'id': 'test_id',
                'type': 'Microsoft.Compute/availabilitySets'
            }
        ]
    }
    return 200, data


def mock_get_from_currentdata(name):
    return {}


def mock_http_get_request_error(url, headers=None, name=""):
    data = {'a': 'b'}
    return 400, data

def mock_get_client_secret():
    return None

def mock_db_json_source():
    return True

def mock_fs_json_source():
    return False

def mock_get_collection_size(collection_name):
    return 100

def mock_config_value(section, key, default=None):
    if key == 'structure':
        return 'structure'
    elif key == 'dbname':
        return 'dbname'
    return 'pytestdb'

def mock_api_version_get_document(collection, dbname=None, sort=None, query=None, limit=1):
    return [{
        "json": {
          "fileType": "structure",
          "type": "others",
          "Microsoft.RecoveryServices/locations/backupStatus": {
            "version": "2017-07-01"
          }
        }
    }]

def test_get_version_for_type(monkeypatch):
    from processor.connector.snapshot_azure import get_version_for_type
    assert None == get_version_for_type({})
    assert '2019-09-01' == get_version_for_type({'type': 'Microsoft.Network/virtualNetworks'})

    monkeypatch.setattr('processor.connector.snapshot_azure.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_azure.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_documents', mock_api_version_get_document)
    assert '2017-07-01' == get_version_for_type({'type': 'Microsoft.RecoveryServices/locations/backupStatus'})


def test_get_node_happy(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    from processor.connector.snapshot_azure import get_node
    data = {
        'type': 'Microsoft.Network/virtualNetworks',
        'snapshotId': '1',
        'path': "/resourceGroups/mno-nonprod-shared-cet-eastus2-networkWatcher/providers/"
                "Microsoft.Compute/availabilitySets/mno-nonprod-shared-cet-eastus2-tab-as03"

    }
    ret = get_node(None, None, None, data, 'abc', 'azureStructure')
    assert True == isinstance(ret, dict)
    ret = get_node('abcd', 'devtest', 'xyz', data, 'abc', 'azureStructure')
    assert True == isinstance(ret, dict)
    # assert {'resources': [{'a': 'b'}]} == ret['json']
    assert {'a': 'b'} == ret['json']


def test_get_node_error(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_error)
    from processor.connector.snapshot_azure import get_node
    data = {
        'type': 'Microsoft.Network/virtualNetworks',
        'snapshotId': '1',
        'path': "/resourceGroups/mno-nonprod-shared-cet-eastus2-networkWatcher/providers/"
                "Microsoft.Compute/availabilitySets/mno-nonprod-shared-cet-eastus2-tab-as03"

    }
    ret = get_node(None, None, None, data, 'abc', 'azureStructure')
    assert True == isinstance(ret, dict)
    ret = get_node('abcd', 'sub', 'xyz', data, 'abc', 'azureStructure')
    assert True == isinstance(ret, dict)
    assert {} == ret['json']


def test_populate_azure_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_access_token', mock_get_access_token)
    monkeypatch.setattr('processor.connector.snapshot_azure.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_web_client_data', mock1_get_web_client_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_client_secret', mock_get_client_secret)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_azure import populate_azure_snapshot
    val = populate_azure_snapshot(snapshot, 'azure')
    assert val == {'1': True}
    snapshot['testUser'] = 'abcd'
    with pytest.raises(Exception):
        populate_azure_snapshot(snapshot, 'azure')
    # val = populate_azure_snapshot(snapshot, 'azure')
    # assert val == {'1': False}

def test_populate_azure_snapshot_invalid_token(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_access_token', mock_empty_get_access_token)
    monkeypatch.setattr('processor.connector.snapshot_azure.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_client_secret', mock_get_client_secret)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_azure import populate_azure_snapshot
    snapshot["testUser"] = "ajeybk1@kbajeygmail.onmicrosoft.com"
    with pytest.raises(Exception):
        populate_azure_snapshot(snapshot, 'azure')
    # val = populate_azure_snapshot(snapshot, 'azure')
    # assert val == {'1': False}


def test_populate_azure_snapshot_invalid_secret(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_access_token', mock_get_access_token)
    monkeypatch.setattr('processor.connector.snapshot_azure.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_web_client_data', mock_get_web_client_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_client_secret', mock_get_client_secret)
    from processor.connector.snapshot_azure import populate_azure_snapshot
    snapshot["testUser"] = "ajeybk1@kbajeygmail.onmicrosoft.com"
    with pytest.raises(Exception):
        populate_azure_snapshot(snapshot, 'azure')
    # val = populate_azure_snapshot(snapshot, 'azure')
    # assert val == {'1': False}


def test_populate_azure_snapshot_crawler(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_crawler_request)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_access_token', mock_get_access_token)
    monkeypatch.setattr('processor.connector.snapshot_azure.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_web_client_data', mock1_get_web_client_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_client_secret', mock_get_client_secret)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_from_currentdata', mock_get_from_currentdata)
    
    from processor.connector.snapshot_azure import populate_azure_snapshot
    val = populate_azure_snapshot(snapshot_crawler, 'azure')
    assert val == {'31': [{'masterSnapshotId': ['31'], 'path': 'test_id', 'snapshotId': '310', 'status': 'active', 'validate': True}]}
