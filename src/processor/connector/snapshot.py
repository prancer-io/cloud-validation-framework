"""
   Common file for running snapshot functions.
   Snapshot is the current configuration of a resource representation in cloud or a git repository.
   For a given test or comparison or evaluation, the tests are mentioned in the a test file.
   The test file references a snapshot file and snapshot file references a list of snapshots to be
   populated using a connector.
   This file is the entry point for all snapshots population.
"""
import json
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    get_container_snapshot_json_files, SNAPSHOT, JSONTEST,\
    collectiontypes, get_json_files, TEST
from processor.helper.config.config_utils import config_value, framework_dir
from processor.database.database import DATABASE, DBNAME, get_documents, sort_field
from processor.connector.snapshot_azure import populate_azure_snapshot
from processor.connector.snapshot_custom import populate_custom_snapshot
from processor.connector.snapshot_aws import populate_aws_snapshot


logger = getlogger()
# Different of snapshots supported by the validation framework.
# The structure has callables for each type of snapshot.
# Each snapshot has been implemented in its own file.
# A new snapshot type xyz will have to be implemented in snapshot_xyz.py
# and callable function for this type of snapshot should be populate_xyz_snapshot
snapshot_fns = {
    'azure': populate_azure_snapshot,
    'git': populate_custom_snapshot,
    'aws': populate_aws_snapshot
}


def populate_snapshot(snapshot):
    """
    Every snapshot should have collection of nodes which are to be populated.
    Each node in the nodes list of the snapshot shall have a unique id in this
    container so as not to clash with other node of a snapshots.
    """
    snapshot_type = get_field_value(snapshot, 'type')
    if snapshot_type and snapshot_type in snapshot_fns:
        if 'nodes' not in snapshot or not snapshot['nodes']:
            logger.info("No nodes in snapshot to be backed up!...")
            return False
        return snapshot_fns[snapshot_type](snapshot)
    return False


def populate_snapshots_from_json(snapshot_json_data):
    """
    Get the snapshot and validate list of snapshots in the json.
    The json could be from the database or from a filesystem.
    """
    snapshots = get_field_value(snapshot_json_data, 'snapshots')
    if not snapshots:
        logger.info("Json Snapshot does not contain snapshots, next!...")
        return False
    for snapshot in snapshots:
        populate_snapshot(snapshot)
    return True


def populate_snapshots_from_file(snapshot_file):
    """
    Each snapshot file from the filesystem is loaded as a json datastructue
     and populate all the nodes in this json datastructure.
    """
    file_name = '%s.json' % snapshot_file if snapshot_file and not \
        snapshot_file.endswith('.json') else snapshot_file
    snapshot_json_data = json_from_file(file_name)
    if not snapshot_json_data:
        logger.info("Snapshot file %s looks to be empty, next!...", snapshot_file)
        return False
    logger.debug(json.dumps(snapshot_json_data, indent=2))
    return populate_snapshots_from_json(snapshot_json_data)


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
    snapshot_dir, snapshot_files = get_container_snapshot_json_files(container)
    if not snapshot_files:
        logger.info("No Snapshot files in %s, exiting!...", snapshot_dir)
        return False
    logger.info('\n'.join(snapshot_files))
    snapshots = container_snapshots_filesystem(container)
    populated = []
    for snapshot_file in snapshot_files:
        parts = snapshot_file.rsplit('/', 1)
        if parts[-1] in snapshots and parts[-1] not in populated:
            # Take the snapshot and populate whether it was susccessful or not.
            # Then pass it back to the validation tests, so that tests for those
            # snapshots that have been susccessfully fetched shall be executed.
            populate_snapshots_from_file(snapshot_file)
            populated.append(parts[-1])
    return True


def populate_container_snapshots_database(container):
    """
    Get the snapshot files from the container with storage system as database.
    The table or collection and database is configured in the config.ini, for the default
    location configuration is "validator" database with "snapshots" as its collections.
    """
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    if docs and len(docs):
        logger.info('Number of Snapshot Documents: %s', len(docs))
        snapshots = container_snapshots_database(container)
        populated = []
        for doc in docs:
            if doc['json']:
                snapshot = doc['name']
                if snapshot in snapshots and snapshot not in populated:
                    # Take the snapshot and populate whether it was susccessful or not.
                    # Then pass it back to the validation tests, so that tests for those
                    # snapshots that have been susccessfully fetched shall be executed.
                    populate_snapshots_from_json(doc['json'])
                    populated.append(snapshot)
    return True


def container_snapshots_filesystem(container):
    """
    Get snapshot list used in all test files of a container from the filesystem.
    This gets list of all the snapshots used in the container.
    The list will be used to not populate the snapshots multiple times, if the same
    snapshots are used in different test files of a container.
    The configuration of the default path is configured in config.ini.
    """
    snapshots = []
    logger.info("Starting to get list of snapshots")
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info(json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        test_json_data = json_from_file(test_file)
        if test_json_data:
            snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
            if snapshot:
                file_name = snapshot if snapshot.endswith('.json') else '%s.json' % snapshot
                snapshots.append(file_name)
    return list(set(snapshots))


def container_snapshots_database(container):
    """
    Get snapshot list used in test files of a container from the database.
    The snapshots list are read from database. The default configuration of database and
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
    return list(set(snapshots))