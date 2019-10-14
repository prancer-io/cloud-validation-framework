"""
   Common file for populating json files to json.
"""
import argparse
import sys
import atexit
import time
import hashlib
import glob
import json
from pymongo import TEXT
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata, delete_currentdata
from processor.database.database import init_db, create_indexes, insert_one_document
from processor.helper.config.config_utils import DATABASE, DBNAME, config_value
from processor.helper.file.file_utils import exists_dir, exists_file
from processor.helper.json.json_utils import json_from_file,collectiontypes


logger = getlogger()



def json_record(container, filetype, filename, json_data=None):
    parts = filename.rsplit('/')
    fparts = parts[-1].split('.')
    db_record = {
        "timestamp": int(time.time() * 1000),
        "container": container,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "type": filetype,
        "name": fparts[0],
        "collection": config_value(DATABASE, collectiontypes[filetype]),
        "json": json_data if json_data else {}
    }
    if '$schema' in db_record['json']:
        del db_record['json']['$schema']
    return db_record


def populate_json_files(args):
    dbname = config_value(DATABASE, DBNAME)
    if args.dir:
        logger.info("Checking this directory: %s for json files", args.dir)
        json_dir = args.dir
        if exists_dir(args.dir):
            for filename in glob.glob('%s/*.json' % json_dir.replace('//', '/')):
                json_data = json_from_file(filename)
                if json_data and 'fileType' in json_data:
                    filetype = json_data['fileType']
                else:
                    filetype = 'structure'
                logger.info('Storing file:%s from directory: %s', json_dir, filename)
                db_record = json_record(args.container, filetype, filename, json_data)
                if validate_json_data(db_record['json'], db_record['type']):
                    insert_one_document(db_record, db_record['collection'], dbname, False)
                    logger.debug('DB Record: %s', json.dumps(db_record, indent=2))
                else:
                    logger.info('Invalid json for type:%s', db_record['type'])
                logger.info('*' * 80)
    if args.file:
        logger.info("Populating %s json file.", args.file)
        json_file = args.file
        if exists_file(json_file):
            json_data = json_from_file(json_file)
            if json_data and 'fileType' in json_data:
                filetype = json_data['fileType']
            elif args.type:
                filetype = args.type
            else:
                filetype = 'structure'
            logger.info('Storing file:%s', json_file)
            db_record = json_record(args.container, filetype, json_file, json_data)
            if validate_json_data(db_record['json'], db_record['type']):
                insert_one_document(db_record, db_record['collection'], dbname, False)
                logger.debug('DB Record: %s', json.dumps(db_record, indent=2))
            else:
                logger.info('Invalid json for type:%s', db_record['type'])
            logger.info('*' * 80)


def validate_json_data(json_data, filetype):
    try:
        valid = json_data['fileType'] == filetype
        if filetype == 'snapshot':
            valid = json_data['snapshots'] and isinstance(json_data['snapshots'], list)
        elif filetype == 'masterSnapshot':
            valid = json_data['snapshots'] and isinstance(json_data['snapshots'], list)
        elif filetype == 'test':
            valid = json_data['snapshot'] and json_data['testSet'] and \
                    isinstance(json_data['testSet'], list)
        elif filetype == 'mastertest':
            valid = json_data['masterSnapshot'] and json_data['testSet'] and \
                    isinstance(json_data['testSet'], list)
        elif filetype == 'structure':
            valid = True if json_data else False
        elif filetype == 'notifications':
            valid = True if json_data else False
    except Exception as ex:
        logger.info('Exception json population: %s', ex)
        valid = False if filetype != 'structure' else True
    return valid


def populate_json_main(arg_vals=None):
    """Main driver utility for running validator tests."""
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Populate json files")
    cmd_parser.add_argument('container', action='store',
                            help='Container name for the json files.')
    cmd_parser.add_argument('--dir', action='store', default=None,
                            help='Populate all json files from this directory.')
    cmd_parser.add_argument('--file', action='store', default=None,
                            help='Populate only this file')
    cmd_parser.add_argument('--type', action='store', default='structure',
                            choices=['test', 'structure', 'snapshot', 'output', 'notifications'])

    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    atexit.register(delete_currentdata)
    logger.info(args)
    init_currentdata()
    dbname, db_init_res = init_db()
    if db_init_res:
        for _, collection in collectiontypes.items():
            create_indexes(config_value(DATABASE, collection), dbname, [('timestamp', TEXT)])
        populate_json_files(args)
    else:
        logger.error("Error initializing DB, exiting....!")
    return 0
