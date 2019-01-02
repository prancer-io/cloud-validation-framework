"""
   Common file for running validations.
"""
import json
import pymongo
from processor.logging.log_handler import getlogger
from processor.comparison.interpreter import Comparator
from processor.helper.json.json_utils import get_field_value, get_json_files,\
    json_from_file
from processor.helper.config.config_utils import config_value, get_test_json_dir,\
    DATABASE, DBNAME, framework_dir
from processor.database.database import create_indexes, COLLECTION
from processor.reporting.json_output import dump_output_results


JSONTEST = 'test'
logger = getlogger()


def get_snapshot_id_to_collection_dict(snapshot_file, container, dbname):
    snapshot_file = '%s/%s/%s' % (get_test_json_dir(), container, snapshot_file)
    snapshot_data = {}
    snapshot_json_data = json_from_file(snapshot_file)
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


def run_file_validation_tests(test_file, container):
    logger.info("*" * 50)
    logger.info("validator tests: %s", test_file)
    test_json_data = json_from_file(test_file)
    if not test_json_data:
        logger.info("Test file %s looks to be empty, next!...", test_file)
        return False
    logger.debug(json.dumps(test_json_data, indent=2))
    testsets = get_field_value(test_json_data, 'testSet')
    if not testsets or not isinstance(testsets, list):
        logger.info("Test file %s does not contain testset, next!...", test_file)
        return False
    dbname = config_value(DATABASE, DBNAME)
    # Populate the snapshotId => collection for the snapshot.json in the test file.
    collection_data = get_snapshot_id_to_collection_dict(test_json_data['snapshot'],
                                                         container, dbname)
    resultset = []
    for testset in testsets:
        version = get_field_value(testset, 'version')
        testcases = get_field_value(testset, 'cases')
        if not testcases or not isinstance(testcases, list):
            logger.info("No testcases in testSet!...")
            continue
        for testcase in testset['cases']:
            result_val = run_validation_test(version, dbname, collection_data, testcase)
            resultset.append(result_val)
    dump_output_results(resultset, test_file, container)
    return True


def run_container_validation_tests(container):
    logger.info("Starting validation tests")
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info(json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        run_file_validation_tests(test_file, container)
    return True
