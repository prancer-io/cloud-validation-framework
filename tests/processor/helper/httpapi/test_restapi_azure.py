import os


def mock_config_value(key, default=None):
    return 'pytestdb'

def mock_getenv(key, default=None):
    return 'clientSecret'

def mock_empty_getenv(key, default=None):
    return default

def mock_input(text):
    return 'clientSecret'

def mock_valid_http_post_request(url, data, headers={}):
    return 200, {'access_token': 'abcd'}

def mock_invalid_http_post_request(url, data, headers={}):
    return 401, {'access_token': None}

def mock_valid_http_get_request(url, headers=None, name='GET'):
    return 200, {'access_token': 'abcd'}

def mock_invalid_http_get_request(url, headers=None, name='GET'):
    return 401, {'access_token': None}

def mock_get_from_currentdata(key):
    if key == 'subscriptionId':
        return 'subscriptionId'
    elif key == 'tenant_id':
        return 'tenant_id'
    elif key == 'clientId':
        return 'clientId'
    elif key == 'rg':
        return 'rg'
    elif key == 'vaultClientSecret':
        return 'vaultClientSecret'
    elif key == 'jsonsource':
        return False
    else:
        return None

def mock_empty_get_from_currentdata(key):
    if key == 'subscriptionId':
        return 'subscriptionId'
    elif key == 'tenant_id':
        return 'tenant_id'
    else:
        return None

def mock_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "_id": "5c24af787456217c485ad1e6",
        "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
        "collection": "microsoftcompute",
        "json":{
            "id": 124,
            "location": "eastus2",
            "name": "mno-nonprod-shared-cet-eastus2-tab-as03"
        },
        "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
        "snapshotId": 1,
        "timestamp": 1545908086831
    }]

def mock_json_source():
    return True

def test_get_azure_functions(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.input', mock_input)
    from processor.helper.httpapi.restapi_azure import get_subscription_id,\
        get_tenant_id, get_client_id, get_resource_group, get_client_secret
    assert 'subscriptionId' == get_subscription_id()
    assert 'tenant_id' == get_tenant_id()
    assert 'clientId' == get_client_id()
    assert 'rg' == get_resource_group()
    assert 'clientSecret' == get_client_secret()


def test_web_client_data(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_empty_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.input', mock_input)
    from processor.helper.httpapi.restapi_azure import get_client_secret, get_web_client_data
    assert 'clientSecret' == get_client_secret()
    client_id, client_secret, sub_name, sub_id, tenant_id = \
        get_web_client_data('azure', 'azureStructure.json', '<User name abc@mno.com>')
    assert client_id is not None
    assert client_secret == '<Service Principal Secret, if empty will prompt>'
    assert sub_id is not None
    assert sub_name is not None
    assert tenant_id is not None


def test_get_access_token(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_post_request',
                        mock_valid_http_post_request)
    from processor.helper.httpapi.restapi_azure import get_access_token
    val = get_access_token()
    assert val == 'abcd'


def test_none_get_access_token(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_empty_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_post_request',
                        mock_valid_http_post_request)
    from processor.helper.httpapi.restapi_azure import get_access_token
    val = get_access_token()
    assert val is None


def test_invalid_http_get_access_token(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_post_request',
                        mock_invalid_http_post_request)
    from processor.helper.httpapi.restapi_azure import get_access_token
    val = get_access_token()
    assert val is None


def test_get_azure_data(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_documents', mock_get_documents)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.json_source', mock_json_source)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.config_value', mock_config_value)
    from processor.helper.httpapi.restapi_azure import get_azure_data
    data = get_azure_data('snapshot')
    assert data is not None


def test_get_vault_client_secret(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    from processor.helper.httpapi.restapi_azure import get_vault_client_secret
    val = get_vault_client_secret()
    assert val is not None


def test_empty_get_vault_client_secret(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_empty_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    from processor.helper.httpapi.restapi_azure import get_vault_client_secret
    val = get_vault_client_secret()
    assert val is not None


def test_empty_env_get_vault_client_secret(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_empty_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_empty_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.input', mock_input)
    from processor.helper.httpapi.restapi_azure import get_vault_client_secret
    val = get_vault_client_secret()
    assert val is not None


def test_get_keyvault_secret(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_get_request',
                        mock_valid_http_get_request)
    from processor.helper.httpapi.restapi_azure import get_keyvault_secret
    val = get_keyvault_secret('abcdvault', 'abcdsecret', 'vaulttoken')
    assert val == {'access_token': 'abcd'}


def test_invalid_get_keyvault_secret(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_get_request',
                        mock_invalid_http_get_request)
    from processor.helper.httpapi.restapi_azure import get_keyvault_secret
    val = get_keyvault_secret('abcdvault', 'abcdsecret', 'vaulttoken')
    assert val == {'access_token': None}


def test_get_vault_access_token(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_post_request',
                        mock_valid_http_post_request)
    from processor.helper.httpapi.restapi_azure import get_vault_access_token
    val = get_vault_access_token('tenant_id', 'vault_client_id', 'client_secret')
    assert val == 'abcd'


def test_invalid_get_vault_access_token(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.get_from_currentdata',
                        mock_get_from_currentdata)
    monkeypatch.setattr(os, 'getenv', mock_getenv)
    monkeypatch.setattr('processor.helper.httpapi.restapi_azure.http_post_request',
                        mock_invalid_http_post_request)
    from processor.helper.httpapi.restapi_azure import get_vault_access_token
    val = get_vault_access_token('tenant_id', 'vault_client_id', 'client_secret')
    assert val is None
