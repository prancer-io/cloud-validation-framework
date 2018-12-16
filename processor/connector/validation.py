"""
   Common file for running validations.
"""
import json
import pymongo
from processor.logging.log_handler import getlogger
from processor.comparison.interpreter import Comparator
from processor.helper.json.json_utils import get_field_value, get_json_files,\
    load_json
from processor.helper.config.config_utils import get_config, get_test_json_dir,\
    DATABASE, DBNAME, get_solution_dir
from processor.database.database import get_documents, create_indexes, COLLECTION
from processor.reporting.json_output import dump_output_results


JSONTEST = 'test'
logger = getlogger()


def run_validation_test(version, dbname, collection, snapshot_id, testcase):

    if snapshot_id:
        docs = get_documents(collection, dbname=dbname,
                             sort=[('timestamp', pymongo.DESCENDING)],
                             query={'snapshotId': snapshot_id},
                             limit=1)
        logger.info('Number of Snapshot Documents: %s', len(docs))
        if docs and len(docs):
            comparator = Comparator(version, docs[0]['json'], testcase['attribute'],
                                    testcase['comparison'])
            result = comparator.validate()
            logger.info('Testid: %s, snapshot:%s, attribute: %s, comparison:%s, result: %s',
                        testcase['testId'], testcase['snapshotId'], testcase['attribute'],
                        testcase['comparison'], result)
            result_val = {
                "result": "passed" if result else "failed"
            }
        else:
            result_val = {
                "result": "skipped",
                "reason": "Missing documents for the snapshot"
            }
    else:
        result_val = {
            "result": "skipped",
            "reason": "Missing snapshotId for testcase"
        }
    result_val.update(testcase)

    return result_val


def get_snapshot_id_to_collection_dict(snapshot_file, container, dbname):
    snapshot_file = '%s/%s/%s' % (get_test_json_dir(), container, snapshot_file)
    snapshot_data = {}
    snapshot_json_data = load_json(snapshot_file)
    if not snapshot_json_data:
        return snapshot_data
    for snapshot in snapshot_json_data['snapshots']:
        for snode in snapshot['nodes']:
            collection = snode['collection'] if 'collection' in snode else COLLECTION
            snapshot_data[snode['snapshotId']] = collection.replace('.', '').lower()
            create_indexes(snapshot_data[snode['snapshotId']], dbname, [('timestamp', pymongo.TEXT)])
    return snapshot_data


def run_file_validation_tests(test_file, container):
    logger.info("*" * 50)
    logger.info("validator tests: %s", test_file)
    test_json_data = load_json(test_file)
    if not test_json_data:
        logger.info("Test file %s looks to be empty, next!...", test_file)
        return False
    logger.debug(json.dumps(test_json_data, indent=2))
    testsets = get_field_value(test_json_data, 'testSet')
    if not testsets or not isinstance(testsets, list):
        logger.info("Test file %s does not contain testset, next!...", test_file)
        return False
    dbname = get_config(DATABASE, DBNAME)
    collection_data = get_snapshot_id_to_collection_dict(test_json_data['snapshot'], container, dbname)
    resultset = []
    for testset in testsets:
        version = get_field_value(testset, 'version')
        if 'cases' not in testset or not isinstance(testset['cases'], list):
            logger.info("No testcases in testSet!...")
            continue
        for testcase in testset['cases']:
            snapshot_id = testcase['snapshotId'] if 'snapshotId' in testcase and \
                                                    testcase['snapshotId'] else None
            collection = collection_data[snapshot_id] if snapshot_id and \
                                                         snapshot_id in collection_data else COLLECTION
            result_val = run_validation_test(version, dbname, collection, snapshot_id, testcase)
            resultset.append(result_val)
    dump_output_results(resultset, test_file, container)


def run_container_validation_tests(container):
    logger.info("Starting validation tests")
    reporting_path = get_config('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (get_solution_dir(), reporting_path, container)
    logger.info(json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        run_file_validation_tests(test_file, container)
    return True
