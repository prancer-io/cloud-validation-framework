"""
File for execute the Az cli command for validate the azure deployment
for validate the azure deployment template files, first require login to Azure.
Once you install the requirements using `pip install -r requirements.txt`, then `azure-cli` package 
will install and you can run the following command from cmd.
    1) az login
"""
import glob
import time
import hashlib
import os
import pymongo
from processor.templates.azure.azure_parser import main
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import get_dbtests
from processor.helper.json.json_utils import get_container_dir, get_field_value, json_from_file, \
     make_snapshots_dir, store_snapshot, get_field_value_with_default, save_json_to_file
from processor.helper.config.config_utils import config_value, get_test_json_dir, framework_dir
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.database.database import insert_one_document, COLLECTION, DATABASE, DBNAME, \
    get_collection_size, create_indexes

from azure.cli.core import get_default_cli

logger = getlogger()


def get_dir_path(folder_path):
    """ Path to get the deployment and parameter JSON files """
    fw_dir = framework_dir()
    deployment_dir_path = '%s/%s' % (fw_dir, folder_path)
    return deployment_dir_path.replace('//', '/')


def invoke_az_cli(args_str):
    """ 
    Invoke azure cli command
    """
    login_user = os.environ.get('AD_LOGIN_USER', None)
    login_password = os.environ.get('AD_LOGIN_PASSWORD', None)

    if not login_user or not login_password:
        logger.error("`loginUser` or `loginPassword` field is not set in environment")
        return {"error" : "`loginUser` or `loginPassword` field is not set in environment"}
        
    azexe = os.environ.get('AZEXE', 'az')
    os.system(azexe + " login -u " + login_user + " -p " + login_password)

    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args)
    logger.info('Invoked Azure CLI command :: az %s' % args)
    if cli.result.result:
        os.system(azexe + " logout")
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True


def get_custom_data(snapshot_source):
    """
    Get source JSON data
    """
    sub_data = {}
    json_test_dir = get_test_json_dir()
    file_name = '%s.json' % snapshot_source if snapshot_source and not \
        snapshot_source.endswith('.json') else snapshot_source
    custom_source = '%s/../%s' % (json_test_dir, file_name)
    logger.info('Custom source: %s', custom_source)
    if exists_file(custom_source):
        sub_data = json_from_file(custom_source)
    return sub_data

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


def populate_arm_snapshot(container, dbname, snapshot_source, sub_data, snapshot_data, node, repopath):
    """
    Populate snapshot by running arm command
    """
    dir_path = get_field_value(sub_data, 'folderPath')
    if not dir_path:
        dir_path = repopath 

    location = get_field_value(node, 'location')
    paths = get_field_value(node, 'paths')
    azure_cli_flag = config_value("AZURE", "azureCli")
    
    template_file_path = ""
    deployment_file_path = ""

    if paths and isinstance(paths, list):
        if azure_cli_flag and azure_cli_flag == "true" and not location:
            logger.error("Invalid json : 'location' field is required in node")
            node['status'] = 'inactive'
            return snapshot_data
        for json_file in paths:
            json_file = '%s.json' % json_file if json_file and not \
                json_file.endswith('.json') else json_file
            json_file_path = '%s/%s' % (dir_path, json_file)
            logger.info("Fetching data : %s ", json_file)
            json_data = json_from_file(json_file_path)
            if not json_data:
                logger.error("Invalid path or json")
                node['status'] = 'inactive'
                return snapshot_data

            elif "$schema" not in json_data:
                logger.error(
                    "Invalid json : does not contains '$schema' field in json.")
                node['status'] = 'inactive'
                return snapshot_data
            else:
                if "deploymentTemplate.json" in json_data['$schema'].split("/")[-1]:
                    template_file_path = json_file_path
                elif "deploymentParameters.json" in json_data['$schema'].split("/")[-1]:
                    deployment_file_path = json_file_path
                else:
                    logger.error("Invalid json : $schema does not contains the correct value")

        if template_file_path and deployment_file_path:
            if azure_cli_flag and azure_cli_flag == "true":
                response = invoke_az_cli("deployment validate --location " + location +
                                         " --template-file " + template_file_path
                                         + " --parameters @" + deployment_file_path)
            else:
                paths = [deployment_file_path]
                response = main(template_file_path, False, *paths)

            data_record = create_database_record(node, snapshot_source, response, sub_data)
            
            if get_dbtests():
                logger.info(get_collection_size(node['collection']))
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
    else:
        node['status'] = 'inactive'
        logger.error("Invalid json : `paths` field is missing for 'arm' node type or it is not a list")

    return snapshot_data


