# Snapshot configuration file

The Google snapshot configuration file type is used along with the **Google** connector. It allows you to take snapshots of ReST API calls to the **Google Cloud Platform** API.

To setup an **GCP** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

```json
    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "<GCP-Connector>",
                "testUser": "<service-account>",
                "project-id": "<project-id>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "<resource-provider>",
                        "collection": "<collection-name>",
                        "path": "<selfLink>",
                        "status": "active",
                        "validate": true
                    }
                ]
            }
        ]
    }
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| GCP-connector | Name of the **GCP Connector** file you want to use to connect to GCP backend |
| service-account | Name of the **service account**  to connect to the GCP backend, must be present in the **GCP** connector file |
| project-id | Id of the project to inspect, must be the same as the one described in the **GCP** connector file |
| snapshot-name | Name of the snapshot, you will use this in test files. This name should be unique in the container |
| resource-provider | Type of resource being queried for, see below for more information |
| collection-name | Name of the **NoSQL** db collection used to store snapshots of this file |
| selfLink | Server-defined URL for the resource, see selfLink below |
| status | status of the resource. It can be active or inactive |
| validate | Boolean. resource validation |

### Google Resource Provider



### selfLink

selfLink is a GCP Server-defined URL for each resource. For example:

    "selfLink": "projects/learning-123/zones/us-central1-a/instances/instance-1"

# Master Snapshot Configuration File
Master Snapshot Configuration File is to define **resource types**. We do not have individual resources in the Master Snapshot Configuration File, instead we have the type of resources.
Prancer validation framework is using the Master Snapshot Configuration File in the crawler functionality to find new resources.

```json
{
  "contentVersion": "1.0.0.0",
  "fileType": "masterSnapshot",
  "snapshots": [
    {
      "type": "google",
      "source": "<name-of-connector-file>",
      "testUser": "<test-username>",
      "project-id": "<project-id>",
      "nodes": [
        {
          "masterSnapshotId": "<mastersnapshot-id>",
          "type": "<list-api-from-googleParmas>",
          "get_method": ["<get-api-from-googleParams-if-there-is-any>"],
          "collection": "<name of collection in mongo db>",
          "tags": [
            {
              "cloud": "GCP",
              "service": [
                "<GCP-service-name>"
              ]
            }
          ]
        }
      ]
    }
  ],
  "type":"google"
}
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Key|Value| Example|
|:---------------- |:------------|:------------|
| source| GCP connector file name |googleConnector|
| project-id        |Project Id from the GCP console|      my-project-1234567890      |
| masterSnapshotId  |        Name of the snapshot to be used  in test files |     GOOGLE_PROJECTS_IAM|
| type| API type from googleParams.json/GoogleApis(Supported API types are in googleParams.json)|"compute/projects.list",</br> "gcp.services.list",</br> "projects.accounts.list"|
| get_method|Get API methods from the googleParams.json/GoogleGetApis. </br>There can be multiple value.(Supported API types are in googleParams.json)|    "cloudresourcemanager/projects.getIamPolicy",</br> "serviceusage/gcp.services.get", </br> "iam/projects.accounts.get"    |
| collection|        It represents the name of the collection in mongo db. |     project_iam_user|
| service|        It represents the name of the service in GCP. |     compute|

> <Notetitle>Note:</Notetitle>
>
> Here, **get_method** attribute is only required for limited api types. To check the supported get api for **get_method**, please checkout **GoogleGetApis** in **googleParams.json** in our [prancer-hello-world](https://github.com/prancer-io/prancer-hello-world) repository.
