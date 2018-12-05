"""
   Common file for running validator functions.
"""
import argparse
import sys
import atexit
import json
import pymongo
from processor.helper.file.file_utils import check_filename
from processor.helper.loglib.log_handler import getlogger
from processor.helper.config.rundata_utils import (init_config,
                                                   add_to_run_config,
                                                   delete_from_run_config,
                                                   delete_run_config)
from processor.helper.comparison.interpreter import Comparator
from processor.helper.json.json_utils import get_field_value,\
    set_timestamp, set_field_value, get_json_files, load_json,\
    dump_output_results
from processor.helper.httpapi.restapi_azure import get_access_token
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import get_config, get_test_json_dir
from processor.helper.dbapi.database import get_documents, insert_one_document,\
    create_indexes

SNAPSHOT = 'snapshot'
JSONTEST = 'test'
COLLECTION = 'resources'
logger = getlogger()


def main(arg_vals=None):
    """Main driver utility for running validator tests."""
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Validator functional tests.")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    atexit.register(delete_run_config)
    logger.info(args)
    init_config()
    dbname = get_config('MONGODB', 'dbname')
    create_indexes(COLLECTION, dbname, [('timestamp', pymongo.TEXT)])
    status = populate_snapshot(args.container)
    if status:
        run_validator_tests(args.container)


