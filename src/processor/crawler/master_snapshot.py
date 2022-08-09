"""
   Common file for generating snapshot functions.
   Mastersnapshot is the current configuration of a resource representation in cloud or a git repository.
   For a given test or comparison or evaluation, the tests are mentioned in the a test file.
   The test file references a snapshot file and snapshot file references a list of snapshots to be
   populated using a connector.
   This file is the entry point for all snapshots population.
    Different types of mastersnapshots supported by the validation framework are:
    1) azure: Microsoft Azure cloud.
    2) git: Git server.
   The mastersnapshot structure has callables for each type of supported snapshot.
   Each mastersnapshot has been implemented in its own file viz azure in snapshot_azure.py etc.
   A new snapshot type xyz will have to be implemented in snapshot_xyz.py and callable function for this type 'xyz'
   of snapshot should be populate_xyz_snapshot
   A snapshot typically is a structure consisting these:
   {
      "source" : "azureStructure1",
      "type" : "azure",
      "testUser" : "ajey.khanapuri@liquware.com",
      "subscriptionId" : "<sub id>",
      "nodes" : [

      ]
   }
"""
import json
import time
import copy
import hashlib

from bson.objectid import ObjectId
from processor.helper.config.rundata_utils import get_from_currentdata
from processor.logging.log_handler import getlogger, get_dblog_handler
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    get_container_snapshot_json_files, MASTERSNAPSHOT, SNAPSHOT,\
    collectiontypes, get_json_files, MASTERTEST, save_json_to_file, OUTPUT,\
    get_field_value_with_default
from processor.helper.config.config_utils import config_value, framework_dir
from processor.database.database import DATABASE, DBNAME, find_and_update_document, get_documents, sort_field, insert_one_document, update_one_document
from processor.connector.snapshot_azure import populate_azure_snapshot
from processor.connector.snapshot_custom import populate_custom_snapshot, get_custom_data
from processor.connector.snapshot_aws import populate_aws_snapshot
from processor.connector.snapshot_google import populate_google_snapshot
from processor.connector.snapshot_kubernetes import populate_kubernetes_snapshot
from processor.connector.populate_json import pull_json_data
from processor.helper.file.file_utils import exists_file,remove_file
from processor.template_processor.base.base_template_processor import set_processed_templates

doc_id = None
logger = getlogger()
# Different types of snapshots supported by the validation framework.
mastersnapshot_fns = {
    'azure': populate_azure_snapshot,
    'filesystem': populate_custom_snapshot,
    'aws': populate_aws_snapshot,
    'google' : populate_google_snapshot,
    'kubernetes': populate_kubernetes_snapshot
}

REMOVE_SNAPSHOTGEN_FIELDS = [
    "exclude",
    "source",
]

def generate_snapshot(snapshot_json_data, snapshot_file_data):
    """
    Checks if the snapshot is a master snapshot file.
    """
    if snapshot_json_data:
        snapshot_type = get_field_value(snapshot_json_data, 'fileType')
        if snapshot_type and snapshot_type == 'masterSnapshot':
            snapshots = get_field_value(snapshot_json_data, 'snapshots')
            if snapshots:
                for snapshot in snapshots:
                    nodes = get_field_value(snapshot, 'nodes')
                    if nodes:
                        new_nodes = []
                        for node in nodes:
                            mastersnapshotId = get_field_value(node, 'masterSnapshotId')
                            if mastersnapshotId and mastersnapshotId in snapshot_file_data and \
                                    isinstance(snapshot_file_data[mastersnapshotId], list):
                                for sid_data in snapshot_file_data[mastersnapshotId]:
                                    structure = sid_data.pop('structure', None)
                                    # if structure and structure == 'aws':
                                    #     newnode = {}
                                    # else:
                                    if "source" in sid_data and sid_data["source"] != snapshot.get("source"):
                                        continue
                                    newnode = copy.deepcopy(node)
                                    newnode.update(sid_data)
                                    
                                    for field in REMOVE_SNAPSHOTGEN_FIELDS:
                                        if field in newnode:
                                            del newnode[field]
                                        # if field in sid_data:
                                        #     del sid_data[field]
                                    
                                    new_nodes.append(newnode)
                        # if new_nodes:
                        snapshot['nodes'] = new_nodes
            snapshot_json_data["fileType"] = "snapshot"


