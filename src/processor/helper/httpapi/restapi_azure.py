"""Rest API utils and calls. Fetch access token and make http calls."""

from builtins import input
import os
import requests
import json
from datetime import datetime
from processor.logging.log_handler import getlogger
from processor.helper.file.file_utils import exists_file
from processor.helper.config.rundata_utils import get_from_currentdata, put_in_currentdata
from processor.helper.httpapi.http_utils import http_post_request, http_get_request,\
    http_put_request, http_delete_request
from processor.helper.json.json_utils import get_field_value, get_field_value_with_default, json_from_file, collectiontypes, STRUCTURE
from processor.helper.config.config_utils import get_test_json_dir, config_value, CUSTOMER
from processor.database.database import DATABASE, DBNAME, sort_field, get_documents


ACCESSTOKEN = 'token'
VAULTACCESSTOKEN = 'vaulttoken'
UAMIVAULTACCESSTOKEN = 'uamivaulttoken'
SUBSCRIPTION = 'subscriptionId'
TENANT = 'tenant_id'
RESOURCEGROUP = 'rg'
STORAGE = 'storageid'
CLIENTID = 'clientId'
CLIENTSECRET = 'clientSecret'
VAULTCLIENTSECRET = 'vaultClientSecret'
VAULTOKENEXPIRY = 'vaultTokenExpiry'
UAMIVAULTOKENEXPIRY = 'uamivaultTokenExpiry'
JSONSOURCE = 'jsonsource'


logger = getlogger()

def get_azure_data(snapshot_source):
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of Snapshot Documents: %s', len(docs))
        if docs and len(docs):
            sub_data = docs[0]['json']
    else:
        json_test_dir = get_test_json_dir()
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        azure_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('\tCONNECTOR: %s', azure_source)
        if exists_file(azure_source):
            sub_data = json_from_file(azure_source)
    return sub_data


def get_web_client_data(snapshot_type, snapshot_source, snapshot_user):
    client_id = None
    client_secret = None
    sub_id = None
    sub_name = None
    tenant_id = None
    found = False
    if snapshot_type == 'azure':
        sub_data = get_azure_data(snapshot_source)
        if sub_data:
            accounts = get_field_value_with_default(sub_data, 'accounts', [])
            for account in accounts:
                subscriptions = get_field_value_with_default(account, 'subscription', [])
                for subscription in subscriptions:
                    users = get_field_value_with_default(subscription, 'users', [])
                    if users:
                        for user in users:
                            name = get_field_value(user, 'name')
                            if name and name == snapshot_user:
                                client_id = get_field_value(user, 'client_id')
                                client_secret = get_field_value(user, 'client_secret')
                                sub_id = get_field_value(subscription, 'subscription_id')
                                sub_name = get_field_value(subscription, 'subscription_name')
                                tenant_id = get_field_value(sub_data, 'tenant_id')
                                found = True
                            if found:
                                break
                    if found:
                        break
                if found:
                    break
    if not found:
        logger.error("No connector data found, check the connector configuration and snapshot configuration files.")
    return client_id, client_secret, sub_name, sub_id, tenant_id


def get_subscription_id():
    """ Return the subscription Id used for the current run"""
    return get_from_currentdata(SUBSCRIPTION)


def get_tenant_id():
    """ Return the tenant_id"""
    return get_from_currentdata(TENANT)


def get_client_id():
    """ Return the client Id used for the current run"""
    return get_from_currentdata(CLIENTID)


def get_resource_group():
    """ Return the resource group"""
    return get_from_currentdata(RESOURCEGROUP)


def json_source():
    """Return the json source, file system or mongo """
    val = get_from_currentdata(JSONSOURCE)
    return val if val else False


def get_client_secret1(key='CLIENTKEY'):
    """ Return the client secret used for the current run"""
    client_secret = get_from_currentdata(CLIENTSECRET)
    if not client_secret:
        client_secret = os.getenv(key, None)
    # if not client_secret:
    #     client_secret = input('Enter the client secret for the app: ')
    return client_secret


