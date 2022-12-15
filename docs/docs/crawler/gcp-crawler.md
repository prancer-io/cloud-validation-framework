# GCP Structure

GCP Structure is the connector configuration file has information about how to connect to that provider and the credential.

```json
{
    "autoRemediate": true,
    "fileType": "structure",
    "organization":"<company-name>",
    "projects": [
      {
        "project-id": "<project-id>",
        "project-name": "<project-name>",
        "users": [
          {
            "client_email": "<gcp-service-account-email>",
            "client_id": "<client-id>",
            "name": "<company-name>",
            "private_key_id": "<gcp-private-key-id>",
            "private_key" : "<gcp-private-key>",
            "type": "service_account"
          }
        ]
      }
    ],
    "type": "google"
}

```

| Key | Value | Example |
|:-----------|:------------|:------------:|
|client_email|GCP service account email|1131198831-compute@developer.gserviceaccount.com|
|client_id|GCP service account client-id for the perticular service account |123456789012345678901|

## Basic Structure of a mastersnapshot

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

| Key|Value| Example|
|:---------------- |:------------|:------------|
| source| GCP connector file name |googleConnector|
| project-id        |Project Id from the GCP console|      my-project-1234567890      |
| masterSnapshotId  |        Name of the snapshot to be used  in test files |     GOOGLE_PROJECTS_IAM|
| type| API type from googleParams.json/GoogleApis(Supported API types are in googleParams.json)|"compute/projects.list",</br> "gcp.services.list",</br> "projects.accounts.list"|
| get_method|Get API methods from the googleParams.json/GoogleGetApis. </br>There can be multiple value.(Supported API types are in googleParams.json)|    "cloudresourcemanager/projects.getIamPolicy",</br> "serviceusage/gcp.services.get", </br> "iam/projects.accounts.get"    |
| collection|        It represents the name of the collection in mongo db. |     project_iam_user|
| service|        It represents the name of the service in GCP. |     compute|

## Sample Mastersnapshot

```json
{
  "contentVersion": "1.0.0.0",
  "fileType": "masterSnapshot",
  "snapshots": [
    {
      "type": "google",
      "source": "googleConnector",
      "testUser": "<IAM username>",
      "project-id":"<your project id>",
      "nodes": [
        {
          "masterSnapshotId": "GOOGLE_PROJECTS_IAM",
          "type": "compute/projects.list",
          "get_method": ["cloudresourcemanager/projects.getIamPolicy"],
          "collection": "project_iam_user",
          "tags": [
            {
              "cloud": "GCP",
              "service": [
                "compute"
              ]
            }
          ]
        }
      ]
    }
  ],
 "type": "google"
}
```

> <Notetitle>Note:</Notetitle>
>
> Here, **get_method** attribute is only required for limited api types. To check the supported get api for **get_method**, please check the file **googleParams.json/GoogleGetApis** in our [prancer-hello-world](https://github.com/prancer-io/prancer-hello-world) repository.

## Basic mastertest Structure

```json
{
  "contentVersion": "1.0.0.0",
  "fileType": "mastertest",
  "masterSnapshot": "master-snapshot",
  "notification": [],
  "testSet": [
    {
      "masterTestName": "<master-test-name>",
      "version": "0.1",
      "cases": [
            {
            "masterTestId": "<test id>",
            "rule": "<rule>"
            }
        ]
    }
  ]
}
```

| Key        | Value       | Example |
|:-----------|:------------|:------------|
| cases       |        All the test cases are written under this section |     The json enclosed in cases block (Refer below)    |
| masterTestId     |      The id of the master test case |    PR-GCP-CLD-PRIF-001    |
| rule       |        Programmatic representation of the rule we want to test |     {PR_GCP_CLD_PRIF_001}.input[0].commonInstanceMetadata.items[0].key='enable-oslogin'     |


## Sample Test

```json
{
  "contentVersion": "1.0.0.0",
  "fileType": "mastertest",
  "masterSnapshot": "master-snapshot",
  "notification": [],
  "testSet": [
    {
      "masterTestName": "TEST_CLOUD_GOOGLE",
      "version": "0.1",
      "cases": [
            {
            "masterTestId": "PR-GCP-CLD-PRIF-001",
            "rule": "{PR_GCP_CLD_PRIF_001}.input[0].commonInstanceMetadata.items[0].key='enable-oslogin'"
            }
        ]
    }
  ]
}
```

## Steps to run gcp crawler

- `populate_json lq --file ./realm/gcpStructure.json --type structure`:  Stores gcp srtucture in mongodb collection named structures
- `populate_json crawlertest --dir ./realm/validation/gcpcrawler`: loads entire directory in mongodb
- `prancer --crawler crawlertest --db FULL`: Generates snapshots from mastersnapshot
- `prancer crawlertest --db FULL`: Fetches snapshots and runs tests from mastertests on them.

## Support for using multiple services in a single rego test case

Here's the testcase format:

```json  
{           
    "masterTestId": "PR-GCP-CLD-PRIF-001",
    "type": "rego",
    "rule": "file(iam.rego)",
    "masterSnapshotId": ["GOOGLE_PROJECT_INFO"],
    "eval": "data.rule.rulepass"
}
```

Here's the rego rule:

	package rule
	default rulepass = false
	rulepass = true{
	    contains(input.commonInstanceMetadata.items[_].key, "enable-oslogin")
	    lower(input.commonInstanceMetadata.items[_].value) == "false"}

To include multiple services in a single test case, we need to provide the mastersnapshot Ids of all the services in **masterSnapshotId** in testcase and then access the response using mastersnapshot ids in rego file.