def create_snapshot_record(snapshot, sub_dir_path, node, deployment_file_path_list, count):
    nodes = []
    collection = get_field_value(node, 'collection')
    location = get_field_value(node, 'location')
    test_user = get_field_value(snapshot, 'testUser')
    source = get_field_value(snapshot, 'source')
    master_snapshot_id = get_field_value(node, 'masterSnapshotId')

    for deployment_file_path in deployment_file_path_list:
        count = count + 1
        node_dict = {
            "snapshotId": '%s%s' % (master_snapshot_id, str(count)),
            "type": "arm",
            "collection": collection,
            "paths": [
                deployment_file_path['template_file_path'],
                deployment_file_path['path']
            ],
            "status": deployment_file_path['status'],
            "validate": deployment_file_path['validate']
        }
        if location:
            node_dict["location"] = location
        nodes.append(node_dict)

    db_record = {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": source,
                "testUser": test_user,
                "nodes": nodes
            }
        ]
    }

    return db_record, count



def populate_sub_directory_snapshot(file_path, base_dir_path, sub_dir_path, snapshot, dbname, node, snapshot_data, count):
    logger.info("Finding template and deployment files in : %s" % sub_dir_path)
    dir_path = str('%s/%s' % (base_dir_path, sub_dir_path)).replace('//', '/')
    if exists_dir(dir_path):
        list_of_file = os.listdir(dir_path)
        template_file_path_list = []
        deployment_file_path_list = []

        for entry in list_of_file:
            new_dir_path = ('%s/%s' % (dir_path, entry)).replace('//', '/')
            new_sub_directory_path = ('%s/%s' % (sub_dir_path, entry)).replace('//', '/')
            if exists_dir(new_dir_path):
                count = populate_sub_directory_snapshot(file_path, base_dir_path, new_sub_directory_path, snapshot, dbname, node, snapshot_data, count)
            elif exists_file(new_dir_path):
                if len(entry.split(".")) > 0 and "json" in entry.split(".")[-1]:
                    json_data = json_from_file(new_dir_path)
                    if json_data and "$schema" in json_data:
                        if "deploymentTemplate.json" in json_data['$schema'].split("/")[-1]:
                            template_file_path_list.append(new_sub_directory_path)
                        elif "deploymentParameters.json" in json_data['$schema'].split("/")[-1]:
                            deployment_file_path_list.append(new_sub_directory_path)
        
        location = get_field_value(node, 'location')
        new_deployment_file_path_list = []
        azure_cli_flag = config_value("AZURE", "azureCli")

        if template_file_path_list and deployment_file_path_list:
            for template_file_path in template_file_path_list:
                template_file_json_path = str('%s/%s' % (base_dir_path, template_file_path)).replace('//', '/')

                template_file_path = ("%s/%s" % (file_path, template_file_path)).replace("//", "/")
                for deployment_file_path in deployment_file_path_list:
                    deployment_file_json_path = str('%s/%s' % (base_dir_path, deployment_file_path)).replace('//', '/')
                    if azure_cli_flag and azure_cli_flag == "true":
                        response = invoke_az_cli("deployment validate --location " + location +
                                                " --template-file " + template_file_json_path
                                                + " --parameters @" + deployment_file_json_path)
                    else:
                        paths = [deployment_file_json_path]
                        response = main(template_file_json_path, False, *paths)

                    if "error" in response and response['error']:
                        logger.info("error in template_file_path : %s" , str(response['error']))
                        new_deployment_file_path_list.append({
                            "template_file_path" : template_file_path,
                            "path" : ("%s/%s" % (file_path, deployment_file_path)).replace("//", "/"),
                            "status" : "inactive",
                            "validate" : node['validate'] if 'validate' in node else True
                        })
                    else:
                        new_deployment_file_path_list.append({
                            "template_file_path" : template_file_path,
                            "path" : ("%s/%s" % (file_path, deployment_file_path)).replace("//", "/"),
                            "status" : "active",
                            "validate" : node['validate'] if 'validate' in node else True
                        })

            data_record, count = create_snapshot_record(snapshot, new_sub_directory_path, node, new_deployment_file_path_list, count)
            if node['masterSnapshotId'] not in snapshot_data or not isinstance(snapshot_data[node['masterSnapshotId']], list):
                snapshot_data[node['masterSnapshotId']] = []

            snapshot_data[node['masterSnapshotId']] = snapshot_data[node['masterSnapshotId']] + data_record['snapshots'][0]['nodes']
            logger.info(data_record)
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
                logger.error("Invalid json : directory does not exist : " + dir_path)
    else:
        logger.error("Invalid json : `paths` field is missing for 'arm' node type or it is not a list")

    return

