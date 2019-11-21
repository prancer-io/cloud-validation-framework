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

from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import get_dbtests
from processor.helper.json.json_utils import get_container_dir, get_field_value, json_from_file, \
     make_snapshots_dir, store_snapshot, get_field_value_with_default
from processor.helper.config.config_utils import config_value, get_test_json_dir, framework_dir
from processor.helper.file.file_utils import exists_file
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.database.database import insert_one_document, COLLECTION

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
    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args)
    logger.info('Invoked Azure CLI command :: az %s' % args)
    if cli.result.result:
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
    db_record = {
        "structure": "azure",
        "error": snapshot_data['error'] if 'error' in snapshot_data else None,
        "reference": "",
        "source": parts[0],
        "path": "",
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
    
    template_file_path = ""
    deployment_file_path = ""

    if paths and isinstance(paths, list):
        if not location:
            logger.error("Invalid json : 'location' field is required in node")
            node['status'] = 'inactive'
            return snapshot_data
        for json_file in paths:
            json_file_path = '%s/%s.json' % (
                dir_path, json_file)
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
                    logger.error(
                        "Invalid json : $schema does not contains the correct value")

        if template_file_path and deployment_file_path:
            response = invoke_az_cli("deployment validate --location " + location +
                " --template-file " + template_file_path
                + " --parameters @" + deployment_file_path)

            data_record = create_database_record(node, snapshot_source, response, sub_data)
            
            if get_dbtests():
                insert_one_document(data_record, node['collection'], dbname)
            else:
                snapshot_dir = make_snapshots_dir(container)
                if snapshot_dir:
                    store_snapshot(snapshot_dir, data_record)
            snapshot_data[node['snapshotId']] = False if data_record['error'] else True
            node['status'] = 'active'
        else:
            node['status'] = 'inactive'
    else:
        node['status'] = 'inactive'
        logger.error("Invalid json : `paths` field is missing for 'arm' node type or it is not a list")

    return snapshot_data