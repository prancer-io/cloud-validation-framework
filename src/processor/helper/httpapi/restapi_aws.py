"""
AWS Secrets Manager equivalents of restapi_azure.py.

Parallel implementation — does not replace the Azure path. Selected via
[VAULT] type = aws in the config (see processor/connector/vault.py).

Auth: relies on the boto3 default credential chain (env vars, IAM role via
EKS Pod Identity / IRSA, instance profile). No explicit credential handling
needed when running in the cluster.

Secret naming convention: AWS Secrets Manager uses path-like names. The
[VAULT] aws_secrets_prefix config value is prepended to every secret key,
matching the V3 layout:

   prancer/prod/customer170/<secret_key>
   prancer/prod/platform/<secret_key>
"""
import json
from processor.logging.log_handler import getlogger

logger = getlogger()

_boto3 = None
_boto3_client_cache = {}


def _client(service='secretsmanager', region=None):
    global _boto3
    if _boto3 is None:
        try:
            import boto3
        except ImportError:
            raise RuntimeError("boto3 required for [VAULT] type=aws. pip install boto3")
        _boto3 = boto3
    key = (service, region or 'default')
    if key not in _boto3_client_cache:
        kwargs = {'region_name': region} if region else {}
        _boto3_client_cache[key] = _boto3.client(service, **kwargs)
    return _boto3_client_cache[key]


def _full_name(secret_key, prefix=None):
    if not prefix:
        return secret_key
    if secret_key.startswith(prefix + '/') or secret_key == prefix:
        return secret_key
    return f"{prefix.rstrip('/')}/{secret_key.lstrip('/')}"


def get_aws_secret(secret_key, prefix=None, region=None):
    """Returns dict with 'value' key (parity with Azure response shape)."""
    name = _full_name(secret_key, prefix)
    client = _client(region=region)
    try:
        resp = client.get_secret_value(SecretId=name)
        val = resp.get('SecretString')
        if val is None:
            binary = resp.get('SecretBinary')
            val = binary.decode('utf-8') if binary else None
        logger.info('AWS secret read: %s', '*' * len(name))
        return {'value': val} if val is not None else None
    except client.exceptions.ResourceNotFoundException:
        logger.warning('AWS secret not found: %s', name)
        return None
    except Exception as e:
        logger.error('AWS secret read failed for %s: %s', name, e)
        return None


def set_aws_secret(secret_key, value, prefix=None, region=None):
    name = _full_name(secret_key, prefix)
    client = _client(region=region)
    try:
        try:
            client.put_secret_value(SecretId=name, SecretString=value)
        except client.exceptions.ResourceNotFoundException:
            client.create_secret(Name=name, SecretString=value)
        logger.info('AWS secret written: %s', '*' * len(name))
        return True
    except Exception as e:
        logger.error('AWS secret write failed for %s: %s', name, e)
        return False


def set_aws_secret_with_response(secret_key, value, prefix=None, region=None):
    name = _full_name(secret_key, prefix)
    client = _client(region=region)
    try:
        try:
            resp = client.put_secret_value(SecretId=name, SecretString=value)
        except client.exceptions.ResourceNotFoundException:
            resp = client.create_secret(Name=name, SecretString=value)
        return resp.get('ResponseMetadata', {}).get('HTTPStatusCode', 200), resp
    except Exception as e:
        logger.error('AWS secret write failed for %s: %s', name, e)
        return 500, {'error': str(e)}


def delete_aws_secret(secret_key, prefix=None, region=None, recovery_window_days=7):
    name = _full_name(secret_key, prefix)
    client = _client(region=region)
    try:
        if recovery_window_days == 0:
            client.delete_secret(SecretId=name, ForceDeleteWithoutRecovery=True)
        else:
            client.delete_secret(SecretId=name, RecoveryWindowInDays=recovery_window_days)
        return True
    except client.exceptions.ResourceNotFoundException:
        return True
    except Exception as e:
        logger.error('AWS secret delete failed for %s: %s', name, e)
        return False


def get_all_aws_secrets(prefix=None, region=None):
    client = _client(region=region)
    out = []
    paginator = client.get_paginator('list_secrets')
    filters = [{'Key': 'name', 'Values': [prefix + '/']}] if prefix else []
    try:
        for page in paginator.paginate(Filters=filters or None):
            for entry in page.get('SecretList', []):
                full_name = entry['Name']
                short = full_name[len(prefix) + 1:] if prefix and full_name.startswith(prefix + '/') else full_name
                val_resp = client.get_secret_value(SecretId=full_name)
                out.append({'key': short, 'value': val_resp.get('SecretString')})
        return out
    except Exception as e:
        logger.error('AWS secret list failed: %s', e)
        return []
