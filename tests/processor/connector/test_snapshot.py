""" Tests for snapshot azure"""

def mock_populate_azure_snapshot(snapshot, snapshot_type='azure'):
    return True


def mock_populate_custom_snapshot(snapshot, snapshot_type='custom'):
    return True


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


def test_populate_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot', mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot', mock_populate_custom_snapshot)
    from processor.connector.snapshot import populate_snapshot
    assert False == populate_snapshot({})
    assert False == populate_snapshot({'type': 'azure'})
    assert True == populate_snapshot({'type': 'azure', 'nodes': [{'a': 'b'}]})
    assert True == populate_snapshot({'type': 'custom', 'nodes': [{'a': 'b'}]})


def test_populate_snapshots_from_json(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot', mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot', mock_populate_custom_snapshot)
    monkeypatch.setattr('processor.comparison.interpreter.get_documents', mock_get_documents)
    from processor.connector.snapshot import populate_snapshots_from_json
    assert False == populate_snapshots_from_json({})
    assert False == populate_snapshots_from_json({'snapshots': []})
    testdata = {
        'snapshots': [
            {'type': 'azure', 'nodes': [{'a': 'b'}]},
            {'type': 'custom', 'nodes': [{'a': 'b'}]}
        ]
    }
    assert True == populate_snapshots_from_json(testdata)


def test_populate_snapshots_from_file(monkeypatch, create_temp_dir, create_temp_json):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot', mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot', mock_populate_custom_snapshot)
    from processor.connector.snapshot import populate_snapshots_from_file
    assert False == populate_snapshots_from_file('/tmp/xyza')
    newpath = create_temp_dir()
    testdata = {
        'snapshots': [
            {'type': 'azure', 'nodes': [{'a': 'b'}]},
            {'type': 'custom', 'nodes': [{'a': 'b'}]}
        ]
    }
    fname = create_temp_json(newpath, data=testdata)
    assert True == populate_snapshots_from_file('%s/%s' % (newpath, fname))


def test_populate_container_snapshots(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.populate_azure_snapshot', mock_populate_azure_snapshot)
    monkeypatch.setattr('processor.connector.snapshot_custom.populate_custom_snapshot', mock_populate_custom_snapshot)
    from processor.connector.snapshot import populate_container_snapshots
    assert False == populate_container_snapshots('abc')
    assert True == populate_container_snapshots('container2')
    assert True == populate_container_snapshots('container2', False)