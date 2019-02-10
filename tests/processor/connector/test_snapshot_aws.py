""" Tests for snapshot azure"""
from unittest.mock import Mock

snapshot = {
    "source": "awsStructure.json",
    "type": "aws",
    "testUser": "AKIAIY7ZSPUJE4XLZ4WA",
    "nodes": [
        {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id": {"GroupNames": ["launch-wizard-1"]}
        }
    ]
}


def mock_db_json_source():
    return True

def mock_fs_json_source():
    return False

def mock_config_value(section, key, default=None):
    if key == 'structure':
        return 'structure'
    elif key == 'dbname':
        return 'dbname'
    return 'pytestdb'

def mock_snapshot_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{'json': snapshot}]


def mock_aws_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{'json':
        {
            "companyName": "abcd",
            "fileType": "structure",
            "aws_access_key_id": "AKIAIY7ZSPUJE4XLZ4WA",
            "aws_secret_access_key": "",
            "region_name": "us-west-2",
            "client": "EC2"
        }
    }]

def mock_describe_security_groups(**kwargs):
    return {'a': 'b'}

def mock_describe_regions(**kwargs):
    return {}

def mock_get_vault_data(client_id):
    return 'abcd'

class MyMock(Mock):
    def __getattr__(self, name):
        if name == 'describe_security_groups':
            return mock_describe_security_groups
        elif name == 'describe_regions':
            return mock_describe_regions
        return None


def mock_insert_one_document(doc, collection, dbname):
    pass


def mock_client(*args, **kwargs):
    return  MyMock()

def mock_invalid_client(*args, **kwargs):
    raise Exception("Unknown access key and secret")


def test_get_aws_describe_function():
    from processor.connector.snapshot_aws import get_aws_describe_function
    assert None == get_aws_describe_function({})
    assert 'describe_security_groups' == get_aws_describe_function({'type': 'security_groups'})

def test_get_checksum():
    from processor.connector.snapshot_aws import get_checksum
    assert get_checksum(None) is not None
    assert get_checksum('abc') is not None
    assert get_checksum(Mock()) is None


def test_get_node():
    from processor.connector.snapshot_aws import get_node
    awsclient = MyMock()
    val = get_node(awsclient, {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id": {"GroupNames": ["launch-wizard-1"]}
        }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id1": {"GroupNames": ["launch-wizard-1"]}
        }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "8",
        "type": "security_groups1",
        "collection": "security_groups",
        "id": {"GroupNames": ["launch-wizard-1"]}
    }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "8",
        "type1": "security_groups1",
        "collection": "security_groups",
        "id": {"GroupNames": ["launch-wizard-1"]}
    }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "9",
        "type": "regions",
        "collection": "regions",
        "id": {"RegionNames": ["us-west-2"]}
    }, 'awsStructure')
    assert val is not None

def test_db_get_aws_data(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_snapshot_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    from processor.connector.snapshot_aws import get_aws_data
    val = get_aws_data('awsStructure.json')
    assert True == isinstance(val, dict)


def test_filesystem_get_aws_data(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_snapshot_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_fs_json_source)
    from processor.connector.snapshot_aws import get_aws_data
    val = get_aws_data('awsStructure.json')
    assert True == isinstance(val, dict)


def test_populate_aws_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(snapshot)
    assert val == True


def test_exception_populate_aws_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_invalid_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(snapshot)
    assert val == False