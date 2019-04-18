# Tutorial - Security group monitoring in AWS

This tutorial will show you all the steps required to write a basic test that connects to AWS and validates that a security group's name hasn't changed.

Before taking this tutorial, you will need to follow some steps in other more generic tutorials:

1. First, let's [setup the `Prancer` environment](../common/01-setup-the-prancer-environment.md)
2. Next, let's [setup a `Prancer` project](../common/02-setup-a-prancer-project.md)
3. Finaly, let's [connect to `AWS`](../common/03-connect-to-aws.md)

Then, you can follow these steps:

1. Setup the monitored AWS environment
2. Create the snapshot configuration
3. Create the test case
4. Run the tests
5. Trigger a failure
6. Cleanup and rejoice

## Setup the monitored AWS environment

To run tests against an environment, well, you need an environment. To create the environment that we'll work with, we'll use a simple custom `CloudFormation` template.

Copy the following code into a `YAML` file called `prancer-security-group-tutorial.yml`:

> It doesn't need to be in your project folder, it can be in a discardable temporary directory if you want.

    Resources:
        PrancerTutorialVPC:
            Type: AWS::EC2::VPC
            Properties:
                CidrBlock: 172.16.0.0/16
                EnableDnsSupport: true
                EnableDnsHostnames: true
                InstanceTenancy: default
        PrancerTutorialSecGroup:
            Type: AWS::EC2::SecurityGroup
            Properties: 
                GroupName: prancer-tutorial-sg
                GroupDescription: Simple SG to demonstrate Prancer framework
                VpcId: !Ref PrancerTutorialVPC

Now, let's create that `CloudFormation` stack:

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `Create a new stack`.
2. Upload the file we created by choosing `Upload a template to Amazon S3` and click `Next`.
3. Give your stack a simple name such as `tutorial` and click `Next`.
4. Skip to the bottom and click `Next`.
5. Skip to the bottom and click `Create`.
6. Wait for `CloudFormation` to finish it's job. Once you see that the stack has been created, you can move on.

## Create the snapshot configuration

Now that we have our environment set up for testing, we'll need a snapshot configuration file. 

The snapshot configuration file is used to specify which resources we want to work on for the test suite. You might have a lot of resources already created and not everything is meant to be validated.

Copy the following content to a file named `validation/container1/snapshot.json` and replace the <iam-user> and <security-group-id> with the proper values that you can find in the `EC2 AWS console` or `VPC AWS console`:

    {
        "snapshots": [
            {
                "source": "tutorial",
                "type": "aws",
                "testUser": "<iam-user>",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "security_groups",
                        "collection": "security_groups",
                        "id": {
                            "GroupIds": [
                                "<security-group-id>"
                            ]
                        }
                    }
                ]
            }
        ]
    }

> It is important to use strings as snapshot ids because the testing framework will not match the braced identifiers to snapshots if they are integers in your snapshot configuration file.

For more information on the structure of snapshot files, please refer to the [Snapshot documentation](http://www.prancer.io/documentation/?section=snapshot).

### More info: What is this `id` section?

If you have you ever used the `AWS CLI` then, head to the [latest AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference) documentation to learn more about it.

`Prancer` uses the `AWS CLI/api` to communicate with your `AWS` infrastructure. Anything you can pass to those commands can be passed into the `id` object:

    "id": {
        // Insert stuff here
    }

When you add fields to the `id` object, you append additional parameters to the api call. For example: 

    "id": {
        "GroupIds": [
            "sg-0e11620b9a9660278"
        ]
    }

Is the equivalent of using the `AWS CLI` like so:

    aws ec2 describe-security-groups --group-ids sg-0e11620b9a9660278

### Tips and tricks: Using `tags` in the `id` section

You can also use the `id` object to refer to tags instead of specific ids. Beware though that the result of a snapshot resource **`must always be 1 item`**.

Here is an example of a tag based research:

    "id": {
        "Filters": [
            {
                "Name": "tag:mytag",
                "Values": ["myvalue"]
            }
        ]
    }

This is the equivalent of calling the same command on the command line:

    aws ec2 describe-security-groups --filters Name=tag:mytag,Values=myvalue

And it will return the resources that match those filters.

In a more evolved scenario, you will want to use more tags to pin point one exact resource. For example, in a multiple security group scenario generated using a complex CloudFormation template, you could use the following approach:

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

Which translates into calling:

    aws ec2 describe-security-groups --filters Name=tag:aws:cloudformation:stack-name,Values=tutorial Name=tag:aws:cloudformation:logical-id,Values=PrancerTutorialSecGroup

## Create the tests

The next step is to create the tests that will validate your snapshot. A test file is a `JSON` file that describes the tests that need to run on the snapshot you previously defined.

Copy the following content to a file named `validation/container1/test.json`:

    {
        "fileType": "test",
        "snapshot": "snapshot.json",
        "testSet": [
            {
                "testName ": "Ensure Name",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "{1}.SecurityGroups[0].GroupName='prancer-tutorial-sg'"
                    }
                ]
            }
        ]
    }

