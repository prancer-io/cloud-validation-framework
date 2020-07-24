"""Common file for running validator functions."""

import json
import hashlib
import tempfile
import shutil
import re
import os
from subprocess import Popen, PIPE
import stat
import glob
import copy
import urllib.parse
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, get_field_value_with_default
from processor.helper.config.rundata_utils import get_from_currentdata
from processor.connector.vault import get_vault_data
from processor.connector.snapshot_utils import get_data_record
from processor.template_processor.base.base_template_constatns import TEMPLATE_NODE_TYPES
from processor.connector.snapshot_base import Snapshot


logger = getlogger()


def get_node(repopath, node, snapshot, ref, connector):
    """ Fetch node from the cloned git repository."""
    base_path = get_field_value_with_default(connector, "folderPath", "")
    snapshot_source = get_field_value(snapshot, 'source')
    ref_name = ref if not base_path else ""
    ref_type = get_field_value(connector, "type")
    db_record = get_data_record(ref_name, node, "", snapshot_source, ref_type)
    # Modify path to point to  the actual path
    db_record["path"] = base_path + node['path']
    json_path = '%s/%s' % (repopath, node['path'])
    file_path = json_path.replace('//', '/')
    logger.info('File: %s', file_path)
    if exists_file(file_path):
        node_type = node['type'] if 'type' in node and node['type'] else 'json'
        json_data = Snapshot.convert_to_json(file_path, node_type)
        logger.info('type: %s, json:%s', node_type, json_data)
        if json_data:
            db_record['json'] = json_data
            data_str = json.dumps(json_data)
            db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    else:
        logger.info('Get requires valid file for snapshot not present!')
    logger.debug('DB: %s', db_record)
    return db_record


def get_all_nodes(repopath, node, snapshot, ref, connector):
    """ Fetch all the nodes from the cloned git repository in the given path."""
    db_records = []
    base_path = get_field_value_with_default(connector, "folderPath", "")
    snapshot_source = get_field_value(snapshot, 'source')
    ref_name = ref if not base_path else ""
    ref_type = get_field_value(connector, "type")
    d_record = get_data_record(ref_name, node, "", snapshot_source, ref_type)
    d_record["masterSnapshotId"] = node['masterSnapshotId']
    d_record["mastersnapshot"] = False
    node_type = node['type'] if 'type' in node and node['type'] else 'json'
    json_path = '%s/%s' % (repopath, node['path'])
    file_path = json_path.replace('//', '/')
    logger.info('Dir: %s', file_path)
    if exists_dir(file_path):
        count = 0
        for filename in glob.glob('%s/*.json' % file_path.replace('//', '/')):
            parts = filename.rsplit('/', 1)
            path = '%s/%s' % (node['path'], parts[-1])
            json_data = Snapshot.convert_to_json(filename, node_type)
            logger.info('type: %s, json:%s', node_type, json_data)
            if json_data:
                db_record = copy.deepcopy(d_record)
                db_record['snapshotId'] = '%s%s' % (node['masterSnapshotId'], str(count))
                db_record['path'] = path.replace('//', '/')
                db_record['json'] = json_data
                data_str = json.dumps(json_data)
                db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
                db_records.append(db_record)
                count += 1
    else:
        logger.info('Get requires valid directory for snapshot not present!')
    return db_records


def create_ssh_config(ssh_dir, ssh_key_file, ssh_user):
    ssh_config = '%s/config' % ssh_dir
    if exists_file(ssh_config):
        logger.error("Git config: %s already exists, cannot modify it!")
        return None
    with open(ssh_config, 'w') as f:
        f.write('Host *\n')
        f.write('   User %s\n' % ssh_user)
        f.write('   IdentityFile %s\n\n' % ssh_key_file)
        f.write('   IdentitiesOnly yes\n')
        f.write('   ServerAliveInterval 100\n')
    return ssh_config


