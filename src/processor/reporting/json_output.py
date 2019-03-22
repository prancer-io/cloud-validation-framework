"""Reporting related utility functions."""
import hashlib
import time
from processor.helper.config.config_utils import config_value
from collections import OrderedDict
from processor.helper.json.json_utils import save_json_to_file, collectiontypes, OUTPUT
from processor.database.database import DATABASE, DBNAME, insert_one_document
from processor.logging.log_handler import get_dblogger


def json_record(container, filetype, filename, json_data=None):
    db_record = {
        "timestamp": int(time.time() * 1000),
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


def dump_output_results(results, container, test_file, snapshot, filesystem=True):
    """ Dump the report in the json format for test execution results."""
    od = OrderedDict()
    od["$schema"] = ""
    od["contentVersion"] = "1.0.0.0"
    od["fileType"] = OUTPUT
    od["timestamp"] = int(time.time() * 1000)
    od["snapshot"] = snapshot
    od["container"] = container
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
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[OUTPUT])
        insert_one_document(doc, collection, dbname)
