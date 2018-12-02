"""
   Common file for running validator functions.
"""

import argparse
import sys
import atexit
import json
from processor.helper.loglib.log_handler import getlogger
from processor.helper.config.rundata_utils import (init_config,
                                                   add_to_run_config,
                                                   delete_run_config)
from processor.helper.json.json_utils import get_vars_json, get_field_value,\
    set_timestamp, set_field_value
from processor.helper.httpapi.restapi_azure import get_access_token
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.config.config_utils import get_config
from processor.helper.dbapi.database import mongodb, insert_one_document



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
    status = populate_snapshot(args.container, None)
    if status and args.template:
        run_validator_tests(args.container, args.template)


def run_validator_tests(container, var_file):
    logger.info("Run validator tests")


def populate_snapshot(container, var_file=None):
    """ Get the current snapshot of the resources """
    vars_json = var_file if var_file else 'snapshot.json'
    vars_file, vars_json_data = get_vars_json(container, vars_json)
    if not vars_json_data:
        logger.info("File %s does not exist, exiting!...", vars_file)
        return False
    logger.info(json.dumps(vars_json_data, indent=2))
    sub_id = get_field_value(vars_json_data, 'subscription.subscriptionId')
    tenant_id = get_field_value(vars_json_data, 'subscription.tenantId')
    logger.info('Sub:%s, tenant:%s', sub_id, tenant_id)
    add_to_run_config('subscriptionId', sub_id)
    add_to_run_config('tenant_id', tenant_id)
    token = get_access_token()
    logger.info('TOKEN: %s', token)
    if token:
        dbname = get_config('MONGODB', 'dbname')
        for node in vars_json_data['nodes']:
            data = get_node(token, sub_id, node)
            if 'snapshotId' in node and node['snapshotId']:
                set_field_value(data, 'snapshotId', node['snapshotId'])
            set_timestamp(data)
            insert_one_document(data, 'resources', dbname)
            logger.info('Type: %s', type(data))
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
