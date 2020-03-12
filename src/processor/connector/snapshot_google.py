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
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata, get_dbtests
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE, save_json_to_file, get_field_value_with_default,\
    make_snapshots_dir, store_snapshot
from processor.connector.vault import get_vault_data
from processor.helper.config.config_utils import config_value, get_test_json_dir, framework_dir
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME, get_collection_size, create_indexes
from processor.helper.httpapi.restapi_azure import json_source
from processor.connector.snapshot_utils import validate_snapshot_nodes

logger = getlogger()


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
    return sub_data


def get_call_kwargs_for_crawler(node, project_id):
    """Get argument names and their values in kwargs for Crawler"""
    kwargs = {}
    logger.info("Get node's kwargs")
    params_source = config_value('GOOGLE', 'params')
    paramsversions = None
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
            paramsversions = docs[0]['json']
    else:
        paramsversions_file = '%s/%s' % (framework_dir(), params_source)
        logger.info(paramsversions_file)
        if exists_file(paramsversions_file):
            paramsversions = json_from_file(paramsversions_file)
    if paramsversions:
        if node and 'type' in node and "crawler_queryprameters" in paramsversions:
            for prameter in paramsversions["crawler_queryprameters"]:
                if node['type'] in prameter['services']:
                    for param in prameter['params']:
                        if param == "project":
                            kwargs['project'] = project_id
                        elif param == "projectId":
                            kwargs['projectId'] = project_id
                        elif param == "zone":
                            kwargs['zone'] = "-"
                
    return kwargs

def get_call_kwargs(node):
    """Get argument names and their values in kwargs"""
    kwargs = {
        "params" : {}
    }
    logger.info("Get node's kwargs")
    params_source = config_value('GOOGLE', 'params')
    paramsversions = None
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
            paramsversions = docs[0]['json']
    else:
        paramsversions_file = '%s/%s' % (framework_dir(), params_source)
        logger.info(paramsversions_file)
        if exists_file(paramsversions_file):
            paramsversions = json_from_file(paramsversions_file)

    path = node['path']
    if paramsversions and "queryprameters" in paramsversions:
        if node['type'] in paramsversions["queryprameters"]:
            for param, parameter_type in paramsversions["queryprameters"][node['type']].items():
                add_argument_parameter(path, kwargs, param, parameter_type)

    return kwargs

def add_argument_parameter(path, kwargs, param, prameter_type):
    """Add query parameter."""
    path_list = path.split(prameter_type + "/")
    arg = "-"
    if len(path_list) > 1:
        arg = path_list[1].split("/")[0]
    kwargs['params'][param] = arg

def get_google_call_function(node):
    """Get the callable for the type of compute resource."""
    fn_str_list = None
    kwargs = {}
    if node and 'type' in node and node['type']:
        path = get_field_value(node, 'path')
        path = path[:-1] if path and path.endswith('/') else path
        path = path[1:] if path and path.startswith('/') else path
        params = path.split('/')

        if node and 'type' in node and node['type']:
            fn_str = get_field_value(node, 'type')
            if fn_str:
                fn_str_list = fn_str.split(".")
            kwargs = get_call_kwargs(node)
    return fn_str_list, kwargs

def get_google_call_function_for_crawler(node, project_id):
    """Get the callable for the type of compute resource."""
    fn_str_list = None
    kwargs = None
    if node and 'type' in node and node['type']:
        fn_str_list = get_field_value(node, 'type').split(".")
        kwargs = get_call_kwargs_for_crawler(node, project_id)
    return fn_str_list, kwargs