def get_client_secret(key='CLIENTKEY', client_id=None):
    """ Return the client secret used for the current run"""
    # logger.info('before get_from_currentdata CLIENTSECRET invoked! ')
    client_secret = get_from_currentdata(CLIENTSECRET)
    # logger.info('after get_from_currentdata CLIENTSECRET invoked! %s', client_secret)
    if not client_secret:
        if 'UAMI' in os.environ and os.environ['UAMI'] == 'true':
            # client_secret = get_vault_data(client_id)
            vaulttoken = get_uami_vault_access_token()
            keyvault = config_value('VAULT', 'keyvault')
            # secret_key = config_value('VAULT', 'secret_key')
            logger.info('Keyvault: %s, key:%s', keyvault, client_id)
            secret_data = get_keyvault_secret(keyvault, client_id, vaulttoken)
            if secret_data and 'value' in secret_data:
                client_secret = secret_data['value']
        else:
            if not client_secret:
                client_secret = os.getenv(key, None)
            if not client_secret and not get_from_currentdata(CUSTOMER):
                client_secret = input('Enter the client secret for the app: ')
    return client_secret

def get_access_token():
    """
    Get the access token if stored in rundata, otherwise get the token from
    management.azure.com portal for the webapp.
    """
    token = get_from_currentdata(ACCESSTOKEN)
    if not token:
        tenant_id = get_tenant_id()
        client_id = get_client_id()
        if client_id:
            # client_secret = get_client_secret()
            client_secret = get_client_secret(key='CLIENTKEY',client_id=client_id)
        else:
            logger.info('client Id required for REST API access!')
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
            # logger.info('Get Azure token REST API invoked!')
            status, data = http_post_request(url, data, headers=hdrs, json_type=True, name='\tAZURE TOKEN')
            if status and isinstance(status, int) and status == 200:
                token = data['access_token']
                put_in_currentdata(ACCESSTOKEN, token)
            else:
                put_in_currentdata('errors', data)
                logger.info("Get Azure token returned invalid status: %s", status)
    return token


def get_vault_client_secret():
    """ Return the vault client secret used."""
    vault_client_secret = get_from_currentdata(VAULTCLIENTSECRET)
    if not vault_client_secret:
        vault_client_secret = os.getenv('VAULTCLIENTKEY', None)
    if not vault_client_secret:
        vault_client_secret = input('Enter the vault client secret: ')
    return vault_client_secret


