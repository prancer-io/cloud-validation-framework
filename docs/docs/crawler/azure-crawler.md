# Azure Structure

Azure Structure is the connector configuration file has information about how to connect to that provider and the credential.

```json
{
    "filetype": "structure",
    "type": "azure",
    "companyName": "<company-name>",
    "accounts": [
        {
            "department": "<unit/department-name>",
            "subscription": [
                {
                    "subscription_name": "<subscription(account)-name>",
                    "subscription_description": "<subscription(account)-description>",
                    "subscription_id": "<subscription(account)-id>",
                    "users": [
                        {
                            "name": "<username>"
                        }
                    ]
                }
            ]
        }
    ]
}

```

| Key | Value | Example |
|:-----------|:------------|:------------:|
|subscription_name|Azure account(subscription) name|prancer-test|
|subscription_description|Azure account(subscription) description | |
|subscription_id|Azure account(subscription) id | |

## Basic Structure of a mastersnapshot

```json
{
  "fileType": "masterSnapshot",
  "snapshots": [
    {
      "type": "azure",
      "testUser": "<username>",
      "subscriptionId": "<subscription-id>",
      "source": "<Azure-connector-file-name>",
      "nodes": [
        {
          "masterSnapshotId":"<mastersnapshot-id>",
          "type": "<Azure-api-from-azureApiVersions>",
          "collection": "<Collection-name>",
          "version": "<Azure-api-version-from->"
        }
      ]
    }
  ],
  "type": "azure",
}
```

| Key|Value| Example|
|:---------------- |:------------|:------------|
| source| Azure connector file name |azureConnector|
| masterSnapshotId  |        ID of the snapshot to be used  in test files |     AZRSNP_274|
| type| API type from azureApiVersions.json(Supported API types are in azureApiVersions.json)|"Microsoft.Compute/virtualMachines",</br> "Microsoft.Sql/instancePools",</br> "Microsoft.HealthcareApis/services"|
| collection|        It represents the name of the collection in mongo db. |Microsoft.Compute|
| version|API version from azureApiVersions.json(Supported API versions are in azureApiVersions.json)|  2021-07-01|

## Sample Mastersnapshot

```json
{
    "$schema": "",
    "contentVersion": "1.0.0.0",
    "fileType": "masterSnapshot",
    "snapshots": [
        {
            "type": "azure",
            "subscriptionId": "7a19-4458-f038bb7760c1",
            "testUser": "prancer_ro",
            "source": "azureConnector",
            "nodes": [
                {
                    "masterSnapshotId": "AZRSNP_274",
                    "type": "Microsoft.Compute/virtualMachines",
                    "collection": "Microsoft.Compute",
                    "version": "2021-07-01",
                }
            ]
        }
    ]
}
```

> <Notetitle>Note:</Notetitle>
>
> To check the supported  **type**, please check the file **azureApiVersions.json** in our [prancer-hello-world](https://github.com/prancer-io/prancer-hello-world) repository.

## Basic mastertest Structure

```json
{
  "fileType": "mastertest",
  "masterSnapshot": "<master-snapshot-name>",
  "notification": [],
  "testSet": [
    {
      "masterTestName": "<master-test-name>",
      "version": "0.1",
      "cases": [
        {
          "masterTestId": "<master-test-id>",
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
| masterTestId     |      The id of the master test case |    PR-AZR-CLD-KV-001    |
| rule       |        Programmatic representation of the rule we want to test | {PR_AZR_CLD_KV_001}.input.resources[_].properties.enableSoftDelete != true |

## Sample Test

```json
{
  "fileType": "mastertest",
  "masterSnapshot": "mastersnapshot_azure_cloud",
  "notification": [],
  "testSet": [
    {
      "masterTestName": "AZURE_Cloud_TEST",
      "version": "0.1",
      "cases": [
        {
          "masterTestId": "PR-AZR-CLD-KV-001",
          "rule": "{PR_AZR_CLD_KV_001}.input.resources[_].properties.enableSoftDelete != true",
        }
      ]
    }
  ]
}
```

## Steps to run azure crawler

- `populate_json lq --file ./realm/azureStructure.json --type structure`:  Stores gcp srtucture in mongodb collection named structures
- `populate_json crawlertest --dir ./realm/validation/azurecrawler`: loads entire directory in mongodb
- `prancer --crawler crawlertest --db FULL`: Generates snapshots from mastersnapshot
- `prancer crawlertest --db FULL`: Fetches snapshots and runs tests from mastertests on them.

## Support for using multiple services in a single rego test case

Here's the testcase format:

```json  
{           
    "masterTestId": "PR-AZR-CLD-KV-001",
    "type": "rego",
    "rule": "file(iam.rego)",
    "masterSnapshotId": ["AZRSNP_228"],
    "eval": "data.rule.rulepass"
}
```

Here's the rego rule:

	package rule
	default rulepass = false
	rulepass = true{
	    {PR_AZR_CLD_KV_001}.input.resources[_].properties.enableSoftDelete != true}

To include multiple services in a single test case, we need to provide the mastersnapshot Ids of all the services in **masterSnapshotId** in testcase and then access the response using mastersnapshot ids in rego file.
