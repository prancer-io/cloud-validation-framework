"""
   Common file for running validations.
"""
from datetime import datetime
import json
import re
from time import time
import pymongo
import copy 

from collections import defaultdict
from processor.logging.log_handler import getlogger
from processor.comparison.interpreter import Comparator
from processor.helper.json.json_utils import get_field_value, get_json_files,\
    json_from_file, TEST, collectiontypes, SNAPSHOT, JSONTEST, MASTERTEST, get_field_value_with_default
from processor.helper.config.config_utils import config_value, get_test_json_dir,\
    DATABASE, DBNAME, framework_dir, EXCLUSION
from processor.database.database import create_indexes, COLLECTION,\
    sort_field, get_documents
from processor.reporting.json_output import dump_output_results, update_output_testname
from processor.helper.config.rundata_utils import get_dbtests, get_from_currentdata
from processor.connector.populate_json import pull_json_data
from processor.connector.special_compliance.compliances import COMPLIANCES

logger = getlogger()

def get_snapshot_file(snapshot_file, container, dbname, filesystem):
    snapshot_json_data = {}
    if filesystem:
        file_name = '%s.json' % snapshot_file if snapshot_file and not \
            snapshot_file.endswith('.json') else snapshot_file
        snapshot_file = '%s/%s/%s' % (get_test_json_dir(), container, file_name)
        snapshot_json_data = json_from_file(snapshot_file)
    else:
        # parts = snapshot_file.split('.')
        collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
        qry = {'container': container, 'name': snapshot_file}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of Snapshot Documents: %s', len(docs))
        if docs and len(docs):
            snapshot_json_data = docs[0]['json']
    return snapshot_json_data

def get_snapshot_id_to_collection_dict(snapshot_file, container, dbname, filesystem=True):
    snapshot_data = {}
    snapshot_json_data = get_snapshot_file(snapshot_file, container, dbname, filesystem)
    if snapshot_json_data and "connector" in snapshot_json_data and "remoteFile" in snapshot_json_data \
        and snapshot_json_data["connector"] and snapshot_json_data["remoteFile"]:
            _, pull_response = pull_json_data(snapshot_json_data)
            if not pull_response:
                return snapshot_data

    snapshots = get_field_value(snapshot_json_data, 'snapshots')
    if not snapshots:
        logger.info("\tERROR: Snapshot does not contain snapshots, continuing...")
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
            if get_dbtests():
                create_indexes(collection, dbname, [('timestamp', pymongo.TEXT)])
    return snapshot_data


def run_validation_test(version, container, dbname, collection_data, testcase, excludedTestIds, includeTests):
    comparator = Comparator(version, container, dbname, collection_data, testcase, excludedTestIds, includeTests)
    results = comparator.validate()
    if isinstance(results, list):
        for result in results:
            result["result_id"] = "%s_%s" % (re.sub(r"(?=[-_\s\.]).", "", container).lower(), str(int(datetime.now().timestamp())))
            result.update(testcase)
        return results
    else:
        results.update(testcase)
        return[results]

def get_min_severity_error_list():
    severity_list = []
    console_min_severity_error = config_value("RESULT", "console_min_severity_error", default="Low")
    if str(console_min_severity_error).lower() == "low":
        severity_list = ["low", "medium", "high"]
    elif str(console_min_severity_error).lower() == "medium":
        severity_list = ["medium", "high"]
    elif str(console_min_severity_error).lower() == "high":
        severity_list = ["high"]
    return severity_list

def validate_result(resultset, finalresult):
    min_severity_list = get_min_severity_error_list()
    if resultset:
        for result in resultset:
            if 'result' in result:
                if not re.match(r'passed', result['result'], re.I) and str(result.get("severity", "low")).lower() in min_severity_list:
                    logger.info("\tTEST: %s", result)
                    finalresult = False
                    break
    return finalresult

