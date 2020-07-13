"""
   Common file for running validator functions.
"""
import json
import copy
import hashlib
import time
import pymongo
import os
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata,\
    delete_from_currentdata, get_from_currentdata, get_dbtests
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE, TEST, MASTERTEST, SNAPSHOT, MASTERSNAPSHOT, make_snapshots_dir,\
    store_snapshot, get_field_value_with_default, get_json_files, get_container_snapshot_json_files
from processor.helper.httpapi.restapi_azure import get_access_token,\
    get_web_client_data, get_client_secret, json_source
from processor.connector.vault import get_vault_data
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import config_value, framework_dir, CUSTOMER, get_test_json_dir
from processor.database.database import insert_one_document, COLLECTION, get_collection_size, create_indexes, \
     DATABASE, DBNAME, sort_field, get_documents, update_one_document
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.connector.populate_json import pull_json_data
from processor.reporting.json_output import dump_output_results

from processor.connector.snapshot_custom import populate_custom_snapshot, get_custom_data





logger = getlogger()



def get_version_for_type(node):
    """Url version of the resource."""
    version = None
    apiversions = None
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

def get_all_nodes(token, sub_name, sub_id, node, user, snapshot_source):
    """ Fetch all nodes from azure portal using rest API."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    db_records = []
    d_record = {
        "structure": "azure",
        "reference": sub_name,
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": user,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": None,
        "mastersnapshot": True,
        "masterSnapshotId": [node['masterSnapshotId']],
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    # version = get_version_for_type(node)
    # if sub_id and token and node and version:
    nodetype = None
    if node and 'type' in node and node['type']:
        nodetype = node['type']
    if sub_id and token and nodetype:
        hdrs = {
            'Authorization': 'Bearer %s' % token
        }
        # urlstr = 'https://management.azure.com/subscriptions/%s/providers/%s?api-version=%s'
        # url = urlstr % (sub_id, node['type'], version)
        # db_record['path'] = node['path']
        resources = get_from_currentdata('resources')
        if not resources:
            urlstr = 'https://management.azure.com/subscriptions/%s/resources?api-version=2017-05-10'
            url = urlstr % sub_id
            logger.info('Get Id REST API invoked!')
            status, data = http_get_request(url, hdrs)
            logger.info('Get Id status: %s', status)
            if status and isinstance(status, int) and status == 200:
                resources = data['value']
                put_in_currentdata('resources', resources)
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

def get_node(token, sub_name, sub_id, node, user, snapshot_source):
    """ Fetch node from azure portal using rest API."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    db_records = []
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
        "mastersnapshot": False,
        "masterSnapshotId": None,
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    version = get_version_for_type(node)
    if sub_id and token and node and node['path'] and version:
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


