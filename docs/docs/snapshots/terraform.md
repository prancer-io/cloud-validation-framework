This snapshot configuration file type is used along with the **Git** connector. It allows you to take snaphots of the **tfvars** of a **Terraform** file and convert them to **JSON** to be snapshotted and saved as resources to test.

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> As of now, there is no way to select only a portion of the **Terraform** file, therefore, all values of the file will be converted to **JSON** and then saved as a snapshot!

# Terraform to JSON

Here is a quick example of what a **Terraform**'s **tfvars** file will look like after being transformed to **JSON**. Example:

    resource_group_name = "AzureQuickstart"
    resource_group_location = "West US"
    dns_name_prefix = "REPLACE_WITH_UNIQUE_NAME"
    linux_agent_count = "3"
    linux_agent_vm_size = "Standard_D2_v2"
    linux_admin_username = "azure"
    linux_admin_ssh_publickey = "REPLACE_WITH_SSHKEY"
    master_count = "1"
    service_principal_client_id = "REPLACE_WITH_SERVICEPRINCIPAL_CLIENTID"
    service_principal_client_secret = "REPLACE_WITH_SERVICEPRINCIPAL_CLIENTSECRET"

Would be converted to:

    {
        "resource_group_name": "AzureQuickstart",
        "resource_group_location": "West US",
        "dns_name_prefix": "REPLACE_WITH_UNIQUE_NAME",
        "linux_agent_count": "3",
        "linux_agent_vm_size": "Standard_D2_v2",
        "linux_admin_username": "azure",
        "linux_admin_ssh_publickey": "REPLACE_WITH_SSHKEY",
        "master_count": "1",
        "service_principal_client_id": "REPLACE_WITH_SERVICEPRINCIPAL_CLIENTID",
        "service_principal_client_secret": "REPLACE_WITH_SERVICEPRINCIPAL_CLIENTSECRET"
    }

# Snapshot configuration file

To setup a **Terraform** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "type": "git",
                "testUser": "<user-to-use-on-connector>",
                "branchName": "<branch-to-use-on-connector>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "terraform",
                        "collection": "<collection-name>",
                        "path": "<relative-path-to-file>"
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| user-to-use-on-connector | Same username as defined in the **Git** connector configuration file |
| branch-to-use-on-connector | Same branch as defined in the **Git** connector configuration file |
| snapshot-name | Name of the snapshot, you will use this in test files |
| collection-name | Name of the **MongoDB** collection used to store snapshots of this file |
| relative-path-to-file | Path to the file to read, relative to the root of the repository |