def get_node(compute_fn, node, snapshot_source, snapshot):
    """
    Fetch node from google using connection. In this case using google client API's
    functions.
    """
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    project_id = get_field_value_with_default(snapshot, 'project-id',"")
    path = get_field_value_with_default(node, 'path',"")
    db_record = {
        "structure": "google",
        "error": None,
        "reference": project_id,
        "source": parts[0],
        "path": path,
        "timestamp": int(time.time() * 1000),
        "queryuser": "",
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    fn_str_list, kwargs = get_google_call_function(node)

    if fn_str_list:
        for i in range(0, len(fn_str_list)):
            compute_fn = getattr(compute_fn, fn_str_list[i], None)
            if compute_fn and i != len(fn_str_list)-1:
                compute_fn = compute_fn()

        response_param = ""
        if fn_str_list and len(fn_str_list) > 1:
            response_param = fn_str_list[-2]
        elif fn_str_list and len(fn_str_list) == 1:
            response_param = fn_str_list[0]

        if compute_fn and callable(compute_fn):
            try:
                data = compute_fn(**kwargs["params"]).execute()
                if data:
                    db_record['json'] = data
                    checksum = get_checksum(data)
                    if checksum:
                        db_record['checksum'] = checksum
            except Exception as ex:
                logger.info('Compute function exception: %s', ex)
                db_record['error'] = 'Compute function exception: %s' % ex
        else:
            logger.info('Invalid Compute function exception: %s', str(fn_str_list))
            db_record['error'] = 'Invalid Compute function exception: %s' % str(fn_str_list)
    else:
        logger.info('Missing Compute function')
        db_record['error'] = 'Missing Compute function'
    return db_record


def get_all_nodes(compute_fn, node, snapshot_source, snapshot, snapshot_data):
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
        "source": parts[0],
        "path": "",
        "timestamp": int(time.time() * 1000),
        "queryuser": "",
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": None,
        "masterSnapshotId": [node['masterSnapshotId']],
        "collection": collection.replace('.', '').lower(),
        "json": {},  # Refactor when node is absent it should None, when empty object put it as {}
        "items": []
    }

    if node_type:
        fn_str_list, kwargs = get_google_call_function_for_crawler(node, project_id)
        
        if fn_str_list and kwargs:
            for i in range(0, len(fn_str_list)):
                compute_fn = getattr(compute_fn, fn_str_list[i], None)
                if compute_fn and i != len(fn_str_list)-1:
                    compute_fn = compute_fn()

            response_param = ""
            if fn_str_list and len(fn_str_list) > 1:
                response_param = fn_str_list[-2]
            elif fn_str_list and len(fn_str_list) == 1:
                response_param = fn_str_list[0]

            if compute_fn and callable(compute_fn):
                try:
                    data = compute_fn(**kwargs).execute()
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
                    else:
                        put_in_currentdata('errors', data)
                        logger.info("Compute function does not exist: %s", str(fn_str_list))
                        db_record['error'] = "Compute function does not exist: %s" % str(fn_str_list)
                except Exception as ex:
                    logger.info('Compute function exception: %s', ex)
                    db_record['error'] = 'Compute function exception: %s' % ex
            else:
                logger.info('Invalid Compute function exception: %s', str(fn_str_list))
                db_record['error'] = 'Invalid Compute function exception: %s' % str(fn_str_list)
        else:
            logger.info('Missing Compute function')
            db_record['error'] = 'Missing Compute function'
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
    for item in items:
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
                compute = get_google_client_data(sub_data, snapshot_user, node_type, project_id)
                if not compute:
                    logger.info("No  GCE connection in the snapshot to access Google resource!...")
                    return snapshot_data
                if 'snapshotId' in node:
                    if validate:
                        data = get_node(compute, node, snapshot_source, snapshot)
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
                        data = get_all_nodes(compute, node, snapshot_source, snapshot, snapshot_data)
                        logger.debug('Type: %s', type(data))
        except Exception as ex:
            logger.info('Unable to create Google client: %s', ex)
            raise ex
    return snapshot_data


def get_service_name(node_type):
    """
    Get service name for init compute function
    """
    service = None
    params_source = config_value('GOOGLE', 'params')
    paramsversions = None
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
            paramsversions = docs[0]['json']
    else:
        paramsversions_file = '%s/%s' % (framework_dir(), params_source)
        logger.info(paramsversions_file)
        if exists_file(paramsversions_file):
            paramsversions = json_from_file(paramsversions_file)

    check_node_type = node_type 
    node_type_list = node_type.split(".")
    if len(node_type_list) > 1:
        del node_type_list[-1]
        check_node_type = ".".join(node_type_list)
        
    if paramsversions and "serviceName" in paramsversions:
        for service_name, resource_list in paramsversions['serviceName'].items():
            if check_node_type in resource_list:
                service = service_name
                
    return service

def get_private_key(gce):
    """
    Fetches the Private Key for get the google service account credentials
    """
    if ('UAMI' not in os.environ or os.environ['UAMI'] != 'true'):
        # if private_key does not exist then it will set to None:
        gce["private_key"] = get_field_value(gce, 'private_key')

    if ('UAMI' in os.environ and os.environ['UAMI'] == 'true') or not gce["private_key"]:
        private_key = get_vault_data(gce['private_key_id'])
        if private_key:
            gce["private_key"] = private_key.replace("\\n","\n")
        else:
            raise Exception("Private key does not set in a vault")
    
    return gce

def generate_gce(google_data, project, user):
    """
    Generate client secret json from the google data
    """
    logger.info("Generating GCE")
    gce = {
        "type": get_field_value(user, "type"),
        "project_id": get_field_value(project, "project-id"),
        "private_key_id": get_field_value(user, "private_key_id"),
        "client_email": get_field_value(user, "client_email"),
        "client_id": get_field_value(user, "client_id"),
        "auth_uri": get_field_value(google_data, "auth_uri"),
        "token_uri": get_field_value(google_data, "token_uri"),
        "auth_provider_x509_cert_url": get_field_value(google_data, "auth_provider_x509_cert_url"),
        "client_x509_cert_url": get_field_value(google_data, "client_x509_cert_url"),
    }
    gce = get_private_key(gce)
    return gce


def get_google_client_data(google_data, snapshot_user, node_type, project_id):
    """
    Generate Google compute object from the google structure file.
    """
    compute = None
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
                                scopes = ['https://www.googleapis.com/auth/compute', "https://www.googleapis.com/auth/cloud-platform"]
                                credentials = ServiceAccountCredentials.from_json_keyfile_name('/tmp/gce.json', scopes)
                                service_name = get_service_name(node_type)
                                compute = discovery.build(service_name, 'v1', credentials=credentials, cache_discovery=False)
                            break 
            if found:
                break
    return compute
