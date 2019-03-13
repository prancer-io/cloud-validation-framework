"""
   Common file for running validator functions.
"""
import json
import hashlib
import time
from boto3 import client
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE
from processor.connector.vault import get_vault_data
from processor.helper.config.config_utils import config_value, get_test_json_dir
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME
from processor.helper.httpapi.restapi_azure import json_source
from processor.helper.httpapi.restapi_azure import get_client_secret



logger = getlogger()


def get_aws_data(snapshot_source):
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of AWS structure Documents: %d', len(docs))
        if docs and len(docs):
            sub_data = docs[0]['json']
    else:
        json_test_dir = get_test_json_dir()
        aws_source = '%s/../%s' % (json_test_dir, snapshot_source)
        logger.info('AWS source: %s', aws_source)
        if exists_file(aws_source):
            sub_data = json_from_file(aws_source)
    return sub_data


def get_aws_describe_function(node):
    """Describe function for the node."""
    describe_fn_str = None
    if node and 'type' in node and node['type']:
        describe_fn_str = 'describe_%s' % node['type']
    return describe_fn_str


def get_node(awsclient, node, snapshot_source):
    """ Fetch node from aws using rest API."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    db_record = {
        "structure": "aws",
        "reference": "",
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": "",
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    describe_fn_str = get_aws_describe_function(node)
    if describe_fn_str:
        describe_fn = getattr(awsclient, describe_fn_str, None)
        if describe_fn and callable(describe_fn):
            queryval = get_field_value(node, 'id')
            try:
                data = describe_fn(**queryval)
                if data:
                    db_record['json'] = data
                    checksum = get_checksum(data)
                    if checksum:
                        db_record['checksum'] = checksum
                else:
                    put_in_currentdata('errors', data)
                    logger.info("Describe function does not exist: %s", describe_fn_str)
            except Exception as ex:
                logger.info('Describe function exception: %s', ex)
        else:
            logger.info('Invalid describe function exception: %s', describe_fn_str)
    else:
        logger.info('Missing describe function')
    return db_record

def get_checksum(data):
    checksum = None
    try:
        data_str = json.dumps(data)
        checksum = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    except:
        pass
    return checksum

def populate_aws_snapshot(snapshot):
    """ Populates the resources from aws."""
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_user = get_field_value(snapshot, 'testUser')
    sub_data = get_aws_data(snapshot_source)
    if sub_data:
        logger.debug(sub_data)
        access_key, secret_access, region, client_str = \
            get_aws_client_data(sub_data, snapshot_user)
        if not access_key:
            logger.info("No access_key in the snapshot to access aws resource!...")
            return False
        if not secret_access:
            secret_access = get_vault_data(access_key)
            logger.info('Vault Secret: %s', secret_access)
        if not secret_access:
            secret_access = get_client_secret()
            logger.info('Environment variable or Standard input, Secret: %s', secret_access)
        if not secret_access:
            logger.info("No secret_access in the snapshot to access aws resource!...")
            return False
        if client_str and access_key and secret_access:
            try:
                awsclient = client(client_str.lower(), aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_access, region_name=region)
            except Exception as ex:
                logger.info('Unable to create AWS client: %s', ex)
                awsclient = None
            logger.info(awsclient)
            if awsclient:
                for node in snapshot['nodes']:
                    logger.info(node)
                    data = get_node(awsclient, node, snapshot_source)
                    if data:
                        insert_one_document(data, data['collection'], dbname)
                return True
    return False


def get_aws_client_data(aws_data, snapshot_user):
    accesskey = None
    secret_access = None
    region = None
    client_str = None
    if aws_data and snapshot_user:
        org_units = get_field_value(aws_data, "organization-unit")
        if org_units:
            found = False
            for org_unit in org_units:
                accounts = get_field_value(org_unit, 'accounts')
                if accounts:
                    for account in accounts:
                        users = get_field_value(account, 'users')
                        if users:
                            for user in users:
                                username = get_field_value(user, 'name')
                                if username and username == snapshot_user:
                                    found = True
                                    accesskey = get_field_value(user, 'access-key')
                                    secret_access = get_field_value(user, 'secret-access')
                                    region = get_field_value(user, 'region')
                                    client_str = get_field_value(user, 'client')
                                    break
                        if found:
                            break
                if found:
                    break
    return accesskey, secret_access, region, client_str