def create_ssh_file_vault_data(ssh_dir, ssh_key_file_data, ssh_fname):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL  # Refer to "man 2 open".
    mode = stat.S_IRUSR | stat.S_IWUSR
    umask = 0o777 ^ mode
    umask_original = os.umask(umask)
    ssh_key_file = '%s/%s' % (ssh_dir, ssh_fname)
    try:
        fdesc = os.open(ssh_key_file, flags, mode)
        with os.fdopen(fdesc, 'w') as fout:
            for l in  ssh_key_file_data.split('\\n'):
                fout.write(l + '\n')
    finally:
        os.umask(umask_original)
    return ssh_key_file


def get_pwd_from_vault(password_key):
    """ Return the git password from vault """
    password = get_vault_data(password_key)
    if not password:
        logger.info("Password does not set in the vault")
    return password


def get_git_pwd(key='GIT_PWD'):
    """ Return the git password for https connection"""
    git_pwd = get_from_currentdata('GIT_PWD')
    if not git_pwd:
        git_pwd = os.getenv(key, None)
        if git_pwd:
            logger.debug("Git password from envirnment: %s", '*' * len(git_pwd))
    return git_pwd


def run_subprocess_cmd(cmd, ignoreerror=False, maskoutput=False, outputmask="Error output is masked"):
    """ Run a sub-process command"""
    result = ''
    errresult = None
    if cmd:
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)
        myprocess = Popen(cmd, shell=True, stdout=PIPE,
                                     stderr=PIPE,
                                     stdin=PIPE)
        out, err = myprocess.communicate()
        result = out.rstrip()
        errresult = err.rstrip() if err else None
        if isinstance(result, bytes):
            result = result.decode()
        if errresult and isinstance(errresult, bytes):
            errresult = errresult.decode()
    return errresult, result


def git_clone_dir(connector):
    clonedir = None
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
            username = get_field_value(connector, 'httpsUser')
            if username:
                pwd = get_field_value(connector, 'httpsPassword')
                schema = giturl[:http_match.span()[-1]]
                other_part = giturl[http_match.span()[-1]:]
                # pwd = pwd if (pwd and not json_source()) else (get_git_pwd() if not json_source() else get_pwd_from_vault(pwd))
                pwd = pwd if pwd else get_git_pwd(key=username)

                # populate the password from vault
                if not pwd:
                    pwd = get_pwd_from_vault(username)
                    if pwd:
                        logger.info("Git password from vault: %s", '*' * len(pwd))
                if pwd:
                    git_cmd = 'git clone %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username),
                                                        urllib.parse.quote_plus(pwd), other_part, repopath)
                elif isprivate:
                    logger.error("Please provide password for connect to git repository.")
                    return repopath, clonedir
                else:
                    git_cmd = 'git clone %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username), "",
                                                     other_part, repopath)
            else:
                git_cmd = 'git clone %s %s' % (giturl, repopath)
        else:
            logger.info("SSH (private:%s) giturl: %s, Repopath: %s", "YES" if isprivate else "NO",
                        giturl, repopath)
            if isprivate:
                ssh_key_file = get_field_value(connector, 'sshKeyfile')
                ssh_key_name = get_field_value(connector, 'sshKeyName')
                ssh_key_file_data = None
                if ssh_key_file:
                    if not exists_file(ssh_key_file):
                        logger.error("Git connector points to a non-existent ssh keyfile!")
                        return repopath, clonedir
                elif ssh_key_name:
                    ssh_key_file_data = get_vault_data(ssh_key_name)
                    if not ssh_key_file_data:
                        logger.info('Git connector points to a non-existent ssh keyName in the vault!')
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
                if not ssh_key_file and ssh_key_name and ssh_key_file_data:
                    ssh_key_file = create_ssh_file_vault_data(ssh_dir, ssh_key_file_data, ssh_key_name)
                    if not ssh_key_file:
                        logger.info('Git connector points to a non-existent ssh keyName in the vault!')
                        return repopath, clonedir
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
        git_cmd = '%s --branch %s' % (git_cmd, brnch)
        if git_cmd:
            error_result, result = run_subprocess_cmd(git_cmd)
            checkdir = '%s/tmpclone' % repopath if subdir else repopath
            clonedir = checkdir if exists_dir('%s/.git' % checkdir) else None
            if not exists_dir(clonedir):
                logger.error("No valid data provided for connect to git : %s", error_result)
        if 'GIT_SSH_COMMAND' in os.environ:
            os.environ.pop('GIT_SSH_COMMAND')
    return repopath, clonedir


