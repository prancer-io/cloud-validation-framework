import warnings

def mock_config_value(key, default=None):
    return 'pytestdb'


def abctest_mongoconnection(monkeypatch):
    monkeypatch.setattr('processor.database.database.config_value', mock_config_value)
    from processor.database.database import mongoconnection, mongodb, init_db,\
        get_collection, collection_names, insert_one_document, insert_documents,\
        check_document, get_documents, count_documents, index_information, distinct_documents
    # assert MONGO is None
    mongo = mongoconnection()
    assert mongo is not None
    dbname = mock_config_value(None, None)
    testdb = mongodb(dbname)
    assert testdb is not None
    testdb = mongodb()
    assert testdb is not None
    init_db()
    coll = get_collection(dbname, 'a1')
    assert coll is not None
    colls = collection_names(dbname)
    assert colls is not None
    val = insert_one_document({'a':'b'}, 'a1', dbname)
    assert val is not None
    val = distinct_documents('a1', 'a', dbname)
    assert val is not None
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        val = insert_one_document({'a': 'b'}, 'a1', dbname, False)
        assert val is not None
    doc = check_document('a1', val, dbname)
    assert doc is not None
    vals = insert_documents([{'a': 'b'}, {'c': 'd'}], 'a1', dbname)
    assert len(vals) == 2
    vals = get_documents('a1',dbname=dbname, sort=None)
    assert vals is not None
    count = count_documents('a1', dbname=dbname)
    assert type(count) is int
    assert count > 0
    info = index_information('a1', dbname)
    assert info is not None
    mongo.drop_database(dbname)

def test_sort_dict():
    from processor.database.database import sort_dict
    a = {'a': 1, 'b': 2, 'f': 5, 'c': 3, 'd': 4}
    b = {'z': a, 'y': {'x': 1, 'a': a}, 'm': 2, 'n': 'abc'}
    # c = {'n': 'abc', 'y': {'x': 1, 'a': a}, 'z': a, 'm': 2}
    d = sort_dict(b)
    # e = sort_dict(c)
    assert ['m', 'n', 'y', 'z'] == list(d.keys())
