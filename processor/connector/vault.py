"""
   Common file for vault functionality.
"""
from processor.logging.log_handler import getlogger
from processor.helper.config.config_utils import config_value
from processor.helper.httpapi.restapi_azure import get_vault_access_token, get_keyvault_secret

logger = getlogger()


def get_vault_data():
    """Read vault data from config"""
    vaulttype = config_value('VAULT', 'type')
    val = None
    if vaulttype:
        if vaulttype == 'azure':
            val = get_azure_vault_data()
    return val


def get_azure_vault_data():
    val = None
    client_id = config_value('VAULT', 'client_id')
    client_secret = config_value('VAULT', 'client_secret')
    tenant_id = config_value('VAULT', 'tenant_id')
    logger.info('Id: %s, secret: %s, tenant: %s', client_id, client_secret, tenant_id)
    vaulttoken = get_vault_access_token(tenant_id, client_id, client_secret)
    logger.debug('Vault Token: %s', vaulttoken)
    if vaulttoken:
        keyvault = config_value('VAULT', 'keyvault')
        secret_key = config_value('VAULT', 'secret_key')
        logger.info('Keyvault: %s, key:%s', keyvault, secret_key)
        secret_data = get_keyvault_secret(keyvault, secret_key, vaulttoken)
        if secret_data and 'value' in secret_data:
            val = secret_data['value']
    logger.info('Secret Value: %s', val)
    return val