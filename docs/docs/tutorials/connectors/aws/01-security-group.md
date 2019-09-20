This tutorial will show you all the steps required to write a basic test that connects to **AWS** and validates that a security group's ip ranges havn't changed.

Before taking this tutorial, you will need to follow some more generic steps:

1. First, let's [install Prancer](../../../installation.md)
2. Next, let's [configure a project](../../../configuration/basics.md)
3. Finaly, let's [connect to AWS](../../../connectors/aws.md)

Then, you can follow these steps:

1. Setup the monitored **AWS** environment
2. Create the snapshot configuration file
3. Create the test case
4. Run the tests
5. Trigger a failure
6. Cleanup and rejoice

# Setup the monitored AWS environment

To run tests against an environment, well, you need an environment. To create the environment that we'll work with, we'll use a simple custom **CloudFormation** template.

Copy the following code into a **YAML** file called `prancer-security-group-tutorial.yml`:

> <NoteTitle>Note</NoteTitle>
>
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
                SecurityGroupIngress:
                    - 
                        IpProtocol: tcp
                        FromPort: 22
                        ToPort: 22
                        CidrIp: 200.200.200.200/32
                    - 
                        IpProtocol: tcp
                        FromPort: 22
                        ToPort: 22
                        CidrIp: 172.16.0.0/16

Now, let's create that **CloudFormation** stack:

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `Create a new stack`.
2. Upload the file we created by choosing `Upload a template to Amazon S3` and click `Next`.
3. Give your stack a simple name such as `tutorial` and click `Next`.
4. Skip to the bottom and click `Next`.
5. Skip to the bottom and click `Create`.
6. Wait for **CloudFormation** to finish it's job. Once you see that the stack has been created, you can move on.

# Create the snapshot configuration file

Now that we have our environment set up for testing, we'll need a snapshot configuration file. 

The snapshot configuration file is used to specify which resources we want to work on for the test suite. You might have a lot of resources already created and not everything is meant to be validated.

Copy the following content to a file named `validation/container1/snapshot.json` and replace the `<iam-user>` and `<security-group-id>` with the proper values that you can find in the **EC2 AWS console** or **VPC AWS console**:

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "awsConnector",
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

For more information on the structure of snapshot configuration files, please refer to the [Snapshot documentation](../../../snapshots/aws.md).

# Create the tests

The next step is to create the tests that will validate your snapshot. A test file is a **JSON** file that describes the tests that need to run on the snapshot you previously defined.

Copy the following content to a file named `validation/container1/test.json`:

    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Ensure ip ranges",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "count({1}.SecurityGroups[0].IpPermissions[0].IpRanges)=2"
                    }
                ]
            }
        ]
    }

> <NoteTitle>Note</NoteTitle>
>
> Remember to use `'` in rules because **JSON** wraps strings using `"`

This test set contains only 1 test called "Ensure ip ranges". It uses the snapshot id 1 and digs into the data to ensure that the ip permission ranges is properly accounted for.

# Run the tests

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase:

    prancer container1

Once this has run, you can find a `validation/container1/output-test.json` in the container folder and a log file in the `log/` folder.

The exit code of the tool should reflect the status of the tests. 

* If any test fail, the tool will return an exit code of 1. 
* If all tests pass, it will return an exit code of 0.

If you end up with failed tests, you can look at the `validation/container1/output-test.json` to figure out what went wrong. The output file is again another **JSON** file and it will contain details of each test.

Most of the time, the file will contain sensibly the same information that you would have had in a test file. If you re-run the test, the `validation/container1/output-test.json` file is lost.

> <NoteTitle>Notes: Good practices</NoteTitle>
>
> In a continuous improvement scenario, you should store all `validation/*/output-test.json` into an artifact system for later reference. This is especialy important in failure scenarios to ensure you keep a track of what failed.

# Triggering a failure

Now that we have passing tests, let's trigger a simple failure to see how everything fits together. To achieve this, we'll need to create a configuration drift, that is, change something in the infrastructure that doesn't match the expected infrastructure tests.

First, let's change our infrastructure to create a configuration drift.

1. Login to your [EC2 AWS console](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SecurityGroups)
2. Find the security group named `prancer-tutorial-sg`
3. Change to the `Inbound tab` and click `Edit`
4. Delete the rule about `200.200.200.200/32` about SSH and save
5. Run the tests again using `prancer container1`
5. Check the results: `echo $?`

You should have a failing state proving that the drift was indeed detected.

# Cleanup your AWS resources

If you followed this tutorial without altering the resources to create, then nothing should cost you anything over time, but let's just go back to **CloudFormation** and destroy the stack to make sure. *(It is a good habit when testing things)*

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `tutorial` stack.
2. Click on the `Actions` drop down and click `Delete stack`.
3. Confirm the deletion.
4. Wait for the operation to complete.

# Conclusion

That's it, you are done. You now know how to write a basic `Prancer` test related to an existing `AWS` infrastructure.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!