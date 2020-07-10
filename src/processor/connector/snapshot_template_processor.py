"""
File for execute the Az cli command for validate the azure deployment
for validate the azure deployment template files, first require login to Azure.
Once you install the requirements using `pip install -r requirements.txt`, then `azure-cli` package 
will install and you can run the following command from cmd.
    1) az login
"""
import time
import hashlib
import os
import pymongo
from processor.helper.config.rundata_utils import get_dbtests
from processor.templates.aws.aws_parser import main as aws_parser
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file, store_snapshot, make_snapshots_dir
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.helper.config.config_utils import config_value
from processor.database.database import insert_one_document, COLLECTION, DATABASE, DBNAME, \
    get_collection_size, create_indexes

logger = getlogger()

def create_database_record(node, snapshot_source, snapshot_data, source_data):
    """
    Create database record object for store in database
    """
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')

    ref = ""
    if "branchName" in source_data:
        ref = source_data["branchName"]
    elif "folderPath" in source_data:
        ref = source_data["folderPath"]

    db_record = {
        "structure": source_data["type"],
        "error": snapshot_data['error'] if 'error' in snapshot_data else None,
        "reference": ref,
        "source": parts[0],
        "paths": node["paths"],
        "timestamp": int(time.time() * 1000),
        "queryuser": source_data['username'] if 'username' in source_data else None,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": snapshot_data
    }
    return db_record

def populate_template_snapshot(container, dbname, snapshot_source, sub_data, snapshot_data, node, repopath):
    """
    Populate AWS cloudformation snapshot
    """
    type = node["type"]
    dir_path = get_field_value(sub_data, 'folderPath')
    if not dir_path:
        dir_path = repopath 

    paths = get_field_value(node, 'paths')
    if paths:
        path = paths[0]
    else:
        logger.error("paths is not defined or it is empty")
        return snapshot_data
    
    file_path = ('%s/%s' % (dir_path, path)).replace("//", "/")
    template_json = aws_parser(file_path)
    if template_json:
        data_record = create_database_record(node, snapshot_source, template_json, sub_data)
        if get_dbtests():
            if get_collection_size(node['collection']) == 0:
                #Creating indexes for collection
                create_indexes(
                    node['collection'], 
                    config_value(DATABASE, DBNAME), 
                    [
                        ('snapshotId', pymongo.ASCENDING),
                        ('timestamp', pymongo.DESCENDING)
                    ]
                )

                create_indexes(
                    node['collection'], 
                    config_value(DATABASE, DBNAME), 
                    [
                        ('_id', pymongo.DESCENDING),
                        ('timestamp', pymongo.DESCENDING),
                        ('snapshotId', pymongo.ASCENDING)
                    ]
                )
            insert_one_document(data_record, node['collection'], dbname, check_keys=False)
        else:
            snapshot_dir = make_snapshots_dir(container)
            if snapshot_dir:
                store_snapshot(snapshot_dir, data_record)
            
        if 'masterSnapshotId' in node:
            snapshot_data[node['snapshotId']] = node['masterSnapshotId']
        else:
            snapshot_data[node['snapshotId']] = False if ('error' in data_record and data_record['error']) else True
        node['status'] = 'active'
    else:
        node['status'] = 'inactive'
            
    return snapshot_data


def create_node_record(snapshot, node, template_node, count):
    nodes = []
    collection = get_field_value(node, 'collection')
    test_user = get_field_value(snapshot, 'testUser')
    source = get_field_value(snapshot, 'source')
    master_snapshot_id = get_field_value(node, 'masterSnapshotId')
    
    count = count + 1
    node_dict = {
        "snapshotId": '%s%s' % (master_snapshot_id, str(count)),
        "type": "cloudformation",
        "collection": collection,
        "paths": [ template_node["dir_path"] ],
        "status": template_node['status'],
        "validate": template_node['validate']
    }
    nodes.append(node_dict)
    return nodes, count

def populate_sub_directory_snapshot(file_path, base_dir_path, sub_dir_path, snapshot, dbname, node, snapshot_data, count):
    logger.info("Finding cloudformation yaml or json files in : %s" % sub_dir_path)
    dir_path = str('%s/%s' % (base_dir_path, sub_dir_path)).replace('//', '/')
    if exists_dir(dir_path):
        list_of_file = os.listdir(dir_path)
        for entry in list_of_file:
            new_dir_path = ('%s/%s' % (dir_path, entry)).replace('//', '/')
            new_sub_directory_path = ('%s/%s' % (sub_dir_path, entry)).replace('//', '/')
            if exists_dir(new_dir_path):
                count = populate_sub_directory_snapshot(file_path, base_dir_path, new_sub_directory_path, snapshot, dbname, node, snapshot_data, count)
            elif exists_file(new_dir_path):
                if len(entry.split(".")) > 0 and entry.split(".")[-1] in ["json","yaml"]:
                    template_json = aws_parser(new_dir_path)
                    if template_json:
                        template_node = {
                            "dir_path" : ("%s/%s" % (file_path, new_sub_directory_path)).replace("//", "/"),
                            "status" : "active",
                            "validate" : node['validate'] if 'validate' in node else True
                        }
                    else:
                        template_node = {
                            "dir_path" : ("%s/%s" % (file_path, new_sub_directory_path)).replace("//", "/"),
                            "status" : "inactive",
                            "validate" : node['validate'] if 'validate' in node else True
                        }
                    nodes, count = create_node_record(snapshot, node, template_node, count)
                    if node['masterSnapshotId'] not in snapshot_data or not isinstance(snapshot_data[node['masterSnapshotId']], list):
                        snapshot_data[node['masterSnapshotId']] = []
                    snapshot_data[node['masterSnapshotId']] = snapshot_data[node['masterSnapshotId']] + nodes
    return count

def populate_all_arm_snapshot(snapshot, dbname, sub_data, node, repopath, snapshot_data):
    """
    Populate all snapshot by running arm command
    """
    root_dir_path = get_field_value(sub_data, 'folderPath')
    if not root_dir_path:
        root_dir_path = repopath 

    paths = get_field_value(node, 'paths')
    if paths and isinstance(paths, list):
        count = 0
        for path in paths:
            dir_path = str('%s/%s' % (root_dir_path, path)).replace('//', '/')
            if exists_dir(dir_path):
                list_of_file = os.listdir(dir_path)
                for entry in list_of_file:
                    count = populate_sub_directory_snapshot(path, dir_path, entry, snapshot, dbname, node, snapshot_data, count)
            else:
                logger.error("Invalid path : directory does not exist : " + dir_path)
    else:
        logger.error("Invalid json : `paths` field is missing for 'arm' node type or it is not a list")    