"""
   Rest API utils and calls. Fetch access token and make http calls.
"""

import os
from processor.logging.log_handler import getlogger
from processor.helper.file.file_utils import check_filename
from processor.helper.config.rundata_utils import get_from_run_config, add_to_run_config
from processor.helper.httpapi.http_utils import http_post_request
from processor.helper.json.json_utils import get_field_value, load_json
from processor.helper.config.config_utils import get_test_json_dir


ACCESSTOKEN = 'token'
SUBSCRIPTION = 'subscriptionId'
TENANT = 'tenant_id'
RESOURCEGROUP = 'rg'
STORAGE = 'storageid'
CLIENTID = 'clientId'
CLIENTSECRET = 'clientSecret'


logger = getlogger()


def get_web_client_data(snapshot_type, snapshot_source, snapshot_user):
    client_id = None
    client_secret = None
    sub_id = None
    tenant_id = None
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
                                    sub_id = get_field_value(subscription, 'subscription_id')
                                    tenant_id = get_field_value(sub_data, 'tenant_id')
                                    found = True
                                if found:
                                    break
                        if found:
                            break
                    if found:
                        break
    return client_id, client_secret, sub_id, tenant_id


def get_subscription_id_from_runconfig():
    """ Return the subscription Id used for the current run"""
    return get_from_run_config(SUBSCRIPTION)


def get_tenant_id_from_runconfig():
    """ Return the tenant_id"""
    return get_from_run_config(TENANT)


def get_client_id_from_runconfig():
    """ Return the client Id used for the current run"""
    return get_from_run_config(CLIENTID)


def get_resource_group_from_runconfig():
    """ Return the resource group"""
    return get_from_run_config(RESOURCEGROUP)


def get_client_secret():
    """ Return the client secret used for the current run"""
    client_secret = get_from_run_config(CLIENTSECRET)
    if not client_secret:
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
        # subid = get_subscription_id_from_runconfig()
        client_id = get_client_id_from_runconfig()
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
