""" Tests for snapshot custom"""
import os
from tests.conftest import data_dict
from unittest import mock

frameworkdir = '/tmp'

class Popen:

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd

    def communicate(self, input=None, timeout=None):
        return "", None


def repo_exception():
    raise Exception("Repo clone Exception")

def mock_insert_one_document(doc, collection, dbname):
    pass

def mock_get_test_json_dir():
    return frameworkdir

def mock_json_source():
    return True

def mock_false_json_source():
    return False

def mock_get_vault_data(client_id):
    return 'abcd'

def mock_empty_get_vault_data(client_id):
    return None

def mock_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "_id": "5c24af787456217c485ad1e6",
        "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
        "collection": "microsoftcompute",
        "json":{
            "id": 124,
            "location": "eastus2",
            "name": "mno-nonprod-shared-cet-eastus2-tab-as03"
        },
        "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
        "snapshotId": 1,
        "timestamp": 1545908086831
    }]


def test_get_node(create_temp_json, create_temp_dir):
    from processor.connector.snapshot_custom import get_node
    data = {
        'type': 'json',
        'snapshotId': '1',
        'path': "a/b/c"
    }
    ret = get_node('/tmp', data, 'parameterStructure', 'master')
    assert True == isinstance(ret, dict)
    assert {} == ret['json']
    newpath = create_temp_dir()
    os.makedirs('%s/%s' % (newpath, data['path']))
    fname = create_temp_json('%s/%s' % (newpath, data['path']))
    data['path'] = '%s/%s' % (data['path'], fname)
    ret = get_node(newpath, data, 'parameterStructure', 'master')
    assert True == isinstance(ret, dict)
    assert data_dict == ret['json']


def test_terraform_get_node(create_terraform, create_temp_dir):
    from processor.connector.snapshot_custom import get_node
    data = {
        "type": "terraform",
        'snapshotId': '1',
        'path': "a/b/c"
    }
    terr_data = [
        'name="azrcterrafstr02"',
        'locatio="neastus2"',
        'resourceGroup="core-terraf-auto-rg"',
        'containerName="states"'
    ]
    terr_data_dict = {
        'name': "azrcterrafstr02",
        'locatio': "neastus2",
        'resourceGroup': "core-terraf-auto-rg",
        'containerName': "states"
    }
    ret = get_node('/tmp', data, 'terraform', 'master')
    assert True == isinstance(ret, dict)
    assert {} == ret['json']
    newpath = create_temp_dir()
    os.makedirs('%s/%s' % (newpath, data['path']))
    fname = create_terraform('%s/%s' % (newpath, data['path']), '\n'.join(terr_data))
    data['path'] = '%s/%s' % (data['path'], fname)
    ret = get_node(newpath, data, 'terraform', 'master')
    assert True == isinstance(ret, dict)
    assert ret['json'] == terr_data_dict

    data["type"] = "terraform1"
    ret = get_node(newpath, data, 'terraform', 'master')
    assert True == isinstance(ret, dict)
    assert ret['json'] == {}

def ignoretest_valid_clone_dir(create_temp_dir):
    from processor.connector.snapshot_custom import valid_clone_dir
    newpath = create_temp_dir()
    exists, empty = valid_clone_dir(newpath)
    assert True == exists
    assert True == empty
    exists, empty = valid_clone_dir('%s/a/b/c' % newpath)
    assert True == exists
    assert True == empty
    # create_temp_json(newpath)
    exists, empty = valid_clone_dir(newpath)
    assert True == exists
    assert False == empty
    exists, empty = valid_clone_dir('/a/b/c')
    assert False == exists
    assert False == empty


def test_get_custom_data_database(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_custom.get_documents', mock_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_custom.json_source', mock_json_source)
    from processor.connector.snapshot_custom import get_custom_data
    snapshot = get_custom_data('abc.json')
    assert snapshot is not None


def test_get_custom_data_filesystem(create_temp_dir, create_temp_json, monkeypatch):
    global frameworkdir
    monkeypatch.setattr('processor.connector.snapshot_custom.json_source', mock_false_json_source)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_test_json_dir', mock_get_test_json_dir)
    from processor.connector.snapshot_custom import get_custom_data
    tmpdir = create_temp_dir()
    frameworkdir = '%s/a/b/c' % tmpdir
    os.makedirs(frameworkdir)
    testfile = create_temp_json('%s/a/b' % tmpdir)
    snapshot = get_custom_data(testfile)
    assert snapshot is not None


def test_populate_custom_snapshot(create_temp_dir, create_temp_json, monkeypatch):
    global frameworkdir
    monkeypatch.setattr('processor.connector.snapshot_custom.json_source', mock_false_json_source)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_test_json_dir', mock_get_test_json_dir)
    monkeypatch.setattr('processor.connector.snapshot_custom.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_custom.Popen', Popen)
    from processor.connector.snapshot_custom import populate_custom_snapshot
    tmpdir = create_temp_dir()
    frameworkdir = '%s/a/b/c' % tmpdir
    os.makedirs(frameworkdir)
    param_structure = {
        "companyName": "abcd",
        "gitProvider": "https://ebizframework.visualstudio.com/whitekite/_git/whitekite",
        "repoCloneAddress": "/tmp/m",
        "branchName": "master",
        "username": "abcd"
    }
    testfile = create_temp_json('%s/a/b' % tmpdir,data=param_structure)
    snapshot = {
        "source": testfile,
        "type": "custom",
        "nodes": [
            {
                "snapshotId": "3",
                "collection": "Microsoft.Keyvault",
                "path": "realm/azure/validation/container1/sample-db-record.json"
            }
        ]
    }
    snapshot1 = {
        "source": "a2.json",
        "type": "custom",
        "nodes": []
    }
    with mock.patch('processor.connector.snapshot_custom.Repo', autospec=True) as RepoMockHelper:
        RepoMockHelper.return_value.clone_from.return_value = None
        snapshot_data = populate_custom_snapshot(snapshot)
        assert snapshot_data == {'3': False}
        snapshot_data = populate_custom_snapshot(snapshot1)
        assert snapshot_data == {}


