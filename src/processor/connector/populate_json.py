from processor.helper.json.json_utils import get_field_value_with_default, get_field_value, json_from_file
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.vault import get_vault_data
from processor.connector.snapshot_custom import get_custom_data, git_clone_dir
from processor.logging.log_handler import getlogger
from subprocess import Popen, PIPE
import tempfile
import re
import os
import urllib

logger = getlogger()

def run_subprocess_cmd(cmd, ignoreerror=False, maskoutput=False, outputmask="Error output is masked"):
    """ Run a sub-process command"""
    result = ''
    error_result = None
    if cmd:
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)
        myprocess = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = myprocess.communicate()
        result = out.rstrip()
        error_result = err.rstrip() if err else None
        if isinstance(result, bytes):
            result = result.decode()
        if error_result and isinstance(error_result, bytes):
            error_result = error_result.decode()
        if not ignoreerror and error_result:
            if maskoutput:
                logger.info("OUTPUT: %s, ERROR: %s", outputmask, outputmask)
            else:
                logger.info("CMD: '%s', OUTPUT: %s, ERROR: %s", cmd, result, error_result)
    return error_result, result

def validate_snapshot_data(snapshot_json, document_json, file_location):
    validate = True
    if "snapshots" not in snapshot_json:
        logger.error("Invalid json %s: 'Snapshots' field is not exists in remote snapshot configuration file." % file_location)
        return False

    snapshots = snapshot_json["snapshots"]
    if not isinstance(snapshots, list):
        logger.error("Invalid json %s: 'Snapshots' field is not type of list." % file_location)
        return False

    # Add validations based on snapshot type
    if validate:
        document_json["snapshots"] = snapshot_json["snapshots"]
    
    return validate

def validate_master_snapshot_data(master_snapshot_json, document_json, file_location):
    validate = True
    
    connector_users = get_field_value(document_json, "connectorUsers")
    if not connector_users:
        logger.error("Invalid snapshot %s: 'connectorUsers' field does not exists or it is empty." % file_location)
        return False

    if "snapshots" not in master_snapshot_json:
        logger.error("Invalid json %s: 'Snapshots' field does not exists in mastersnapshot configuration file." % file_location)
        return False

    snapshots = master_snapshot_json["snapshots"]
    if not isinstance(snapshots, list):
        logger.error("Invalid json %s: 'Snapshots' field is not type list in snapshot configuration file." % file_location)
        return False

    for snapshot in snapshots:
        if "type" not in snapshot:
            logger.error("Invalid json %s: 'type' field is not exists in snapshot configuration file." % file_location)
            validate = False
            break

        if "connectorUser" not in snapshot:
            logger.error("Invalid json %s: 'connectorUser' field is not exists in snapshot configuration file." % file_location)
            validate = False
            break
        else:
            found_connector_user = False
            for connector_user in connector_users:
                if connector_user["id"] == snapshot["connectorUser"]:
                    found_connector_user = True
                    for key, value in connector_user.items():
                        if key != "id":
                            snapshot[key] = value
        
            if not found_connector_user:
                logger.error("Invalid json %s: `testUser` in snapshot configuration file is not mactch with the 'connectorUser' in remote snapshot file." % file_location)
                validate = False
                break
            
        if "nodes" not in snapshot:
            logger.error("Invalid json %s: 'nodes' field is not exists in snapshot configuration file." % file_location)
            validate = False
            break

        if not isinstance(snapshot["nodes"], list):
            logger.error("Invalid json %s: 'snapshots -> nodes' field is not type list." % file_location)
            validate = False
            break

        for node in snapshot["nodes"]:
            if "masterSnapshotId" not in node:
                logger.error("Invalid json %s: 'masterSnapshotId' field is not exists in node." % file_location)
                validate = False
                break

            if snapshot["type"] == "aws" and "arn" not in node:
                logger.error("Invalid json %s: 'arn' field is not exists in node." % file_location)
                validate = False
                break

            elif snapshot["type"] != "aws" and "type" not in node:
                logger.error("Invalid json %s: 'type' field is not exists in node." % file_location)
                validate = False
                break

            if "collection" not in node:
                logger.error("Invalid json %s: 'collection' field is not exists in node." % file_location)
                validate = False
                break
        
        if not validate:
            break

    if validate:
        document_json.pop("connector")
        document_json.pop("remoteFile")
        document_json.pop("connectorUsers")
        document_json["snapshots"] = master_snapshot_json["snapshots"]
    
    return validate    