> Remember to use single quotes `'` in rules because `JSON` wraps strings using double quotes `"`

This test set contains only 1 test called "Ensure Name" exists. It uses the snapshot id 1 and digs into the data to ensure that the GroupName is properly set.

### More info: Rule structure

A rule is the most important part of the test. It specifies what to use to run the test.

A test rule is usually a comparison operator such as `=` and should feature a `left hand side` operator (`LHS`) and a `right hand side` operator (`RHS`). The system will parse this rule and create references to the items that are represented in braces such as `{1}`.

These `{1}{2}{3}{4}...` are references to the snapshot ids that you set in the `snapshot.json` file that lives beside the `test.json` file.

> Mentioning this again, in the `snapshot.json` files, ensure you are using `string` based snapshot ids.

### More info: What fields can you use in rules?

If you connect to the `MongoDB` server using `mongo` and then issue the following commands:

    use validator
    db.security_groups.find().pretty()

You should end up with a result set with the data you can use in your rules. 

> If you don't have any result in `MongoDB`, just exit the `mongo` client and run:
>
>       validator container1
>
> This will trigger a test, snapshot your system and put data inside the `MongoDB` server.

This data contains a lot of metadata but the most important part is the `json` field part. This is what the rule will operate over. For example:

    "json" : {
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

In this data, you can see that there is a section `SecurityGroups` that is an `Array`. You can use the following rule to validate something from it:

    {1}.SecurityGroups[0].GroupName='prancer-tutorial-sg'

When a value in the json is an array, you can use the array notation to get a certain element. Even better, you can even use selectors like:

    {1}.SecurityGroups['GroupId'='sg-0125a7610cd1dd391'].GroupName='prancer-tutorial-sg'

This last example isn't really useful as you want to avoid hardcoding ids in your configuration files but it is an example of what you can do with it in more complex scenarios.

### More info: Rule functions and operators

Rules are not only about comparing for equality. You can use rules in a rather complex way using functions. For example:

| function | note |
| -------- | ---- |
| exists(x) | Checks that the operand exists, returns a boolean |
| count(x) | Returns the count of the operand when it is an `Array` |

Another thing you can do is use operators to create mathematical expressions. You can add, subtract, multiply, divide. For example:

    {1}.somevalue + {2}.somevalue = 20

That is a perfectly valid rule!

## Run the tests

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase:

    validator container1

Once this has run, you can find a `validation/container1/output-test.json` in the container folder and a log file in the `log/` folder.

The exit code of the validator should reflect the status of the tests. 

* If any test fail, the validator will return an exit code of 1. 
* If all tests pass, it will return an exit code of 0.

If you end up with failed tests, you can look at the `validation/container1/output-test.json` to figure out what went wrong. The output file is again another `JSON` file and it will contain details of each test.

Most of the time, the file will contain sensibly the same information that you would have had in a test file. If you re-run the test, the `validation/container1/output-test.json` file is lost.

> In a continuous improvement scenario, you should store all `validation/*/output-test.json` into an artifact system for later reference. This is especialy important in failure scenarios to ensure you keep a track of what failed.

## Triggering a failure

Now that we have passing tests, let's trigger a simple failure to see how everything fits together. To achieve this, we'll need to create a configuration drift, that is, change something in the infrastructure that doesn't match the expected infrastructure tests.

First, let's change our infrastructure to create a configuration drift.

1) Login to your [EC2 AWS console](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SecurityGroups)
2) Find the security group named `prancer-tutorial-sg`
3) Change it's name to `prancer-tut-sg`
4) Run the tests again

        validator container1

5) Check the results

        echo $?

You should have a failing state proving that the drift was indeed detected.

## Cleanup your AWS resources

If you followed this tutorial without altering the resources to create, then nothing should cost you anything over time, but let's just go back to `CloudFormation` and destroy the stack to make sure. *(It is a good habit when testing things)*

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `tutorial` stack.
2. Click on the `Actions` drop down and click `Delete stack`.
3. Confirm the deletion.
4. Wait for the operation to complete.

## Conclusion

That's it, you are done.

Thank you for completing this tutorial on `Prancer`.

We hope to see you in the next tutorial!