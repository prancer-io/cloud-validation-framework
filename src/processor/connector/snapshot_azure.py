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
    collectiontypes, STRUCTURE, TEST, MASTERTEST, make_snapshots_dir,\
    store_snapshot, get_field_value_with_default, get_json_files
from processor.helper.httpapi.restapi_azure import get_access_token,\
    get_web_client_data, get_client_secret, json_source
from processor.connector.vault import get_vault_data
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import config_value, framework_dir, CUSTOMER
from processor.database.database import insert_one_document, COLLECTION, get_collection_size, create_indexes, \
     DATABASE, DBNAME, sort_field, get_documents
from processor.connector.snapshot_utils import validate_snapshot_nodes


logger = getlogger()

class SnapshotsException(Exception):
    """Exception raised for snapshots"""

    def __init__(self, message="Error in snapshots for container"):
        self.message = message
        super().__init__(self.message)



class Snapshot:
    """ Base class for snapshot processing"""

    LOGPREFIX = 'Snapshots:'

    def __init__(self, container):
        self.container = container
        self.appObject = {}
        self.singleTest = None

    def store_value(self, key, value):
        if key and value:
            self.appObject[key] = value

    def get_value(self, key):
        if key and key in self.appObject:
            return self.appObject.get(key)
        return None

    def get_snapshots(self):
        """ Iterator based implementation"""
        return []

    def get_snapshot_nodes(self, snapshot):
        """ Iterate over the nodes of the snapshot object"""
        return []


class FSSnapshot(Snapshot):
    """
    Filesystem snapshot utilities.
    """
    def __init__(self, container, singleTest=None):
        super().__init__(container)
        self.singleTest = singleTest
        reporting_path = config_value('REPORTING', 'reportOutputFolder')
        self.container_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)

    def get_snapshots(self):
        """ Iterator based implementation"""
        snapshots = []
        logger.info("%s Fetching files for %s from container dir: %s", Snapshot.LOGPREFIX,
                    self.container, self.container_dir)
        for testType, snapshotType, replace in (
                (TEST, 'snapshot', False),
                (MASTERTEST, 'masterSnapshot', True)):
            test_files = get_json_files(self.container_dir, testType)
            logger.info('%s fetched %s number of files: %s', Snapshot.LOGPREFIX, self.container, len(test_files))
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
                    if self.singletest:
                        testsets = get_field_value_with_default(test_json_data, 'testSet', [])
                        for testset in testsets:
                            for testcase in testset['cases']:
                                if ('testId' in testcase and testcase['testId'] == self.singletest) or \
                                        ('masterTestId' in testcase and testcase['masterTestId'] == self.singletest):
                                    if file_name not in snapshots:
                                        snapshots.append(file_name)
                    else:
                        snapshots.append(file_name)
        return snapshots

    def get_snapshot_nodes(self, snapshot):
        """ Iterate over the nodes of the snapshot object"""
        pass


class DBSnapshot(Snapshot):
    """
    Database snapshot utilities.
    """
    def __init__(self, container):
        super().__init__(container)
        self.dbname = config_value(DATABASE, DBNAME)
        self.qry = {'container': container}
        self.sort = [sort_field('timestamp', False)]

    def collection(self, name=TEST):
        return config_value(DATABASE, collectiontypes[name])

    def get_snapshots(self):
        """ Iterator based implementation"""
        snapshots = []
        logger.info("%s Fetching documents for %s", Snapshot.LOGPREFIX, self.container)
        for collection, snapshotType, suffix in (
                (TEST, 'snapshot', ''),
                (MASTERTEST, 'masterSnapshot', '_gen')):
            docs = get_documents(self.collection(collection), dbname=self.dbname, sort=self.sort, query=self.qry)
            logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, collection, len(docs))
            snapshots.extend(self.process_docs(docs, snapshotType, suffix))
        return list(set(snapshots))

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

    def get_snapshot_nodes(self, snapshot):
        """ Iterate over the nodes of the snapshot object"""
        pass



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
