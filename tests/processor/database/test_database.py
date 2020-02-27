import warnings
import os
from unittest.mock import MagicMock

class result:
    def __init__(self, val):
        self.inserted_ids = range(len(val))

class MyCollection:
    def create_index(self, fields, unique=True):
        return True

    def __getitem__(self, val):
        cm = MagicMock()
        cm.inserted_ids = result([1,2])
        return cm

    def list_collection_names(self):
        return []

    def insert_one(self, val):
        cm = MagicMock()
        cm.inserted_id = 'abcd'
        return cm

    def distinct(self, val):
        return 1

    def insert(self, doc, check_keys=False):
        return '1'

    def find_one(self, val):
        return {}

    def insert_many(self, vals):
        return result(vals)

    def find(self, filter, projection=None):
        return self

    def sort(self, val):
        return self

    def limit(self, val):
        return self

    def skip(self, val):
        return [{}, {}]

    def count_documents(self, qry):
        return 1

    def index_information(self):
        return []

class MyMongoDB:

    def __getitem__(self, val):
        return MyCollection()

    def list_collection_names(self):
        return []



class MyMongoClient:
    def __init__(
            self,
            host=None,
            port=None,
            document_class=dict,
            tz_aware=None,
            connect=None,
            **kwargs):
        pass

    def __getitem__(self, val):
        return MyMongoDB()

    def drop_database(self, dbname):
        pass

    def list_database_names(self):
        return []


def mock_get_dburl():
    return ''

def mock_config_value(key, default=None):
    return 'pytestdb'

def mock_create_indexes(sid, dbname, flds):
    return None


def test_mongoconnection(monkeypatch):
    monkeypatch.setattr('processor.database.database.config_value', mock_config_value)
    monkeypatch.setattr('processor.database.database.get_dburl', mock_get_dburl)
    monkeypatch.setattr('processor.database.database.MongoClient', MyMongoClient)
    from processor.database.database import mongoconnection, mongodb, init_db,\
        get_collection, collection_names, insert_one_document, insert_documents,\
        check_document, get_documents, count_documents, index_information, distinct_documents
    # assert MONGO is None
    mongo = mongoconnection()
    assert mongo is not None
    dbname = 'abcd'
    testdb = mongodb(dbname)
    assert testdb is not None
    testdb = mongodb()
    assert testdb is not None
    val = testdb['abcd']
    assert val is not None
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
    val = '123456789012345678901234' # 24 character string
    doc = check_document('a1', val, dbname)
    assert doc is not None
    vals = insert_documents([{'a': 'b'}, {'c': 'd'}], 'a1', dbname)
    assert len(vals) == 2
    vals = get_documents('a1',dbname=dbname, sort=None)
    assert vals is not None
    vals = get_documents('a1', dbname=dbname, sort='abcd')
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

def test_log_DBhandler(monkeypatch, create_temp_dir, create_terraform):
    monkeypatch.setattr('processor.logging.log_handler.MongoClient', MyMongoClient)
    from processor.logging.log_handler import MongoDBHandler
    logger = MongoDBHandler(None, None)
    assert logger.collection is not None
    logger = MongoDBHandler(None, 'abcd')
    assert logger.collection is not None
    cm = MagicMock()
    cm.getMessage.return_value = 'Test message'
    logger.emit(cm)
    logger.collection = 'abcd'
    logger.emit(cm)

def test_db_log_DBhandler(monkeypatch, create_temp_dir, create_terraform):
    monkeypatch.setattr('processor.logging.log_handler.MongoClient', MyMongoClient)
    os.environ['UNITTEST'] = 'false'
    log_config = [
        '[LOGGING]',
        'level = INFO',
        'maxbytes = 10',
        'backupcount = 10',
        'propagate = true',
        'logFolder = log',
        'dbname = whitekite',
        '[MONGODB]',
        'dburl = mongodb://localhost:27017/validator'
    ]
    newpath = create_temp_dir()
    fname = create_terraform(newpath, '\n'.join(log_config), 'a1.ini')
    log_ini = '%s/%s' % (newpath, fname)
    from processor.logging.log_handler import logging_fw
    logger = logging_fw(log_ini, 0)
    assert logger is not None
