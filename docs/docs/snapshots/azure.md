# Snapshot configuration file

To setup an **Azure** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "<azure-Connector>",
                "testUser": "<spn-username>",
                "subscriptionId": "<subscription-id>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "<resource-provider>",
                        "collection": "<collection-name>",
                        "path": "<resource-id>"
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| azure-connector | Name of the **Azure Connector** file you want to use to connect to Azure backend |
| spn-username | Name of the **SPN** user to connect to the Azure backend, must be present in the **Azure** connector file |
| subscription-id | Id of the subscription to inspect, must be the same as the user described in the **Azure** connector file |
| snapshot-name | Name of the snapshot, you will use this in test files. This name should be unique in the container |
| resource-provider | Type of resource being queried for, see below for more information |
| collection-name | Name of the **NoSQL** db collection used to store snapshots of this file |
| resource-id | The id that corresponds to the resource you want to take snapshot, see Paths below |

### Azure Resource Provider

The **resource-provider** parameter refers to a very wide list. Let's see how the **Azure** connector works to know how to properly set it up!

The **Azure** connector is a wrapper around the **Azure** ReST api. **Prancer** will call a **GET** operation on the api using the **type-of-node** and **path**. For example:

| What you need | Type of node |
|---------------|--------------|
| Availability Sets | Microsoft.Compute/availabilitySets | 
| Virtual machines | Microsoft.Compute/virtualMachines |
| MySQL databases | Microsoft.DBforMySQL/servers/{replaceThisWithServerName}/databases |

The important part to remember is that if you find an **Azure** api endpoint in the documentation, you usually just need to copy and paste everything after the `providers/` in the endpoint and paste it in the node type.

### Resource id

the id of the resource in the Azure. Usually it is in the format of: 
`/resourceGroups/<name-of-the-resource-group>/providers/<name-of-the-provider>/<resource-name/`

You can get the resource id from the URL in the Azure portal, or from the Azure CLI.

# Master Snapshot Configuration File
Master Snapshot Configuration File is to define **resource types**. We do not have individual resources in the Master Snapshot Configuration File, instead we have the type of resources.
Prancer validation framework is using the Master Snapshot Configuration File in the crawler functionality to find new resources.

```
{
    "contentVersion": "1.0.0.0",
    "fileType":"masterSnapshot",
    "snapshots": [
        {
            "source": "<connector-name>",
            "testUser" : "<spn-username>",
            "subscriptionId" : ["<subscription-id>"],
            "nodes": [
                {
                    "masterSnapshotId": "<master-Snapshot-Id>",
                    "type": "<resource-provider>",
                    "collection": "<name-of-collection>"
                }
            ]
        }
    ]
}
```
Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| azure-connector | Name of the **Azure Connector** file you want to use to connect to Azure backend |
| spn-username | Name of the **SPN** user to connect to the Azure backend, must be present in the **Azure** connector file |
| subscription-id | Id of the subscription to inspect, must be the same as the user described in the **Azure** connector file |
| master-Snapshot-Id | Name of the master snapshot id, you will use this in master test files. This name should be unique in the container |
| resource-provider | the type of the resource we want to capture during the crawl process. In the `azure` connector, this should be the resource type supported by Azure. |
| collection-name | in which collection in database we want to store this resource type. Usually it is a good practice to have a separate collection for each type. But based on the scale of implementation, you may want to put multiple resource types in a single collection |

# Master Snapshot Configuration File in remote git
It is possible to centrally manage your master snapshot configuration files from a git repository. When you are doing that, you can make sure one version of truth is circulating in your different collections and you can manage it centrally. Here USER_1 is the user associated in the connector. A connector could have different users to connect to different resources in the cloud.

The format for the remote git master snapshot configuration file is like this:

```
    {
    "$schema": "",
    "contentVersion": "1.0.0.0",
    "fileType": "masterSnapshot",
    "connector": "prancer_compliance_structure",
    "remoteFile": "azure/iac/master-config.json",
    "connectorUsers": [
        {
        "id": "USER_1",
        "testUser": "farchide",
        "source": "quickstart_structure"
        }
    ]
    }
```