def generate_mastersnapshot(mastersnapshot):
    """
    Every mastersnapshot should have collection of nodes which are to be populated.
    Each node in the nodes list of the snapshot shall have a unique id in this
    container so as not to clash with other node of a snapshots.
    """
    snapshot_data = {}
    snapshot_type = get_field_value(mastersnapshot, 'type')
    if not snapshot_type:
        snapshot_source = get_field_value(mastersnapshot, "source")
        connector_data = get_custom_data(snapshot_source)
        if connector_data:
            snapshot_type = get_field_value(connector_data, "type")
    if snapshot_type and snapshot_type in mastersnapshot_fns:
        if 'nodes' not in mastersnapshot or not mastersnapshot['nodes']:
            logger.error("No nodes in snapshot to be backed up!...")
            return snapshot_data
        snapshot_data = mastersnapshot_fns[snapshot_type](mastersnapshot)
    # logger.info('Snapshot: %s', snapshot_data)
    logger.info('\tSnapshot:')
    for key,value in snapshot_data.items():
        logger.info('\t%s:%s', key, json.dumps(value))
    
    return snapshot_data


def generate_mastersnapshots_from_json(mastersnapshot_json_data, snapshot_json_data):
    """
    Get the masternapshot and validate list of snapshots in the json.
    The json could be from the database or from a filesystem.
    """
    snapshot_data = {}
    mastersnapshots = get_field_value(mastersnapshot_json_data, 'snapshots')
    if not mastersnapshots:
        logger.error("Json MasterSnapshot does not contain snapshots, next!...")
        return snapshot_data
    for mastersnapshot in mastersnapshots:
        set_processed_templates({})
        node_resource_types = {}
        for nd in mastersnapshot.get('nodes', []):
            if 'masterSnapshotId' in nd and 'type' in  nd:
                node_resource_types[nd['masterSnapshotId']] = nd['type']
        current_data = generate_mastersnapshot(mastersnapshot)
        # snapshot_data.update(current_data)
        for ms_id, node_list in current_data.items():
            if isinstance(node_list, list):
                if ms_id in snapshot_data:
                    if isinstance(snapshot_data[ms_id], list):
                        snapshot_data[ms_id].extend(node_list)
                    else:
                        snapshot_data[ms_id] = node_list
                else:
                    snapshot_data[ms_id] = node_list
            else:
                logger.debug("No snapshot found for resource type: \"%s\" in %s connector " % (node_resource_types[ms_id], get_field_value(mastersnapshot, "source")))
                if ms_id not in snapshot_data:
                    snapshot_data[ms_id] = node_list

    # for each snapshot_json_data, update the existing json data or add the new json data here.
    return snapshot_data


def generate_snapshots_from_mastersnapshot_file(mastersnapshot_file):
    """
    Each snapshot file from the filesystem is loaded as a json datastructue
     and generate all the nodes in this json datastructure.
    """
    mastersnapshot_file_name = '%s.json' % mastersnapshot_file if mastersnapshot_file and not \
        mastersnapshot_file.endswith('.json') else mastersnapshot_file
    mastersnapshot_json_data = json_from_file(mastersnapshot_file_name)
    if not mastersnapshot_json_data:
        logger.error("masterSnapshot file %s looks to be empty, next!...", mastersnapshot_file)
        return {}, {}

    if "connector" in mastersnapshot_json_data and "remoteFile" in mastersnapshot_json_data and mastersnapshot_json_data["connector"] and mastersnapshot_json_data["remoteFile"]:
        _, pull_response = pull_json_data(mastersnapshot_json_data)
        if not pull_response:
            return {}, {}
    logger.debug(json.dumps(mastersnapshot_json_data, indent=2))
    parts = mastersnapshot_file_name.rsplit('.', 1)
    snapshot_file_name = '%s_gen.%s' % (parts[0], parts[1])
    snapshot_json_data = json_from_file(snapshot_file_name)
    if not snapshot_json_data:
        snapshot_json_data = {}
    snapshot_data = generate_mastersnapshots_from_json(mastersnapshot_json_data, snapshot_json_data)
    # save_json_to_file(mastersnapshot_json_data, mastersnapshot_file)
    if exists_file(snapshot_file_name) : 
        remove_file(snapshot_file_name)        

    save_json_to_file(snapshot_json_data, snapshot_file_name)
    return snapshot_data, mastersnapshot_json_data


