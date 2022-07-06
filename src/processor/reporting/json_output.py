"""Reporting related utility functions."""
import hashlib
import time
from datetime import datetime
from bson.objectid import ObjectId
from processor.helper.config.config_utils import config_value
from collections import OrderedDict
from processor.helper.config.rundata_utils import get_from_currentdata
from processor.helper.json.json_utils import save_json_to_file, collectiontypes, OUTPUT
from processor.database.database import DATABASE, DBNAME, find_and_update_document, get_documents, insert_one_document, update_one_document
from processor.logging.log_handler import get_dblogger

doc_id = None
dbname = None
collection = None

def json_record(container, filetype, filename, json_data=None):

    db_record = {
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
        "container": container,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "type": filetype,
        "name": filename,
        "collection": config_value(DATABASE, collectiontypes[filetype]),
        "json": json_data if json_data else {}
    }
    if '$schema' in db_record['json']:
        del db_record['json']['$schema']
    return db_record

def create_output_entry(container, test_file="", filesystem=False):
    global doc_id, dbname, collection
    session_id = get_from_currentdata("session_id")
    isremote = get_from_currentdata('remote')
    isremote = True if isremote else False
    od = OrderedDict()
    od["$schema"] = ""
    od["contentVersion"] = "1.0.0.0"
    od["fileType"] = OUTPUT
    od["timestamp"] = int(datetime.utcnow().timestamp() * 1000)
    od["container"] = container
    od["status"] = "Running"
    od["session_id"] = session_id
    od["remote_run"] = isremote
    dblog = get_dblogger()
    od["log"] = dblog if dblog else ""
    if not filesystem:
        od["test"] = test_file
        od["results"] = []
        del od["$schema"]
        doc = json_record(container, OUTPUT, test_file, od)
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[OUTPUT])
        doc_id = insert_one_document(doc, collection, dbname)
    return doc_id

def update_output_testname(test_file="", snapshot="", filesystem=False):
    if doc_id and not filesystem:
        find_and_update_document(
            collection=collection,
            dbname=dbname,
            query={"_id" : ObjectId(doc_id)},
            update_value={
                "$set" :  {
                    "json.test": test_file,
                    "json.snapshot" : snapshot
                }
            }
        )

def dump_output_results(results, container, test_file, snapshot, filesystem=True, status=None):
    """ Dump the report in the json format for test execution results."""
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[OUTPUT])
    session_id = get_from_currentdata("session_id")
    if not doc_id:
        isremote = get_from_currentdata('remote')
        isremote = True if isremote else False
        od = OrderedDict()
        od["$schema"] = ""
        od["contentVersion"] = "1.0.0.0"
        od["fileType"] = OUTPUT
        od["timestamp"] = int(datetime.utcnow().timestamp() * 1000)
        od["snapshot"] = snapshot
        od["container"] = container
        od["session_id"] = session_id
        od["remote_run"] = isremote
        dblog = get_dblogger()
        od["log"] = dblog if dblog else ""
        if filesystem:
            test_file_parts = test_file.rsplit('/', 1)
            od["test"] = test_file_parts[-1]
            output_file = '%s/output-%s' % (test_file_parts[0], test_file_parts[-1])
            od["results"] = results
            save_json_to_file(od, output_file)
        else:
            od["test"] = test_file
            od["results"] = results
            del od["$schema"]
            doc = json_record(container, OUTPUT, test_file, od)
            insert_one_document(doc, collection, dbname)
    else:
        update_value = {}
        if results:
            update_value["$push"] = { "json.results": { "$each" : results }}
        
        if status:
            update_value["$set"] = { "json.status": status }
            
        find_and_update_document(
            collection=collection,
            dbname=dbname,
            query={"_id" : ObjectId(doc_id)},
            update_value=update_value
        )
