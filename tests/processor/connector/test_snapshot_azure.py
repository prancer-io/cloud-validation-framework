""" Tests for snapshot azure"""

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

def mock_insert_one_document(doc, collection, dbname):
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

def mock_http_get_request_happy(url, headers=None):
    data = {'a': 'b'}
    return 200, data

def mock_http_get_request_error(url, headers=None):
    data = {'a': 'b'}
    return 400, data

def mock_get_client_secret():
    return None

def test_get_version_for_type():
    from processor.connector.snapshot_azure import get_version_for_type
    assert None == get_version_for_type({})
    assert '2019-09-01' == get_version_for_type({'type': 'Microsoft.Network/virtualNetworks'})

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
    from processor.connector.snapshot_azure import populate_azure_snapshot
    val = populate_azure_snapshot(snapshot, 'azure')
    assert val == {'1': True}
    snapshot['testUser'] = 'abcd'
    val = populate_azure_snapshot(snapshot, 'azure')
    assert val == {'1': False}

def test_populate_azure_snapshot_invalid_token(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_access_token', mock_empty_get_access_token)
    monkeypatch.setattr('processor.connector.snapshot_azure.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_client_secret', mock_get_client_secret)
    from processor.connector.snapshot_azure import populate_azure_snapshot
    snapshot["testUser"] = "ajeybk1@kbajeygmail.onmicrosoft.com"
    val = populate_azure_snapshot(snapshot, 'azure')
    assert val == {'1': False}


def test_populate_azure_snapshot_invalid_secret(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_access_token', mock_get_access_token)
    monkeypatch.setattr('processor.connector.snapshot_azure.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_web_client_data', mock_get_web_client_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_azure.get_client_secret', mock_get_client_secret)
    from processor.connector.snapshot_azure import populate_azure_snapshot
    snapshot["testUser"] = "ajeybk1@kbajeygmail.onmicrosoft.com"
    val = populate_azure_snapshot(snapshot, 'azure')
    assert val == {'1': False}
