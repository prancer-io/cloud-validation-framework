This snapshot configuration file type is used along with the **Azure** connector. It allows you to take snapshots of ReST api calls to the **Azure** api.

# Snapshot configuration file

To setup an **Azure** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "azureConnector",
                "testUser": "<spn-username>",
                "subscriptionId": "<subscription-id>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "<type-of-node>",
                        "collection": "<collection-name>",
                        "path": "<path-to-resource>"
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| spn-username | Name of the **SPN** user, must be present in the **Azure** connector file |
| subscription-id | Id of the subscription to inspect, must be the same as the user described in the **Azure** connector file |
| snapshot-name | Name of the snapshot, you will use this in test files |
| type-of-node | Type of resource being queried for, see below for more information |
| collection-name | Name of the **MongoDB** collection used to store snapshots of this file |
| path-to-resource | The url that corresponds to the resource you want to snapshot, see Paths below |

# Types of nodes

The **type-of-node** parameter refers to a very wide list. Let's see how the **Azure** connector works to know how to properly set it up!

The **Azure** connector is a wrapper around the **Azure** ReST api. **Prancer** will call a **GET** operation on the api using the **type-of-node** and **path**. For example:

| What you need | Type of node |
|---------------|--------------|
| Availability Sets | Microsoft.Compute/availabilitySets | 
| Virtual machines | Microsoft.Compute/virtualMachines |
| MySQL databases | Microsoft.DBforMySQL/servers/{replaceThisWithServerName}/databases |

The important part to remember is that if you find an **Azure** api endpoint in the documentation, you usually just need to copy and paste everything after the `providers/` in the endpoint and paste it in the node type.

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> Note: If you have parameters that must be replaced, you must hardcode them into the snapshot configuration file. We are working on a way to pass parameters to be replaced in different places such as paths, types, filters and so on.

# Paths to resource

On the contrary of the **AWS** connector and snapshot configuration file which features the `id` section to filter and search for items, there are no way to select data in the **Azure** snapshot configuration files other than providing a specific path to a resource.

We are working on ways to add this support to **Prancer**.