def run_file_validation_tests(test_file, container, filesystem=True, snapshot_status=None):
    # logger.info("*" * 50)
    logger.info("\tTEST: %s", test_file)
    dirpath = None
    test_json_data = json_from_file(test_file)
    if not test_json_data:
        logger.info("\t\tTest file %s looks to be empty, next!...", test_file)

    if test_json_data and "connector" in test_json_data and "remoteFile" in test_json_data and test_json_data["connector"] and test_json_data["remoteFile"]:
        dirpath, pull_response = pull_json_data(test_json_data)
        if not pull_response:
            return {}

    # singletest = get_from_currentdata(SINGLETEST)
    # if singletest:
    #     testsets = get_field_value_with_default(test_json_data, 'testSet', [])
    #     for testset in testsets:
    #         newtestcases = []
    #         for testcase in testset['cases']:
    #             if ('testId' in testcase and testcase['testId'] == singletest) or \
    #                     ('masterTestId' in testcase and testcase['masterTestId'] == singletest):
    #                 newtestcases.append(testcase)
    #         testset['cases'] = newtestcases
    resultset = run_json_validation_tests(test_json_data, container, filesystem, snapshot_status, dirpath=dirpath)
    finalresult = True
    if resultset:
        snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
        # if singletest:
        #     print(json.dumps(resultset, indent=2))
        # else:
        #     dump_output_results(resultset, container, test_file, snapshot, filesystem)
        dump_output_results(resultset, container, test_file, snapshot, filesystem)
        finalresult = validate_result(resultset, finalresult)
    else:
        # TODO: NO test cases in this file.
        # LOG HERE that no test cases are present in this file.
        finalresult = False
    return finalresult