def mastersnapshots_used_in_mastertests_filesystem(container):
    """
    Get mastersnapshot list used in all mastertest files of a container from the filesystem.
    This gets list of all the mastersnapshots used in the container.
    The list will be used to make sure the snapshots are not generated multiple times, if the same
    mastersnapshots are used in different mastertest files of a container.
    The configuration of the default path is configured in config.ini.
    """
    snapshots = []
    # logger.info("Starting to get list of mastersnapshots used in test files.")
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    # logger.info(json_dir)
    # Only get list of mastertest files.
    test_files = get_json_files(json_dir, MASTERTEST)
    # logger.info('\n'.join(test_files))
    for test_file in test_files:
        logger.info('\tMASTERTEST:%s', test_file)
        test_json_data = json_from_file(test_file)
        if test_json_data:
            snapshot = test_json_data['masterSnapshot'] if 'masterSnapshot' in test_json_data else ''
            if snapshot:
                file_name = snapshot if snapshot.endswith('.json') else '%s.json' % snapshot
                snapshots.append(file_name)
    return list(set(snapshots))  # set so that unique list of files are returned.


def generate_container_mastersnapshots_filesystem(container):
    """
    Using the mastersnapshot files from the container with storage system as filesystem.
    The path for looking into the container is configured in the config.ini, for the
    default location configuration is $SOLUTIONDIR/realm/validation/<container>
    """
    snapshots_status = {}
    snapshot_dir, snapshot_files = get_container_snapshot_json_files(container, mastersnapshot=True)
    if not snapshot_files:
        logger.error("No mastersnapshot files in %s, exiting!...", snapshot_dir)
        return snapshots_status
    # logger.info('\n'.join(snapshot_files))
    snapshots = mastersnapshots_used_in_mastertests_filesystem(container)
    populated = []
    for snapshot_file in snapshot_files:
        logger.info('\tMASTERSNAPSHOT:%s', snapshot_file)
        parts = snapshot_file.rsplit('/', 1)
        if parts[-1] in snapshots:
            if parts[-1] not in populated:
                # Take the snapshot and crawl for the  resource types.
                snapshot_file_data, snapshot_json_data = generate_snapshots_from_mastersnapshot_file(snapshot_file)
                file_name = '%s.json' % snapshot_file if snapshot_file and not snapshot_file.endswith('.json') else snapshot_file
                # snapshot_json_data = json_from_file(file_name)
                generate_snapshot(snapshot_json_data, snapshot_file_data)
                parts = file_name.rsplit('.', 1)
                new_file_name = '%s_gen.%s' % (parts[0], parts[1])
                save_json_to_file(snapshot_json_data, new_file_name)
                populated.append(parts[-1])
                name = parts[-1].replace('.json', '') if parts[-1].endswith('.json') else parts[-1]
                snapshots_status[name] = snapshot_file_data
        else:
            logger.error("No master testcase found for %s " % parts[-1])
    return snapshots_status


