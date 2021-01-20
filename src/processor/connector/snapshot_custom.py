"""Common file for running validator functions."""
# 1) github
# 1a) private
# HTTP - https://github.com/ajeybk/mytest.git
# username - kbajey@gmail.com or ajeybk
# password - prompt and env variable or form in the https url
# SSH - git@github.com:ajeybk/mytest.git
# identity file for host - /home/ajey/ssh_working/id_rsa_bitbucket

# 1b) public
# HTTP - https://github.com/prancer-io/cloud-validation-framework.git
# username - kbajey@gmail.com or ajeybk
# password - should not prompt, even if passed should work in url or from env variable, should work
# SSH - git@github.com:prancer-io/cloud-validation-framework.git
# identity file for host - /home/ajey/ssh_working/id_rsa_bitbucket

# 2) gitlab
# 2a) private
# HTTP - https://gitlab.com/tsdeepak/ulic_backend.git
# username - kbajey@gmail.com or kbajey
# password - prompt and env variable or form in the https url
# SSH - git@gitlab.com:kbajey/myrepo.git
# identity file for host - /home/ajey/ssh_working/id_rsa_bitbucket

# 2b) public
# HTTP - https://gitlab.com/kbajey/myrepo.git
# username - kbajey@gmail.com or kbajey
# password - prompt and env variable or form in the https url
# SSH - git@gitlab.com:kbajey/myrepo.git
# identity file for host - /home/ajey/ssh_working/id_rsa_bitbucket


# 3) bitbucket
# 3a) private
# HTTP - https://ajeybk@bitbucket.org/ajeybk/azframework.git
# username - kbajey@gmail.com or ajeybk
# password - prompt and env variable or form in the https url
# SSH - git@bitbucket.org:ajeybk/azframework.git
# identity file for host - /home/ajey/ssh_working/id_rsa_bitbucket

# 3b) public
# HTTP - https://ajeybk@bitbucket.org/ajeybk/aws-cli.git
# HTTP - https://ajeybk@bitbucket.org/ajeybk/mytestpub.git
# username - kbajey@gmail.com or ajeybk
# password - prompt and env variable or form in the https url
# SSH - git@bitbucket.org:ajeybk/aws-cli.git
# SSH - git@bitbucket.org:ajeybk/mytestpub.git
# identity file for host - /home/ajey/ssh_working/id_rsa_bitbucket

# 4) visualstudio
# 4a) private
# HTTP - https://ebizframework.visualstudio.com/whitekite/_git/whitekite
# HTTP - https://ajey.khanapuri%40liquware.com@ebizframework.visualstudio.com/whitekite/_git/whitekite
# username - ajey.khanapuri@liquware.com
# password - prompt and env variable or form in the https url
# SSH - Ebizframework@vs-ssh.visualstudio.com:v3/Ebizframework/whitekite/whitekite
# identity file for host - /home/ajey/ssh_working/id_rsa_azure
# 4b) public



#### Algorithm
# Add a attribute 'sshhost' : 'vs-ssh.visualstudio.com' or 'bitbucket.org' or 'gitlab.com' or 'github.com'
# Add a attribute 'sshuser': 'git' # All git servers expect 'git' as the user, but if there is an exception
# Add a attribute 'private': true|false
# For backward compatability it is assumed to be true.
# If giturl starts with https://, it is https based access otherwise ssh based access.

# For https public repo, username and password do not harm.
# For private https repo, read username from connector, if not present ignore.
# For https private repo, if username given, then read user_secret from connector, if present use,
# then check env variable, then prompt only

# For public ssh repo, ssh_key_file has to be present.
# Public repo clone with ssh_key_file does not require ssh/config file, whereas StrictHostKeyChecking=no
# may be required so that the user prompt may come up if githost is not present in known hosts.
# For private ssh repo with ssh_key_file, ssh/config file has to be created using 'sshhost', 'sshuser',
#  'ssh_key_file'
# Host <sshhost>
#   HostName <sshhost>
#   User <sshuser>
#   IdentityFile <ssh_key_file>
#
# Host *
#   IdentitiesOnly yes
#   ServerAliveInterval 100
import json
import hashlib
import time
import tempfile
import shutil
import hcl
import re
import os
import stat
import glob
import copy
import pymongo
from subprocess import Popen, PIPE
import urllib.parse
from git import Repo
from git import Git
from processor.helper.file.file_utils import exists_file, exists_dir, mkdir_path, remove_file
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE, get_field_value_with_default, \
    make_snapshots_dir, store_snapshot
from processor.helper.yaml.yaml_utils import yaml_from_file
from processor.helper.config.config_utils import config_value, get_test_json_dir
from processor.helper.config.rundata_utils import get_from_currentdata, get_dbtests
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME, get_collection_size, create_indexes
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.connector.vault import get_vault_data
from processor.template_processor.base.base_template_constatns import TEMPLATE_NODE_TYPES


logger = getlogger()

