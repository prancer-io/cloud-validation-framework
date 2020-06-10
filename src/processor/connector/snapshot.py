"""
   Common file for running snapshot functions.
   Snapshot is the current configuration of a resource representation in cloud or a git repository.
   For a given test or comparison or evaluation, the tests are mentioned in the a test file.
   The test file references a snapshot file and snapshot file references a list of snapshots to be
   populated using a connector.
   This file is the entry point for all snapshots population.
    Different of snapshots supported by the validation framework are:
    1) azure: Microsoft Azure cloud.
    2) aws: Amazon cloud servoices.
   The snapshot structure has callables for each type of supported snapshot.
   Each snapshot has been implemented in its own file viz aws in snapshot_aws.py, azure in snapshot_azure.py etc.
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
   OR
   {
        "source": "awsStructure",
        "type": "aws",
        "testUser": "ajeybk",
        "account-id": "<AWS account-id>",
        "nodes": [

        ]
   }
"""
import json
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    get_container_snapshot_json_files, SNAPSHOT, JSONTEST,\
    collectiontypes, get_json_files, TEST, MASTERTEST, save_json_to_file, get_field_value_with_default
from processor.helper.config.config_utils import config_value, framework_dir, SINGLETEST
from processor.database.database import DATABASE, DBNAME, get_documents, sort_field, update_one_document
from processor.connector.snapshot_azure import populate_azure_snapshot
from processor.connector.snapshot_custom import populate_custom_snapshot, get_custom_data
from processor.connector.snapshot_aws import populate_aws_snapshot
from processor.connector.snapshot_google import populate_google_snapshot
from processor.helper.config.rundata_utils import get_from_currentdata
from processor.reporting.json_output import dump_output_results
from processor.connector.populate_json import pull_json_data

logger = getlogger()
# Different types of snapshots supported by the validation framework.
snapshot_fns = {
    'azure': populate_azure_snapshot,
    'aws': populate_aws_snapshot,
    'google': populate_google_snapshot,
    'filesystem': populate_custom_snapshot
}


def populate_snapshot(snapshot, container):
    """
    Every snapshot should have collection of nodes which are to be populated.
    Each node in the nodes list of the snapshot shall have a unique id in this
    container so as not to clash with other node of a snapshots.
    """
    snapshot_data = {}
    snapshot_type = None
    snapshot_source = get_field_value(snapshot, "source")
    connector_data = get_custom_data(snapshot_source)
    if connector_data:
        snapshot_type = get_field_value(connector_data, "type")
    if snapshot_type and snapshot_type in snapshot_fns:
        if 'nodes' not in snapshot or not snapshot['nodes']:
            logger.error("No nodes in snapshot to be backed up!...")
            return snapshot_data
        snapshot_data = snapshot_fns[snapshot_type](snapshot, container)
    logger.info('Snapshot: %s', snapshot_data)
    return snapshot_data


def populate_snapshots_from_json(snapshot_json_data, container):
    """
    Get the snapshot and validate list of snapshots in the json.
    The json could be from the database or from a filesystem.
    """
    snapshot_data = {}
    snapshots = get_field_value(snapshot_json_data, 'snapshots')
    if not snapshots:
        logger.error("Json Snapshot does not contain snapshots, next!...")
        return snapshot_data
    for snapshot in snapshots:
        current_data = populate_snapshot(snapshot, container)
        snapshot_data.update(current_data)
    return snapshot_data


def populate_snapshots_from_file(snapshot_file, container):
    """
    Each snapshot file from the filesystem is loaded as a json datastructue
     and populate all the nodes in this json datastructure.
    """
    file_name = '%s.json' % snapshot_file if snapshot_file and not \
        snapshot_file.endswith('.json') else snapshot_file
    snapshot_json_data = json_from_file(file_name)
    if not snapshot_json_data:
        logger.error("Snapshot file %s looks to be empty, next!...", snapshot_file)
        return {}

    if "connector" in snapshot_json_data and "remoteFile" in snapshot_json_data and snapshot_json_data["connector"] and snapshot_json_data["remoteFile"]:
        _, pull_response = pull_json_data(snapshot_json_data)
        if not pull_response:
            return {}

    logger.debug(json.dumps(snapshot_json_data, indent=2))
    snapshot_data = populate_snapshots_from_json(snapshot_json_data, container)
    # save_json_to_file(snapshot_json_data, snapshot_file)
    return snapshot_data


def populate_container_snapshots(container, dbsystem=True):
    """
    All snapshots are contained in a workspace which is called as a container.
    So tests are run for a container. The snapshots can be present in a filesystem or
    a database as storage.
    This function is starting point for snapshot population.
    The default location for snapshots of the container is the database.
    """
    logger.critical("SNAPSHOTS: Populate snapshots for '%s' container from %s",
                    container, "the database." if dbsystem  else "file system.")
    if dbsystem:
        return populate_container_snapshots_database(container)
    else:
        return populate_container_snapshots_filesystem(container)


def populate_container_snapshots_filesystem(container):
    """
    Get the snapshot files from the container with storage system as filesystem.
    The path for looking into the container is configured in the config.ini, for the
    default location configuration is $SOLUTIONDIR/relam/validation/<container>
    """
    snapshots_status = {}
    snapshot_dir, snapshot_files = get_container_snapshot_json_files(container)
    if not snapshot_files:
        logger.error("No Snapshot files in %s, exiting!...", snapshot_dir)
        return snapshots_status
    logger.info('\n'.join(snapshot_files))
    snapshots = container_snapshots_filesystem(container)
    populated = []
    for snapshot_file in snapshot_files:
        parts = snapshot_file.rsplit('/', 1)
        if parts[-1] in snapshots and parts[-1] not in populated:
            # Take the snapshot and populate whether it was successful or not.
            # Then pass it back to the validation tests, so that tests for those
            # snapshots that have been susccessfully fetched shall be executed.
            snapshot_file_data = populate_snapshots_from_file(snapshot_file, container)
            populated.append(parts[-1])
            name = parts[-1].replace('.json', '') if parts[-1].endswith('.json') else parts[-1]
            snapshots_status[name] = snapshot_file_data
    return snapshots_status


