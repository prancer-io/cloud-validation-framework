This snapshot configuration file type is used along with the **filesystem** connector. It allows you to take snaphots of entire files as resources to test.

# Snapshot configuration file

To setup a **filesystem** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "<name-of-connector>",
                "type": "filesystem",
                "testUser": "<user-to-use-on-connector>",
                "branchName": "<branch-to-use-on-connector>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "<file-type>",
                        "collection": "<collection-name>",
                        "paths": [
                            "<relative-paths-to-file>"
                        ]
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| name-of-connector | name of the **filesystem** connector configuration file |
| user-to-use-on-connector | Same username as defined in the **filesystem** connector configuration file |
| branch-to-use-on-connector | Same branch as defined in the **filesystem** connector configuration file. This attribute is only used when we are connecting to a **git** repository |
| snapshot-name | Name of the snapshot, you will use this in test files |
| file-type | type of the file. it could be `json` or `yaml` or `arm` or `cloudformation` |
| collection-name | Name of the **NoSQL** database collection used to store snapshots of this file |
| relative-paths-to-file | Path to the file to read, relative to the root of the repository that the connector checks out |

# Master Snapshot configuration file
We use master snapshot configuration file to read all the files in a directory with the **filesystem** connector. 
> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "masterSnapshot",
        "snapshots": [
            {
                "source": "<name-of-connector>",
                "testUser": "<user-to-use-on-connector>",
                "nodes": [
                    {
                        "masterSnapshotId": "<master-snapshot-name>",
                        "type": "<file-type>",
                        "collection": "<collection-name>",
                        "paths": [
                            "<relative-paths-to-file>"
                        ]
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| name-of-connector | name of the **filesystem** connector configuration file |
| user-to-use-on-connector | Same username as defined in the **filesystem** connector configuration file |
| branch-to-use-on-connector | Same branch as defined in the **filesystem** connector configuration file. This attribute is only used when we are connecting to a **git** repository |
| master-snapshot-name | Name of the snapshot, you will use this in test files |
| file-type | type of the file. it could be `json` or `yaml` or `arm` or `cloudformation` |
| collection-name | Name of the **NoSQL** database collection used to store snapshots of this file |
| relative-paths-to-file | Path to the file to read, relative to the root of the repository that the connector checks out |