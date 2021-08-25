"""
snapshot connector file for aws type snapshot. When the 'type' is 'aws', the
resource objects have to be fetched from the AWS interface.
The connection could use python SDK libraries or https calls or other known methods
provided by the provider.
Here in case of AWS, have used boto python SDK released and maintained by AWS.
boto library provides different 'describe_' functions and using this functionality,
the snapshot mentions which describe function has to be called, so 'type' could
be 'security_groups' , 'instances', 'regions' and using python reflection capabilities
a callable from describe_security_groups gets callable for this function to return security groups.
The describe_ functions lots of methods to query AWS resources, since we know what resource we need
we always query by id, so AWS snapshots shall always have {"id": "123de23"} to uniquely
identify the resource object.
"""
import json
import hashlib
import time
import pymongo
import os
import re
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.rundata_utils import put_in_currentdata, get_dbtests, get_from_currentdata
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE, save_json_to_file, get_field_value_with_default,\
    make_snapshots_dir, store_snapshot
from processor.connector.vault import get_vault_data
from processor.helper.config.config_utils import config_value, get_test_json_dir, framework_dir, CUSTOMER, EXCLUSION
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME, get_collection_size, create_indexes
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.snapshot_utils import validate_snapshot_nodes

logger = getlogger()
google_parameters = None

def get_google_parameters():
    """
    Return the google parameter object read from database or the filesystem
    """
    global google_parameters
    if not google_parameters:
        params_source = config_value('GOOGLE', 'params')
        if json_source():
            dbname = config_value(DATABASE, DBNAME)
            collection = config_value(DATABASE, collectiontypes[STRUCTURE])
            parts = params_source.rsplit('/')
            name = parts[-1].split('.')
            qry = {'name': name[0]}
            sort = [sort_field('timestamp', False)]
            docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
            logger.info('Number of Google Params versions: %s', len(docs))
            if docs and len(docs):
                google_parameters = docs[0]['json']
        else:
            params_file = '%s/%s' % (framework_dir(), params_source)
            logger.info(params_file)
            if exists_file(params_file):
                google_parameters = json_from_file(params_file)
    return google_parameters

def get_google_data(snapshot_source):
    """
    The Google source object to be fetched from database or the filesystem
    The initial configuration for database is 'validator' and collection
    is 'structures', whereas for the filesystem the path to fetch the
    'structures' is  $SOLUTIONDIR/realm/<structure>.json
    """
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of Google structure Documents: %d', len(docs))
        if docs and len(docs):
            sub_data = docs[0]['json']
    else:
        json_test_dir = get_test_json_dir()
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        google_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('Google source: %s', google_source)
        if exists_file(google_source):
            sub_data = json_from_file(google_source)

    if not sub_data:
        logger.error("Google connector file %s does not exist, or it does not contains the valid JSON.", snapshot_source)
    return sub_data



def generate_request_url(base_url, project_id):
    """Generate request url from base url"""
    try:
        path_list = base_url.split("https://")
        path_list = path_list[1].split('/')

        request_url = "https:/"
        for path in path_list:
            field_expresion = re.compile("\{([^}]+)\}")
            field = field_expresion.search(path)
            if field:
                field = path[1:len(path)-1]
                if field in ["projectId", "project"]:
                    path = project_id
                elif field in ["zone"]:
                    path = "-"
            request_url = "%s/%s" % (request_url, path)

        logger.info(request_url)
        return request_url
    except:
        logger.error("Invalid api url")
        return None

def get_api_path(node_type):
    """
    Get api path for populate snapshot
    """
    api_url = None
    params = get_google_parameters()
    if params and "GoogleApis" in params:
        for method, request_url in params['GoogleApis'].items():
            if method == node_type:
                api_url = request_url
    return api_url