def run_json_validation_tests(test_json_data, container, filesystem=True, snapshot_status=None, dirpath=None):
    resultset = []
    if not test_json_data:
        return resultset
    if not snapshot_status:
        snapshot_status = {}
    # logger.info("Valid Test JSON data")
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

    includeTestConfig = get_from_currentdata("INCLUDETESTS")
    includeTests = []
    if includeTestConfig:
        includeTests = get_from_currentdata("TESTIDS")
    excludedTestIds = {}
    exclusions = get_from_currentdata(EXCLUSION).get('exclusions', [])
    for exclusion in exclusions:
        if 'exclusionType' in exclusion and exclusion['exclusionType'] and exclusion['exclusionType'] == 'single':
            if 'masterTestID' in exclusion and exclusion['masterTestID'] \
                    and 'paths' in exclusion and exclusion['paths']:
                toAdd = False
                if includeTestConfig:
                    if exclusion['masterTestID'] not in includeTests:
                        toAdd = True
                else:
                    toAdd =  True
                if toAdd:
                    if exclusion['masterTestID'] not in excludedTestIds:
                        excludedTestIds[exclusion['masterTestID']] = exclusion['paths']
                    else:
                        excludedTestIds[exclusion['masterTestID']].extend(exclusion['paths'])

    skip = 0
    limit = 10
    dumpsize = 10
    for testset in testsets:
        version = get_field_value(testset, 'version')
        testcases = get_field_value(testset, 'cases')
        if not testcases or not isinstance(testcases, list):
            logger.info("No testcases in testSet!...")
            continue
        for testcase in testset['cases']:
            if "status" in testcase and testcase["status"] == "disable":
                continue
            else:
                testcase["status"] = "enable"
            if dirpath:
                testcase['dirpath'] = dirpath
            results = run_validation_test(version, container, dbname, collection_data,
                                             testcase, excludedTestIds, includeTests)
            resultset.extend(results)
            if not filesystem:
                if len(resultset) >= limit:
                    dump_output_results(resultset[skip:limit], container, test_file="", snapshot="", filesystem=False)
                    skip = limit
                    limit = skip + dumpsize
        
        if not filesystem and len(resultset) >= (skip+1):
            dump_output_results(resultset[skip:], container, test_file="", snapshot="", filesystem=False)
            skip = len(resultset)
            limit = skip + dumpsize
        
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
    # logger.info("Starting validation tests")
    logger.info("VALIDATION:")
    logger.info("\tCollection: %s,  Type: FILESYSTEM", container)
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info('\tLOCATION: %s', json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    # logger.info('\n'.join(test_files))
    result = True
    for test_file in test_files:
        logger.info('\tCOLLECTION: %s', test_file)
        val = run_file_validation_tests(test_file, container, True, snapshot_status)
        result = result and val
    if test_files:
        # return the result value if "test" file is processed collection
        logger.critical("VALIDATION COMPLETE:")
        return result

    # mastertest files
    test_files = get_json_files(json_dir, MASTERTEST)
    # logger.info('\n'.join(test_files))
    if not test_files:
        logger.error("ERROR: No `test` or `mastertest` file found. collection should contain either `test` or `mastertest` file")
        return False

    finalresult = result
    for test_file in test_files:
        logger.info('\tCOLLECTION: %s', test_file)
        # logger.info("*" * 50)
        # logger.info("validator tests: %s", test_file)
        dirpath = None
        test_json_data = json_from_file(test_file)
        if not test_json_data:
            logger.info("Test file %s looks to be empty, next!...", test_file)
            continue

        if "connector" in test_json_data and "remoteFile" in test_json_data and test_json_data["connector"] and test_json_data["remoteFile"]:
            dirpath, pull_response = pull_json_data(test_json_data)
            if not pull_response:
                return {}

        snapshot_key = '%s_gen' % test_json_data['masterSnapshot']
        mastersnapshots = defaultdict(list)
        snapshot_data = snapshot_status[snapshot_key] if snapshot_key in snapshot_status else {}
        for snapshot_id, mastersnapshot_id in snapshot_data.items():
            if isinstance(mastersnapshot_id, list):
                for master_snapshot_id in mastersnapshot_id:
                    mastersnapshots[master_snapshot_id].append(snapshot_id)
            elif isinstance(mastersnapshot_id, str):
                mastersnapshots[mastersnapshot_id].append(snapshot_id)
        if not mastersnapshots:
            logger.error("No generated snapshots found for validation.")
            continue
        test_json_data['snapshot'] = snapshot_key
        testsets = get_field_value_with_default(test_json_data, 'testSet', [])
        for testset in testsets:
            testcases = get_field_value_with_default(testset, 'cases', [])
            testset['cases'] = _get_new_testcases(testcases, mastersnapshots, snapshot_key, container, filesystem=True)
        # print(json.dumps(test_json_data, indent=2))
        # singletest = get_from_currentdata(SINGLETEST)
        # if singletest:
        #     for testset in testsets:
        #         newtestcases = []
        #         for testcase in testset['cases']:
        #             if ('testId' in testcase and  testcase['testId'] == singletest) or \
        #                     ('masterTestId' in testcase and testcase['masterTestId'] == singletest):
        #                 newtestcases.append(testcase)
        #         testset['cases'] = newtestcases
        resultset = run_json_validation_tests(test_json_data, container, True, snapshot_status, dirpath=dirpath)
        if test_json_data.get('testSet') and not resultset:
            logger.error('\tERROR: Testset does not contains any testcases or all testcases are skipped due to invalid rules.')
        elif resultset:
            snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
            # if singletest:
            #     print(json.dumps(resultset, indent=2))
            # else:
            #     dump_output_results(resultset, container, test_file, snapshot, True)
            dump_output_results(resultset, container, test_file, snapshot, True)
            finalresult = validate_result(resultset, finalresult)
        else:
            logger.error('\tERROR: No mastertest Documents found!')
            finalresult = False
    logger.critical("VALIDATION COMPLETE:")
    return finalresult

def run_filecontent_validation(container, snapshot_status=None):
    logger.info("FILE CONTENT VALIDATION:")
    logger.info("\tCollection: %s,  Type: FILESYSTEM", container)
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
    logger.info('\tLOCATION: %s', json_dir)
    test_files = get_json_files(json_dir, MASTERTEST)
    if not test_files:
        logger.error("ERROR: No `test` or `mastertest` file found. collection should contain either `test` or `mastertest` file")
        return False

    finalresult = True
    for test_file in test_files:
        logger.info('\tCOLLECTION: %s', test_file)
        # logger.info("*" * 50)
        # logger.info("validator tests: %s", test_file)
        dirpath = None
        test_json_data = json_from_file(test_file)
        if not test_json_data:
            logger.info("Test file %s looks to be empty, next!...", test_file)
            continue
        snapshot_key = '%s_gen' % test_json_data['masterSnapshot']
        test_json_data['snapshot'] = snapshot_key
        mastersnapshots = defaultdict(list)
        snapshot_data = snapshot_status[snapshot_key] if snapshot_key in snapshot_status else {}
        for snapshot_id, mastersnapshot_id in snapshot_data.items():
            if isinstance(mastersnapshot_id, list):
                for master_snapshot_id in mastersnapshot_id:
                    mastersnapshots[master_snapshot_id].append(snapshot_id)
            elif isinstance(mastersnapshot_id, str):
                mastersnapshots[mastersnapshot_id].append(snapshot_id)
        testsets = get_field_value_with_default(test_json_data, 'testSet', [])
        for testset in testsets:
            testcases = get_field_value_with_default(testset, 'cases', [])
            # if testIds:
            #     newTestcases = []
            #     for testcase in testcases:
            #         if testcase['masterTestId'] in testIds:
            #             newTestcases.append(testcase)
            #     testcases = newTestcases
            # testset['cases'] = _get_new_testcases(testcases, mastersnapshots)
            testset['cases'] = _get_new_testcases(testcases, mastersnapshots, snapshot_key, container, filesystem=True)


        resultset = run_json_validation_tests(test_json_data, container, filesystem=True, snapshot_status=snapshot_status)
        if test_json_data.get('testSet') and not resultset:
            logger.error('\tERROR: Testset does not contains any testcases or all testcases are skipped due to invalid rules.')
        elif resultset:
            snapshot = test_json_data['snapshot'] if 'snapshot' in test_json_data else ''
            dump_output_results(resultset, container, test_file, snapshot, True)
            finalresult = validate_result(resultset, finalresult)
        else:
            logger.error('\tERROR: No mastertest Documents found!')
            finalresult = False
    logger.critical("VALIDATION COMPLETE:")
    return finalresult

def _get_snapshot_type_map(container):
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[SNAPSHOT])
    qry = {'container': container}
    docs = get_documents(collection, dbname=dbname, query=qry)
    mappings = {}
    if docs and len(docs):
        for doc in docs:
            given_data = doc['json']
            if given_data:
                snapshots = given_data.get("snapshots", [])
                for snapshot in snapshots:
                    given_type = snapshot.get("type","")
                    if given_type == "aws":
                        nodes = snapshot.get("nodes",[])
                        for node in nodes:
                            mappings[node['snapshotId']] = node['type']
    return mappings