def mastersnapshots_used_in_mastertests_database(container):
    """
    Get mastersnapshot list used in mastertest files of a container from the database.
    The mastersnapshots list are read from database. The default configuration of database and
    snapshot collections is configured in config.ini file.
    """
    snapshots = []
    logger.info("Starting to get list of mastersnapshots from database")
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[MASTERTEST])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    logger.info('Number of mastertest Documents: %s', len(docs))
    if docs and len(docs):
        for doc in docs:
            if doc['json']:
                snapshot = doc['json']['masterSnapshot'] if 'masterSnapshot' in doc['json'] else ''
                if snapshot:
                    if snapshot.endswith('.json'):
                        parts = snapshot.split('.')
                        snapshots.append(parts[0])
                    else:
                        snapshots.append(snapshot)
    return list(set(snapshots))


def generate_container_mastersnapshots_database(container):
    """
    Get the mastersnapshot files from the container with storage system as database.
    The table or collection and database is configured in the config.ini, for the default
    location configuration is "validator" database with "mastersnapshots" as its collections.
    """
    snapshots_status = {}
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[MASTERSNAPSHOT])
    snp_collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
    generate_crawler_run_output(container)
    
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    try:
        if docs and len(docs):
            logger.info('Number of mastersnapshot Documents: %s', len(docs))
            snapshots = mastersnapshots_used_in_mastertests_database(container)
            populated = []
            for doc in docs:
                if doc['json']:
                    snapshot = doc['name']
                    if "connector" in doc['json'] and "remoteFile" in doc['json'] and doc['json']["connector"] and doc['json']["remoteFile"]:
                        _, pull_response = pull_json_data(doc['json'])
                        if not pull_response:
                            logger.info("Failed to populate master snapshot json from the git repository")
                            break

                    if snapshot in snapshots:
                        if snapshot not in populated:
                            snp_collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
                            snp_name = '%s_gen' % snapshot
                            snp_qry = {'container': container, 'name': snp_name}
                            snp_sort = [sort_field('timestamp', False)]
                            snp_docs = get_documents(snp_collection, dbname=dbname, sort=snp_sort, query=snp_qry, _id=True)
                            snp_json_data = {}
                            if snp_docs and len(snp_docs):
                                logger.info('Number of snapshot Documents: %s', len(snp_docs))
                                snp_json_data = snp_docs[0]
                            # Take the mastersnapshot and populate the mastersnapshot
                            snapshot_file_data = generate_mastersnapshots_from_json(doc['json'], snp_json_data)
                            # Insert or update the new generated snapshot document with name='*_gen' and same container name.
                            generate_snapshot(doc['json'], snapshot_file_data)
                            if snp_json_data:
                                set_snapshot_activate_and_validate_data(doc['json'], snp_json_data['json'])
                                snp_json_data['json'] = doc['json']
                                snp_json_data["timestamp"] = int(time.time() * 1000)
                                update_one_document(snp_json_data, snp_json_data['collection'], dbname)
                            else:
                                db_record = {
                                    "timestamp": int(time.time() * 1000),
                                    "container": container,
                                    "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
                                    "type": "snapshot",
                                    "name": snp_name,
                                    "collection": "snapshots",
                                    "json": doc['json']
                                }
                                insert_one_document(db_record, db_record['collection'], dbname, False)
                            populated.append(snapshot)
                            snapshots_status[snapshot] = snapshot_file_data
                    else:
                        logger.error("No master testcase found for %s " % snapshot)
    
        update_crawler_run_status("Completed")
    except Exception as e:
        update_crawler_run_status("Completed")
        raise e
    return snapshots_status

