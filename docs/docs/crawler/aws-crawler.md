# AWS Crawler
Following are the components of an aws crawler. 
The code for aws crawler lies in **/cloud-validation-framework/realm/awscrawler**. You can find mastersnapshot and mastertest configuration files here. 

AWS Structure is the connector configuration file has information about how to connect to that provider and the credential.
    
### AWS Structure

```json
{
    "organization":"<Company Name>",
    "type":"aws",
    "fileType":"structure",
    "organization-unit":[
        {
            "name":"<Organization Unit Name>",
            "accounts":[
                {
                    "account-name":"<Account Name>",
                    "account-description":"AWS cloud details",
                    "account-id":"<Account ID>",
                    "account-user":"<user email>",
                    "users":[
                        {
                            "name":"<IAM User Name>",
                            "access-key":"<AWS Access Key>",
                            "secret-access":"<AWS Secret Key>",
                            "region":"<region name>",
                            "client":"<client name>"
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
|region|Region where service instance is to be searched(Optional)|us-west-1|
|client|AWS service name(Optional)|EC2, S3 etc|

### Basic Structure of a mastersnapshot

```json
{
    "$schema":"",
    "contentVersion":"1.0.0.0",
    "fileType":"masterSnapshot",
    "snapshots":[
        {
            "source":"<name of connector file>",
            "testUser":"<IAM user name>",
            "projectId":[
                "<your project id>"
            ],
            "nodes":[
                {
                    "masterSnapshotId":"<mastersnapshot id>",
                    "arn":"<your arn>",
                    "collection":"<name of collection in mongo db>",
                    "listMethod":"<list method of service>",
                    "detailMethods":[
                        "<detail method of service>",
                        "<detail method of service>"
                    ]
                }
            ]
        }
    ],
    "type":"aws"
}
```

| Key|Value| Example|
|:---------------- |:------------|:------------|
| masterSnapshotId  |        Name of the snapshot to be used  in test files |     AWS_EC2_01     |
| arn|      It uniquely identify AWS resources. It consists of service name(ec2), region(us-west-2), account id, region id. |    arn:aws:ec2:us-west-1::, <br/> arn:aws:ec2:::,<br/> arn:aws:rds:::,<br/> arn:aws:rds:us-east-1::    |
| collection|        It represents the name of the collection in mongo db. |     ec2     |
| listMethod        |          This includes a list method that can be called on boto client of particular service and returns various ids and other data in reponse. *For example*, describe_instances returns image_id in response along with other data. |      describe_instances      |
| detailMethods     |       Every detail method uses response of list method(id or some other data) and gives detailed information for that particular service. Here describe_images used image_id from list method response and returns detailed image response. |    "describe_instances", "describe_images",                  "describe_volumes"    |

### Sample Mastersnapshot

```json
{
    "$schema":"",
    "contentVersion":"1.0.0.0",
    "fileType":"masterSnapshot",
    "snapshots":[
        {
            "source":"awsStructure",
            "testUser":"<IAM user name>",
            "projectId":[
                "<your project id>"
            ],
            "nodes":[
                {
                    "masterSnapshotId":"AWS_EC2_01",
                    "arn":"arn:aws:ec2:us-west-1::",
                    "collection":"ec2",
                    "listMethod":"describe_instances",
                    "detailMethods":[
                        "describe_instances",
                        "describe_images",
                        "describe_volumes"
                    ]
                }
            ]
        }
    ],
 "type": "aws"
}
```

> <Notetitle>Note:</Notetitle>
>
> If we have two mastersnapshots with same **ARN**, and **detailMethods**, then snapshots for these mastersnapshots will be common with the list of mastersnapshot ids

### Basic mastertest Structure

```json
{
 "$schema": "",
 "contentVersion": "1.0.0.0",
 "fileType": "mastertest",
 "notification": [],
 "masterSnapshot": "awssnapshot",
 "testSet": [
  {
   "masterTestName": "test3",
   "version": "0.1",
   "cases": [
    {
     "masterTestId": "<test id>",
     "rule": "<rule >"
    }
   ]
  }
 ]
}
```

| Key        | Value       | Example |
|:-----------|:------------|:------------|
| cases       |        All the test cases are written under this section |     The json enclosed in cases block (Refer below)    |
| masterTestId     |      The id of the master test case |    AWS_EC2_02    |
| rule       |        Programmatic representation of the rule we want to test |     {AWS_EC2_01}.Reservations[0].Instances[0].SecurityGroups[0].GroupName='launch-wizard-1'     |


### Sample Test

```json
{
    "$schema":"",
    "contentVersion":"1.0.0.0",
    "fileType":"mastertest",
    "notification":[
        
    ],
    "masterSnapshot":"awssnapshot",
    "testSet":[
        {
            "masterTestName":"test3",
            "version":"0.1",
            "cases":[
                {
                    "masterTestId":"AWS_EC2_02",
                    "rule":"{AWS_EC2_01}.Reservations[0].Instances[0].SecurityGroups[0].GroupName='launch-wizard-1'"
                }
            ]
        }
    ]
}
```

### Steps to run aws crawler

- `populate_json lq --file ./realm/awsStructure.json --type structure`: Stores aws srtucture in mongodb collection named structures
- `populate_json crawlertest --dir ./realm/validation/awscrawler`: loads entire directory in mongodb
- `prancer --crawler crawlertest --db FULL`: Generates snapshots from mastersnapshot
- prancer crawlertest --db FULL: Fetches snapshots and runs tests from mastertests on them.

### Support for using multiple services in a single rego test case

Here's the testcase format:

```json  
	{           
      "masterTestId": "AWS_EFS_01_KMS_01_TEST_1",
      "type": "rego",
      "rule": "file(input_efs_kms_1.rego)",
      "masterSnapshotId": ["AWS_EFS_01", "AWS_KMS_01"],
      "eval": "data.rule.rulepass"
    }
```

Here's the rego rule:

	package rule
	default rulepass = false
	rulepass = true{
	    contains(input[AWS_EFS_01].FileSystems[_].KmsKeyId, input[AWS_KMS_01].KeyMetadata.KeyId)
	    input[AWS_KMS_01].KeyMetadata.KeyManager="AWS"
	    }

To include multiple services in a single test case, we need to provide the mastersnapshot Ids of all the services in **masterSnapshotId** in testcase and then access the response using mastersnapshot ids in rego file.