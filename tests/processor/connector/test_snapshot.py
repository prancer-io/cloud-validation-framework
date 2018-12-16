""" Tests for snapshot azure"""

def mock_populate_azure_snapshot(snapshot, snapshot_type='azure'):
    return True


def mock_populate_custom_snapshot(snapshot, snapshot_type='custom'):
    return True


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