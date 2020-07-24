"""
   Common file for running validator functions.
"""
import json
import copy
import hashlib
import time
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    STRUCTURE
from processor.helper.httpapi.restapi_azure import get_access_token,\
    get_web_client_data
from processor.connector.vault import get_vault_data
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import config_value, framework_dir, CUSTOMER
from processor.database.database import COLLECTION, get_documents
from processor.connector.snapshot_utils import get_data_record
from processor.connector.snapshot_exception import SnapshotsException

logger = getlogger()

###############  Refactored Code ######################


def get_node_version(node, snapshot):
    """Url version of the resource."""
    version = None
    apiversions = None
    logger.info("Get type's version")
    api_source = config_value('AZURE', 'api')
    if snapshot.isDb:
        parts = api_source.rsplit('/')
        name = parts[-1].split('.')
        qry = {'name': name[0]}
        docs = get_documents(snapshot.collection(STRUCTURE), dbname=snapshot.dbname, sort=snapshot.sort, query=qry, limit=1)
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

def get_snapshot_node(snapshot, token, sub_name, sub_id, node, user, snapshot_source, connector_type):
    """ Fetch node from azure portal using rest API."""
    version = get_node_version(node, snapshot)
    if sub_id and token and node and node['path'] and version:
        db_record = get_data_record(sub_name, node, user, snapshot_source, connector_type)
        hdrs = {
            'Authorization': 'Bearer %s' % token
        }
        if node['path'].startswith('/subscriptions'):
            urlstr = 'https://management.azure.com%s?api-version=%s'
            url = urlstr % (node['path'], version)
        else:
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
            logger.info("Get Id returned invalid status: %s, response: %s", status, data)
            logger.error("Failed to get Azure resourse with given path : %s, please verify your azure connector detail and path given in snapshot.", node['path'])
    else:
        logger.info('Get requires valid subscription, token and path.!')
    return db_record


def get_snapshot_nodes(snapshot, token, sub_name, sub_id, node, user, snapshot_source, connector_type):
    """ Fetch all nodes from azure portal using rest API."""
    db_records = []
    d_record = get_data_record(sub_name, node, user, snapshot_source, connector_type)
    nodetype = node['type'] if node and 'type' in node and node['type'] else None
    if sub_id and token and nodetype:
        hdrs = {
            'Authorization': 'Bearer %s' % token
        }
        resources = snapshot.get_value('resources')
        if not resources:
            urlstr = 'https://management.azure.com/subscriptions/%s/resources?api-version=2017-05-10'
            url = urlstr % sub_id
            logger.info('Get Id REST API invoked!')
            status, data = http_get_request(url, hdrs)
            logger.info('Get Id status: %s', status)
            if status and isinstance(status, int) and status == 200:
                resources = data['value']
                snapshot.store_value('resources', resources)
            else:
                put_in_currentdata('errors', data)
                logger.info("Get Id returned invalid status: %s", status)
        if resources:
            for idx, value in enumerate(resources):
                if nodetype in value['type']:
                    db_record = copy.deepcopy(d_record)
                    db_record['snapshotId'] = '%s%s' % (node['masterSnapshotId'], str(idx))
                    db_record['path'] = value['id']
                    db_record['json'] = value
                    data_str = json.dumps(value)
                    db_record['checksum'] = hashlib.md5(data_str.encode('utf-8')).hexdigest()
                    db_records.append(db_record)
    else:
        logger.info('Get requires valid subscription, token and path.!')
    return db_records


def get_web_client_data(snapshot_json, snapshot):
    """ Get the client id and secret, specific to azure"""
    client_id = None
    client_secret = None
    sub_id = None
    sub_name = None
    tenant_id = None
    found = False
    connector_type = None
    snapshot_user = get_field_value(snapshot_json, 'testUser')
    sub_data = snapshot.get_structure_data(snapshot_json)
    if sub_data and snapshot_user:
        connector_type = get_field_value(sub_data, "type")
        accounts = get_field_value(sub_data, 'accounts')
        for account in accounts:
            subscriptions = get_field_value(account, 'subscription')
            for subscription in subscriptions:
                users = get_field_value(subscription, 'users')
                if users:
                    for user in users:
                        name = get_field_value(user, 'name')
                        # Match user name and subscription Id (or name) TODO
                        if name and name == snapshot_user:
                            client_id = get_field_value(user, 'client_id')
                            client_secret = get_field_value(user, 'client_secret')
                            sub_id = get_field_value(subscription, 'subscription_id')
                            sub_name = get_field_value(subscription, 'subscription_name')
                            tenant_id = get_field_value(sub_data, 'tenant_id')
                            found = True
                        if found:
                            break
                if found:
                    break
            if found:
                break
    return client_id, client_secret, sub_name, sub_id, tenant_id, connector_type


