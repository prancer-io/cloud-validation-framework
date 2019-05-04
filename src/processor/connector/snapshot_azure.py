"""
   Common file for running validator functions.
"""
import json
import hashlib
import time
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata,\
    delete_from_currentdata
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE
from processor.helper.httpapi.restapi_azure import get_access_token,\
    get_web_client_data, get_client_secret, json_source
from processor.connector.vault import get_vault_data
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import config_value, framework_dir
from processor.database.database import insert_one_document, COLLECTION
from processor.database.database import DATABASE, DBNAME, sort_field, get_documents
from processor.connector.snapshot_utils import validate_snapshot_nodes


logger = getlogger()


def get_version_for_type(node):
    """Url version of the resource."""
    version = None
    logger.info("Get type's version")
    api_source = config_value('AZURE', 'api')
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = api_source.rsplit('/')
        name = parts[-1].split('.')
        qry = {'name': name[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of Azure API versions: %s', len(docs))
        if docs and len(docs):
            apiversions = docs[0]['json']
    else:
        apiversions_file = '%s/%s' % (framework_dir(), api_source)
        logger.info(apiversions_file)
        if exists_file(apiversions_file):
            apiversions = json_from_file(apiversions_file)
    if apiversions:
        if node and 'type' in node and node['type'] in apiversions:
            version = apiversions[node['type']]['version']
    return version


def get_node(token, sub_name, sub_id, node, user, snapshot_source):
    """ Fetch node from azure portal using rest API."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    db_record = {
        "structure": "azure",
        "reference": sub_name,
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": user,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    version = get_version_for_type(node)
    if sub_id and token and node and node['path'] and version:
        hdrs = {
            'Authorization': 'Bearer %s' % token
        }
        urlstr = 'https://management.azure.com/subscriptions/%s%s?api-version=%s'
        url = urlstr % (sub_id, node['path'], version)
        db_record['path'] = node['path']
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
    snapshot_nodes = get_field_value(snapshot, 'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    client_id, client_secret, sub_name, sub_id, tenant_id = \
        get_web_client_data(snapshot_type, snapshot_source, snapshot_user)
    if not client_id:
        logger.info("No client_id in the snapshot to access azure resource!...")
        return snapshot_data
    if not client_secret:
        client_secret = get_vault_data(client_id)
        if client_secret:
            logger.info('Vault Secret: %s', '*' * len(client_secret))
    if not client_secret:
        client_secret = get_client_secret()
        if client_secret:
            logger.info('Environment variable or Standard input, Secret: %s',
                        '*' * len(client_secret))
    if not client_secret:
        logger.info("No client secret in the snapshot to access azure resource!...")
        return snapshot_data
    logger.info('Sub:%s, tenant:%s, client: %s', sub_id, tenant_id, client_id)
    put_in_currentdata('clientId', client_id)
    put_in_currentdata('clientSecret', client_secret)
    put_in_currentdata('subscriptionId', sub_id)
    put_in_currentdata('tenant_id', tenant_id)
    token = get_access_token()
    logger.debug('TOKEN: %s', token)
    # snapshot_nodes = get_field_value(snapshot, 'nodes')
    # snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    if valid_snapshotids and token and snapshot_nodes:
        for node in snapshot_nodes:
            data = get_node(token, sub_name, sub_id, node, snapshot_user, snapshot_source)
            if data:
                insert_one_document(data, data['collection'], dbname)
                snapshot_data[node['snapshotId']] = True
            logger.debug('Type: %s', type(data))
        delete_from_currentdata('clientId')
        delete_from_currentdata('client_secret')
        delete_from_currentdata('subscriptionId')
        delete_from_currentdata('tenant_id')
        delete_from_currentdata('token')
    return snapshot_data
