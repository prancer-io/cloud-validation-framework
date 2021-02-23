"""
   Common file for populating json files to json.
"""
import argparse
import datetime
import sys
import atexit
import time
import hashlib
import glob
import json
from pymongo import TEXT
from bson.objectid import ObjectId
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata, delete_currentdata
from processor.database.database import init_db, create_indexes, insert_one_document,\
    get_documents, update_one_document
from processor.helper.config.config_utils import DATABASE, DBNAME, config_value
from processor.helper.file.file_utils import exists_dir, exists_file
from processor.helper.json.json_utils import json_from_file,collectiontypes


logger = getlogger()

def json_record(container, filetype, filename, json_data=None):
    parts = filename.rsplit('/')
    fparts = parts[-1].split('.')
    db_record = {
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "collection": config_value(DATABASE, collectiontypes[filetype]),
        "container": container,
        "name": fparts[0],
        "timestamp": int(time.time() * 1000),
        "type": filetype,
        "json": json_data if json_data else {}
    }
    if '$schema' in db_record['json']:
        del db_record['json']['$schema']
    return db_record


# Save Snapshot, MasterSnapshot, Test and MasterTest object
def save_container_object(container_name, object_type, data, dbname):
    """
    container_name : Name of container in which new object will store
    object_type: Type of the object must be in masterSnapshots, Snapshots, masterTests or Tests
    data: container
        1. object_id: table Id of object
        2. name: Display name of that object
    """

    container_struture_list = get_documents('structures', {'type':'container'}, dbname)
    if not container_struture_list:
        # create container_json
        create_container_json_to_db(dbname)
        container_struture_list = get_documents('structures', {'type':'container'}, dbname)
    container_json = container_struture_list[0]['json']
    container_list = container_json['containers']

    filtered_list = list(filter(lambda i: i['name'] == container_name, container_list))
    if not filtered_list:
        # add new container if container not exist
        add_new_container(container_name, dbname)
        container_struture_list = get_documents('structures', {'type':'container'}, dbname)
        container_json = container_struture_list[0]['json']
        container_list = container_json['containers']
        filtered_list = list(filter(lambda i: i['name'] == container_name, container_list))

    container = filtered_list[0]

    if object_type == 'others':
        exist = False
        for obj in container[object_type]:
            if obj['name'] == data['name']:
                exist = True

        if not exist:
            container[object_type].append({
                'id': data['object_id'],
                'name': data['name']
            })
            container_struture_list[0]['json'] = container_json
            update_one_document(container_struture_list[0], container_struture_list[0]['collection'], dbname)
    else:
        exist = False
        for obj in container[object_type]:
            if obj['id'] == data['object_id']:
                exist = True

        if not exist:
            container[object_type].append({
                'id': data['object_id'],
                'name': data['name']
            })
            container_struture_list[0]['json'] = container_json
            update_one_document(container_struture_list[0], container_struture_list[0]['collection'], dbname)


def save_container_to_db(container_name, container_id, file_name, content_type, file_content, dbname):
    file_content_list = []
    structure_model_obj = get_documents('structures', {'json.containerId': container_id, 'type': 'others'}, dbname, _id=True)

    file_obj = {
        'name': file_name,
        'container_file': file_content,
        'content_type': content_type
    }

    if structure_model_obj:
        exist = False
        for file_data in structure_model_obj[0]['json']['file']:
            for key, value in file_data.items():
                if value == file_name:
                    exist = True

        if exist:
            for file_data in structure_model_obj[0]['json']['file']:
                for key, value in file_data.items():
                    if value == file_name:
                        file_data['container_file'] = file_content
        else:
            structure_model_obj[0]['json']['file'].append(file_obj)
        update_one_document(structure_model_obj[0], 'structures', dbname)
        # print(structure_model_obj)
        data = {
            'object_id': structure_model_obj[0]['_id'],
            'name': file_name
        }
    else:
        file_obj = {
            'name': file_name,
            'container_file': file_content,
            'content_type': content_type
        }
        file_content_list.append(file_obj)

        container_json = {
            'name': container_name,
            'containerId': container_id,
            'file': file_content_list
        }
        structure_model_obj = {
            'checksum': '',
            'collection': 'structures',
            'container': container_name,
            'name': 'file_upload',
            'timestamp': int(datetime.datetime.now().timestamp() * 1000),
            'type': 'others',
            'json': container_json
        }
        docId = insert_one_document(structure_model_obj, structure_model_obj['collection'], dbname, False)
        # print(docId)
        data = {
            'object_id': ObjectId(docId),
            'name': file_name
        }

    save_container_object(container_name, 'others', data, dbname)