def populate_snapshot_azure(snapshot_json, fssnapshot):
    """ Populates the resources from azure."""
    snapshot_data, valid_snapshotids = fssnapshot.validate_snapshot_ids_in_nodes(snapshot_json)
    client_id, client_secret, sub_name, sub_id, tenant_id, connector_type = get_web_client_data(snapshot_json, fssnapshot)

    if not client_id:
        logger.info("No client_id in the snapshot to access azure resource!...")
        # raise Exception("No client id in the snapshot to access azure resource!...")
        raise SnapshotsException("Container %s failure as no client id in the snapshot to access azure resource!..." % fssnapshot.container)

    # Read the client secrets from the vault
    if not client_secret:
        client_secret = get_vault_data(client_id)
        if client_secret:
            logger.info('Client Secret from Vault, Secret: %s', '*' * len(client_secret))
        elif fssnapshot.get_value(CUSTOMER):
            logger.error("Client Secret key does not set in a vault")
            raise SnapshotsException("Client Secret key does not set in a vault")

    if not client_secret:
        raise SnapshotsException("No `client_secret` key in the connector file to access azure resource!...")

    logger.info('Sub:%s, tenant:%s, client: %s', sub_id, tenant_id, client_id)
    fssnapshot.store_value('clientId', client_id)
    fssnapshot.store_value('clientSecret', client_secret)
    fssnapshot.store_value('subscriptionId', sub_id)
    fssnapshot.store_value('tenant_id', tenant_id)
    token = get_access_token()
    logger.debug('TOKEN: %s', token)
    if not token:
        logger.info("Unable to get access token, will not run tests....")
        raise SnapshotsException("Unable to get access token, will not run tests....")

    snapshot_source = get_field_value(snapshot_json, 'source')
    snapshot_user = get_field_value(snapshot_json, 'testUser')
    for node in fssnapshot.get_snapshot_nodes(snapshot_json):
        validate = node['validate'] if 'validate' in node else True
        if 'path' in node:
            data = get_snapshot_node(fssnapshot, token, sub_name, sub_id, node, snapshot_user, snapshot_source, connector_type)
            if data and validate:
                fssnapshot.store_data_node(data)
                snapshot_data[node['snapshotId']] = node['masterSnapshotId'] if 'masterSnapshotId' in node else True
                node['status'] = 'active'
            else:
                # TODO alert if notification enabled or summary for inactive.
                node['status'] = 'inactive'
            logger.debug('Type: %s', type(data))
        else:
            # Crawler Operation
            alldata = get_snapshot_nodes(fssnapshot, token, sub_name, sub_id, node, snapshot_user, snapshot_source, connector_type)
            if alldata:
                snapshot_data[node['masterSnapshotId']] = []
                for data in alldata:
                    found_old_record = False
                    for masterSnapshotId, snapshot_list in snapshot_data.items():
                        old_record = None
                        if isinstance(snapshot_list, list):
                            for item in snapshot_list:
                                if item["path"] == data['path']:
                                    old_record = item

                            if old_record:
                                found_old_record = True
                                if node['masterSnapshotId'] not in old_record['masterSnapshotId']:
                                    old_record['masterSnapshotId'].append(node['masterSnapshotId'])

                    if not found_old_record:
                        snapshot_data[node['masterSnapshotId']].append(
                            {
                                'masterSnapshotId': [node['masterSnapshotId']],
                                'snapshotId': data['snapshotId'],
                                'path': data['path'],
                                'validate': validate,
                                'status': 'active'
                            })
            logger.debug('Type: %s', type(alldata))
    return snapshot_data