def set_snapshot_activate_and_validate_data(snapshot_data, snapshot_doc_data):
    snapshots = snapshot_data["snapshots"]
    doc_node_list = []

    for snapshot in snapshot_doc_data["snapshots"]:
        if "nodes" in snapshot:
            doc_node_list = doc_node_list + snapshot["nodes"]
    
    for snapshot in snapshots:
        if "nodes" in snapshot and "type" in snapshot:
            for node in snapshot["nodes"]:
                for doc_node in doc_node_list:
                    if snapshot["type"] == "aws":
                        if doc_node["arn"] == node["arn"] and doc_node["masterSnapshotId"] == node["masterSnapshotId"]:
                            node["validate"] = doc_node["validate"] if "validate" in doc_node else node["validate"]
                            node["status"] = doc_node["status"] if "status" in doc_node else node["status"]

                    if snapshot["type"] == "google" or snapshot["type"] == "azure":
                        if doc_node["path"] == node["path"]:
                            node["validate"] = doc_node["validate"] if "validate" in doc_node else node["validate"]
                            node["status"] = doc_node["status"] if "status" in doc_node else node["status"]


def generate_container_mastersnapshots(container, dbsystem=True):
    """
    All master snapshots are also contained in a workspace(which is called as a container) along with regular snapshots .
    So for a crawler operation of a container, the mastersnapshots generate snapshots after crawling the resources using
    the configured connector. The mastersnapshots can be present in a filesystem or a database as storage.
    This function is starting point for mastersnapshot crawler operation.
    The default location for mastersnapshots of the container is the database.
    """
    # logger.critical("MASTERSNAPSHOTS: Generate mastersnapshots for '%s' container from %s",
    #                 container, "the database." if dbsystem  else "file system.")
    logger.info("MASTERSNAPSHOTS:")
    logger.info("\tCollection: %s,  Type: %s",
                    container, "DATABASE" if dbsystem  else "FILESYSTEM")
    if dbsystem:
        return generate_container_mastersnapshots_database(container)
    else:
        return generate_container_mastersnapshots_filesystem(container)

def generate_crawler_run_output(container):
    """
    This creates a entry in the output collection, whenever a crawler runs
    to fetch data. 
    """
    global doc_id
    timestamp = int(time.time() * 1000)
    sort = [sort_field('timestamp', False)]    
    qry = {'container': container}    
    output_collection = config_value(DATABASE, collectiontypes[OUTPUT])    
    dbname = config_value(DATABASE, DBNAME)
    
    collection = config_value(DATABASE, collectiontypes[MASTERTEST])
    tests = get_documents(collection, dbname=dbname, sort=sort, query=qry, _id=True)
    master_tests = [{
                    "id" : str(test['_id']), 
                    "name" : test['name']
                } for test in tests]
    
    mastersp_collection = config_value(DATABASE, collectiontypes[MASTERSNAPSHOT])
    snapshots = get_documents(mastersp_collection, dbname=dbname, sort=sort, query=qry, _id=True)
    master_snapshots = [{
                    "id" : str(snapshot['_id']), 
                    "name" : snapshot['name']
                } for snapshot in snapshots]
    session_id = get_from_currentdata("session_id")
    db_record = { 
        "timestamp" : timestamp,     
        "checksum" : hashlib.md5("{}".encode('utf-8')).hexdigest(), 
        "collection" : output_collection, 
        "container" : container, 
        "name" : "Crawlertest_%s"%(container), 
        "type" : "crawlerOutput", 
        "json" : {
            "container" : container, 
            "contentVersion" : "", 
            "fileType" : "output", 
            "snapshot" : "", 
            "test" : "Crawlertest_%s"%(container), 
            "log" : get_dblog_handler().get_log_collection(), 
            "timestamp" : timestamp, 
            "master_test_list" : master_tests, 
            "master_snapshot_list" : master_snapshots, 
            "output_type" : "crawlerrun", 
            "results" : [],
            "status": "Running",
            "session_id": session_id,
        }
    }
    doc_id = insert_one_document(db_record, db_record['collection'], dbname, False)

def update_crawler_run_status(status):
    """
    Update the status of crawler process in database
    """
    output_collection = config_value(DATABASE, collectiontypes[OUTPUT])
    dbname = config_value(DATABASE, DBNAME)
    
    find_and_update_document(
        collection=output_collection,
        dbname=dbname,
        query={"_id" : ObjectId(doc_id)},
        update_value={ "$set" : { "json.status": status }}
    )