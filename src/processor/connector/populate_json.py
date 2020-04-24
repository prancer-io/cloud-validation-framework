from processor.helper.json.json_utils import get_field_value_with_default, get_field_value, json_from_file
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.vault import get_vault_data
from processor.connector.snapshot_custom import get_custom_data
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

def get_pwd_from_vault(password_key):
    password = get_vault_data(password_key)
    if not password:
        logger.info("Password does not set in the vault")
    return password


def git_clone_dir(connector):
    logger.info('connector')
    logger.info(connector)
    clonedir = None
    git_cmd = None
    repopath = tempfile.mkdtemp()
    subdir = False
    if connector and isinstance(connector, dict):
        giturl = get_field_value(connector, 'gitProvider')
        if not giturl:
            logger.error("Git connector does not have valid git provider URL")
            return repopath, clonedir
        brnch = get_field_value_with_default(connector, 'branchName', 'master')
        isprivate = get_field_value(connector, 'private')
        isprivate = True if isprivate is None or not isinstance(isprivate, bool) else isprivate
        logger.info("Repopath: %s", repopath)
        http_match = re.match(r'^http(s)?://', giturl, re.I)
        if http_match:
            logger.info("Http (private:%s) giturl: %s, Repopath: %s", "YES" if isprivate else "NO",
                        giturl, repopath)
            
            logger.info(connector)
            username = get_field_value(connector, 'httpsUser')
            logger.info("username")
            logger.info(username)
            if username:
                pwd = get_field_value(connector, 'httpsPassword')
                schema = giturl[:http_match.span()[-1]]
                other_part = giturl[http_match.span()[-1]:]
                pwd = pwd if not json_source() else get_pwd_from_vault(pwd)
                if pwd:
                    git_cmd = 'git clone %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username),
                                                        urllib.parse.quote_plus(pwd), other_part, repopath)
                # else:
                #     git_cmd = 'git clone %s%s@%s %s' % (schema, urllib.parse.quote_plus(username),
                #                                      other_part, repopath)
            else:
                git_cmd = 'git clone %s %s' % (giturl, repopath)
        else:
            logger.info("SSH (private:%s) giturl: %s, Repopath: %s", "YES" if isprivate else "NO",
                        giturl, repopath)
            if isprivate:
                ssh_key_file = get_field_value(connector, 'sshKeyfile')
                if not exists_file(ssh_key_file):
                    logger.error("Git connector points to a non-existent ssh keyfile!")
                    return repopath, clonedir
                ssh_host = get_field_value(connector, 'sshHost')
                ssh_user = get_field_value_with_default(connector, 'sshUser', 'git')
                if not ssh_host:
                    logger.error("SSH host not set, could be like github.com, gitlab.com, 192.168.1.45 etc")
                    return repopath, clonedir
                ssh_dir = '%s/.ssh' % repopath
                if exists_dir(ssh_dir):
                    logger.error("Git ssh dir: %s already exists, cannot recreate it!", ssh_dir)
                    return repopath, clonedir
                os.mkdir('%s/.ssh' % repopath, 0o700)
                ssh_cfg = create_ssh_config(ssh_dir, ssh_key_file, ssh_user)
                if not ssh_cfg:
                    logger.error("Creation of Git ssh config in dir: %s failed!", ssh_dir)
                    return repopath, clonedir
                git_ssh_cmd = 'ssh -o "StrictHostKeyChecking=no" -F %s' % ssh_cfg
                git_cmd = 'git clone %s %s/tmpclone' % (giturl, repopath)
                subdir = True
            else:
                git_ssh_cmd = 'ssh -o "StrictHostKeyChecking=no"'
                git_cmd = 'git clone %s %s' % (giturl, repopath)
            os.environ['GIT_SSH_COMMAND'] = git_ssh_cmd
            logger.info("GIT_SSH_COMMAND=%s", git_ssh_cmd)
        git_cmd = '%s --branch %s' % (git_cmd, brnch)
        logger.info("os.system(%s)", git_cmd)
        if git_cmd:
            run_subprocess_cmd(git_cmd)
            checkdir = '%s/tmpclone' % repopath if subdir else repopath
            clonedir = checkdir if exists_dir('%s/.git' % checkdir) else None
        if 'GIT_SSH_COMMAND' in os.environ:
            os.environ.pop('GIT_SSH_COMMAND')
    return repopath, clonedir

