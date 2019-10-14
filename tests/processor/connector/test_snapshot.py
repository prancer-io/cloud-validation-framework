
""" Tests for common snapshot file."""
from tests.conftest import load_test_json

def mock_container_snapshot_get_documents(collection, query=None, dbname=None,
                                          sort=None, limit=10):
    if collection == 'tests':
        return load_test_json('git_snapshot.json')
    return []


def mock_populate_azure_snapshot(snapshot, snapshot_type='azure'):
    print("azure snapshot: %s" % snapshot)
    if 'testUser' in snapshot and \
      snapshot['testUser'] == 'ajeybk1@kbajeygmail.onmicrosoft.com':
        return {'31': True, '32': False, '33': True, '34': False}

    return {}
    # return {}


def mock_populate_git_snapshot(snapshot, snapshot_type='git'):
    print(snapshot)
    if 'testUser' in snapshot and \
            snapshot['testUser'] in ['git', 'ajeybk1@kbajeygmail.onmicrosoft.com']:
        return {'1': True, '31': True, '32': False, '33': True, '34': False}
    return {}


def mock_snap_populate_git_snapshot(snapshot, snapshot_type='git'):
    return {"1": True}


def mock_populate_aws_snapshot(snapshot, snapshot_type='aws'):
    return {}


def mock_snap_populate_azure_snapshot(snapshot, snapshot_type='azure'):
    print("mock_snap_populate_azure_snapshot")
    return {'31': True, '32': False, '33': True, '34': False}


def mock_populate_google_snapshot(snapshot, snapshot_type='google'):
    return {}


def mock_empty_snapshot_get_documents(collection, query=None, dbname=None,
                                      sort=None, limit=10):
    json_data = load_test_json('git_snapshot.json')
    json_data[0]['json']['snapshots'] = []
    return json_data


def mock_empty_get_documents(collection, query=None, dbname=None, sort=None,
                             limit=10):
    return []

def mock_update_one_document(doc, collection, dbname):
    """ Update the document into the collection. """
    pass

def mock_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    print('Collection: %s' % collection)
    if collection == 'tests':
        if 'container' in query and query['container'] == 'gitcontainer':
            json_data = load_test_json('git_tests.json')
        else:
            json_data = []
    else:
        json_data = load_test_json('git_snapshot.json')
    return json_data


def test_populate_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot',
                        mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot',
                        mock_populate_git_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_aws.populate_aws_snapshot',
                        mock_populate_aws_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_google.populate_google_snapshot',
                        mock_populate_google_snapshot)
    from processor.connector.snapshot import populate_snapshot
    assert {} == populate_snapshot({})
    assert {} == populate_snapshot({'type': 'azure'})
    assert {} == populate_snapshot({'type': 'azure', 'nodes': [{'a': 'b'}]})
    assert {} == populate_snapshot({'type': 'git'})
    assert {} == populate_snapshot({'type': 'git', 'nodes': [{'a': 'b'}]})
    assert {} == populate_snapshot({'type': 'aws'})
    assert {} == populate_snapshot({'type': 'aws', 'nodes': [{'a': 'b'}]})
    assert {} == populate_snapshot({'type': 'google'})
    assert {} == populate_snapshot({'type': 'google', 'nodes': [{'a': 'b'}]})



def test_populate_snapshots_from_json(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot',
                        mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot',
                        mock_populate_git_snapshot)
    from processor.connector.snapshot import populate_snapshots_from_json
    assert {} == populate_snapshots_from_json({})
    assert {} == populate_snapshots_from_json({'snapshots': []})
    testdata = {
        'snapshots': [
            {'type': 'azure', 'nodes': [{'a': 'b'}]},
            {'type': 'git', 'nodes': [{'a': 'b'}]}
        ]
    }
    assert {} == populate_snapshots_from_json(testdata)


def test_populate_snapshots_from_file(monkeypatch, create_temp_dir, create_temp_json):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot',
                        mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot',
                        mock_populate_git_snapshot)
    from processor.connector.snapshot import populate_snapshots_from_file
    assert {} == populate_snapshots_from_file('/tmp/xyza')
    newpath = create_temp_dir()
    testdata = {
        'snapshots': [
            {'type': 'azure', 'nodes': [{'a': 'b'}]},
            {'type': 'git', 'nodes': [{'a': 'b'}]}
        ]
    }
    fname = create_temp_json(newpath, data=testdata)
    assert {} == populate_snapshots_from_file('%s/%s' % (newpath, fname))


def test_empty_snapshot_populate_container_snapshots(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot',
                        mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot',
                        mock_populate_git_snapshot)
    monkeypatch.setattr('processor.connector.snapshot.get_documents',
                        mock_empty_snapshot_get_documents)
    from processor.connector.snapshot import populate_container_snapshots
    assert {} == populate_container_snapshots('abc')


def test_empty_populate_container_snapshots(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot',
                        mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot',
                        mock_populate_git_snapshot)
    monkeypatch.setattr('processor.connector.snapshot.get_documents',
                        mock_empty_get_documents)
    from processor.connector.snapshot import populate_container_snapshots
    assert {} == populate_container_snapshots('abc')


def test_populate_container_snapshots(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot.populate_azure_snapshot',
                        mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot.populate_custom_snapshot',
                        mock_populate_git_snapshot)
    monkeypatch.setattr('processor.connector.snapshot.get_documents', mock_get_documents)
    monkeypatch.setattr('processor.connector.snapshot.update_one_document', mock_update_one_document)
    from processor.connector.snapshot import populate_container_snapshots, snapshot_fns
    snapshot_fns['git'] = mock_populate_git_snapshot
    assert {} == populate_container_snapshots('container2')
    assert {'snapshot3': {'1': True, '31': True, '32': False, '33': True, '34': False}} == \
           populate_container_snapshots('container3', False)
    assert {'snapshot': {'1': True, '31': True, '32': False, '33': True, '34': False}} == populate_container_snapshots('gitcontainer', False)
    assert {'snapshot': {'1': True, '31': True, '32': False, '33': True, '34': False}} == populate_container_snapshots('gitcontainer', True)
    assert {} == populate_container_snapshots('container21', False)