def get_vault_access_token(tenant_id, vault_client_id, client_secret=None):
    """
    Get the vault access token to get all the other passwords/secrets.
    """
    vaulttoken = get_from_currentdata(VAULTACCESSTOKEN)
    expiry_time = get_from_currentdata(VAULTOKENEXPIRY)
    is_token_valid = isinstance(expiry_time, str) and \
        datetime.now() < datetime.fromtimestamp(float(expiry_time))
    if (not vaulttoken) or (not is_token_valid):
        vault_client_secret = client_secret if client_secret else get_vault_client_secret()
        data = {
            'grant_type': 'client_credentials',
            'client_id': vault_client_id,
            'client_secret': vault_client_secret,
            'resource': 'https://vault.azure.net'
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
                vaulttoken = data['access_token']
                expiry_time = data['expires_on']
                put_in_currentdata(VAULTACCESSTOKEN, vaulttoken)
                put_in_currentdata(VAULTOKENEXPIRY, expiry_time)
            else:
                put_in_currentdata('errors', data)
                logger.info("Get Azure token returned invalid status: %s", status)
    return vaulttoken

def get_uami_vault_access_token():
    """
    Get the vault access token to get all the other passwords/secrets.
    """
    hdrs = {
       "Metadata": "true",
       "Cache-Control": "no-cache"
    }
    vaulttoken = get_from_currentdata(UAMIVAULTACCESSTOKEN)
    # print(vaulttoken)
    expiry_time = get_from_currentdata(UAMIVAULTOKENEXPIRY)
    is_token_valid = isinstance(expiry_time, str) and \
        datetime.now() < datetime.fromtimestamp(float(expiry_time))
    if (not vaulttoken) or (not is_token_valid):
        url = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net'
        # logger.info('Get Azure UAMI token REST API invoked!')
        print('Get Azure UAMI token REST API invoked!')
        status, data = http_get_request(url, headers=hdrs)
        print(data)
        if status and isinstance(status, int) and status == 200:
            vaulttoken = data['access_token']
            expiry_time = data['expires_on']
            put_in_currentdata(UAMIVAULTACCESSTOKEN, vaulttoken)
            put_in_currentdata(UAMIVAULTOKENEXPIRY, expiry_time)
        else:
            put_in_currentdata('errors', data)
            # logger.info("Get Azure token returned invalid status: %s", status)
            print("Get Azure token returned invalid status: %s" % status)
    return vaulttoken


def get_keyvault_secret(keyvault, secret_key, vaulttoken):
    hdrs = {
        'Authorization': 'Bearer %s' % vaulttoken
    }
    logger.info('Get Id REST API invoked!')
    urlstr = 'https://%s.vault.azure.net/secrets/%s?api-version=7.0'
    url = urlstr % (keyvault, secret_key)
    status, data = http_get_request(url, hdrs)
    logger.debug('Get Id status: %s', status)

    if status and isinstance(status, int) and status == 200:
        logger.debug('Data: %s', data)
    else:
        put_in_currentdata('errors', data)
        logger.info("Get Id returned invalid status: %s", status)
    return data


def get_all_secrets(keyvault, vaulttoken):
    hdrs = {
        'Authorization': 'Bearer %s' % vaulttoken
    }
    logger.info('Get Id REST API invoked!')
    urlstr = 'https://%s.vault.azure.net/secrets?api-version=7.0'
    url = urlstr % (keyvault)
    keys_response = []
    keys = []
    while url != None:
        status, data = http_get_request(url, hdrs)
        if status and isinstance(status, int) and status == 200:
            logger.debug('Data: %s', data)
            values = data.get("value", [])
            url = data.get("nextLink",None)
            keys_response.extend(values)
        else:
            put_in_currentdata('errors', data)
            url = None
            logger.info("Get Id returned invalid status: %s", status)
    for each_key in keys_response:
        key_url = each_key.get("id",None)
        if key_url:
            secret_key = key_url.split("secrets/",1)[1].split("/")[0]
            keys.append(secret_key)
    return keys


def set_keyvault_secret(keyvault, vaulttoken, secret_key, value):

    hdrs = {
        'Authorization': 'Bearer %s' % vaulttoken,
        'Content-Type': 'application/json'
    }
    logger.info('Put Id REST API invoked!')
    urlstr = 'https://%s.vault.azure.net/secrets/%s?api-version=7.0'
    url = urlstr % (keyvault, secret_key)
    request_data = {
        "value" : value
    }
    status, data = http_put_request(url, request_data, headers=hdrs, json_type=True)
    logger.info('Set Id status: %s', status)
    if status and isinstance(status, int) and status == 200:
        logger.debug('Data: %s', data)
        return True
    else:
        put_in_currentdata('errors', data)
        logger.info("Set Id returned invalid status: %s", status)
        return False

def set_keyvault_secret_with_response(keyvault, vaulttoken, secret_key, value):
    hdrs = {
        'Authorization': 'Bearer %s' % vaulttoken,
        'Content-Type': 'application/json'
    }
    urlstr = 'https://%s.vault.azure.net/secrets/%s?api-version=7.0'
    url = urlstr % (keyvault, secret_key)
    params = {
        "value" : value
    }
    params = json.dumps(params)
    response = requests.put(url, data=params, headers=hdrs)
    return response.status_code, response.json()

def delete_keyvault_secret(keyvault, secret_key, vaulttoken):
    hdrs = {
        'Authorization': 'Bearer %s' % vaulttoken
    }
    success = False
    logger.info('Delete Id REST API invoked!')
    urlstr = 'https://%s.vault.azure.net/secrets/%s?api-version=7.0'
    url = urlstr % (keyvault, secret_key)
    status, data = http_delete_request(url, headers=hdrs)
    logger.info('Delete Id status: %s', status)
    if status and isinstance(status, int) and status == 200:
        logger.debug('Data: %s', data)
        success = True
    else:
        put_in_currentdata('errors', data)
        logger.info("Get Id returned invalid status: %s", status)
    return success
