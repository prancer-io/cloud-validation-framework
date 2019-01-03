"""Common file for running validator functions."""
import json
import hashlib
import time
import tempfile
import shutil
import os
from git import Repo
from git import Git
from processor.helper.file.file_utils import exists_file, exists_dir, mkdir_path
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE
from processor.helper.config.config_utils import config_value, get_test_json_dir
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME
from processor.helper.httpapi.restapi_azure import json_source


logger = getlogger()


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
        custom_source = '%s/../%s' % (json_test_dir, snapshot_source)
        logger.info('Custom source: %s', custom_source)
        if exists_file(custom_source):
            sub_data = json_from_file(custom_source)
    return sub_data


def get_node(repopath, node):
    """ Fetch node from the cloned git repository."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    db_record = {
        "timestamp": int(time.time() * 1000),
        "queryuser": "",
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}
    }
    logger.info('DB: %s', db_record)
    json_path = '%s/%s' % (repopath, node['path'])
    file_path = json_path.replace('//', '/')
    logger.info('File: %s', file_path)
    if exists_file(file_path):
        json_data = json_from_file(file_path)
        if json_data:
            db_record['json'] = json_data
            data_str = json.dumps(json_data)
            db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    else:
        logger.info('Get requires valid file for snapshot not present!')
    return db_record


def populate_custom_snapshot(snapshot):
    """ Populates the resources from git."""
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    sub_data = get_custom_data(snapshot_source)
    # json_test_dir = get_test_json_dir()
    # custom_source = '%s/../%s' % (json_test_dir, snapshot_source)
    # logger.info('Custom source: %s', custom_source)
    # if exists_file(custom_source):
    #     sub_data = json_from_file(custom_source)
    if sub_data:
        giturl = get_field_value(sub_data, 'gitProvider')
        # repopath = get_field_value(sub_data, 'repoCloneAddress')
        ssh_key_file = get_field_value(sub_data, 'sshKeyfile')
        brnch = get_field_value(sub_data, 'branchName')
        repopath = tempfile.mkdtemp()
        exists, empty = valid_clone_dir(repopath)
        if exists and empty:
            try:
                if ssh_key_file and exists_file(ssh_key_file):
                    git_ssh_cmd = 'ssh -i %s' % ssh_key_file
                    with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
                        repo = Repo.clone_from(giturl, repopath, branch=brnch)
                else:
                    repo = Repo.clone_from(giturl, repopath, branch=brnch)
            except Exception as ex:
                logger.info('Unable to clone the repo: %s', ex)
                repo = None
            if repo:
                for node in snapshot['nodes']:
                    logger.info(node)
                    data = get_node(repopath, node)
                    if data:
                        insert_one_document(data, data['collection'], dbname)
                if os.path.exists(repopath):
                    shutil.rmtree(repopath)
                return True
        elif exists and not empty:
            try:
                Repo(repopath)
                logger.info("A repository exists in this directory: %s", repopath)
            except:
                logger.info("A non-empty directory, clean it and run: %s", repopath)
    return False


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