def run_container_validation_tests_database(container, snapshot_status=None):
    """ Get the test files from the database"""
    dirpath = None
    dbname = config_value(DATABASE, DBNAME)
    test_files_found = True
    mastertest_files_found = True
    # For test files
    collection = config_value(DATABASE, collectiontypes[TEST])
    qry = {'container': container}
    sort = [sort_field('timestamp', False)]
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    finalresult = True
    if docs and len(docs):
        logger.info('Number of test Documents: %s', len(docs))
        for doc in docs:
            if doc['json']:
                try:
                    snapshot = doc['json']['snapshot'] if 'snapshot' in doc['json'] else ''
                    test_file = doc['name'] if 'name' in doc else ''
                    update_output_testname(test_file, snapshot, filesystem=False)
                    if "connector" in doc['json'] and "remoteFile" in doc['json'] and doc['json']["connector"] and doc['json']["remoteFile"]:
                        dirpath, pull_response = pull_json_data(doc['json'])
                        if not pull_response:
                            return {}
                    resultset = run_json_validation_tests(doc['json'], container, False, dirpath=dirpath)
                    if resultset:
                        finalresult = validate_result(resultset, finalresult)
                except Exception as e:
                    # dump_output_results([], container, "-", snapshot, False)
                    raise e
    else:
        logger.info('No test Documents found!')
        test_files_found = False
        # finalresult = False
    # For mastertest files
    collection = config_value(DATABASE, collectiontypes[MASTERTEST])
    docs = get_documents(collection, dbname=dbname, sort=sort, query=qry)
    # snapshots_details_map = _get_snapshot_type_map(container)
    if docs and len(docs):
        logger.info('Number of mastertest Documents: %s', len(docs))
        for doc in docs:
            test_json_data = doc['json']
            if test_json_data:
                snapshot = doc['json']['masterSnapshot'] if 'masterSnapshot' in doc['json'] else ''
                test_file = doc['name'] if 'name' in doc else '-'
                update_output_testname(test_file, snapshot, filesystem=False)
                try:
                    if "connector" in test_json_data and "remoteFile" in test_json_data and test_json_data["connector"] and test_json_data["remoteFile"]:
                        dirpath, pull_response = pull_json_data(test_json_data)
                        if not pull_response:
                            return {}
                    snapshot_key = '%s_gen' % test_json_data['masterSnapshot']
                    mastersnapshots = defaultdict(list)
                    snapshot_data = snapshot_status[snapshot_key] if snapshot_key in snapshot_status else {}
                    for snapshot_id, mastersnapshot_id in snapshot_data.items():
                        if isinstance(mastersnapshot_id, list):
                            for msnp_id in mastersnapshot_id:
                                mastersnapshots[msnp_id].append(snapshot_id)    
                        else:
                            mastersnapshots[mastersnapshot_id].append(snapshot_id)
                    test_json_data['snapshot'] = snapshot_key
                    testsets = get_field_value_with_default(test_json_data, 'testSet', [])
                    for testset in testsets:
                        testcases = get_field_value_with_default(testset, 'cases', [])
                        testcases += COMPLIANCES
                        testset['cases'] = _get_new_testcases(testcases, mastersnapshots, snapshot_key, container, dbname, False)
                    # print(json.dumps(test_json_data, indent=2))
                    resultset = run_json_validation_tests(test_json_data, container, False, snapshot_status, dirpath=dirpath)
                    finalresult = validate_result(resultset, finalresult)
                except Exception as e:
                    # dump_output_results([], container, test_file, snapshot, False)
                    raise e
    else:
        logger.info('No mastertest Documents found!')
        mastertest_files_found = False
        # finalresult = False
    if not test_files_found and not mastertest_files_found:
        raise Exception("No complaince tests for this container: %s, add and run!", container)
    return finalresult


