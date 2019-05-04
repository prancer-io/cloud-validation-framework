"""
   Common file for running validations.
"""
import json
import re
import pymongo
from processor.logging.log_handler import getlogger
from processor.comparison.interpreter import Comparator
from processor.helper.json.json_utils import get_field_value, get_json_files,\
    json_from_file, TEST, collectiontypes, SNAPSHOT, JSONTEST
from processor.helper.config.config_utils import config_value, get_test_json_dir,\
    DATABASE, DBNAME, framework_dir
from processor.database.database import create_indexes, COLLECTION,\
    sort_field, get_documents
from processor.reporting.json_output import dump_output_results


logger = getlogger()


def get_snapshot_id_to_collection_dict(snapshot_file, container, dbname, filesystem=True):
    snapshot_data = {}
    snapshot_json_data = {}
    if filesystem:
        file_name = '%s.json' % snapshot_file if snapshot_file and not \
            snapshot_file.endswith('.json') else snapshot_file
        snapshot_file = '%s/%s/%s' % (get_test_json_dir(), container, file_name)
        snapshot_json_data = json_from_file(snapshot_file)
    else:
        parts = snapshot_file.split('.')
        collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
        qry = {'container': container, 'name': parts[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of Snapshot Documents: %s', len(docs))
        if docs and len(docs):
            snapshot_json_data = docs[0]['json']
    snapshots = get_field_value(snapshot_json_data, 'snapshots')
    if not snapshots:
        logger.info("Snapshot does not contain snapshots...")
        return snapshot_data
    for snapshot in snapshots:
        nodes = get_field_value(snapshot, 'nodes')
        if not nodes:
            logger.info("No nodes in snapshot, continuing to next!...")
            continue
        for node in nodes:
            sid = get_field_value(node, 'snapshotId')
            coll = node['collection'] if 'collection' in node else COLLECTION
            collection = coll.replace('.', '').lower()
            snapshot_data[sid] = collection
            create_indexes(collection, dbname, [('timestamp', pymongo.TEXT)])
    return snapshot_data


def run_validation_test(version, dbname, collection_data, testcase):
    comparator = Comparator(version, dbname, collection_data, testcase)
    result_val = comparator.validate()
    result_val.update(testcase)
    return result_val


def run_file_validation_tests(test_file, container, filesystem=True, snapshot_status=None):
    logger.info("*" * 50)
    logger.info("validator tests: %s", test_file)
    test_json_data = json_from_file(test_file)
    if not test_json_data:
        logger.info("Test file %s looks to be empty, next!...", test_file)
    resultset = run_json_validation_tests(test_json_data, container, filesystem, snapshot_status)
    finalresult = True
    if resultset:
        snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
        dump_output_results(resultset, container, test_file, snapshot, filesystem)
        for result in resultset:
            if 'result' in result:
                if not re.match(r'passed', result['result'], re.I):
                    finalresult = False
                    break
    else:
        # TODO: NO test cases in this file.
        # LOG HERE that no test cases are present in this file.
        finalresult = False
    return finalresult


def run_json_validation_tests(test_json_data, container, filesystem=True, snapshot_status=None):
    resultset = []
    if not test_json_data:
        return resultset
    if not snapshot_status:
        snapshot_status = {}
    logger.debug(json.dumps(test_json_data, indent=2))
    testsets = get_field_value(test_json_data, 'testSet')
    if not testsets or not isinstance(testsets, list):
        logger.info("Test json does not contain testset, next!...")
        return resultset
    dbname = config_value(DATABASE, DBNAME)
    # Populate the snapshotId => collection for the snapshot.json in the test file.
    collection_data = get_snapshot_id_to_collection_dict(test_json_data['snapshot'],
                                                         container, dbname, filesystem)
    if test_json_data['snapshot'] in snapshot_status:
        current_snapshot_status = snapshot_status[test_json_data['snapshot']]
    else:
        current_snapshot_status = {}
    for testset in testsets:
        version = get_field_value(testset, 'version')
        testcases = get_field_value(testset, 'cases')
        if not testcases or not isinstance(testcases, list):
            logger.info("No testcases in testSet!...")
            continue
        for testcase in testset['cases']:
            result_val = run_validation_test(version, dbname, collection_data,
                                             testcase)
            resultset.append(result_val)
    return resultset


def run_container_validation_tests(container, dbsystem=True, snapshot_status=None):
    if not snapshot_status:
        snapshot_status = {}
    if dbsystem:
        return run_container_validation_tests_database(container, snapshot_status)
    else:
        return run_container_validation_tests_filesystem(container, snapshot_status)


def run_container_validation_tests_filesystem(container, snapshot_status=None):
    """Get test files from the filesystem."""
    logger.info("Starting validation tests")
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info(json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    result = True
    for test_file in test_files:
        val = run_file_validation_tests(test_file, container, True, snapshot_status)
        result = result and val
    return result


def run_container_validation_tests_database(container, snapshot_status=None):
    """ Get the test files from the database"""
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[TEST])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    finalresult = True
    if docs and len(docs):
        logger.info('Number of test Documents: %s', len(docs))
        for doc in docs:
            if doc['json']:
                resultset = run_json_validation_tests(doc['json'], container, False)
                if resultset:
                    snapshot = doc['json']['snapshot'] if 'snapshot' in doc['json'] else ''
                    test_file = doc['name'] if 'name' in doc else ''
                    dump_output_results(resultset, container, test_file, snapshot, False)
                    for result in resultset:
                        if 'result' in result:
                            if not re.match(r'passed', result['result'], re.I):
                                finalresult = False
                                break
    else:
        # TODO: Didnt find any tests
        # LOG HERE
        finalresult = False
    return finalresult


def container_snapshots_filesystem(container):
    """Get snapshot list used in test files from the filesystem."""
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
                snapshots.append(snapshot)
    return snapshots