""" Tests for validation"""


def mock_create_indexes(sid, dbname, flds):
    return None


def test_get_snapshot_id_to_collection_dict(monkeypatch):
    monkeypatch.setattr('processor.connector.validation.create_indexes', mock_create_indexes)
    from processor.connector.validation import get_snapshot_id_to_collection_dict
    val = get_snapshot_id_to_collection_dict('snapshot.json', 'container', 'abcd')
    assert True == isinstance(val, dict)
    val = get_snapshot_id_to_collection_dict('snapshot.json', 'container1', 'abcd')
    assert True == isinstance(val, dict)

