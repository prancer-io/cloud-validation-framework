This snapshot configuration file type is used along with the **Git** connector. It allows you to take snaphots of entire **JSON** files as resources to test.

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> As of now, there is no way to select only a portion of the **JSON** file and this makes your tests more complex but we are working on it!

# CloudFormation and Azure ARM templates

We currently do not support any of the **CloudFormation** or **Azure Resource Management** templates, but you can use this snapshot configuration file type to read the **JSON** version of these templates until we have a proper snapshot configuration file type dedicated to these template based resource managers!

# Snapshot configuration file

To setup a **JSON** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "testUser": "<user-to-use-on-connector>",
                "branchName": "<branch-to-use-on-connector>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "json",
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
| relative-path-to-file | Path to the file to read, relative to the root of the repository that the connector checks out |