def test_username_populate_custom_snapshot(create_temp_dir, create_temp_json, monkeypatch):
    global frameworkdir
    monkeypatch.setattr('processor.connector.snapshot_custom.json_source', mock_false_json_source)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_test_json_dir', mock_get_test_json_dir)
    monkeypatch.setattr('processor.connector.snapshot_custom.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_vault_data', mock_empty_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_custom.Popen', Popen)
    from processor.connector.snapshot_custom import populate_custom_snapshot
    tmpdir = create_temp_dir()
    frameworkdir = '%s/a/b/c' % tmpdir
    os.makedirs(frameworkdir)
    param_structure = {
        "companyName": "abcd",
        "gitProvider": "https://ebizframework.visualstudio.com/whitekite/_git/whitekite",
        "repoCloneAddress": "/tmp/m",
        "branchName": "master",
        "username": "abcd"
    }
    testfile = create_temp_json('%s/a/b' % tmpdir,data=param_structure)
    snapshot = {
        "source": testfile,
        "type": "custom",
        "nodes": [
            {
                "snapshotId": "3",
                "collection": "Microsoft.Keyvault",
                "path": "realm/azure/validation/container1/sample-db-record.json"
            }
        ]
    }
    with mock.patch('processor.connector.snapshot_custom.Repo', autospec=True) as RepoMockHelper:
        RepoMockHelper.return_value.clone_from.return_value = None
        snapshot_data = populate_custom_snapshot(snapshot)
        assert snapshot_data == {'3': False}

def test_populate_custom_snapshot_exception(create_temp_dir, create_temp_json, monkeypatch):
    global frameworkdir
    monkeypatch.setattr('processor.connector.snapshot_custom.json_source', mock_false_json_source)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_test_json_dir', mock_get_test_json_dir)
    monkeypatch.setattr('processor.connector.snapshot_custom.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_custom.Popen', Popen)
    from git import Repo
    from processor.connector.snapshot_custom import populate_custom_snapshot
    tmpdir = create_temp_dir()
    frameworkdir = '%s/a/b/c' % tmpdir
    os.makedirs(frameworkdir)
    param_structure = {
        "companyName": "abcd",
        "gitProvider": "https://ebizframework.visualstudio.com/whitekite/_git/whitekite",
        "repoCloneAddress": "/tmp/m",
        "branchName": "master",
        "username": ""
    }
    testfile = create_temp_json('%s/a/b' % tmpdir,data=param_structure)
    snapshot = {
        "source": testfile,
        "type": "custom",
        "nodes": [
            {
                "snapshotId": "3",
                "collection": "Microsoft.Keyvault",
                "path": "realm/azure/validation/container1/sample-db-record.json"
            }
        ]
    }
    with mock.patch.object(Repo, 'clone_from', autospec=True, side_effect=repo_exception):
        snapshot_data = populate_custom_snapshot(snapshot)
        assert snapshot_data == {'3': False}


def test_populate_custom_snapshot_sshkey(create_temp_dir, create_temp_json, monkeypatch):
    global frameworkdir
    monkeypatch.setattr('processor.connector.snapshot_custom.json_source', mock_false_json_source)
    monkeypatch.setattr('processor.connector.snapshot_custom.get_test_json_dir', mock_get_test_json_dir)
    monkeypatch.setattr('processor.connector.snapshot_custom.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_custom.Popen', Popen)
    from git import Git
    from processor.connector.snapshot_custom import populate_custom_snapshot
    tmpdir = create_temp_dir()
    frameworkdir = '%s/a/b/c' % tmpdir
    os.makedirs(frameworkdir)
    testfile1 = create_temp_json('%s/a' % tmpdir, data={'ab':'c'})
    param_structure = {
        "companyName": "abcd",
        "gitProvider": "https://ebizframework.visualstudio.com/whitekite/_git/whitekite",
        "repoCloneAddress": "/tmp/m",
        "branchName": "master",
        "sshKeyfile": '%s/a/%s' % (tmpdir, testfile1),
        "username": ""
    }
    testfile = create_temp_json('%s/a/b' % tmpdir,data=param_structure)
    snapshot = {
        "source": testfile,
        "type": "custom",
        "nodes": [
            {
                "snapshotId": "3",
                "collection": "Microsoft.Keyvault",
                "path": "realm/azure/validation/container1/sample-db-record.json"
            }
        ]
    }
    # with mock.patch('processor.connector.snapshot_custom.Git', autospec=True) as GitMockHelper:
    #     GitMockHelper.return_value.custom_environment.return_value = None
    with mock.patch.object(Git, 'custom_environment', autospec=True):
        with mock.patch('processor.connector.snapshot_custom.Repo', autospec=True) as RepoMockHelper:
            RepoMockHelper.return_value.clone_from.return_value = None
            snapshot_data = populate_custom_snapshot(snapshot)
            assert snapshot_data == {'3': False}
