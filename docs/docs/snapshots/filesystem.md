The Filesystem snapshot configuration file type is used along with the **filesystem** connector. It allows you to take snapshots of an entire file as a resource to test.

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
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "<file-type>",
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
| name-of-connector | name of the **filesystem** connector configuration file |
| snapshot-name | Name of the snapshot, you will use this in test files. The snapshot name should be unique |
| file-type | type of the file. it could be `json` or `yaml` |
| collection-name | Name of the **NoSQL** database collection used to store snapshots of this file |
| relative-path-to-file | Path to the file to read, relative to the root of the repository that the connector checks out |

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
                "nodes": [
                    {
                        "masterSnapshotId": "<master-snapshot-name>",
                        "type": "<file-type>",
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
| name-of-connector | name of the **filesystem** connector configuration file |
| master-snapshot-name | Name of the snapshot, you will use this in test files |
| file-type | type of the file. it could be `json` or `yaml` |
| collection-name | Name of the **NoSQL** database collection used to store snapshots of this file |
| relative-path-to-file | Path to the file to read, relative to the root of the repository that the connector checks out |