def validate_test_data(test_json, document_json, file_location):
    validate = True
    
    if "testSet" not in test_json:
        logger.error("Invalid json %s: 'testSet' field does not exists." % file_location)
        return False

    testsets = test_json["testSet"]
    if not isinstance(testsets, list):
        logger.error("Invalid json %s: 'testSet' field is not type list." % file_location)
        return False

    for testset in testsets:
        if "testName" not in testset:
            logger.error("Invalid json %s: 'testName' field is not exists in testset." % file_location)
            validate = False
            break
            
        if "cases" not in testset:
            logger.error("Invalid json %s: 'cases' field is not exists in testset." % file_location)
            validate = False
            break

        if not isinstance(testset["cases"], list):
            logger.error("Invalid json %s: 'testset -> cases' field is not type list." % file_location)
            validate = False
            break

        for case in testset["cases"]:
            if "testId" not in case:
                logger.error("Invalid json %s: 'testId' field is not exists in case." % file_location)
                validate = False
                break
        
        if not validate:
            break

    if validate:
        document_json.pop("connector")
        document_json.pop("remoteFile")
        document_json["testSet"] = test_json["testSet"]
    
    return validate

def validate_master_test_data(master_test_json, document_json, file_location):
    validate = True
    
    if "testSet" not in master_test_json:
        logger.error("Invalid json %s: 'testSet' field does not exists." % file_location)
        return False

    testsets = master_test_json["testSet"]
    if not isinstance(testsets, list):
        logger.error("Invalid json %s: 'testSet' field is not type list." % file_location)
        return False

    for testset in testsets:
        if "masterTestName" not in testset:
            logger.error("Invalid json %s: 'masterTestName' field is not exists in testset." % file_location)
            validate = False
            break
            
        if "cases" not in testset:
            logger.error("Invalid json %s: 'cases' field is not exists in testset." % file_location)
            validate = False
            break

        if not isinstance(testset["cases"], list):
            logger.error("Invalid json %s: 'testset -> cases' field is not type list." % file_location)
            validate = False
            break

        for case in testset["cases"]:
            if "masterTestId" not in case:
                logger.error("Invalid json %s: 'masterTestId' field is not exists in case." % file_location)
                validate = False
                break
        
        if not validate:
            break

    if validate:
        document_json.pop("connector")
        document_json.pop("remoteFile")
        document_json["testSet"] = master_test_json["testSet"]
    
    return validate

def pull_json_data(document_json):
    """
    Pull the JSON data from the git based on filetype and it will update the document json.
    """
    dirpath = None
    connector = get_field_value(document_json, "connector")
    file_location = get_field_value(document_json, "remoteFile")
    file_type = get_field_value(document_json, "fileType")

    if not connector:
        logger.error("Invalid json: 'connector' field does not exists or it is empty.")
        return dirpath, False

    if not file_location:
        logger.error("Invalid json: 'remoteFile' field does not exists or it is empty.")
        return dirpath, False

    if not file_type:
        logger.error("Invalid json: 'fileType' field does not exists or it is empty.")
        return dirpath, False

    connector_data = get_custom_data(connector)
    baserepo, repopath = git_clone_dir(connector_data)
    
    if repopath:
        json_path = '%s/%s' % (repopath, file_location)
        dirpath = os.path.dirname(json_path)
        file_path = json_path.replace('//', '/')
        json_data = json_from_file(file_path, escape_chars=['$'])

        validate = False
        if json_data:
            if file_type == "snapshot":
                validate = validate_snapshot_data(json_data, document_json, file_location)

            if file_type == "masterSnapshot":
                validate = validate_master_snapshot_data(json_data, document_json, file_location)

            if file_type == "test":
                validate = validate_test_data(json_data, document_json, file_location)

            if file_type == "mastertest":
                validate = validate_master_test_data(json_data, document_json, file_location)
        else:
            logger.error("Failed to fetch remote file %s : either file does not exist or invalid file format!" % file_location)
        
        return dirpath, validate
    else:
        raise Exception("ERROR: Failed to clone the remote repository, check the connection configuration in %s connector. " % connector)

    return dirpath, False