def convert_to_json(file_path, node_type):
    json_data = {}
    if node_type == 'json':
        json_data = json_from_file(file_path, escape_chars=['$'])
    elif node_type == 'terraform':
        with open(file_path, 'r') as fp:
            json_data = hcl.load(fp)
    elif node_type == 'yaml' or node_type == 'yml':
        json_data = yaml_from_file(file_path)
    else:
        logger.error("Snapshot error type:%s and file: %s", node_type, file_path)
    return json_data


def get_custom_data(snapshot_source, tabs=2):
    sub_data = {}
    if json_source():
        container = get_from_currentdata('container')
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0], 'container' : container }
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of Custom Documents: %d', len(docs))
        if docs and len(docs):
            sub_data = docs[0]['json']
    else:
        json_test_dir = get_test_json_dir()
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        custom_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('\t\tCUSTOM CONNECTOR: %s ', custom_source)
        # logger.info('Custom source: %s', custom_source)
        if exists_file(custom_source):
            sub_data = json_from_file(custom_source)
    return sub_data


def get_node(repopath, node, snapshot, ref, connector):
    """ Fetch node from the cloned git repository."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    given_type = get_field_value(connector, "type")
    base_path = get_field_value_with_default(connector, "folderPath", "")
    snapshot_source = get_field_value(snapshot, 'source')
    parts = snapshot_source.split('.')
    db_record = {
        "structure": given_type,
        "reference": ref if not base_path else "",
        "source": parts[0],
        "path": base_path + node['path'],
        "timestamp": int(time.time() * 1000),
        "queryuser": get_field_value(snapshot, 'testUser'),
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}
    }
    json_path = '%s/%s' % (repopath, node['path'])
    file_path = json_path.replace('//', '/')
    logger.info('\t\t\tFile: %s', file_path)
    if exists_file(file_path):
        node_type = node['type'] if 'type' in node and node['type'] else 'json'
        json_data = convert_to_json(file_path, node_type)
        # logger.info('type: %s, json:%s', node_type, json_data)
        # json_data = json_from_file(file_path)
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
    collection = node['collection'] if 'collection' in node else COLLECTION
    given_type = get_field_value(connector, "type")
    base_path = get_field_value_with_default(connector, "folderPath", "")
    snapshot_source = get_field_value(snapshot, 'source')
    parts = snapshot_source.split('.')
    d_record = {
        "structure": given_type,
        "reference": ref if not base_path else "",
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": get_field_value(snapshot, 'testUser'),
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": None,
        "masterSnapshotId": node['masterSnapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}
    }
    node_type = node['type'] if 'type' in node and node['type'] else 'json'
    json_path = '%s/%s' % (repopath, node['path'])
    file_path = json_path.replace('//', '/')
    logger.info('Dir: %s', file_path)
    if exists_dir(file_path):
        count = 0
        for filename in glob.glob('%s/*.json' % file_path.replace('//', '/')):
            parts = filename.rsplit('/', 1)
            path = '%s/%s' % (node['path'], parts[-1])
            json_data = convert_to_json(filename, node_type)
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
        # f.write('Host %s\n' % ssh_host)
        # f.write('   HostName %s\n' % ssh_host)
        f.write('   User %s\n' % ssh_user)
        f.write('   IdentityFile %s\n\n' % ssh_key_file)
        # f.write('Host *\n')
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
            logger.info("Git password from envirnment: %s", '*' * len(git_pwd))
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
        
        branch = get_from_currentdata('branch')
        if not branch:
            branch = get_field_value_with_default(connector, 'branchName', 'master')

        isprivate = get_field_value(connector, 'private')
        isprivate = True if isprivate is None or not isinstance(isprivate, bool) else isprivate
        # logger.info("Repopath: %s", repopath)
        logger.info("\t\t\tRepopath: %s", repopath)
        http_match = re.match(r'^http(s)?://', giturl, re.I)
        if http_match:
            logger.info("\t\t\tHttp (private:%s) giturl: %s", "YES" if isprivate else "NO", giturl)
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
                    git_cmd = 'git clone --depth 1 %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username),
                                                        urllib.parse.quote_plus(pwd), other_part, repopath)
                elif isprivate:
                    logger.error("Please provide password for connect to git repository.")
                    return repopath, clonedir
                else:
                    git_cmd = 'git clone --depth 1 %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username), "",
                                                     other_part, repopath)
            else:
                git_cmd = 'git clone --depth 1 %s %s' % (giturl, repopath)
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
        git_cmd = '%s --branch %s' % (git_cmd, branch)
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


def populate_custom_snapshot(snapshot, container=None):
    """ Populates the resources from git."""
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    connector_data = get_from_currentdata('connector')
    if connector_data:
        sub_data = get_custom_data(connector_data)
        if not sub_data:
            logger.error("No connector data found in '%s'", connector_data)
    else:
        sub_data = get_custom_data(snapshot_source)
    snapshot_nodes = get_field_value(snapshot, 'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    if valid_snapshotids and sub_data and snapshot_nodes:
        baserepo, repopath = _get_repo_path(sub_data, snapshot)
        if repopath:
            brnch = get_field_value_with_default(sub_data, 'branchName', 'master')
            for node in snapshot_nodes:
                node_type = node['type'] if 'type' in node and node['type'] else ''
                if node_type in TEMPLATE_NODE_TYPES:
                    template_data = {
                        "container" : container,
                        "dbname" : dbname,
                        "snapshot_source" : snapshot_source,
                        "connector_data" : sub_data,
                        "snapshot_data" : snapshot_data,
                        "repopath" : repopath,
                        "snapshot" : snapshot
                    }
                    template_processor = TEMPLATE_NODE_TYPES[node_type](node, **template_data)
                    if 'snapshotId' in node:
                        snapshot_data = template_processor.populate_template_snapshot()
                    elif 'masterSnapshotId' in node:
                        snapshot_data = template_processor.populate_all_template_snapshot()
                elif 'paths' in node:
                    logger.error("ERROR: Invalid json : `%s` is not a valid node type." % (node_type))
                else:
                    # logger.debug(node)
                    # data = get_node(repopath, node, snapshot_source, brnch)
                    # if data:
                    #     insert_one_document(data, data['collection'], dbname)
                    #     snapshot_data[node['snapshotId']] = True
                    validate = node['validate'] if 'validate' in node else True
                    if 'snapshotId' in node:
                        logger.debug(node)
                        data = get_node(repopath, node, snapshot, brnch, sub_data)
                        if data:
                            if validate:
                                if get_dbtests():
                                    if get_collection_size(data['collection']) == 0:
                                        #Creating indexes for collection
                                        create_indexes(data['collection'],
                                            config_value(DATABASE, DBNAME), 
                                            [('snapshotId', pymongo.ASCENDING),
                                            ('timestamp', pymongo.DESCENDING)])
                                            
                                        create_indexes(
                                            data['collection'], 
                                            config_value(DATABASE, DBNAME), 
                                            [
                                                ('_id', pymongo.DESCENDING),
                                                ('timestamp', pymongo.DESCENDING),
                                                ('snapshotId', pymongo.ASCENDING)
                                            ]
                                        )
                                    insert_one_document(data, data['collection'], dbname)
                                else:
                                    snapshot_dir = make_snapshots_dir(container)
                                    if snapshot_dir:
                                        store_snapshot(snapshot_dir, data)
                                if 'masterSnapshotId' in node:
                                    snapshot_data[node['snapshotId']] = node['masterSnapshotId']
                                else:
                                    snapshot_data[node['snapshotId']] = True
                            # else:
                            #     snapshot_data[node['snapshotId']] = False
                            node['status'] = 'active'
                        else:
                            node['status'] = 'inactive'
                        logger.debug('Type: %s', type(data))
                    elif 'masterSnapshotId' in node:
                        alldata = get_all_nodes(repopath, node, snapshot, brnch, sub_data)
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
            # logger.info('\t\tCLEANING Repo: %s', baserepo)
            shutil.rmtree(baserepo)
    return snapshot_data


def main():
    connectors = [
        {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "gitProvider": "https://github.com/ajeybk/mytest.git",
            "branchName": "master",
            "username": None,
            "password": None,
            "sshKeyfile": None,
            "private": True,
            "sshHost": "github.com",
            "sshUser": "git"
        },
        {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "gitProvider": "https://github.com/ajeybk/mytest.git",
            "branchName": "master",
            "username": "kbajey@gmail.com",
            "password": None,
            "sshKeyfile": None,
            "private": True,
            "sshHost": "github.com",
            "sshUser": "git"
        },
        {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "gitProvider": "https://github.com/ajeybk/mytest.git",
            "branchName": "master",
            "username": "ajeybk",
            "password": None,
            "sshKeyfile": None,
            "private": True,
            "sshHost": "github.com",
            "sshUser": "git"
        },
        {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "gitProvider": "git@github.com:ajeybk/mytest.git",
            "branchName": "master",
            "username": "ajeybk",
            "sshKeyfile": "/home/ajey/ssh_working/id_rsa_bitbucket",
            "private": True,
            "sshHost": "github.com",
            "sshUser": "git"
        },
        {
            "fileType": "structure",
            "type": "filesystem",            
            "companyName": "prancer-test",
            "gitProvider": "https://github.com/prancer-io/cloud-validation-framework.git",
            "branchName": "master",
            "username": "kbajey@gmail.com",
            "password": None,
            "sshKeyfile": None,
            "private": False,
            "sshHost": "github.com",
            "sshUser": "git"
        },
        {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "gitProvider": "git@github.com:prancer-io/prancer-hello-world.git",
            "branchName": "master",
            "sshKeyfile": None,
            "sshKeyName": "<thenameofthekeyinthevault>",
            "sshUser": "git",
            "sshHost": "github.com",
            "private": True
        }
    ]
    for conn in connectors:
        logger.info('#' * 50)
        repodir, clonedir = git_clone_dir(conn)
        logger.info("Delete: %s, clonedir: %s", repodir, clonedir)



if __name__ == "__main__":
    main()