def get_node(credentials, node, snapshot_source, snapshot):
    """
    Fetch node from google using connection. In this case using google client API's
    functions.
    """
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    project_id = get_field_value_with_default(snapshot, 'project-id',"")
    path = get_field_value_with_default(node, 'path',"")
    zone = re.findall(r"(?<=zones\/)[a-zA-Z0-9\-]*(?=\/)", path)
    db_record = {
        "structure": "google",
        "error": None,
        "reference": project_id,
        "contentType": "json",
        "source": parts[0],
        "path": path,
        "timestamp": int(time.time() * 1000),
        "queryuser": get_field_value(snapshot, 'testUser'),
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "region" : zone[0] if zone else "",
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }

    try:
        access_token = credentials.get_access_token().access_token
        header = {
            "Authorization" : ("Bearer %s" % access_token)
        }

        node_type = node['type'] if node and 'type' in node else ""
        base_node_type_list = node_type.split("/")
        if len(base_node_type_list) > 1:
            base_node_type = base_node_type_list[0]
        else:
            logger.error("Invalid node type %s", node_type)
            return db_record
        
        base_url = "%s%s" % (base_node_type, ".googleapis.com")
        request_url = "https://%s/%s" % (base_url, path)
        logger.info("Invoke request for get snapshot: %s", request_url)
        status, data = http_get_request(request_url, header)
        logger.info('Get snapshot status: %s', status)
        
        if status and isinstance(status, int) and status == 200:
            if data:
                db_record['json'] = data
                checksum = get_checksum(data)
                if checksum:
                    db_record['checksum'] = checksum
        else:
            logger.error("Get snapshot returned invalid status: %s", status)
            db_record['error'] = ("Get snapshot returned invalid status: %s" % status)
    except Exception as ex:
        logger.error('Failed to populate the snapshot : %s', ex)
        db_record['error'] = 'Failed to populate the snapshot: %s' % ex
    
    return db_record


def get_all_nodes(credentials, node, snapshot_source, snapshot, snapshot_data):
    """
    Fetch all nodes from google using connection using google client API's functions.
    """
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    project_id = get_field_value_with_default(snapshot, 'project-id',"")
    node_type = get_field_value_with_default(node, 'type',"")
    
    db_record = {
        "structure": "google",
        "error": None,
        "reference": project_id,
        "contentType": "json",
        "source": parts[0],
        "path": "",
        "timestamp": int(time.time() * 1000),
        "queryuser": get_field_value(snapshot, 'testUser'),
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": None,
        "masterSnapshotId": [node['masterSnapshotId']],
        "collection": collection.replace('.', '').lower(),
        "json": {},  # Refactor when node is absent it should None, when empty object put it as {}
        "items": []
    }

    if node_type:
        access_token = credentials.get_access_token().access_token
        header = {
            "Authorization" : ("Bearer %s" % access_token)
        }

        base_node_type_list = node_type.split("/")
        if len(base_node_type_list) > 1:
            base_node_type = base_node_type_list[1]
        else:
            logger.error("Invalid node type '%s'", node_type)
            return db_record

        request_url = get_api_path(base_node_type)
        request_url = generate_request_url(request_url, project_id)
        logger.info("Invoke request for get snapshot: %s", request_url)
        
        status, data = http_get_request(request_url, header)
        logger.info('Get snapshot status: %s', status)

        fn_str_list = ""
        if node and 'type' in node and node['type']:
            fn_str_list = get_field_value(node, 'type').split(".")
        
        response_param = ""
        if fn_str_list and len(fn_str_list) > 1:
            response_param = fn_str_list[-2]
        elif fn_str_list and len(fn_str_list) == 1:
            response_param = fn_str_list[0]
        
        if data:
            check_node_type = node_type 
            node_type_list = node_type.split(".")
            if len(node_type_list) > 1:
                del node_type_list[-1]
                check_node_type = ".".join(node_type_list)

            db_record['json'] = data
            if response_param in data:
                db_record['items'] = data[response_param]
            elif "items" in data:
                if isinstance(data['items'], dict):
                    for name, scoped_dict in data['items'].items():
                        if response_param in scoped_dict:
                            db_record['items'] = db_record['items'] + scoped_dict[check_node_type]

                if not db_record['items']:
                    db_record['items'] = data['items']

            set_snapshot_data(node, db_record['items'], snapshot_data)

            checksum = get_checksum(data)
            if checksum:
                db_record['checksum'] = checksum

    return db_record

