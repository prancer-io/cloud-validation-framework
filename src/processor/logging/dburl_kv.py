"""Helper functions to get data  from KV."""
import json
from urllib.error import HTTPError, URLError
import os
import copy
from urllib import request, parse
from processor.helper.config.config_utils import DBURL, config_value


def json_from_string(json_str):
    """Get json from the string."""
    try:
        jsondata = json.loads(json_str)
        return jsondata
    except:
        pass
    return None


def urlopen_request(urlreq, method):
    """Common utility to trigger the http request."""
    try:
        urlresp = request.urlopen(urlreq)
        respdata = urlresp.read()
        st_code = urlresp.status
        if isinstance(respdata, bytes):
            respdata = respdata.decode()
        data = json_from_string(respdata)
    except HTTPError as ex:
        st_code = ex.code
        data = ex.msg if method == "POST" else None
    except URLError as ex:
        st_code = 500
        data = str(ex)
    return st_code, data


def get_request_headers(headers=None):
    """Add json and no cache headers to the existing headers if passed."""
    hdrs = {
        "Cache-Control": "no-cache",
        "Accept": "application/json"
    }
    req_headers = copy.copy(headers) if headers else {}
    req_headers.update(hdrs)
    return req_headers


def http_get_request(url, headers=None, name='GET'):
    """Get method sends and accepts JSON format."""
    if not url:
        return None, None
    urlreq = request.Request(url, headers=get_request_headers(headers), method=name)
    return urlopen_request(urlreq, name)


def http_post_request(url, mapdata, headers=None, json_type=False, name='POST'):
    """Post method sends and accepts JSON format"""
    if not url:
        return None, None
    if json_type:
        postdata = str.encode(json.dumps(mapdata))
    else:
        postdata = parse.urlencode(mapdata).encode()
    urlreq = request.Request(url, data=postdata, headers=get_request_headers(headers),
                             method='POST')
    return urlopen_request(urlreq, name)


def get_uami_vault_access_token():
    """
    Get the vault access token to get all the other passwords/secrets.
    """
    hdrs = {
       "Metadata": "true",
       "Cache-Control": "no-cache"
    }
    url = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net'
    # print('Get Azure UAMI token REST API invoked!')
    status, data = http_get_request(url, headers=hdrs)
    # print(data)
    if status and isinstance(status, int) and status == 200:
        vaulttoken = data['access_token']
    else:
        pass
    return vaulttoken


def get_vault_access_token(tenant_id, vault_client_id, client_secret=None):
    """ Get the vault access token to get all the other passwords/secrets.  """
    vaulttoken = None
    if client_secret:
        vault_client_secret = client_secret if client_secret else None
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
            status, data = http_post_request(url, data, headers=hdrs)
            if status and isinstance(status, int) and status == 200:
                vaulttoken = data['access_token']
    return vaulttoken


def get_keyvault_secret(keyvault, secret_key, vaulttoken):
    hdrs = {
        'Authorization': 'Bearer %s' % vaulttoken
    }
    urlstr = 'https://%s.vault.azure.net/secrets/%s?api-version=7.0'
    url = urlstr % (keyvault, secret_key)
    status, data = http_get_request(url, hdrs)
    return data


def get_azure_vault_data(secret_key=None):
    """Fetches the bearer token for Azure Vault API calls"""
    val = None
    vaulttoken = _get_vault_token()
    if vaulttoken and secret_key:
        keyvault = config_value('VAULT', 'keyvault')
        secret_data = get_keyvault_secret(keyvault, secret_key, vaulttoken)
        if secret_data and 'value' in secret_data:
            val = secret_data['value']
    return val

def _get_vault_token():
    """Fetches the bearer token for Azure Vault API calls"""
    if 'UAMI' in os.environ and os.environ['UAMI'] == 'true':
        vaulttoken = get_uami_vault_access_token()
    else:
        client_id = config_value('VAULT', 'client_id')
        client_secret = get_config_value('VAULT', 'client_secret', 'CLIENTKEY')
        tenant_id = config_value('VAULT', 'tenant_id')
        vaulttoken = get_vault_access_token(tenant_id, client_id, client_secret)
    return vaulttoken

def get_config_value(section, key, env_var, prompt_str=None):
    """ Return the client secret used for the current run"""
    client_secret = config_value(section, key)
    if not client_secret and env_var:
        client_secret = os.getenv(env_var, None)
    if not client_secret and prompt_str:
        key_str = '%s_%s' % (section, key)
        if not client_secret:
            client_secret = input(prompt_str)
            if client_secret:
                pass
                # logger.info('Key:%s, sec:%s', key_str, client_secret)
    return client_secret

def get_dburl():
    unittest = os.getenv('UNITTEST', "false")
    if unittest == 'true':
        return None
    dburl = os.getenv('DBURL', None)
    if not dburl:
        dburl = get_azure_vault_data(DBURL)
        if dburl:
            os.environ[DBURL] = dburl
    return dburl


