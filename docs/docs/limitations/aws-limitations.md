This page describes limitations when using the **AWS** connector/resources in general but proposes solutions or workarounds.

# Limitations

There are known limitations that we are addressing as of today regarding the beta support of **AWS** resources:

1. Most if not all responses yield an array of items even if the query specifies only one item
2. You can only work with **EC2** based queries
3. There are no easy way to filter by tags
4. We do not support stacks naturally yet, therefore, it is slightly complex to use **Prancer** with them but scroll down to see temporary solutions

# Most if not all responses yield an array of items

Here is an example of what the **JSON** structure of most if not all **AWS** resources look like:

```json
    {
        "ResponseMetadata": {
            "HTTPHeaders": {
                "content-length": "1042",
                "content-type": "text/xml;charset=UTF-8",
                "date": "Mon, 15 Apr 2019 13:15:27 GMT",
                "server": "AmazonEC2"
            },
            "HTTPStatusCode": 200,
            "RequestId": "e0806089-4215-479c-99b3-87f5a52bb273",
            "RetryAttempts": 0
        },
        "SecurityGroups": [
            {
                "Description": "prancer-tutorial-sg",
                "GroupName": "prancer-tutorial-sg",
                "IpPermissions": [],
                "OwnerId": "667095293603",
                "GroupId": "sg-0125a7610cd1dd391",
                "IpPermissionsEgress": [
                    {
                        "IpProtocol": "-1",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": []
                    }
                ],
                "VpcId": "vpc-050b8b70e3593efd2"
            }
        ]
    }
```

As previously stated, you can see a section in this snapshot called `ResponseMetadata`. This is an artifact of the api that appears for now in beta but should not appear in later versions of the container.

Next you can see an array called `SecurityGroups`. This portion will change based on the described resource but will always be an array if you use a multi-resource description operation like `security_groups`. Almost all **EC2** describe operations are for collections of resources but other services might have a non collection describe operation.

To access the element, you should use the array operator to return the element. This makes your rules heavier but until we move out of beta for the **AWS** connector, you will have to do this:

    {snapshot-name}.SecurityGroups[0]

# You can only work with EC2 based queries

The way node types work in snapshot configuration files for the beta version limits you to using only operations that are on the **EC2** service **and** you can only use `describe-xyz` operations instead of any operation you want.

We are considering using a different approach that will allow you to use any service and any operation you want. 

There are no workarounds for this problem yet.

# There are no easy way to filter by tags

A lot of DevOps out there will want to use tags to filter and manage their **AWS** resources and we are aware of this. The initial **AWS** connector concept did not take this into account and thus there is no easy way to filter with tags right now.

This doesn't mean you can't use tags in your filters but it will be harder. If you have used **AWS** cli or api before, you know that most if not all cli/api endpoints support a `Filters` parameter. This allows you to filter using **many** different parameters that are not necessarily coded directly as options to the api.

To use tags, you will need to leverage `Filters`. Here is a simple, one tag example:

    "id": {
        "Filters": [
            {
                "Name": "tag:mytag",
                "Values": ["myvalue"]
            }
        ]
    }

This pretty much amounts to using the same filtering mechanism used in the **AWS** api or cli that would look like:

    aws ec2 describe-security-groups --filters Name=tag:mytag,Values=myvalue

If you wanted to have more than one tag you just need to add more tag definitions to the `Filters` array like so:

    "id": {
        "Filters": [
            {
                "Name": "tag:mytag",
                "Values": ["myvalue"]
            },
            {
                "Name": "tag:anothertag",
                "Values": ["anothervalue"]
            }
        ]
    }

Just remember that all filters are applied at once, all filters must pass for an item to be returned.

# Working with stacks in snapshot configuration files

Because the **AWS** connector is not ready to work with stacks and **CloudFormation** in a native way, we have to work a little harder to extract **CloudFormation** resources properly through the use of **CloudFormation** tags. Thankfully, we have a workaround for tags thus, it isn't much harder to work with **CloudFormation** resources.

**CloudFormation** exposes several tags to you when you create a stack. With those tags, you can select the proper resource you want to inspect:

| Tag | What it is used for |
|-----|---------------------|
| aws:cloudformation:stack-name | Name of the stack that you are looking for |
| aws:cloudformation:logical-id | Name of the resource in the **CloudFormation** template |

So a simple example would be:

    "id": {
        "Filters": [
            {
                "Name": "tag:aws:cloudformation:stack-name",
                "Values": ["tutorial"]
            },
            {
                "Name": "tag:aws:cloudformation:logical-id",
                "Values": ["PrancerTutorialSecGroup"]
            }
        ]
    }