def set_snapshot_data(node, items, snapshot_data):
    if node['masterSnapshotId'] not in snapshot_data or not isinstance(snapshot_data[node['masterSnapshotId']], list):
        snapshot_data[node['masterSnapshotId']] =  []

    # create the node type for sub resources
    node_type = get_field_value(node, "type")
    node_type_list = node_type.split(".")
    resource_node_type = node_type
    if len(node_type_list) > 1:
        del node_type_list[-1]
        node_type_list.append("get")
        resource_node_type = ".".join(node_type_list)

    count = 0
    resource_items = []
    if isinstance(items, dict):
        for zone, resource in items.items():
            if 'selfLink' in resource:
                resource_items.append(resource)
            else:
                resource_type = node_type.split("/")[1].split(".")[-2]
                if resource_type in resource and isinstance(resource[resource_type], list):
                    if len(resource[resource_type]) > 0 and 'selfLink' in resource[resource_type][0]:
                        resource_items += resource[resource_type]
    else:
        resource_items = items

    exclusions = get_from_currentdata(EXCLUSION).get('exclusions', [])
    resourceExclusions = {}
    for exclusion in exclusions:
        if 'exclusionType' in exclusion and exclusion['exclusionType'] and exclusion['exclusionType'] == 'resource':
            if 'paths' in exclusion and isinstance(exclusion['paths'], list):
                resourceExclusions[tuple(exclusion['paths'])] = exclusion

    for item in resource_items:
        count += 1
        path_list = item['selfLink'].split("https://")
        path_list = path_list[1].split('/')
        path = "/".join(path_list[1:])

        found_old_record = False
        for masterSnapshotId, snapshot_list in snapshot_data.items():
            old_record = None
            if isinstance(snapshot_list, list):
                for item in snapshot_list:
                    if item["path"] == path:
                        old_record = item

                if old_record:
                    found_old_record = True
                    if node['masterSnapshotId'] not in old_record['masterSnapshotId']:
                        old_record['masterSnapshotId'].append(
                            node['masterSnapshotId'])

        if not found_old_record:
            if isinstance(path, str):
                key = tuple([path])
            else:
                key = None
            if key and key in resourceExclusions:
                logger.warning("Excluded from resource exclusions: %s", path)
                continue

            snapshot_data[node['masterSnapshotId']].append(
                {
                    "masterSnapshotId" : [node['masterSnapshotId']],
                    "snapshotId": '%s%s' % (node['masterSnapshotId'], str(count)),
                    "type": resource_node_type,
                    "collection": node['collection'],
                    "path": path,
                    "status" : "active",
                    "validate" : node['validate'] if 'validate' in node else True
                })
    return snapshot_data

def get_checksum(data):
    """ Get the checksum for the Google data fetched."""
    checksum = None
    try:
        data_str = json.dumps(data)
        checksum = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    except:
        pass
    return checksum


