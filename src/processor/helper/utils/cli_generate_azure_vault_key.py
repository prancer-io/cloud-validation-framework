import uuid

from processor.connector.vault import get_vault_data, set_vault_data
from processor_enterprise.controller.vaultcontroller import set_key_visbility, EDITABLE

def generate_password():
	return str(uuid.uuid4())

def generate_azure_vault_key():

	key = input("Enter the key to add or update its password: ")
	password = get_vault_data(secret_key=key)

	if password:
		print("Regenerating password for key: ", key)
	else:
		print("Creating and generating password for key: ", key)

	password = generate_password()
	new_password = set_vault_data(key_name=key, value=password)
	set_key_visbility(key, EDITABLE)