def _get_new_testcases(testcases, mastersnapshots, snapshot_key, container, dbname=None, filesystem=True):
    onlysnapshots = get_from_currentdata("ONLYSNAPSHOTS")
    onlysnapshotsIds = get_from_currentdata("ONLYSNAPSHOTIDS")
    includeTestConfig = get_from_currentdata("INCLUDETESTS")
    includeTests = get_from_currentdata("TESTIDS")

    excludedTestIds = []
    exclusions = get_from_currentdata(EXCLUSION).get('exclusions', [])
    for exclusion in exclusions:
        if 'exclusionType' in exclusion and exclusion['exclusionType'] and exclusion['exclusionType'] == 'test':
            if 'masterTestID' in exclusion and exclusion['masterTestID'] and exclusion['masterTestID'] not in excludedTestIds:
                if includeTestConfig:
                    if exclusion['masterTestID'] not in includeTests:
                        excludedTestIds.append(exclusion['masterTestID'])
                else:
                    excludedTestIds.append(exclusion['masterTestID'])
    
    snapshot_json_data = get_snapshot_file(snapshot_key, container, dbname, filesystem)
    snapshots = snapshot_json_data.get("snapshots")
    snapshot_resource_map = {}
    for snapshot in snapshots:
        for node in snapshot["nodes"]:
            snapshot_resource_map[node.get("snapshotId")] = node.get("resourceTypes", [])
    
    snapshot_testcases_map = {}
    newcases = []
    for testcase in testcases:
        if excludedTestIds:
            # Check if masterTestID is present in exclusion list.
            if  'masterTestId' in testcase and testcase['masterTestId'] and testcase['masterTestId'] in excludedTestIds:
                logger.warning("Excluded from testId exclusions: %s", testcase['masterTestId'])
                continue
            # Check if any complianceID is present in the exclusion list. Only that complianceID will be removed and
            # the rest to be run.
            # If there is only complianceID in the testcase (i.e only one eval in the evals list) and that is part of
            # exclusion list, then the testcase is excluded.
            if 'evals' in testcase and testcase['evals'] and isinstance(testcase['evals'], list):
                found = False
                evalsTobeRemoved = []
                for eval in testcase['evals']:
                    if eval['id'] in excludedTestIds:
                        found = True
                        evalsTobeRemoved.append(eval['id'])
                if found:
                    newEvals = []
                    for eval in testcase['evals']:
                        if eval['id'] not in evalsTobeRemoved:
                            newEvals.append(eval)
                    logger.warning("Excluded from testId exclusions: %s with these complianceIds: %s",
                                   testcase['masterTestId'], ','.join(evalsTobeRemoved))
                    if newEvals: # More than one evals was present and one of them was removed.
                        testcase['evals'] = newEvals
                    else:  # There was only one eval, that was removed, so whole testcase will be remove as no eval is present.
                        continue
        if includeTestConfig:
            if 'masterTestId' in testcase and testcase['masterTestId'] and testcase['masterTestId'] not in includeTests:
                # MasterTestID is not present in includeTests, check if any complianceID is present in includeTests
                if 'evals' in testcase and testcase['evals'] and isinstance(testcase['evals'], list):
                    evalsTobeAdded = []
                    for eval in testcase['evals']:
                        if eval['id'] in includeTests:
                            evalsTobeAdded.append(eval)
                    if evalsTobeAdded:
                        testcase['evals'] = evalsTobeAdded
                    else:
                        continue

        test_parser_type = testcase.get('type', None)
        if test_parser_type == 'rego' or test_parser_type == 'python':
            new_cases = _get_rego_testcase(testcase, mastersnapshots, snapshot_resource_map, snapshot_testcases_map)
            newcases.extend(new_cases)
        else:
            rule_str = get_field_value_with_default(testcase, 'rule', '')
            ms_ids = re.findall(r'\{(.*)\}', rule_str)
            # detail_method = get_field_value(testcase, 'detailMethod')
            for ms_id in ms_ids:
                for s_id in mastersnapshots[ms_id]:
                    # new_rule_str = re.sub('{%s}' % ms_id, '{%s}' % s_id, rule_str)
                    # if not detail_method or detail_method == snapshots_details_map[s_id]:
                    toAdd = True
                    if onlysnapshots:
                        if s_id not in onlysnapshotsIds:
                            toAdd = False
                    if toAdd:
                        new_rule_str = rule_str.replace('{%s}' % ms_id, '{%s}' % s_id)
                        new_testcase = {
                            'title': testcase.get('title') if testcase.get('title') else "",
                            'description': testcase.get('description') if testcase.get('description') else "",
                            'rule': new_rule_str,
                            'testId': testcase['masterTestId'],
                            'status' : get_field_value_with_default(testcase, 'status', "enable")
                        }
                        newcases.append(new_testcase)
    return newcases