def populate_google_snapshot(snapshot, container=None):
    """
    This is an entrypoint for populating a snapshot of type google.
    All snapshot connectors should take snapshot object and based on
    'source' field create a method to connect to the service for the
    connector.
    The 'source' field could be used by more than one snapshot, so the
    'testuser' attribute should match to the user the 'source'
    """
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_user = get_field_value(snapshot, 'testUser')
    project_id = get_field_value(snapshot, 'project-id')
    sub_data = get_google_data(snapshot_source)
    snapshot_nodes = get_field_value(snapshot, 'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    if valid_snapshotids and sub_data and snapshot_nodes:
        logger.debug(sub_data)
        try:
            for node in snapshot['nodes']:
                validate = node['validate'] if 'validate' in node else True
                logger.info(node)
                node_type = get_field_value_with_default(node, 'type',"")
                credentials = get_google_client_data(sub_data, snapshot_user, node_type, project_id)
                if not credentials:
                    logger.info("No  GCE connection in the snapshot to access Google resource!...")
                    return snapshot_data
                if 'snapshotId' in node:
                    if validate:
                        data = get_node(credentials, node, snapshot_source, snapshot)
                        if data:
                            error_str = data.pop('error', None)
                            if get_dbtests():
                                if get_collection_size(data['collection']) == 0:
                                    #Creating indexes for collection
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
                                insert_one_document(data, data['collection'], dbname)
                            else:
                                snapshot_dir = make_snapshots_dir(container)
                                if snapshot_dir:
                                    store_snapshot(snapshot_dir, data)
                    
                            if 'masterSnapshotId' in node:
                                snapshot_data[node['snapshotId']] = node['masterSnapshotId']
                            else:
                                snapshot_data[node['snapshotId']] = False if error_str else True
                        else:
                            node['status'] = 'inactive'
                elif 'masterSnapshotId' in node:
                        data = get_all_nodes(credentials, node, snapshot_source, snapshot, snapshot_data)
                        logger.debug('Type: %s', type(data))
        except Exception as ex:
            logger.info('Unable to create Google client: %s', ex)
            raise ex
    return snapshot_data



def generate_gce(google_data, project, user):
    """
    Generate client secret json from the google data
    """
    logger.info("Generating GCE")
    gce = {
        "type": get_field_value(user, "type"),
        "project_id": get_field_value(project, "project-id"),
        "private_key_id": get_field_value(user, "private_key_id"),
        "private_key": get_field_value(user, "private_key"),
        "client_email": get_field_value(user, "client_email"),
        "client_id": get_field_value(user, "client_id"),
        "auth_uri": get_field_value(google_data, "auth_uri"),
        "token_uri": get_field_value(google_data, "token_uri"),
        "auth_provider_x509_cert_url": get_field_value(google_data, "auth_provider_x509_cert_url"),
        "client_x509_cert_url": get_field_value(user, "client_x509_cert_url"),
    }

    # Read the private key from the key path
    if not gce['private_key'] and get_field_value(user, "private_key_path"):
        private_key_path = get_field_value(user, "private_key_path")
        logger.info("Private key path : %s ", private_key_path)
        try:
            gce['private_key'] = open(private_key_path, 'r', encoding="utf-8").read().replace("\\n","\n")
            if gce['private_key']:
                logger.info('Private key from Private key path, Secret: %s', '*' * len(gce['private_key']))
        except Exception as e:
            raise Exception("Private key does not exist at given private key path : %s " % str(e))
        
        if not gce['private_key']:
            raise Exception("Private key does not exist at given private key path : %s " % private_key_path)
    
    # Read the private key from the vault
    if not gce['private_key']:
        private_key = get_vault_data(gce['private_key_id'])
        if private_key:
            gce["private_key"] = private_key.replace("\\n","\n")
            if gce["private_key"]:
                logger.info('Private key from vault Secret: %s', '*' * len(gce["private_key"]))
        elif get_from_currentdata(CUSTOMER):
            raise Exception("Private key does not set in a vault")
    
    if not gce['private_key']:
        raise Exception("No `private_key` field in the connector file to access Google resource!...")

    if (None in list(gce.values())):
        raise Exception("Connector file does not contains valid values or some fields are missing for access Google resources.")

    return gce


def get_google_client_data(google_data, snapshot_user, node_type, project_id):
    """
    Generate Google Service Account credentials object from the google structure file.
    """
    credentials = None
    found = False
    if google_data and snapshot_user:
        projects = get_field_value(google_data, "projects")
        for project in projects:
            structure_project_id = get_field_value(project, 'project-id')
            if structure_project_id == project_id:
                users = get_field_value(project, 'users')
                if users:
                    for user in users:
                        user_name = get_field_value(user, 'name')
                        if user_name == snapshot_user:
                            found = True
                            gce = generate_gce(google_data, project, user)
                            if gce:
                                save_json_to_file(gce, '/tmp/gce.json')
                                logger.info("Creating credential object")
                                scopes = ['https://www.googleapis.com/auth/compute', "https://www.googleapis.com/auth/cloud-platform"]
                                credentials = ServiceAccountCredentials.from_json_keyfile_name('/tmp/gce.json', scopes)
                                # service_name = get_service_name(node_type)
                                # compute = discovery.build(service_name, 'v1', credentials=credentials, cache_discovery=False)
                            break 
            if found:
                break
    return credentials
