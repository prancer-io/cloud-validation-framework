This snapshot configuration file type is used along with the **AWS** connector. It allows you to take snapshots of ReST api calls to the **AWS** api.

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> As of now, the response of the api is always an array of items and this makes the testing a little more complex than expected. We are working on a fix!

# Snapshot configuration file

To setup an **AWS** snapshot configuration file, copy the following code to a file named `snapshot.json` in your container's folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `snapshot.json`

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "awsConnector",
                "testUser": "<iam-user>",
                "nodes": [
                    {
                        "snapshotId": "<snapshot-name>",
                        "type": "<type-of-node>",
                        "collection": "<collection-name>",
                        "region": "<region>",
                        "client": "EC2",
                        "id": {
                            <selectors>
                        }
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| iam-user | Name of the **IAM** user, must be present in **AWS** connector file |
| snapshot-name | Name of the snapshot, you will use this in test files |
| type-of-node | Type of resource being queried for, see below for more information |
| collection-name | Name of the **MongoDB** collection used to store snapshots of this file |
| selectors | A complex object that defines what it is you want to extract and snapshot, see below for more information |
| region | Region of the instance (Optional). Overrides the region provided in Connector File. |
| client | Type of client AWS client (Optional). Overrides the client provided in Connector File. |

# Types of nodes

The **type-of-node** parameter refers to a very wide list. Let's see how the **AWS** connector works to know how to properly set it up!

The **AWS** connector is a wrapper around the **AWS** ReST api. You can also use the **AWS cli** with the exact same approach. **Prancer** will call `aws ec2 describe-xyz` operations on the api and simply substitute the `xyz` for the **type of node**. For example:

| What you need | Type of node |
|---------------|--------------|
| EC2 machine details | instances | 
| Subnets of a VPC | subnets |
| Key pairs for EC2 instanciations | key_pairs |
| Security groups | security_groups |

The important part to remember is that if you find an `aws ec2 cli` describe operation, we'll build the corresponding describe operation for you using the type of node. If you find the describe operation in the **AWS cli**, just change the hyphens `-` for underscores `_` and we'll do the rest.

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> Note: We are in the process of re-thinking our approach for the **AWS** connector. We'll adopt a more flexible approach soon so you can query any kind of service and not just EC2 services.

In case you client does not have a describe method. Like in case of S3, then this field should be populated with the method that has from the boto3 client object.

# Selectors

Selectors are necessary because a node can only be 1 item at a time. To properly describe the result that should be snapshotted, you need to give parameters in the selector block that will identify a single unique resource produced by the describe operation.

The `id` block will contain different parameters that are specific to the `describe-xyz` operation being used. To know what to use, just lookup the **AWS cli** describe operation on the **AWS** documentation and look at the parameters. Any parameter that you can pass to the command line tool can be used in there but you need to use a "PascalCase" version of it. Here are a few examples:

| Type of node | Cli version | Prancer version | Example value |
|--------------|-------------|-----------------|---------------|
| instances | --instance-ids | InstanceIds | `["i-3945hf923h492345h"]` |
| vpcs | --vpc-ids | VpcIds | `["vpc-3923h492345h"]` |
| security_groups | --group-ids | GroupIds | `["sg-3h492345h"]` |

# Using filters

**AWS** selectors will often feature filters. You can also leverage this from **Prancer**. A common reason to use `Filters` in the `id` block is to query using tags which makes more sense than using fixed ids. This is especially true when using infrastructure frameworks such as **Terraform** or **CloudFormation**.

To use filters, add and format a `Filters` node in the `id` node using the following example:

    "id": {
        "Filters": [
            {
                "Name": "tag:aws:cloudformation:stack-name",
                "Values": ["some-stack"]
            },
            {
                "Name": "tag:aws:cloudformation:logical-id",
                "Values": ["resource-name"]
            }
        ]
    }

