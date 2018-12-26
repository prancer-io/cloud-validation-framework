"""
   Common file for running validator functions.
"""
import json
import hashlib
import time
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata, delete_from_currentdata
from processor.helper.json.json_utils import get_field_value, load_json
from processor.helper.httpapi.restapi_azure import get_access_token, get_web_client_data
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import config_value, framework_dir
from processor.database.database import insert_one_document, COLLECTION


logger = getlogger()


def get_version_for_type(node):
    """Url version of the resource."""
    version = None
    logger.info("Get type's version")
    apiversions_file = '%s/%s' % (framework_dir(), config_value('AZURE', 'api'))
    logger.info(apiversions_file)
    if exists_file(apiversions_file):
        apiversions = load_json(apiversions_file)
        if apiversions:
            if node and 'type' in node and node['type'] in apiversions:
                version = apiversions[node['type']]['version']
    return version


def get_node(token, sub_id, node, user):
    """ Fetch node from azure portal using rest API."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    db_record = {
        "timestamp": int(time.time() * 1000),
        "queryuser": user,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}
    }
    version = get_version_for_type(node)
    if sub_id and token and node and node['path'] and version:
        hdrs = {
            'Authorization': 'Bearer %s' % token
        }
        urlstr = 'https://management.azure.com/subscriptions/%s%s?api-version=%s'
        url = urlstr % (sub_id, node['path'], version)
        logger.info('Get Id REST API invoked!')
        status, data = http_get_request(url, hdrs)
        logger.info('Get Id status: %s', status)
        if status and isinstance(status, int) and status == 200:
            db_record['json'] = data
            data_str = json.dumps(data)
            db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
        else:
            put_in_currentdata('errors', data)
            logger.info("Get Id returned invalid status: %s", status)
    else:
        logger.info('Get requires valid subscription, token and path.!')
    return db_record


def populate_azure_snapshot(snapshot, snapshot_type='azure'):
    """ Populates the resources from azure."""
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_user = get_field_value(snapshot, 'testUser')
    client_id, client_secret, sub_id, tenant_id = \
        get_web_client_data(snapshot_type, snapshot_source, snapshot_user)
    if not client_id:
        logger.info("No client_id in the snapshot to access azure resource!...")
        return False
    logger.info('Sub:%s, tenant:%s, client: %s', sub_id, tenant_id, client_id)
    put_in_currentdata('clientId', client_id)
    put_in_currentdata('clientSecret', client_secret)
    put_in_currentdata('subscriptionId', sub_id)
    put_in_currentdata('tenant_id', tenant_id)
    token = get_access_token()
    logger.debug('TOKEN: %s', token)
    if token:
        for node in snapshot['nodes']:
            data = get_node(token, sub_id, node, snapshot_user)
            if data:
                insert_one_document(data, data['collection'], dbname)
            logger.debug('Type: %s', type(data))
        delete_from_currentdata('clientId')
        delete_from_currentdata('client_secret')
        delete_from_currentdata('subscriptionId')
        delete_from_currentdata('tenant_id')
        delete_from_currentdata('token')
        return True
    return False