def run_validator_tests(container):
    dbname = get_config('MONGODB', 'dbname')
    logger.info("Starting validator tests")
    json_dir = '%s/%s' % (get_test_json_dir(), container)
    logger.info(json_dir)
    test_files = get_json_files(json_dir, JSONTEST)
    logger.info('\n'.join(test_files))
    for test_file in test_files:
        logger.info("*" * 50)
        logger.info("validator tests: %s", test_file)
        test_json_data = load_json(test_file)
        if not test_json_data:
            logger.info("Test file %s looks to be empty, next!...", test_file)
            continue
        logger.debug(json.dumps(test_json_data, indent=2))
        testsets = get_field_value(test_json_data, 'testSet')
        if not testsets or not isinstance(testsets, list):
            logger.info("Test file %s does not contain testset, next!...", test_file)
            continue
        resultset = []
        for testset in testsets:
            version = get_field_value(testset, 'version')
            if 'cases' not in testset or not isinstance(testset['cases'], list):
                logger.info("No testcases in testSet!...")
                continue
            for testcase in testset['cases']:
                if 'snapshotId' in testcase and testcase['snapshotId']:
                    docs = get_documents(COLLECTION, dbname=dbname,
                                         sort=[('timestamp', pymongo.DESCENDING)],
                                         query={'snapshotId': testcase['snapshotId']},
                                         limit=1)
                    logger.info('Number of Snapshot Documents: %s', len(docs))
                    if docs and len(docs):
                        comparator = Comparator(version, docs[0], testcase['attribute'],
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
                resultset.append(result_val)
        dump_output_results(resultset, test_file, container)


    return True

# # operators
# # left operator - 'attribute' field of the test case
# # operators - eq, neq, lt, le, gt, ge, not, exist,
# # right operator
#
# # Grammar: Left operator has to be present, i.e 'attribute' field  in the testcase should be present
# #          operator - has to be present and one of the above.
# #          Right operator optional and if present will used in python comparison statements.
# #          Different formats will be evolved as required for the framework.
# # Sample tests:
# # Test for existence of an attribute
# {
#     "snapshotId": "1",
#     "attribute":  "location",
#     "comparison": "exist"
# }
# # Test for non-existence of an attribute
# {
#     "snapshotId": "1",
#     "attribute": "location.name",
#     "comparison":"not exist"
# }
# # Test for numerical less than of an attribute,
# # for string less than quote it in single quotes.
# # "lt 'Red'"
# {
#     "snapshotId": "1",
#     "attribute": "location",
#     "comparison": "lt 10"
# }
# # Test if the attribute is an array and its length is  gt
# {
#     "snapshotId": "1",
#     "attribute": "location",
#     "comparison":"gt len(10)"
# }
# # Test equality and inequality check for ascii and numeric values
# {
#     "snapshotId": "1",
#     "attribute": "location",
#     "comparison": "eq 'eastus2'",
#     "comparison": "neq 'eastus2'",
#     "comparison": "eq 2",
#     "comparison": "neq 2"
# }
# # Test to compare with other snapshot
# {
#     "snapshotId": "1",
#     "attribute": "location",
#     "comparison":"eq '{2}.location'"
# }

def get_web_client_data(snapshot_type, snapshot_source, snapshot_user):
    client_id = None
    client_secret = None
    found = False
    json_test_dir = get_test_json_dir()
    if snapshot_type == 'azure':
        azure_source = '%s/../%s' % (json_test_dir, snapshot_source)
        logger.info('Azure source: %s', azure_source)
        if check_filename(azure_source):
            sub_data = load_json(azure_source)
            if sub_data:
                accounts = get_field_value(sub_data, 'accounts')
                for account in accounts:
                    subscriptions = get_field_value(account, 'subscription')
                    for subscription in subscriptions:
                        users = get_field_value(subscription, 'users')
                        if users:
                            for user in users:
                                name = get_field_value(user, 'name')
                                if name and name == snapshot_user:
                                    client_id = get_field_value(user, 'client_id')
                                    client_secret = get_field_value(user, 'client_secret')
                                    found = True
                                if found:
                                    break
                        if found:
                            break
                    if found:
                        break
    return client_id, client_secret


def populate_snapshot(container):
    """ Get the current snapshot of the resources """
    dbname = get_config('MONGODB', 'dbname')
    json_test_dir = get_test_json_dir()
    container_dir = '%s/%s' % (json_test_dir, container)
    logger.info(container_dir)
    snapshot_files = get_json_files(container_dir, SNAPSHOT)
    if not snapshot_files:
        logger.info("No Snapshot files in %s, exiting!...",  container_dir)
        return False
    logger.info('\n'.join(snapshot_files))
    for snapshot_file in snapshot_files:
        snapshot_json_data = load_json(snapshot_file)
        if not snapshot_json_data:
            logger.info("Snapshot file %s looks to be empty, next!...", snapshot_file)
            continue
        logger.debug(json.dumps(snapshot_json_data, indent=2))
        snapshots = get_field_value(snapshot_json_data, 'snapshots')
        if not snapshots:
            logger.info("Snapshot file %s does not contain snapshots, next!...", snapshot_file)
            continue
        for snapshot in snapshots:
            if 'nodes' not in snapshot or not snapshot['nodes']:
                logger.info("No nodes in snapshot to be backed up!...", snapshot_file)
                continue
            snapshot_type = get_field_value(snapshot, 'type')
            snapshot_source = get_field_value(snapshot, 'source')
            snapshot_user = get_field_value(snapshot, 'testUser')
            client_id, client_secret = get_web_client_data(snapshot_type, snapshot_source,
                                                           snapshot_user)
            if not client_id:
                logger.info("No client_id in the snapshot to access azure resuource!...")
                continue
            sub_id = get_field_value(snapshot, 'subscriptionId')
            tenant_id = get_field_value(snapshot, 'tenantId')
            logger.info('Sub:%s, tenant:%s, client: %s', sub_id, tenant_id, client_id)
            add_to_run_config('clientId', client_id)
            add_to_run_config('clientSecret', client_secret)
            add_to_run_config('subscriptionId', sub_id)
            add_to_run_config('tenant_id', tenant_id)
            token = get_access_token()
            logger.debug('TOKEN: %s', token)
            if token:
                for node in snapshot['nodes']:
                    data = get_node(token, sub_id, node)
                    if 'snapshotId' in node and node['snapshotId']:
                        set_field_value(data, 'snapshotId', node['snapshotId'])
                    set_timestamp(data)
                    insert_one_document(data, COLLECTION, dbname)
                    logger.debug('Type: %s', type(data))
                delete_from_run_config('clientId')
                delete_from_run_config('client_secret')
                delete_from_run_config('subscriptionId')
                delete_from_run_config('tenant_id')
    return True


def get_node(token, sub_id, node):
    """ Fetch node from azure portal using rest API."""
    version = None
    if node and 'type' in node:
        if node['type'] == "Microsoft.Compute/availabilitySets":
            version = '2018-06-01'
        elif node['type'] == "Microsoft.Network/virtualNetworks":
            version = '2018-07-01'
    if sub_id and token and node and node['path'] and version:
        hdrs = {
            'Authorization': 'Bearer %s' % token
        }
        url = 'https://management.azure.com/subscriptions/%s%s?api-version=%s' \
              % (sub_id, node['path'], version)
        logger.info('Get Id REST API invoked!')
        status, data = http_get_request(url, hdrs)
        logger.info('Get Id status: %s', status)
        # logger.info('Get data: %s', data)
        if status and isinstance(status, int) and status == 200:
            return data
        else:
            add_to_run_config('errors', data)
            logger.info("Get Id returned invalid status: %s", status)
    else:
        logger.info('Get requires valid subscription, token and path.!')
        return None


if __name__ == "__main__":
    main()
