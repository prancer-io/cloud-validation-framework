from processor.helper.httpapi.restapi_azure import json_source
from processor.helper.config.config_utils import get_test_json_dir, config_value
from processor.helper.json.json_utils import json_from_file, save_json_to_file, collectiontypes, STRUCTURE, \
    MASTERSNAPSHOT
from processor.helper.file.file_utils import exists_file
from processor.database.database import DATABASE, DBNAME, sort_field, get_documents, find_and_update_document
from processor.logging.log_handler import getlogger
from processor.helper.httpapi.http_utils import http_get_request, http_post_request
from processor.connector.vault import get_vault_data, set_vault_data
from processor.connector.snapshot_azure import populate_client_secret
from oauth2client.service_account import ServiceAccountCredentials
from boto3 import client
import copy
import requests
import tempfile
import re

logger = getlogger()

def get_structure_data(snapshot_source, container=None):
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
        if container:
            qry["container"] = container
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

def update_collection_data(container, source, updated_data, dbname, collection):
    if json_source():
        query = {
            "name": source, 
            "container" : container
        }
        find_and_update_document(collection, dbname, query, {
            '$set': {
                "json" : updated_data
            }
        })
    else:
        json_test_dir = get_test_json_dir()
        file_name = '%s.json' % source if source and not \
            source.endswith('.json') else source
        if collection == "structures":
            file_path = '%s/../%s' % (json_test_dir, file_name)
        else:
            file_path = '%s/%s/%s' % (json_test_dir, container, file_name)
        save_json_to_file(updated_data, file_path)

def populate_azure_accounts(container, source, structure_data, test_user):
    account_index = 0
    subscription_list = []
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[STRUCTURE])
    all_account = False
    
    for account in structure_data.get("accounts"):
        if account.get("subscription") and str(account.get("all-accounts", "")).lower() == "true":
            all_account = True
            subscription = account["subscription"][0]
            if subscription.get("users"):
                tenant_id = structure_data.get("tenant_id")
                client_id = subscription["users"][0]["client_id"]
                client_secret = subscription["users"][0].get("client_secret")
                username = subscription["users"][0]["name"]
                username = re.sub(r"-\d+$", "", username)
                sub_list = get_azure_subscriptions(tenant_id, client_id, client_secret, username, test_user)
                subscription_list += sub_list
                updated_data = copy.deepcopy(structure_data)
                logger.info("sub_list %s", sub_list)
                updated_data["accounts"][account_index]["subscription"] = sub_list
                update_collection_data(container, source, updated_data, dbname, collection)
                account_index += 1
    return subscription_list, all_account

def get_azure_subscriptions(tenant_id, client_id, client_secret, username, test_user):
    """ Get azure subscriptions """
    sub_list = []
    if not client_secret:
        new_client_secret = populate_client_secret(client_id, client_secret, test_user)
    else:
        new_client_secret = client_secret
    token = get_azure_token(tenant_id, client_id, new_client_secret)
    if token:
        url = 'https://management.azure.com/subscriptions?api-version=2014-04-01-preview'
        hdrs = {
            'Authorization': 'Bearer %s' % token,
            'Cache-Control': 'no-cache',
            'Accept': 'application/json'
        }
        status, data = http_get_request(url, hdrs)
        if status and isinstance(status, int) and status == 200:
            if 'value' in data and isinstance(data['value'], list):
                index = 1
                for subdata in data['value']:
                    sub_list.append({
                        "subscription_description": subdata['displayName'],
                        "subscription_id": subdata['subscriptionId'],
                        "subscription_name": subdata['displayName'],
                        "users": [
                            {
                                "client_id": client_id,
                                "client_secret": client_secret if client_secret else "",
                                "name": "%s-%s" % (username, index)
                            }
                        ]
                    })
                    index += 1
    return sub_list
        
def get_azure_token(tenant_id, client_id, client_secret):
    """ Get the access token for azure management.azure.com portal.  """
    token = None
    if tenant_id and client_id and client_secret:
        url = 'https://login.microsoftonline.com/%s/oauth2/token' % tenant_id
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': 'https://management.azure.com'
        }
        hdrs = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json'
        }
        logger.info('Get Azure token REST API invoked!')
        status, data = http_post_request(url, data, headers=hdrs, json_type=True)
        if status and isinstance(status, int) and status == 200:
            token = data['access_token']
        else:
            logger.info("Get Azure token returned invalid status: %s", status)
    return token

def populate_gcp_projects(container, source, structure_data):
    account_list = []
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[STRUCTURE])
    all_account = False
    if structure_data.get("projects"):
        project = structure_data.get("projects")[0]
        if project.get("users") and str(project.get("all-accounts")).lower() == "true":
            all_account = True
            user = project["users"][0]
            client_email = user["client_email"]
            client_id = user["client_id"]
            private_key_id = user["private_key_id"]
            name = user["name"]
            private_key = user.get("private_key")
            name = re.sub(r"-\d+$", "", name)
            account_list += get_projects_list(private_key_id, private_key, client_email, client_id, name)
    updated_data = copy.deepcopy(structure_data)
    updated_data["projects"] = account_list
    update_collection_data(container, source, updated_data, dbname, collection)
    return account_list, all_account

