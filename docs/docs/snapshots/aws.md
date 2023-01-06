# Snapshot configuration file

The aws snapshot configuration file type is used along with the **AWS** connector. It allows you to take snapshots of ReST API calls to the **AWS** API.
To setup an **AWS** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

```json
    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "<connector-name>",
                "type": "aws",
                "testUser": "<iam-user>",
                "accountId": "<account-id>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "arn": "<resource-arn>",
                        "collection": "<collection-name>",
                        "listMethod": "<list-method>",
                        "detailMethods": [
                                    "<list-of-detail-methods>"
                                ]
                    }
                ]
            }
        ]
    }
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| connector-name | Name of the **AWS** connector file |
| iam-user | Name of the **IAM** user, must be present in **AWS** connector file |
| account-id | Name of the **IAM** account id, must be present in **AWS** connector file |
| snapshot-name | Name of the snapshot, you will use this in test files |
| resource-arn | AWS resource ARN you want to monitor |
| collection-name | Name of the **MongoDB** collection used to store snapshots of this file |
| list-method | the name of the AWS function which lists all the available resources. review `AWS SDK for Python` for more info. |
| list-of-detail-methods | a list of detail methods to get the attribute of the resource. review `AWS SDK for Python` for more info. |


## AWS Resource ARN
Amazon Resource Names (ARNs) uniquely identify AWS resources. We require an ARN when you need to specify a resource unambiguously in a snapshot configuration file. To understand more about ARN, you can [read AWS official documentations](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)

# Master Snapshot Configuration File
Master Snapshot Configuration File is to define **resource types**. We do not have individual resources in the Master Snapshot Configuration File, instead we have the type of resources.
**Prancer** validation framework is using the Master Snapshot Configuration File in the crawler functionality to find new resources.
To setup an **AWS** master snapshot configuration file, copy the following code to a file named `masterSnapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `masterSnapshot.json`

```json
{
    "fileType": "masterSnapshot",
    "snapshots": [
        {
            "type": "aws",
            "testUser": "<iam-user>",
            "accountId": "<account-id>",
            "nodes": [
                {
                    "masterSnapshotId": "<master-snapshot-name>",
                    "arn": "<resource-arn>",
                    "collection": "snapshot-collection",
                    "listMethod": "<list-method>",
                    "detailMethods": [
                        "<list-of-detail-methods>"
                    ]
                }
            ]
        }
    ]
}
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | Value Description |
|-----|-------------------|
| connector-name | Name of the **AWS** connector file |
| iam-user | Name of the **IAM** user, must be present in **AWS** connector file |
| account-id | Name of the **IAM** account id, must be present in **AWS** connector file |
| master-snapshot-name | Name of the master snapshot, you will use this in master test files |
| resource-type-arn | AWS resource type ARN you want to monitor |
| collection-name | Name of the **MongoDB** collection used to store snapshots of this file |
| list-method | the name of the AWS function which lists all the available resources. review `AWS SDK for Python` for more info. |
| list-of-detail-methods | a list of detail methods to get the attribute of the resource. review `AWS SDK for Python` for more info. |


## AWS Resource Type ARN
Amazon Resource Names (ARNs) uniquely identify AWS resources. We require a resource type ARN when you need to specify a resource type unambiguously in a master snapshot configuration file. 
The resource type ARN is not a complete ARN, it is a subset of a full ARN which provides a list of resources rather than an individual resource. 
This is an example of a resource type ARN:

    "arn": "arn:aws:ec2:us-west-1::"

notice that this is **not a complete ARN**.

To understand more about ARN, you can [read AWS official documentations](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)

# AWS SDK for Python
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2. You can find the latest, most up to date, [documentation at Boto3 site](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), including a list of services that are supported.
Prancer validation framework use Boto3 library to list AWS resources and get the detail of those resources. In AWS Snapshot configuration file **listMethod** and **detailMethods** attribute values are name of the Boto3 functions from [Available Services](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html).

 > - **listMethod** is a method which capable of output a list of resources in ARN format.
 >
 > - **detailMethod** is a method which capable of accepting ARN as an input and output a json detail of a specific resource.
For example, if I want to get information of the AWS instances, i can use  `EC2.Client.describe_instances` function of the Boto3 framework. The function details are [available here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances). My snapshot will look like this:

```json
{
    "snapshotId": "AWS_EC2_01",
    "arn": "arn:aws:ec2:us-east-2:128391368173667260:instance/i-0e7679edefaf34e00",
    "collection": "ec2",
    "listMethod": "describe_instances",
    "detailMethods": [
    "describe_instances"
    ]
}
```

It is possible to use multiple `detailMethods` here if the attributes we are looking for are from multiple detailed functions. For example:

```json
{
    "snapshotId": "AWS_EC2_01",
    "arn": "arn:aws:ec2:us-east-2:128391368173667260:instance/i-0e7679edefaf34e00",
    "collection": "ec2",
    "listMethod": "describe_instances",
    "detailMethods": [
    "describe_instances",
    "monitor_instances",
    "describe_account_attributes"
    ]
}
```

you can see here we are using three Boto3 functions to get all the attributes we want for the EC2 instance. The result of those detailed functions will be merged in to one JSON file as a snapshot available for tests.