def _get_rego_testcase(testcase, mastersnapshots, snapshot_resource_map, snapshot_testcases_map):
    onlysnapshots = get_from_currentdata("ONLYSNAPSHOTS")
    onlysnapshotsIds = get_from_currentdata("ONLYSNAPSHOTIDS")
    newcases = []
    ms_ids = testcase.get('masterSnapshotId', [])
    # service = ms_ids[0].split('_')[1]
    for ms_id in ms_ids:
        if ms_id == "ALL":
            for ms_id, s_ids in mastersnapshots.items():
                for s_id in s_ids:
                    snapshot_resource_types = snapshot_resource_map.get(s_id, [])
                    testcase_resource_types = testcase.get('resourceTypes', [])
                    
                    if testcase_resource_types and all(resource_type not in snapshot_resource_types for resource_type in testcase_resource_types):
                        continue

                    toAdd = True
                    if onlysnapshots:
                        if s_id not in onlysnapshotsIds:
                            toAdd = False
                    if toAdd:
                        new_testcase = copy.copy(testcase)
                        new_testcase['snapshotId'] = [s_id]
                        newcases.append(new_testcase)
        else:
            for s_id in mastersnapshots[ms_id]:
                snapshot_resource_types = snapshot_resource_map.get(s_id, [])
                testcase_resource_types = testcase.get('resourceTypes', [])
                
                if testcase_resource_types and all(resource_type not in snapshot_resource_types for resource_type in testcase_resource_types):
                    continue

                toAdd = True
                if onlysnapshots:
                    if s_id not in onlysnapshotsIds:
                        toAdd = False
                if toAdd:
                    new_testcase = copy.copy(testcase)
                    
                    testId = None
                    snapshot_ids = []
                    if new_testcase.get("masterTestId"):
                        testId = new_testcase.get("masterTestId")
                        snapshot_ids = new_testcase.get("masterSnapshotId")
                        if new_testcase.get("masterTestId") in snapshot_testcases_map and \
                            s_id in snapshot_testcases_map[new_testcase.get("masterTestId")]:
                            continue
                    else:
                        continue
                    
                    testcase_snapshot_ids = []
                    if len(snapshot_ids) > 1:
                        count = 0
                        parent_mastersnapshot_id = snapshot_ids[0]
                        child_mastersnapshot_ids = snapshot_ids[1:]
                        if parent_mastersnapshot_id in mastersnapshots and isinstance(mastersnapshots[parent_mastersnapshot_id], list):
                            for parent_snapshot_id in mastersnapshots[parent_mastersnapshot_id]:
                                new_testcase = copy.copy(testcase)
                                temp_testcase_snapshot_ids = [parent_snapshot_id]
                                for master_snapshot_id in child_mastersnapshot_ids:
                                    if master_snapshot_id in mastersnapshots and isinstance(mastersnapshots[master_snapshot_id], list):
                                        temp_testcase_snapshot_ids += mastersnapshots[master_snapshot_id]
                                new_testcase['snapshotId'] = temp_testcase_snapshot_ids
                                testcase_snapshot_ids += temp_testcase_snapshot_ids
                                newcases.append(new_testcase)
                    else:
                        testcase_snapshot_ids = [s_id]
                        new_testcase['snapshotId'] = testcase_snapshot_ids
                        newcases.append(new_testcase)
                        
                    if testId in snapshot_testcases_map:
                        snapshot_testcases_map[testId] += list(set(testcase_snapshot_ids))
                    else:
                        snapshot_testcases_map[testId] = list(set(testcase_snapshot_ids))

                    # if service not in ms_id:
                    #     if s_id.split('_')[1] not in newcases[0]['snapshotId'][-1]:
                    #         [newcase['snapshotId'].append(s_id) for newcase in newcases]
                    #     else:
                    #         new_cases = copy.deepcopy(newcases)
                    #         [new_case['snapshotId'].pop(-1) and new_case['snapshotId'].append(s_id) for new_case in new_cases]
                    #         newcases.extend(new_cases)
                    #     continue
    return newcases

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

def main(container):
    run_container_validation_tests_filesystem(container)


if __name__ == '__main__':
    import sys
    from processor.logging.log_handler import getlogger, init_logger, NONE
    init_logger(NONE)
    if len(sys.argv) > 1:
        main(sys.argv[1])
