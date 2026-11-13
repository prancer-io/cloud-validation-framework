"""Integration tests for processor.database.database against a REAL MongoDB server.

They exercise every pymongo / bson API that CVF uses (MongoClient with host/port
and serverSelectionTimeoutMS, list_database_names, list_collection_names,
insert_one/insert_many, replace_one, update_many, update_one($push),
delete_many, find/find_one with projection/sort/limit/skip, count_documents,
distinct, create_index (TEXT, compound, unique), index_information, ObjectId)
so that a pymongo upgrade can be checked against the MongoDB server versions
in use.

Skipped unless CVF_MONGO_TEST_URL is set, e.g.
    CVF_MONGO_TEST_URL=mongodb://127.0.0.1:27017/ pytest tests/processor/database
"""
import logging
import os
import uuid

import pytest

MONGO_URL = os.getenv('CVF_MONGO_TEST_URL')
pytestmark = pytest.mark.skipif(not MONGO_URL, reason='CVF_MONGO_TEST_URL not set')


@pytest.fixture
def db(monkeypatch):
    from processor.database import database
    monkeypatch.setenv('DBURL', MONGO_URL)
    database.clean_mongo_client()
    dbname = 'cvf_it_%s' % uuid.uuid4().hex[:8]
    yield database, dbname
    database.mongoconnection().drop_database(dbname)
    database.mongoconnection().close()
    database.clean_mongo_client()


def test_connection_and_names(db):
    database, dbname = db
    client = database.mongoconnection()
    assert database.mongoconnection() is client  # cached singleton
    assert isinstance(client.list_database_names(), list)
    assert database.mongodb(dbname).name == dbname
    assert database.mongodb().name == 'test'
    assert database.get_collection(dbname, 'c1').name == 'c1'
    database.insert_one_document({'a': 1}, 'c1', dbname)
    assert database.collection_names(dbname) == ['c1']


def test_init_db(db, monkeypatch):
    database, dbname = db
    monkeypatch.setattr(database, 'config_value', lambda *a, **k: dbname)
    assert database.init_db() == (dbname, True)
    assert database.index_information('resources', dbname) == ['_id_', 'timestamp_text']


def test_init_db_unreachable_server(monkeypatch):
    from processor.database import database
    monkeypatch.setenv('DBURL', 'mongodb://127.0.0.1:1/')
    database.clean_mongo_client()  # default 3000 ms server selection timeout
    monkeypatch.setattr(database, 'config_value', lambda *a, **k: 'x')
    assert database.init_db() == (None, False)
    database.clean_mongo_client()


def test_insert_find_check_count_distinct(db):
    database, dbname = db
    doc_id = database.insert_one_document({'z': 1, 'a': {'d': 2, 'b': 1}, 'name': 'n1',
                                           'timestamp': 10}, 'res', dbname)
    assert isinstance(doc_id, str) and len(doc_id) == 24
    # Pre-existing behaviour (pymongo >= 4.0): insert_documents / distinct_documents
    # use `if coll and ...`, which pymongo rejects. Neither is called from src/.
    with pytest.raises(NotImplementedError):
        database.insert_documents([{'name': 'x'}], 'res', dbname)
    with pytest.raises(NotImplementedError):
        database.distinct_documents('res', 'name', dbname)
    coll = database.get_collection(dbname, 'res')
    assert len(coll.insert_many([{'name': 'n2', 'timestamp': 20},
                                 {'name': 'n2', 'timestamp': 30}]).inserted_ids) == 2

    doc = database.check_document('res', doc_id, dbname)
    assert list(doc.keys()) == ['_id', 'a', 'name', 'timestamp', 'z']  # sort_dict order
    assert list(doc['a'].keys()) == ['b', 'd']
    from bson.objectid import ObjectId
    assert database.check_document('res', ObjectId(doc_id), dbname)['name'] == 'n1'

    assert database.count_documents('res', dbname=dbname) == 3
    assert database.count_documents('res', {'name': 'n2'}, dbname) == 2
    assert sorted(coll.distinct('name')) == ['n1', 'n2']

    docs = database.get_documents('res', {'name': 'n2'}, dbname,
                                  sort=[database.sort_field('timestamp', False)])
    assert [d['timestamp'] for d in docs] == [30, 20]
    assert all('_id' not in d for d in docs)
    docs = database.get_documents('res', None, dbname, sort=[('timestamp', 1)],
                                  limit=1, skip=1, proj={'timestamp': 1}, _id=True)
    assert len(docs) == 1 and docs[0]['timestamp'] == 20 and '_id' in docs[0]
    assert 'name' not in docs[0]
    # without sort the projection is not applied (pre-existing behaviour): _id is returned
    docs = database.get_documents('res', {'name': 'n1'}, dbname)
    assert len(docs) == 1 and str(docs[0].pop('_id')) == doc_id
    assert docs == [{'a': {'b': 1, 'd': 2}, 'name': 'n1', 'timestamp': 10, 'z': 1}]


def test_update_replace_delete(db):
    database, dbname = db
    doc_id = database.insert_one_document({'name': 'n1', 'v': 1}, 'res', dbname)
    doc = database.check_document('res', doc_id, dbname)
    doc['v'] = 2
    database.update_one_document(doc, 'res', dbname)
    assert database.check_document('res', doc_id, dbname)['v'] == 2
    database.update_one_document({'name': 'new'}, 'res', dbname)  # no _id -> insert
    assert database.count_documents('res', dbname=dbname) == 2

    assert database.find_and_update_document('res', dbname, {'name': 'n1'},
                                             {'$set': {'v': 3}}) is True
    assert database.check_document('res', doc_id, dbname)['v'] == 3

    assert database.delete_documents('res', {'name': 'new'}, dbname) is True
    assert database.count_documents('res', dbname=dbname) == 1


def test_create_indexes(db):
    database, dbname = db
    name = database.create_indexes('snap', dbname, [('snapshotId', 1), ('timestamp', -1)])
    assert name == 'snapshotId_1_timestamp_-1'
    database.create_indexes('snap', dbname, [('_id', -1), ('timestamp', -1), ('snapshotId', 1)])
    assert database.index_information('snap', dbname) == [
        '_id_', '_id_-1_timestamp_-1_snapshotId_1', 'snapshotId_1_timestamp_-1']
    database.insert_one_document({'snapshotId': 's', 'timestamp': 1}, 'snap', dbname)
    # unique=True: a duplicate is rejected and insert_one_document logs + returns None
    assert database.insert_one_document({'snapshotId': 's', 'timestamp': 1},
                                        'snap', dbname) is None


def test_mongo_log_handler(db):
    database, dbname = db
    from processor.logging.log_handler import MongoDBHandler
    handler = MongoDBHandler(MONGO_URL, dbname, log_type='it')
    assert handler.collection is not None
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger = logging.getLogger('cvf_mongo_it')
    logger.addHandler(handler)
    logger.propagate = False
    try:
        logger.error('hello %s', 'mongo')
    finally:
        logger.removeHandler(handler)
    logs = database.get_documents('logs', {'name': handler.get_log_collection()}, dbname)
    assert len(logs) == 1 and logs[0]['index'] == 0
    assert [l['msg'].split(' ', 2)[2] for l in logs[0]['logs']] == ['hello mongo']
    assert logs[0]['logs'][0]['level'] == 'ERROR'


def test_mongo_log_handler_unreachable():
    from processor.logging.log_handler import MongoDBHandler
    handler = MongoDBHandler('mongodb://127.0.0.1:1/', 'x')
    assert handler.collection is None