def create_container_json_to_db(dbname):
    container_json = {'filterType': 'container', 'containers': []}
    container = {
        'collection' : 'structures',
        'container': '',
        'name': '',
        'type' : 'container',
        'timestamp': int(datetime.datetime.now().timestamp() * 1000),
        'json': container_json
    }
    insert_one_document(container, container['collection'], dbname, False)


def add_new_container(container_name, dbname):
    container_struture_list = get_documents('structures', {'type':'container'}, dbname)
    container_struture = container_struture_list[0]
    container_json = container_struture['json']
    container_list = container_json['containers']

    filtered_list = list(filter(lambda i: i['name'] == container_name, container_list))
    if filtered_list:
        return

    if container_list:
        container = dict(container_list[-1])
        containerId = container['containerId'] + 1
    else:
        containerId = 1

    new_container = {
        'containerId': containerId,
        'status': 'active',
        'name': container_name,
        'masterSnapshots': [],
        'Snapshots': [],
        'masterTests': [],
        'Tests': [],
        'others': []
    }

    container_list.append(new_container)
    container_json['containers'] = container_list
    container_struture['json'] = container_json
    update_one_document(container_struture, container_struture['collection'], dbname)


def populate_json_files(args):
    dbname = config_value(DATABASE, DBNAME)
    containerId = None
    if args.container:
        container_struture_list = get_documents('structures', {'type':'container'}, dbname)
        if not container_struture_list:
            # create container_json
            create_container_json_to_db(dbname)
            container_struture_list = get_documents('structures', {'type':'container'}, dbname)
        container_json = container_struture_list[0]['json']
        container_list = container_json['containers']

        filtered_list = list(filter(lambda i: i['name'] == args.container, container_list))
        if not filtered_list:
            # add new container if container not exist
            add_new_container(args.container, dbname)
            container_struture_list = get_documents('structures', {'type':'container'}, dbname)
            container_json = container_struture_list[0]['json']
            container_list = container_json['containers']
            filtered_list = list(filter(lambda i: i['name'] == args.container, container_list))
        containerId = filtered_list[0]['containerId']
    # return containerId

    # if args.dir:
    #     logger.info("Checking this directory: %s for json files", args.dir)
    #     json_dir = args.dir
    #     if exists_dir(args.dir):
    #         for filename in glob.glob('%s/*.json' % json_dir.replace('//', '/')):
    #             json_data = json_from_file(filename)
    #             if json_data and 'fileType' in json_data:
    #                 filetype = json_data['fileType']
    #             else:
    #                 filetype = 'structure'
    #             logger.info('Storing file:%s from directory: %s', json_dir, filename)
    #             db_record = json_record(args.container, filetype, filename, json_data)
    #             if validate_json_data(db_record['json'], db_record['type']):
    #                 insert_one_document(db_record, db_record['collection'], dbname, False)
    #                 logger.debug('DB Record: %s', json.dumps(db_record, indent=2))
    #             else:
    #                 logger.info('Invalid json for type:%s', db_record['type'])
    #             logger.info('*' * 80)
    if args.file:
        logger.info("Populating %s json file.", args.file)
        json_file = args.file
        if exists_file(json_file):
            if json_file.endswith('.json'):
                json_data = json_from_file(json_file)
                if json_data and 'fileType' in json_data:
                    filetype = json_data['fileType']
                # elif args.type:
                #     filetype = args.type
                else:
                    filetype = 'structure'
                logger.info('Storing file:%s', json_file)
                db_record = json_record(args.container, filetype, json_file, json_data)
                if validate_json_data(db_record['json'], db_record['type']):
                    docId = insert_one_document(db_record, db_record['collection'], dbname, False)
                    data = {
                        'object_id': ObjectId(docId),
                        'name': db_record['name']
                    }
                    if filetype == 'masterSnapshot':
                        save_container_object(args.container, 'masterSnapshots', data, dbname)
                    elif filetype == 'mastertest':
                        save_container_object(args.container, 'masterTests', data, dbname)
                    elif filetype == 'snapshot':
                        save_container_object(args.container, 'Snapshots', data, dbname)
                    elif filetype == 'test':
                        save_container_object(args.container, 'Tests', data, dbname)
                    logger.debug('DB Record: %s', json.dumps(db_record, indent=2))
                else:
                    logger.info('Invalid json for type:%s', db_record['type'])
                logger.info('*' * 80)
            elif json_file.endswith('.rego'):
                with open(json_file) as f:
                    file_content = f.read()
                    content_type = 'application/octet-stream'
                    save_container_to_db(args.container, containerId, json_file, content_type, file_content, dbname)




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
    # cmd_parser.add_argument('--dir', action='store', default=None,
    #                         help='Populate all json files from this directory.')
    cmd_parser.add_argument('--file', action='store', default=None,
                            help='Populate only this file')
    # cmd_parser.add_argument('--type', action='store', default='structure',
    #                         choices=['test', 'structure', 'snapshot', 'output', 'notifications'])

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
