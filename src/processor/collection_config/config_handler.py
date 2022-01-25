import re
import time
from typing import Tuple
from processor.database.database import (
    get_documents,
    find_and_update_document,
    insert_one_document,
)
from processor.helper.config.config_utils import DATABASE, DBNAME, config_value
from processor.logging.log_handler import getlogger


logger = getlogger()


def get_collection_config_data(container: str) -> dict:
    # get config of given collection
    config_data = get_collection_config(container)
    collection_config_data = config_data.get("json", {}).get("configuration", {})
    return collection_config_data


def get_collection_config(container: str) -> dict:
    # get config of given collection
    dbname = config_value(DATABASE, DBNAME)

    collection = "structures"
    query = {"type": "collection_configuration", "container": container}
    config_data_list = get_documents(collection, query, dbname)

    return config_data_list[0] if config_data_list else {}


def update_collection_config(container: str, updated_json: dict) -> bool:
    dbname = config_value(DATABASE, DBNAME)
    collection = "structures"
    query = {"type": "collection_configuration", "container": container}
    updated_json = {"$set": updated_json}
    updated = find_and_update_document(collection, dbname, query, updated_json)
    return updated


def create_collection_config(container: str, configuration: dict):
    dbname = config_value(DATABASE, DBNAME)
    collection = "structures"
    structure = {
        "type": "collection_configuration",
        "collection": collection,
        "container": container,
        "timestamp": int(time.time() * 1000),
        "json": {"configuration": configuration},
    }
    doc_id_str = insert_one_document(structure, collection, dbname, False)
    return doc_id_str


def get_master_collection_config() -> dict:
    dbname = config_value(DATABASE, DBNAME)
    collection = "structures"
    query = {"type": "master_collection_configuration"}
    config_data_list = get_documents(collection, query, dbname)
    config_data = (
        config_data_list[0].get("json", {}).get("configurations", {})
        if config_data_list
        else {}
    )
    return config_data


def validate_master_config(
    collection_config, master_collection_config
) -> Tuple[bool, list]:
    is_valid = True
    messages = []
    if isinstance(master_collection_config, list):
        for master_config_item in master_collection_config:
            if isinstance(master_config_item, dict) and isinstance(
                collection_config, dict
            ):
                master_config_key = master_config_item.get("key")
                required = master_config_item.get("required", False)
                master_config_children = master_config_item.get("children", [])
                allowed_values = master_config_item.get("allowed_values", [])

                if (
                    master_config_key not in collection_config.keys()
                    and required is True
                ):
                    is_valid = False
                    message = f"'{master_config_key}' key is required"
                    messages.append(message)

                elif master_config_key in collection_config.keys():
                    collection_config_value = collection_config[master_config_key]
                    if master_config_children:
                        if isinstance(collection_config_value, dict):
                            is_valid, new_messages = validate_master_config(
                                collection_config_value, master_config_children
                            )
                            messages.extend(new_messages)
                        else:
                            pass
                    elif (
                        allowed_values and collection_config_value not in allowed_values
                    ):
                        is_valid = False
                        message = f"'{master_config_key}'s value '{collection_config_value}' is not a valid value, allowed valued are: {allowed_values}"
                        messages.append(message)

    return is_valid, messages


# master_config = [
#     {
#         "key": "generate_pr",
#         "allowed_values": [True, False],
#         "default": True,
#         "title": "Generate PR",
#         "description": "make it False to not to generate auto Pull Request",
#         "type": "bool",
#         "required": True,
#     },
#     {
#         "key": "aws_secret_remediation",
#         "title": "AWS Secret Remediation",
#         "description": "configure secret vault to store leaked secrets",
#         "type": "json",
#         "required": False,
#         "children": [
#             {
#                 "key": "account_id",
#                 "title": "AWS Account ID",
#                 "description": "AWS Cloud 12-digit account number",
#                 "type": "integer",
#                 "required": True,
#             },
#             {
#                 "key": "region",
#                 "title": "Region",
#                 "allowed_values": [
#                     "us-east-1",
#                     "us-east-2",
#                     "us-west-1",
#                     "us-west-2",
#                     "af-south-1",
#                     "ap-east-1",
#                     "ap-south-1",
#                     "ap-northeast-3",
#                     "ap-northeast-2",
#                     "ap-southeast-1",
#                     "ap-southeast-2",
#                     "ap-northeast-1",
#                     "ca-central-1",
#                     "eu-central-1",
#                     "eu-west-1",
#                     "eu-west-2",
#                     "eu-south-1",
#                     "eu-west-3",
#                     "eu-north-1",
#                     "me-south-1",
#                     "sa-east-1",
#                     "us-gov-east-1",
#                     "us-gov-west-1",
#                 ],
#                 "required": True,
#                 "Description": "Select a region where your secret manager is available",
#             },
#         ],
#     },
# ]
# test_config = {
#     "generate_pr": "False",
#     "aws_secret_remediation": {
#         "account_id": 123456789012,
#         "region": "us"
#     },
# }

# is_valid, messages = validate_master_config(test_config, master_config)

# if is_valid is False:
#     for message in messages:
#         print(message)
# else:
#     print("config file is valid")
