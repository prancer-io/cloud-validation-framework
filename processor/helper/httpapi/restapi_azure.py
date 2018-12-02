"""
   Rest API utils and calls. Fetch access token and make http calls.
"""
import argparse
import atexit
import os
import subprocess
from processor.helper.loglib.log_handler import getlogger
from processor.helper.config.rundata_utils import get_from_run_config,\
    add_to_run_config, init_config, delete_run_config
from processor.helper.httpapi.http_utils import http_post_request, http_get_request
from processor.helper.json.json_utils import get_vars_json, get_field_value, load_json
from processor.helper.config.config_utils import get_subscription_file


ACCESSTOKEN = 'token'
SUBSCRIPTION = 'subscriptionId'
TENANT = 'tenant_id'
RESOURCEGROUP = 'rg'
STORAGE = 'storageid'


logger = getlogger()


def get_web_client_data(subid):
    """Get the client details for the web app with this subscription."""
    client_id = None
    if not subid:
        return client_id
    subscription_file = get_subscription_file(parentdir=True)
    logger.info(subscription_file)
    data = load_json(subscription_file)
    if data and 'accounts' in data:
        for account_data in data['accounts']:
            if 'subscription' in account_data:
                for subscription in account_data['subscription']:
                    if 'subscription_id' in subscription and \
                            subid == subscription['subscription_id']:
                        if 'client_id' in subscription:
                            client_id = subscription['client_id']
                        if client_id:
                            return client_id
    else:
        logger.info('Check the subscription file, should contain client Id for the subscription!')
    return client_id


def get_subscription_id_from_runconfig():
    """ Return the subscription Id used for the current run"""
    return get_from_run_config(SUBSCRIPTION)


def get_tenant_id_from_runconfig():
    """ Return the tenant_id"""
    return get_from_run_config(TENANT)


def get_resource_group_from_runconfig():
    """ Return the resource group"""
    return get_from_run_config(RESOURCEGROUP)

def get_client_secret():
    client_secret = os.getenv('CLIENTKEY', None)
    if not client_secret:
        client_secret = input('Enter the client secret for the app: ')
    return client_secret


def get_access_token():
    """
    Get the access token if stored in rundata, otherwise get the token from
    management.azure.com portal for the webapp.
    """
    token = get_from_run_config(ACCESSTOKEN)
    if not token:
        tenant_id = get_tenant_id_from_runconfig()
        subid = get_subscription_id_from_runconfig()
        client_id = get_web_client_data(subid)
        if client_id:
            client_secret = get_client_secret()
        else:
            logger.info('Subscription file should contain client Id for REST API access!')
            return None
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': 'https://management.azure.com'
        }
        hdrs = {
            'Cache-Control': "no-cache",
            "Accept": "application/json"
        }
        if tenant_id:
            url = 'https://login.microsoftonline.com/%s/oauth2/token' % tenant_id
            logger.info('Get Azure token REST API invoked!')
            status, data = http_post_request(url, data, headers=hdrs)
            if status and isinstance(status, int) and status == 200:
                token = data['access_token']
                add_to_run_config(ACCESSTOKEN, token)
            else:
                add_to_run_config('errors', data)
                logger.info("Get Azure token returned invalid status: %s", status)
    return token


def account_show(query):
    """az account show : Get the details of a subscription."""
    cmdargs = ['az', 'account', 'show']
    if query:
        cmdargs.extend(['--query', query])
    return ' '.join(cmdargs)


def run_subprocess_cmd(cmd, ignoreerror=False):
    """ Run a sub-process command"""
    result = '[]'
    errresult = None
    if cmd:
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)
        myprocess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE)
        out, err = myprocess.communicate()
        result = out.rstrip()
        errresult = err.rstrip() if err else None
        if isinstance(result, bytes):
            result = result.decode()
        if errresult and isinstance(errresult, bytes):
            errresult = errresult.decode()
            if not ignoreerror and errresult and len(errresult) > 2: # Load json and check
                add_to_run_config('errors', errresult)
        if not ignoreerror:
            logger.info("CMD: '%s', OUTPUT: \033[92m %s\033[00m, ERROR:\033[91m %s\033[00m",
                        cmd, result, errresult)
    return errresult, result


def get_tenant_id():
    # Get the Tenant ID
    tenantId = get_from_run_config(TENANT)
    if tenantId:
        return tenantId
    cmd = account_show("tenantId")
    error, tenantId = run_subprocess_cmd(cmd)
    if error:
        logger.error("Error - Fetching the Tenant ID from the Subscription - %s", error)
        return None
    tenantId = tenantId.strip('\"')
    if tenantId:
        add_to_run_config(TENANT, tenantId)
    return tenantId


def main(arg_vals=None):
    """Main driver for running the utility."""
    cmd_parser = argparse.ArgumentParser("Test Azure REST API access.")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    cmd_parser.add_argument('template', action='store', nargs='?', default=None, help='Json file')
    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    init_config()
    atexit.register(delete_run_config)
    logger.info(args)

    # Get the vars json file from the template
    vars_file, vars_json_data = get_vars_json(args.container, args.template)
    if not vars_json_data:
        logger.info("File %s does not exist, exiting!...", vars_file)
        return False

    # Get the subscription Id and name from the vars.json file.
    subid = get_field_value(vars_json_data,
                            'parameters.configurationSettings.value.name.subscriptionId')
    if not subid:
        logger.info("No subcription Id: %s", subid)
        return False
    add_to_run_config(SUBSCRIPTION, subid)
    logger.info("Subcription Id: %s", subid)

    cmd = account_show("tenantId")
    error, tenantId = run_subprocess_cmd(cmd)
    if error:
        logger.error("Error - Fetching the Tenant ID from the Subscription - %s", error)
        return False
    tenantId = tenantId.strip('\"')
    add_to_run_config(TENANT, tenantId)
    get_access_token()


if __name__ == "__main__":
    main()
