import uuid

from processor.connector.vault import get_vault_data, set_vault_data
from processor_enterprise.controller.vaultcontroller import set_key_visbility, EDITABLE

def generate_password():
	return str(uuid.uuid4())

def generate_azure_vault_key():

	key = input("Enter the key to add or update its password: ")

	is_key_exists = get_vault_data(secret_key=key)

	password = generate_password()

	is_created = set_vault_data(key_name=key, value=password)

	if is_key_exists and is_created:
		print("Regenerating password for key: ", key)
	elif is_created:
		set_key_visbility(key, EDITABLE)
		print("Creating and generating password for key: ", key)
	else:
		print("Getting issue while generating key:", key)