def populate_container_snapshots_database(container):
    """
    Get the snapshot files from the container with storage system as database.
    The table or collection and database is configured in the config.ini, for the default
    location configuration is "validator" database with "snapshots" as its collections.
    """
    snapshots_status = {}
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, _id=True)
    if docs and len(docs):
        logger.info('Number of Snapshot Documents: %s', len(docs))
        snapshots = container_snapshots_database(container)
        if not snapshots:
            raise Exception("No snapshots for this container: %s, add and run again!...", container)
        populated = []
        for doc in docs:
            if doc['json']:
                snapshot = doc['name']
                try:
                    git_connector_json = False
                    if "connector" in doc['json'] and "remoteFile" in doc['json'] and doc['json']["connector"] and doc['json']["remoteFile"]:
                        git_connector_json = True

                    if git_connector_json:
                        _, pull_response = pull_json_data(doc['json'])
                        if not pull_response:
                            break

                    if snapshot in snapshots and snapshot not in populated:
                        # Take the snapshot and populate whether it was successful or not.
                        # Then pass it back to the validation tests, so that tests for those
                        # snapshots that have been susccessfully fetched shall be executed.
                        snapshot_file_data = populate_snapshots_from_json(doc['json'], container)

                        if not git_connector_json:
                            update_one_document(doc, collection, dbname)
                            
                        populated.append(snapshot)
                        snapshots_status[snapshot] = snapshot_file_data
                except Exception as e:
                    dump_output_results([], container, "-", snapshot, False)
                    raise e
    if not snapshots_status:
        raise Exception("No snapshots contained for this container: %s, add and run again!...", container)
    return snapshots_status


def container_snapshots_filesystem(container):
    """
    Get snapshot and mastersnapshot list used in all test/mastertest files of a container from the filesystem.
    This gets list of all the snapshots/mastersnapshots used in the container.
    The list will be used to not populate the snapshots/mastersnapshots multiple times, if the same
    snapshots/mastersnapshots are used in different test/mastertest files of a container.
    The configuration of the default path is configured in config.ini.
    """
    snapshots = []
    logger.info("Starting to get list of snapshots")
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info(json_dir)
    singletest = get_from_currentdata(SINGLETEST)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        test_json_data = json_from_file(test_file)
        if test_json_data:
            snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
            if snapshot:
                file_name = snapshot if snapshot.endswith('.json') else '%s.json' % snapshot
                if singletest:
                    testsets = get_field_value_with_default(test_json_data, 'testSet', [])
                    for testset in testsets:
                        for testcase in testset['cases']:
                            if ('testId' in testcase and testcase['testId'] == singletest) or \
                                    ('masterTestId' in testcase and testcase['masterTestId'] == singletest):
                                if file_name not in snapshots:
                                    snapshots.append(file_name)
                else:
                    snapshots.append(file_name)

    test_files = get_json_files(json_dir, MASTERTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        test_json_data = json_from_file(test_file)
        if test_json_data:
            snapshot = test_json_data['masterSnapshot'] if 'masterSnapshot' in test_json_data else ''
            if snapshot:
                file_name = snapshot if snapshot.endswith('.json') else '%s.json' % snapshot
                parts = file_name.split('.')
                file_name = '%s_gen.%s' % (parts[0], parts[-1])
                if singletest:
                    testsets = get_field_value_with_default(test_json_data, 'testSet', [])
                    for testset in testsets:
                        for testcase in testset['cases']:
                            if ('testId' in testcase and testcase['testId'] == singletest) or \
                                    ('masterTestId' in testcase and testcase['masterTestId'] == singletest):
                                if file_name not in snapshots:
                                    snapshots.append(file_name)
                else:
                    snapshots.append(file_name)
    return list(set(snapshots))


def container_snapshots_database(container):
    """
    Get snapshot list used in test and mastertest files of a container from the database.
    The snapshots or mastersnapshots list are read from database. The default configuration of database and
    snapshot collections is configured in config.ini file.
    """
    snapshots = []
    logger.info("Starting to get list of snapshots from database")
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[TEST])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    logger.info('Number of test Documents: %s', len(docs))
    if docs and len(docs):
        for doc in docs:
            if doc['json']:
                snapshot = doc['json']['snapshot'] if 'snapshot' in doc['json'] else ''
                if snapshot:
                    if snapshot.endswith('.json'):
                        parts = snapshot.split('.')
                        snapshots.append(parts[0])
                    else:
                        snapshots.append(snapshot)
    # Look for mastertest files.
    collection = config_value(DATABASE, collectiontypes[MASTERTEST])
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    logger.info('Number of mastertest Documents: %s', len(docs))
    if docs and len(docs):
        for doc in docs:
            if doc['json']:
                # mastertest files have to use masterSnapshot
                snapshot = doc['json']['masterSnapshot'] if 'masterSnapshot' in doc['json'] else ''
                if snapshot:
                    # mastersnapshot are generated with _gen suffix
                    if snapshot.endswith('.json'):
                        parts = snapshot.split('.')
                        snapshots.append('%s_gen' % parts[0])
                    else:
                        snapshots.append('%s_gen' % snapshot)
    return list(set(snapshots))