def populate_azure_snapshot(snapshot, container=None, snapshot_type='azure'):
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
        raise Exception("No client id in the snapshot to access azure resource!...")

    # Read the client secrets from envirnment variable
    if not client_secret:
        client_secret = os.getenv(snapshot_user, None)
        if client_secret:
            logger.info('Client Secret from environment variable, Secret: %s', '*' * len(client_secret))
        
    # Read the client secrets from the vault
    if not client_secret:
        client_secret = get_vault_data(client_id)
        if client_secret:
            logger.info('Client Secret from Vault, Secret: %s', '*' * len(client_secret))
        elif get_from_currentdata(CUSTOMER):
            logger.error("Client Secret key does not set in a vault")
            raise Exception("Client Secret key does not set in a vault")

    if not client_secret:
        raise Exception("No `client_secret` key in the connector file to access azure resource!...")

    logger.info('Sub:%s, tenant:%s, client: %s', sub_id, tenant_id, client_id)
    put_in_currentdata('clientId', client_id)
    put_in_currentdata('clientSecret', client_secret)
    put_in_currentdata('subscriptionId', sub_id)
    put_in_currentdata('tenant_id', tenant_id)
    token = get_access_token()
    logger.debug('TOKEN: %s', token)
    if not token:
        logger.info("Unable to get access token, will not run tests....")
        raise Exception("Unable to get access token, will not run tests....")
        # return {}

    # snapshot_nodes = get_field_value(snapshot, 'nodes')
    # snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    if valid_snapshotids and token and snapshot_nodes:
        for node in snapshot_nodes:
            validate = node['validate'] if 'validate' in node else True
            if 'path' in  node:
                data = get_node(token, sub_name, sub_id, node, snapshot_user, snapshot_source)
                if data:
                    if validate:
                        if get_dbtests():
                            if get_collection_size(data['collection']) == 0:
                                # Creating indexes for collection
                                create_indexes(
                                    data['collection'], 
                                    config_value(DATABASE, DBNAME), 
                                    [
                                        ('snapshotId', pymongo.ASCENDING),
                                        ('timestamp', pymongo.DESCENDING)
                                    ]
                                )

                                create_indexes(
                                    data['collection'], 
                                    config_value(DATABASE, DBNAME), 
                                    [
                                        ('_id', pymongo.DESCENDING),
                                        ('timestamp', pymongo.DESCENDING),
                                        ('snapshotId', pymongo.ASCENDING)
                                    ]
                                )
                            insert_one_document(data, data['collection'], dbname, check_keys=False)
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
                    # TODO alert if notification enabled or summary for inactive.
                    node['status'] = 'inactive'
                logger.debug('Type: %s', type(data))
            else:
                alldata = get_all_nodes(
                    token, sub_name, sub_id, node, snapshot_user, snapshot_source)
                if alldata:
                    snapshot_data[node['masterSnapshotId']] = []
                    for data in alldata:
                        # insert_one_document(data, data['collection'], dbname)
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
                                        old_record['masterSnapshotId'].append(
                                            node['masterSnapshotId'])

                        if not found_old_record:
                            snapshot_data[node['masterSnapshotId']].append(
                                {
                                    'masterSnapshotId': [node['masterSnapshotId']],
                                    'snapshotId': data['snapshotId'],
                                    'path': data['path'],
                                    'validate': validate,
                                    'status': 'active'
                                })
                    # snapshot_data[node['masterSnapshotId']] = True
                logger.debug('Type: %s', type(alldata))
        delete_from_currentdata('resources')
        delete_from_currentdata('clientId')
        delete_from_currentdata('client_secret')
        delete_from_currentdata('subscriptionId')
        delete_from_currentdata('tenant_id')
        delete_from_currentdata('token')
    return snapshot_data

###############  Refactored Code ######################

