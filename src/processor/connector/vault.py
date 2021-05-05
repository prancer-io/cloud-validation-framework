"""
   Common file for vault functionality.
"""
from builtins import input
import os
from subprocess import Popen, PIPE
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import get_from_currentdata,\
    put_in_currentdata, add_to_exclude_list
from processor.helper.config.config_utils import config_value
from processor.helper.httpapi.restapi_azure import get_vault_access_token, get_uami_vault_access_token,\
    get_keyvault_secret, set_keyvault_secret, get_all_secrets, delete_keyvault_secret, set_keyvault_secret_with_response

logger = getlogger()


def get_vault_data(secret_key=None):
    """Read vault data from config"""
    vaulttype = config_value('VAULT', 'type')
    val = None
    if vaulttype:
        if vaulttype == 'azure':
            val = get_azure_vault_data(secret_key)
        elif vaulttype == 'cyberark':
            val = get_cyberark_data(secret_key)
    return val


def set_vault_data(key_name=None, value=None):
    """Update vault data"""
    vaulttype = config_value('VAULT', 'type')
    val = None
    if vaulttype:
        if vaulttype == 'azure':
            val = set_azure_vault_data(key_name, value)
    return val

def set_vault_data_with_response(key_name=None, value=None):
    """Update vault data"""
    vaulttype = config_value('VAULT', 'type')
    status, response = None, None
    if vaulttype:
        if vaulttype == 'azure':
            status, response = set_azure_vault_data_with_response(key_name, value)
    return status, response

def delete_vault_data(secret_key=None):
    """Delete vault data from config"""
    vaulttype = config_value('VAULT', 'type')
    val = None
    if vaulttype:
        if vaulttype == 'azure':
            val = delete_azure_vault_data(secret_key)
    return val


def get_all_vault_secrets():
    """Read all vault secrets"""
    vaulttype = config_value('VAULT', 'type')
    val = None
    if vaulttype:
        if vaulttype == 'azure':
            val = get_all_azure_secrets()
    return val


def get_all_azure_secrets():
    val = None
    vaulttoken = _get_vault_token()
    # logger.debug('Vault Token: %s', vaulttoken)
    if vaulttoken:
        keyvault = config_value('VAULT', 'keyvault')
        logger.info('Keyvault: %s', keyvault)
        data = get_all_secrets(keyvault, vaulttoken)
        if data:
            return data
    return [] 


def get_config_value(section, key, env_var, prompt_str=None):
    """ Return the client secret used for the current run"""
    client_secret = config_value(section, key)
    if not client_secret and env_var:
        client_secret = os.getenv(env_var, None)
    if not client_secret and prompt_str:
        key_str = '%s_%s' % (section, key)
        client_secret = get_from_currentdata(key_str)
        if not client_secret:
            client_secret = input(prompt_str)
            if client_secret:
                put_in_currentdata(key_str, client_secret)
                logger.info('Key:%s, sec:%s', key_str, '*' * len(client_secret))
                add_to_exclude_list(key_str)
    return client_secret


def _get_vault_token():
    """Fetches the bearer token for Azure Vault API calls"""
    if 'UAMI' in os.environ and os.environ['UAMI'] == 'true':
        vaulttoken = get_uami_vault_access_token()
    else:
        client_id = config_value('VAULT', 'client_id')
        client_secret = get_config_value('VAULT', 'client_secret', 'CLIENTKEY',
                                         'Enter the client secret to access keyvault: ')
        # client_secret = config_value('VAULT', 'client_secret')
        tenant_id = config_value('VAULT', 'tenant_id')
        # logger.info('Id: %s, secret: %s, tenant: %s', client_id, client_secret, tenant_id)
        vaulttoken = get_vault_access_token(tenant_id, client_id, client_secret)
    return vaulttoken


def get_azure_vault_data(secret_key=None):
    """Fetches the bearer token for Azure Vault API calls"""
    val = None
    vaulttoken = _get_vault_token()
    # logger.debug('Vault Token: %s', vaulttoken)
    if vaulttoken and secret_key:
        keyvault = config_value('VAULT', 'keyvault')
        # secret_key = config_value('VAULT', 'secret_key')
        logger.info('Keyvault: %s, key:%s', keyvault, '*' * len(secret_key))
        secret_data = get_keyvault_secret(keyvault, secret_key, vaulttoken)
        if secret_data and 'value' in secret_data:
            val = secret_data['value']
    return val


def set_azure_vault_data(secret_key=None, value=None):
    """Fetches the bearer token for Azure Vault API calls"""
    val = None
    vaulttoken = _get_vault_token()
    logger.debug('Vault Token: %s', vaulttoken)
    if vaulttoken and secret_key and value:
        keyvault = config_value('VAULT', 'keyvault')
        # secret_key = config_value('VAULT', 'secret_key')
        logger.info('Keyvault: %s, key:%s', keyvault, '*' * len(secret_key))
        sucess = set_keyvault_secret(keyvault, vaulttoken, secret_key, value)
        if sucess:
            return True
    return False

def set_azure_vault_data_with_response(secret_key=None, value=None):
    """Fetches the bearer token for Azure Vault API calls"""
    status, data = None, None
    vaulttoken = _get_vault_token()
    logger.debug('Vault Token: %s', vaulttoken)
    if vaulttoken and secret_key and value:
        keyvault = config_value('VAULT', 'keyvault')
        logger.info('Keyvault: %s, key:%s', keyvault, '*' * len(secret_key))
        status, data = set_keyvault_secret_with_response(keyvault, vaulttoken, secret_key, value)
    return status, data

def delete_azure_vault_data(secret_key=None):
    """"Delete a key from vault"""
    success = None
    vaulttoken = _get_vault_token()
    logger.debug('Vault Token: %s', vaulttoken)
    if vaulttoken and secret_key:
        keyvault = config_value('VAULT', 'keyvault')
        logger.info('Keyvault: %s, key:%s', keyvault, '*' * len(secret_key))
        success = delete_keyvault_secret(keyvault, secret_key, vaulttoken)
    logger.info('Secret Deleted: %s', success)
    return success


def get_cyberark_data(secret_key=None):
    """Get secret value for the secret key"""
    val = None
    ca_object = config_value('VAULT', 'CA_OBJECT')
    ca_safe = config_value('VAULT', 'CA_SAFE')
    ca_exe = config_value('VAULT', 'CA_EXE')
    ca_appid = config_value('VAULT', 'CA_APPID')
    if ca_object and ca_exe and ca_appid:
        cmd_args = '%s  GetPassword -p AppDescs.AppID=%s -p Query="Safe=%s;Folder=Root;Object=%s-%s" -o Password' \
                  % (ca_exe, ca_appid, ca_safe, ca_object, secret_key)
        my_process = Popen(cmd_args, shell=True, stdout=PIPE,
                                     stderr=PIPE,
                                     stdin=PIPE)
        out, err = my_process.communicate()
        err_result = err.rstrip() if err else None
        val = out.decode() if isinstance(out, bytes) else out.rstrip()
        if err_result:
            val = None
        else:
            logger.info('Secret Value: %s', '*' * len(val))
    return val
