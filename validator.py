"""
   Common file for running validator functions.
"""
import argparse
import sys
import atexit
import json
import pymongo
from processor.helper.loglib.log_handler import getlogger
from processor.helper.config.rundata_utils import (init_config,
                                                   add_to_run_config,
                                                   delete_run_config)
from processor.helper.json.json_utils import get_vars_json, get_field_value,\
    set_timestamp, set_field_value
from processor.helper.httpapi.restapi_azure import get_access_token
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import get_config
from processor.helper.dbapi.database import get_documents, insert_one_document,\
    create_indexes


COLLECTION = 'resources'
logger = getlogger()


def main(arg_vals=None):
    """Main driver utility for running validator tests."""
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Validator functional tests.")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    cmd_parser.add_argument('template', action='store', nargs='?', default=None, help='Json file')
    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    atexit.register(delete_run_config)
    logger.info(args)
    init_config()
    dbname = get_config('MONGODB', 'dbname')
    create_indexes(COLLECTION, dbname, [('timestamp', pymongo.TEXT)])
    status = populate_snapshot(args.container, args.template)
    if status and args.template:
        run_validator_tests(args.container, args.template)


def run_validator_tests(container, vars_json):
    dbname = get_config('MONGODB', 'dbname')
    logger.info("Run validator tests")
    vars_file, vars_json_data = get_vars_json(container, vars_json)
    if not vars_json_data:
        logger.info("File %s does not exist, exiting!...", vars_file)
        return False
    if 'testSet' not in vars_json_data or not isinstance(vars_json_data['testSet'], list):
        logger.info("No tests in testSet!...")
        return False
    for testset in vars_json_data['testSet']:
        if 'cases' not in testset or not isinstance(testset['cases'], list):
            logger.info("No testcases in testSet!...")
            return False
        for testcase in testset['cases']:
            if 'snapshotId' in testcase and testcase['snapshotId']:
                docs = get_documents(COLLECTION, dbname=dbname,
                                     sort=[('timestamp', pymongo.DESCENDING)],
                                     query={'snapshotId': testcase['snapshotId']},
                                     limit=1)
                logger.info('Results: %s', len(docs))
    return True


def populate_snapshot(container, vars_json):
    """ Get the current snapshot of the resources """
    vars_file, vars_json_data = get_vars_json(container, vars_json)
    if not vars_json_data:
        logger.info("File %s does not exist, exiting!...", vars_file)
        return False
    snapshot_json = vars_json_data['snapshot'] if 'snapshot' in vars_json_data and \
                                      vars_json_data['snapshot'] else None
    if not snapshot_json:
        logger.info("File %s does not contain valid snapshot attribute!...", vars_file)
        return False
    snapshot_file, snapshot_json_data = get_vars_json(container, snapshot_json)
    if not snapshot_json_data:
        logger.info("Snapshot file %s does not exist, exiting!...", snapshot_file)
        return False
    logger.debug(json.dumps(snapshot_json_data, indent=2))
    sub_id = get_field_value(snapshot_json_data, 'subscription.subscriptionId')
    tenant_id = get_field_value(snapshot_json_data, 'subscription.tenantId')
    if 'nodes' not in snapshot_json_data or not snapshot_json_data['nodes']:
        logger.info("No nodes in snapshot to be backed up!...", vars_file)
        return False
    logger.info('Sub:%s, tenant:%s', sub_id, tenant_id)
    add_to_run_config('subscriptionId', sub_id)
    add_to_run_config('tenant_id', tenant_id)
    token = get_access_token()
    logger.debug('TOKEN: %s', token)
    if token:
        dbname = get_config('MONGODB', 'dbname')
        for node in snapshot_json_data['nodes']:
            data = get_node(token, sub_id, node)
            if 'snapshotId' in node and node['snapshotId']:
                set_field_value(data, 'snapshotId', node['snapshotId'])
            set_timestamp(data)
            insert_one_document(data, COLLECTION, dbname)
            logger.debug('Type: %s', type(data))
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