# def get_data_record(node, sub_name, snapshot_source):
def get_data_record(sub_name, node, user, snapshot_source):
    """ The data node record, common function across connectors."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    return {
        "structure": "azure",
        "reference": sub_name,
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": user,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "mastersnapshot": False,
        "masterSnapshotId": None,
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }


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

def get_snapshot_node(snapshot, token, sub_name, sub_id, node, user, snapshot_source):
    """ Fetch node from azure portal using rest API."""
    version = get_node_version(node, snapshot)
    if sub_id and token and node and node['path'] and version:
        db_record = get_data_record(sub_name, node, user, snapshot_source)
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


def get_snapshot_nodes(snapshot, token, sub_name, sub_id, node, user, snapshot_source):
    """ Fetch all nodes from azure portal using rest API."""
    db_records = []
    d_record = get_data_record(sub_name, node, user, snapshot_source)
    nodetype = None
    if node and 'type' in node and node['type']:
        nodetype = node['type']
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


def get_web_client_data1(snapshot_json, snapshot):
    """ Get the client id and secret, specific to azure"""
    client_id = None
    client_secret = None
    sub_id = None
    sub_name = None
    tenant_id = None
    found = False
    snapshot_user = get_field_value(snapshot_json, 'testUser')
    sub_data = snapshot.get_structure_data(snapshot_json)
    if sub_data and snapshot_user:
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
    return client_id, client_secret, sub_name, sub_id, tenant_id


def populate_snapshot_azure(snapshot_json, fssnapshot):
    """ Populates the resources from azure."""
    snapshot_data, valid_snapshotids = fssnapshot.validate_snapshot_ids_in_nodes(snapshot_json)
    client_id, client_secret, sub_name, sub_id, tenant_id = get_web_client_data(snapshot_json, fssnapshot)

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
            data = get_snapshot_node(fssnapshot, token, sub_name, sub_id, node, snapshot_user, snapshot_source)
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
            alldata = get_snapshot_nodes(fssnapshot, token, sub_name, sub_id, node, snapshot_user, snapshot_source)
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


class SnapshotsException(Exception):
    """Exception raised for snapshots"""

    def __init__(self, message="Error in snapshots for container"):
        self.message = message
        super().__init__(self.message)



class Snapshot:
    """ Base class for snapshot processing"""

    LOGPREFIX = 'Snapshots:'
    snapshot_fns = {
        'azure1': populate_snapshot_azure,
        'azure': populate_azure_snapshot,
        'filesystem': populate_custom_snapshot
    }

    def __init__(self, container):
        """ Base class, where all attributes are false."""
        self.container = container
        self.appObject = {}
        self.singleTest = None
        self.isDb = False

    def store_value(self, key, value):
        """ Store key value used down the p[rocessing stream."""
        if key and value:
            self.appObject[key] = value

    def get_value(self, key):
        """ Use the app storage and will be garbage collected after the completion of the snapshot fetch process."""
        if key and key in self.appObject:
            return self.appObject.get(key)
        return None

    def get_snapshots(self):
        """ Iterator based implementation"""
        return []

    def get_snapshot_nodes(self, snapshot):
        """ Iterate over the nodes of the snapshot object"""
        snapshot_nodes = get_field_value(snapshot, 'nodes')
        return snapshot_nodes if snapshot_nodes else []

    def validate_snapshot_ids_in_nodes(self, snapshot):
        """ The snapshotsIds should be strings and also quoted."""
        snapshot_data = {}
        valid_snapshotids = True
        for node in self.get_snapshot_nodes(snapshot):
            if 'snapshotId' in node and node['snapshotId']:
                snapshot_data[node['snapshotId']] = False
                if not isinstance(node['snapshotId'], str):
                    valid_snapshotids = False
            elif 'masterSnapshotId' in node and node['masterSnapshotId']:
                snapshot_data[node['masterSnapshotId']] = False
                if not isinstance(node['masterSnapshotId'], str):
                    valid_snapshotids = False
            else:
                logger.error(
                    'All snapshot nodes should contain snapshotId or masterSnapshotId attribute with a string value')
                valid_snapshotids = False
                break
        if not valid_snapshotids:
            logger.error('All snapshot Ids should be strings, even numerals should be quoted')
        return snapshot_data, valid_snapshotids

    def check_and_fetch_remote_snapshots(self, json_data):
        """Could be snapshot that snapshots are fetched from remote repository."""
        git_connector_json = False
        pull_response = False
        if "connector" in json_data and "remoteFile" in json_data and \
                json_data["connector"] and json_data["remoteFile"]:
            git_connector_json = True
            _, pull_response = pull_json_data(json_data)
        return pull_response, git_connector_json

    def get_structure_data(self, snapshot_object):
        """ Return a empty dict in base class."""
        structure_data = {}
        return structure_data

    def store_data_node(self, data):
        """ Store the data record as per the data system"""
        return False

    def populate_snapshots(self, snapshot_json_data):
        """
        Every snapshot should have collection of nodes which are to be populated.
        Each node in the nodes list of the snapshot shall have a unique id in this
        container so as not to clash with other node of a snapshots.
        """
        snapshot_data = {}
        snapshots = get_field_value(snapshot_json_data, 'snapshots')
        if not snapshots:
            logger.error("Json Snapshot does not contain snapshots, next!...")
            return snapshot_data
        for snapshot in snapshots:
            connector_data = self.get_structure_data(snapshot)
            snapshot_type = get_field_value(connector_data, "type")
            if snapshot_type and snapshot_type in self.snapshot_fns:
                if 'nodes' not in snapshot or not snapshot['nodes']:
                    logger.error("No nodes in snapshot to be backed up!...")
                    return snapshot_data
                if snapshot_type == 'azure' or snapshot_type == 'filesystem':
                    current_data = self.snapshot_fns[snapshot_type](snapshot, self.container)
                else:
                    current_data = self.snapshot_fns[snapshot_type](snapshot, self)
                logger.info('Snapshot: %s', current_data)
                snapshot_data.update(current_data)
        return snapshot_data


class FSSnapshot(Snapshot):
    """
    Filesystem snapshot utilities.
    """
    def __init__(self, container, singleTest=None):
        """ Default isDb is false, singletest shall be set to the test that needs to be run."""
        super().__init__(container)
        self.singleTest = singleTest
        reporting_path = config_value('REPORTING', 'reportOutputFolder')
        self.container_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)

    def get_structure_data(self, snapshot_object):
        """ Get the structure from the filesystem."""
        structure_data = {}
        json_test_dir = get_test_json_dir()
        snapshot_source = get_field_value(snapshot_object, "source")
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        custom_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('%s structure file is %s', Snapshot.LOGPREFIX, custom_source)
        if exists_file(custom_source):
            structure_data = json_from_file(custom_source)
        return structure_data

    def get_used_snapshots_in_tests(self):
        """ Iterate through all snapshot and mastersnapshot and list the used snapshots in tests or mastertest."""
        snapshots = []
        logger.info("%s Fetching files for %s from container dir: %s", Snapshot.LOGPREFIX, self.container,
                    self.container_dir)
        for testType, snapshotType, replace in (
                (TEST, SNAPSHOT, False),
                (MASTERTEST, MASTERSNAPSHOT, True)):
            test_files = get_json_files(self.container_dir, testType)
            logger.info('%s fetched %s number of files from %s container: %s', Snapshot.LOGPREFIX, snapshotType,
                        self.container, len(test_files))
            snapshots.extend(self.process_files(test_files, snapshotType, replace))
        return list(set(snapshots))


    def process_files(self, test_files, doctype, replace=False):
        """ Process Test or masterTest json files."""
        snapshots = []
        for test_file in test_files:
            test_json_data = json_from_file(test_file)
            if test_json_data:
                snapshot = test_json_data[doctype] if doctype in test_json_data else ''
                if snapshot:
                    file_name = snapshot if snapshot.endswith('.json') else '%s.json' % snapshot
                    if replace:
                        file_name = file_name.replace('.json', '_gen.json')
                    if self.singleTest:
                        testsets = get_field_value_with_default(test_json_data, 'testSet', [])
                        for testset in testsets:
                            for testcase in testset['cases']:
                                if ('testId' in testcase and testcase['testId'] == self.singleTest) or \
                                        ('masterTestId' in testcase and testcase['masterTestId'] == self.singleTest):
                                    if file_name not in snapshots:
                                        snapshots.append(file_name)
                    else:
                        snapshots.append(file_name)
        return snapshots

    def store_data_node(self, data):
        """Store the data in the filesystem"""
        # Make a snapshots directory if DB is NONW
        snapshot_dir = make_snapshots_dir(self.container)
        if snapshot_dir:
            store_snapshot(snapshot_dir, data)

    def get_snapshots(self):
        """
        Get the snapshot files from the container with storage system as filesystem.
        The path for looking into the container is configured in the config.ini, for the
        default location configuration is $SOLUTIONDIR/relam/validation/<container>
        """
        snapshots_status = {}
        snapshot_dir, snapshot_files = get_container_snapshot_json_files(self.container)
        if not snapshot_files:
            logger.error("%s No Snapshot for this container: %s, in %s, add and run again!...", Snapshot.LOGPREFIX, self.container, snapshot_dir)
            raise SnapshotsException("No snapshots for this container: %s, add and run again!..." % self.container)
        used_snapshots = self.get_used_snapshots_in_tests()
        populated = []
        for snapshot_file in snapshot_files:
            parts = snapshot_file.rsplit('/', 1)
            if parts[-1] in used_snapshots and parts[-1] not in populated:
                # Take the snapshot and populate whether it was successful or not.
                # Then pass it back to the validation tests, so that tests for those
                # snapshots that have been susccessfully fetched shall be executed.
                file_name = '%s.json' % snapshot_file if snapshot_file and not snapshot_file.endswith('.json') else snapshot_file
                snapshot_json_data = json_from_file(file_name)
                if not snapshot_json_data:
                    logger.info("%s snapshot file %s looks to be empty, next!...",  Snapshot.LOGPREFIX, snapshot_file)
                    continue

                pull_response, git_connector_json = self.check_and_fetch_remote_snapshots(snapshot_json_data)
                if git_connector_json and not pull_response:
                    logger.info('%s Fetching remote snapshots failed.', Snapshot.LOGPREFIX)
                    break

                logger.debug(json.dumps(snapshot_json_data, indent=2))
                snapshot_data = self.populate_snapshots(snapshot_json_data)
                populated.append(parts[-1])
                name = parts[-1].replace('.json', '') if parts[-1].endswith('.json') else parts[-1]
                snapshots_status[name] = snapshot_data
        return snapshots_status


class DBSnapshot(Snapshot):
    """
    Database snapshot utilities.
    """
    def __init__(self, container):
        """"DB is true, will be usefule to make checks."""
        super().__init__(container)
        self.dbname = config_value(DATABASE, DBNAME)
        self.qry = {'container': container}
        self.sort = [sort_field('timestamp', False)]
        self.isDb = True

    def collection(self, name=TEST):
        """ Get the collection name for the json object"""
        return config_value(DATABASE, collectiontypes[name])

    def get_structure_data(self, snapshot_object):
        """ Return the structure from the database"""
        structure_data = {}
        snapshot_source = get_field_value(snapshot_object, "source")
        snapshot_source = snapshot_source.replace('.json', '') if snapshot_source else ''
        qry = {'name': snapshot_source}
        structure_docs = get_documents(self.collection(STRUCTURE), dbname=self.dbname, sort=self.sort, query=qry, limit=1)
        logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, STRUCTURE, len(structure_docs))
        if structure_docs and len(structure_docs):
            structure_data = structure_docs[0]['json']
        return structure_data

    def get_used_snapshots_in_tests(self):
        """ Get the snapshots used in test and mastertest of the container."""
        snapshots = []
        logger.info("%s Fetching documents for %s", Snapshot.LOGPREFIX, self.container)
        for collection, snapshotType, suffix in (
                (TEST, SNAPSHOT, ''),
                (MASTERTEST, MASTERSNAPSHOT, '_gen')):
            docs = get_documents(self.collection(collection), dbname=self.dbname, sort=self.sort, query=self.qry)
            logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, collection, len(docs))
            snapshots.extend(self.process_docs(docs, snapshotType, suffix))
        return list(set(snapshots))

    def get_snapshots(self):
        """Populate the used snapshots in test and mastertest for this container."""
        snapshots_status = {}
        docs = get_documents(self.collection(SNAPSHOT), dbname=self.dbname, sort=self.sort, query=self.qry, _id=True)
        if docs and len(docs):
            logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, SNAPSHOT, len(docs))
            used_snapshots = self.get_used_snapshots_in_tests()
            if not used_snapshots:
                raise SnapshotsException("No snapshots for this container: %s, add and run again!..." % self.container)
            populated = []
            for doc in docs:
                if doc['json']:
                    snapshot = doc['name']
                    try:
                        pull_response, git_connector_json = self.check_and_fetch_remote_snapshots(doc['json'])
                        if git_connector_json and not pull_response:
                            logger.info('%s Fetching remote snapshots failed.', Snapshot.LOGPREFIX)
                            break

                        if snapshot in used_snapshots and snapshot not in populated:
                            # Take the snapshot and populate whether it was successful or not.
                            # Then pass it back to the validation tests, so that tests for those
                            # snapshots that have been susccessfully fetched shall be executed.
                            snapshot_file_data = self.populate_snapshots(doc['json'])

                            if not git_connector_json:
                                update_one_document(doc, self.collection(SNAPSHOT), self.dbname)

                            populated.append(snapshot)
                            snapshots_status[snapshot] = snapshot_file_data
                    except Exception as e:
                        dump_output_results([], self.container, "-", snapshot, False)
                        raise e
        if not snapshots_status:
            raise SnapshotsException("No snapshots for this container: %s, add and run again!..." % self.container)
        return snapshots_status

    def process_docs(self, docs, doctype, suffix=''):
        """ Process Test or masterTest documents"""
        snapshots = []
        if docs and len(docs):
            for doc in docs:
                if doc['json']:
                    snapshot = doc['json'][doctype] if doctype in doc['json'] else ''
                    if snapshot:
                        snapshots.append((snapshot.split('.')[0] if snapshot.endswith('.json') else snapshot) + suffix)
        return snapshots

    def store_data_node(self, data):
        """ Store to database"""
        if get_collection_size(data['collection']) == 0:
            # Creating indexes for collection
            create_indexes(
                data['collection'],
                config_value(DATABASE, DBNAME),
                [
                    ('snapshotId', pymongo.ASCENDING),
                    ('timestamp', pymongo.DESCENDING)
                ]
            )

            create_indexes(
                data['collection'],
                config_value(DATABASE, DBNAME),
                [
                    ('_id', pymongo.DESCENDING),
                    ('timestamp', pymongo.DESCENDING),
                    ('snapshotId', pymongo.ASCENDING)
                ]
            )
        insert_one_document(data, data['collection'], self.dbname, check_keys=False)
