"""
   Common file for running validator functions.
"""
import json
import hashlib
import time
from git import Repo
from processor.helper.file.file_utils import check_filename
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, load_json
from processor.helper.config.config_utils import get_config, get_test_json_dir
from processor.database.database import insert_one_document, COLLECTION


logger = getlogger()


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
    if check_filename(file_path):
        json_data = load_json(file_path)
        if json_data:
            db_record['json'] = json_data
            data_str = json.dumps(json_data)
            db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    else:
        logger.info('Get requires valid file for snapshot not present!')
    return db_record


def populate_custom_snapshot(snapshot, snapshot_type='custom'):
    """ Populates the resources from git."""
    dbname = get_config('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    json_test_dir = get_test_json_dir()
    custom_source = '%s/../%s' % (json_test_dir, snapshot_source)
    logger.info('Custom source: %s', custom_source)
    if check_filename(custom_source):
        sub_data = load_json(custom_source)
        if sub_data:
            # print(sub_data)
            giturl = get_field_value(sub_data, 'gitProvider')
            repopath = get_field_value(sub_data, 'repoCloneAddress')
            brnch = get_field_value(sub_data, 'branchName')
            repo = Repo.clone_from(giturl, repopath, branch=brnch)
            if repo:
                for node in snapshot['nodes']:
                    logger.info(node)
                    data = get_node(repopath, node)
                    if data:
                        insert_one_document(data, data['collection'], dbname)
                return True
    return False