def _local_file_directory(connector, snapshot):
    final_path, repopath = None, None
    connector_user = get_field_value(connector, 'username')
    snapshot_user = get_field_value(snapshot, 'testUser')
    if snapshot_user == connector_user:
        folder_path = get_field_value(connector, 'folderPath')
        logger.info("Folder path: %s", folder_path)
        if exists_dir(folder_path):
            final_path = folder_path
        else:
            logger.error("Given folder path is not a directory")
        return repopath, final_path
    else:
        logger.error("Connector and snapshot user do not match.")
        return repopath, final_path 


def _get_repo_path(connector, snapshot):
    if connector and isinstance(connector, dict):
        git_provider = get_field_value(connector, "gitProvider")
        folder_path = get_field_value(connector, "folderPath")
        if git_provider:
            return git_clone_dir(connector)
        elif folder_path:
            return _local_file_directory(connector, snapshot)
    logger.error("Invalid connector or missing folderPath/gitProvider")
    return None, None


def populate_snapshot_custom(snapshot_json, fssnapshot):
    """ Populates the resources from git, filesystem."""
    snapshot_data, valid_snapshotids = fssnapshot.validate_snapshot_ids_in_nodes(snapshot_json)
    sub_data = fssnapshot.get_structure_data(snapshot_json)
    if valid_snapshotids and sub_data:
        baserepo, repopath = _get_repo_path(sub_data, snapshot_json)
        if repopath:
            brnch = get_field_value_with_default(sub_data, 'branchName', 'master')
            snapshot_source = get_field_value(snapshot_json, 'source')
            for node in fssnapshot.get_snapshot_nodes(snapshot_json):
                node_type = node['type'] if 'type' in node and node['type'] else 'json'
                if node_type in TEMPLATE_NODE_TYPES:
                    template_data = {
                        "container": fssnapshot.container,
                        "dbname": fssnapshot.dbname,
                        "snapshot_source": snapshot_source,
                        "connector_data": sub_data,
                        "snapshot_data": snapshot_data,
                        "repopath": repopath,
                        "snapshot": snapshot_json
                    }
                    template_processor = TEMPLATE_NODE_TYPES[node_type](node, **template_data)
                    if 'snapshotId' in node:
                        snapshot_data = template_processor.populate_template_snapshot()
                    elif 'masterSnapshotId' in node:
                        snapshot_data = template_processor.populate_all_template_snapshot()
                else:
                    validate = node['validate'] if 'validate' in node else True
                    if 'snapshotId' in node:
                        logger.debug(node)
                        data = get_node(repopath, node, snapshot_json, brnch, sub_data)
                        if data and validate:
                            fssnapshot.store_data_node(data)
                            snapshot_data[node['snapshotId']] = node['masterSnapshotId'] if 'masterSnapshotId' in node else True
                            node['status'] = 'active'
                        else:
                            # TODO alert if notification enabled or summary for inactive.
                            node['status'] = 'inactive'
                        logger.debug('Type: %s', type(data))
                    elif 'masterSnapshotId' in node:
                        alldata = get_all_nodes(repopath, node, snapshot_json, brnch, sub_data)
                        if alldata:
                            snapshot_data[node['masterSnapshotId']] = []
                            for data in alldata:
                                snapshot_data[node['masterSnapshotId']].append(
                                    {
                                        'snapshotId': data['snapshotId'],
                                        'path': data['path'],
                                        'validate': validate
                                    })
                        logger.debug('Type: %s', type(alldata))
        if baserepo and os.path.exists(baserepo):
            logger.info('Repo path: %s', baserepo)
            shutil.rmtree(baserepo)
    return snapshot_data

