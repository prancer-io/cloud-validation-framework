"""Common file for running validator functions."""
import json
import hashlib
import time
import tempfile
import shutil
import hcl
import os
from git import Repo
from git import Git
from processor.helper.file.file_utils import exists_file, exists_dir, mkdir_path, remove_file
from processor.logging.log_handler import getlogger
from processor.connector.vault import get_vault_data
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE
from processor.helper.config.config_utils import config_value, get_test_json_dir
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.snapshot_utils import validate_snapshot_nodes


logger = getlogger()

def convert_to_json(file_path, node_type):
    json_data = {}
    if node_type == 'json':
        json_data = json_from_file(file_path)
    elif node_type == 'terraform':
        with open(file_path, 'r') as fp:
            json_data = hcl.load(fp)
    else:
        logger.error("Snapshot error type:%s and file: %s", node_type, file_path)
    return json_data


def get_custom_data(snapshot_source):
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
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
        logger.info('Custom source: %s', custom_source)
        if exists_file(custom_source):
            sub_data = json_from_file(custom_source)
    return sub_data


def get_node(repopath, node, snapshot_source, ref):
    """ Fetch node from the cloned git repository."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    db_record = {
        "structure": "git",
        "reference": ref,
        "source": parts[0],
        "path": node['path'],
        "timestamp": int(time.time() * 1000),
        "queryuser": "",
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}
    }
    json_path = '%s/%s' % (repopath, node['path'])
    file_path = json_path.replace('//', '/')
    logger.info('File: %s', file_path)
    if exists_file(file_path):
        node_type = node['type'] if 'type' in node and node['type'] else 'json'
        json_data = convert_to_json(file_path, node_type)
        logger.info('type: %s, json:%s', node_type, json_data)
        # json_data = json_from_file(file_path)
        if json_data:
            db_record['json'] = json_data
            data_str = json.dumps(json_data)
            db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    else:
        logger.info('Get requires valid file for snapshot not present!')
    logger.debug('DB: %s', db_record)
    return db_record


def populate_custom_snapshot(snapshot):
    """ Populates the resources from git."""
    user_secret = None
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    sub_data = get_custom_data(snapshot_source)
    snapshot_nodes = get_field_value(snapshot, 'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    if valid_snapshotids and sub_data and snapshot_nodes:
        giturl = get_field_value(sub_data, 'gitProvider')
        ssh_file = get_field_value(sub_data, 'sshKeyfile')
        brnch = get_field_value(sub_data, 'branchName')
        username = get_field_value(sub_data, 'username')
        if ssh_file:
            if exists_file('%s/%s' % (os.environ['HOME'], ssh_file)):
                ssh_key_file = '%s/%s' % (os.environ['HOME'], ssh_file)
            elif exists_file('%s/.ssh/%s' % (os.environ['HOME'], ssh_file)):
                ssh_key_file = '%s/.ssh/%s' % (os.environ['HOME'], ssh_file)
            else:
                ssh_key_file = None
        else:
            ssh_key_file = None
        # if username:
        #     user_secret = get_vault_data(username)
        #     logger.info('Secret: %s', user_secret)
        repopath = tempfile.mkdtemp()
        logger.info("Repopath: %s", repopath)
        exists, empty = valid_clone_dir(repopath)
        if exists and empty:
            try:
                if ssh_key_file and exists_file(ssh_key_file):
                    # restore, olddir, newdir, ssh_file = make_ssh_dir_before_clone(ssh_key_file)
                    git_ssh_cmd = 'ssh -i %s' % ssh_key_file
                    with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
                        repo = Repo.clone_from(giturl, repopath, branch=brnch)
                    # restore_ssh_dir_after_clone(restore, olddir, newdir)
                else:
                    # if username and user_secret:
                    #    giturl = giturl.replace('https://', 'https://%s:%s@' %(username, user_secret))
                    # elif username:
                    #    giturl = giturl.replace('https://', 'https://%s@' % username)
                    repo = Repo.clone_from(giturl, repopath, branch=brnch)
            except Exception as ex:
                logger.info('Unable to clone the repo: %s', ex)
                repo = None
            if repo:
                for node in snapshot_nodes:
                    logger.debug(node)
                    data = get_node(repopath, node, snapshot_source, brnch)
                    if data:
                        insert_one_document(data, data['collection'], dbname)
                        snapshot_data[node['snapshotId']] = True
                if os.path.exists(repopath):
                    logger.info('Repo path: %s', repopath)
                    shutil.rmtree(repopath)
        # elif exists and not empty:
        #     try:
        #         Repo(repopath)
        #         logger.info("A repository exists in this directory: %s", repopath)
        #     except:
        #         logger.info("A non-empty directory, clean it and run: %s", repopath)
    return snapshot_data


def valid_clone_dir(dirname):
    if exists_dir(dirname):
        exists = True
        if not os.listdir(dirname):
            empty = True
        else:
            empty = False
    else:
        exists = mkdir_path(dirname)
        if exists and not os.listdir(dirname):
            empty = True
        else:
            empty = False
    return exists, empty

def restore_ssh_dir_after_clone(restore, olddir, newdir):
    if restore:
        if exists_dir(olddir):
            shutil.rmtree(newdir, ignore_errors=True)
        if exists_dir(newdir):
            os.rename(newdir, olddir)


def make_ssh_dir_before_clone(ssh_key_file):
    restore = False
    newdir = None
    olddir = None
    ssh_file = None
    if ssh_key_file and exists_file(ssh_key_file):
        restore = True
        tempdir = tempfile.mkdtemp()
        # print(tempdir)
        ssh_parts = ssh_key_file.rsplit('/', 1)
        new_ssh_key_file = '%s/%s' % (tempdir, ssh_parts[-1])
        # print(new_ssh_key_file)
        shutil.copy(ssh_key_file, new_ssh_key_file)
        olddir = '%s/.ssh' % os.environ['HOME']
        # print(olddir)
        if exists_dir(olddir):
            newdir = '%s_old' % olddir
            # print(newdir)
            if exists_dir(newdir):
                shutil.rmtree(newdir, ignore_errors=True)
            os.rename(olddir, newdir)
        os.mkdir(olddir)
        ssh_file = '%s/id_rsa' % olddir
        shutil.copy(new_ssh_key_file, ssh_file)
        remove_file(new_ssh_key_file)
        cfg = '%s/config' % olddir
        with open(cfg, 'w') as f:
            f.write('Host *\n')
            f.write('    StrictHostKeyChecking no\n')
    return restore, olddir, newdir, ssh_file