def access_token_from_service_account(private_key_id, private_key, client_email, client_id):
    """
    Generate a Google Service Account credentials file and 
    """
    credential_path = tempfile.mkdtemp()
    access_token = None
    gce = {
        "type": "service_account",
        "private_key_id": private_key_id,
        "private_key": private_key.replace("\\n", "\n"),
        "client_email": client_email,
        "client_id": client_id
    }
    credential_path = "%s/gce.json" % credential_path
    save_json_to_file(gce, credential_path)
    scopes = ['https://www.googleapis.com/auth/compute', "https://www.googleapis.com/auth/cloud-platform"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, scopes)
        if not credentials:
            return access_token
        return credentials.get_access_token().access_token
    except:
        return access_token

def get_projects_list(private_key_id, private_key, client_email, client_id, test_user):
    """ Get google projects list """
    project_list = []
    if not private_key:
        new_private_key = get_vault_data(private_key_id)
    else:
        new_private_key = private_key

    if new_private_key:
        access_token = access_token_from_service_account(private_key_id, new_private_key, client_email, client_id)
        if access_token:
            hdrs = {"Accept": "application/json", "Authorization": "Bearer %s" % access_token }
            url = "https://cloudresourcemanager.googleapis.com/v1/projects"
            resp = requests.get(url, headers=hdrs)
            if resp.status_code == 200:
                projectData = resp.json()
                if projectData and  'projects' in projectData:
                    index = 1
                    for project in projectData['projects']:
                        project_list.append({
                            "project-id": project['projectId'],
                            "project-name": project['name'],
                            "all-accounts" : True,
                            "users": [
                                {
                                    "client_email": client_email,
                                    "client_id": client_id,
                                    "name": "%s-%s" % (test_user, index),
                                    "private_key_id": private_key_id,
                                    "private_key" : private_key if private_key else "",
                                    "type": "service_account"
                                }
                            ]
                        })
                        index += 1

    return project_list

def check_container_for_all_accounts(container, mastersnapshot, file_name):
    """ fetch all the connector accounts and update the structure and mastersnapshots """
    connector_users = []
    snapshots = []
    remote_file = False
    mastersnapshot_json = copy.deepcopy(mastersnapshot)
    if "connectorUsers" in mastersnapshot and "remoteFile" in mastersnapshot \
        and mastersnapshot["connectorUsers"] and mastersnapshot["remoteFile"]:
        remote_file = True
        connector_user = mastersnapshot["connectorUsers"][0]
        source = connector_user.get("source")
        test_user = connector_user.get("testUser")
    elif "snapshots" in mastersnapshot and mastersnapshot["snapshots"]:
        snapshot = mastersnapshot["snapshots"][0]
        source = snapshot.get("source")
        test_user = snapshot.get("testUser")
    else:
        return mastersnapshot

    structure_data = get_structure_data(source, container=container)
    if structure_data.get("type") == "azure":
        subscription_list, all_account = populate_azure_accounts(container, source, structure_data, test_user)
        if not all_account:
            return mastersnapshot

        for idx, subscription in enumerate(subscription_list, start=1):
            if remote_file:
                testUser = re.sub(r"-\d+$", "", connector_user.get("testUser"))
                connector_users.append({
                    "id": connector_user.get("id"),
                    "source": connector_user.get("source"),
                    "subscriptionId": subscription["subscription_id"],
                    "testUser": "%s-%s" % (testUser, idx)
                })
            else:
                testUser = re.sub(r"-\d+$", "", snapshot.get("testUser"))
                snapshots.append({
                    "source": snapshot.get("source"),
                    "type": snapshot.get("type"),
                    "subscriptionId": subscription["subscription_id"],
                    "testUser": "%s-%s" % (testUser, idx),
                    "nodes": snapshot.get("nodes"),
                })

    elif structure_data.get("type") == "google":
        account_list, all_account = populate_gcp_projects(container, source, structure_data)
        if not all_account:
            return mastersnapshot

        for idx, account in enumerate(account_list, start=1):
            if remote_file:
                testUser = re.sub(r"-\d+$", "", connector_user.get("testUser"))
                connector_users.append({
                    "id": connector_user.get("id"),
                    "source": connector_user.get("source"),
                    "project-id": account.get("project-id"),
                    "testUser": "%s-%s" % (testUser, idx)
                })
            else:
                testUser = re.sub(r"-\d+$", "", snapshot.get("testUser"))
                snapshots.append({
                    "source": snapshot.get("source"),
                    "type": snapshot.get("type"),
                    "project-id": account.get("project-id"),
                    "testUser": "%s-%s" % (testUser, idx),
                    "nodes": snapshot.get("nodes"),
                })
    else:
        return mastersnapshot

    if remote_file:
        mastersnapshot_json["connectorUsers"] = connector_users
    else:
        mastersnapshot_json["snapshots"] = snapshots

    mastersnapshot = mastersnapshot_json
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[MASTERSNAPSHOT])
    update_collection_data(container, file_name, mastersnapshot_json, dbname, collection)
    return mastersnapshot