def pull_json_data(document_json):
    """
    Pull the JSON data from the git based on filetype and it will update the document json.
    """
    connector = get_field_value(document_json, "connector")
    file_location = get_field_value(document_json, "remoteFile")
    file_type = get_field_value(document_json, "fileType")
    

    if not connector:
        logger.info("Invalid snapshot: 'connector' field does not exists or it is empty.")
        return False

    if not file_location:
        logger.info("Invalid snapshot: 'remoteFile' field does not exists or it is empty.")
        return False

    if not file_type:
        logger.info("Invalid snapshot: 'fileType' field does not exists or it is empty.")
        return False

    connector_data = get_custom_data(connector)
    baserepo, repopath = git_clone_dir(connector_data)
    
    if repopath:
        json_path = '%s/%s' % (repopath, file_location)
        file_path = json_path.replace('//', '/')
        json_data = json_from_file(file_path, escape_chars=['$'])

        validate = False
        if file_type == "snapshot":
            validate = validate_snapshot_data(json_data, document_json)

        if file_type == "masterSnapshot":
            validate = validate_master_snapshot_data(json_data, document_json)

        if file_type == "test":
            validate = validate_test_data(json_data, document_json)

        if file_type == "mastertest":
            validate = validate_master_test_data(json_data, document_json)
        
        return validate
    else:
        logger.info('Require valid fields for populate JSON are not present!')

    return False

def validate_snapshot_data(snapshot_json, document_json):
    validate = True
    if "snapshots" not in snapshot_json:
        logger.info("Invalid json: 'Snapshots' field does not exists.")
        return False

    snapshots = snapshot_json["snapshots"]
    if not isinstance(snapshots, list):
        logger.info("Invalid json: 'Snapshots' field is not type list.")
        return False

    # Add validations based on snapshot type
    if validate:
        document_json["snapshots"] = snapshot_json["snapshots"]
    
    return validate

def validate_master_snapshot_data(master_snapshot_json, document_json):
    validate = True
    
    connector_users = get_field_value(document_json, "connectorUsers")
    if not connector_users:
        logger.info("Invalid snapshot: 'connectorUsers' field does not exists or it is empty.")
        return False

    if "snapshots" not in master_snapshot_json:
        logger.info("Invalid json: 'Snapshots' field does not exists.")
        return False

    snapshots = master_snapshot_json["snapshots"]
    if not isinstance(snapshots, list):
        logger.info("Invalid json: 'Snapshots' field is not type list.")
        return False

    for snapshot in snapshots:
        if "type" not in snapshot:
            logger.info("Invalid json: 'type' field is not exists in snapshot.")
            validate = False
            break

        if "connectorUser" not in snapshot:
            logger.info("Invalid json: 'connectorUser' field is not exists in snapshot.")
            validate = False
            break
        else:
            found_connector_user = False
            for connector_user in connector_users:
                if connector_user["id"] == snapshot["connectorUser"]:
                    logger.info(connector_user.items())
                    found_connector_user = True
                    for key, value in connector_user.items():
                        if key != "id":
                            snapshot[key] = value
        
            if not found_connector_user:
                logger.info("Invalid json: given 'connectorUser' not found in 'connectorUsers'.")
                validate = False
                break
            
        if "nodes" not in snapshot:
            logger.info("Invalid json: 'nodes' field is not exists in snapshot.")
            validate = False
            break

        if not isinstance(snapshot["nodes"], list):
            logger.info("Invalid json: 'snapshots -> nodes' field is not type list.")
            validate = False
            break

        for node in snapshot["nodes"]:
            if "masterSnapshotId" not in node:
                logger.info("Invalid json: 'masterSnapshotId' field is not exists in node.")
                validate = False
                break

            if "type" not in node:
                logger.info("Invalid json: 'type' field is not exists in node.")
                validate = False
                break

            if "collection" not in node:
                logger.info("Invalid json: 'collection' field is not exists in node.")
                validate = False
                break
        
        if not validate:
            break

    if validate:
        document_json["snapshots"] = master_snapshot_json["snapshots"]
    
    return validate    

def validate_test_data(test_json, document_json):
    pass

def validate_master_test_data(master_test_json, document_json):
    pass
