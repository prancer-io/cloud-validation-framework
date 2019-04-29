# Tutorial - Testing values in CloudFormation templates

This tutorial will show you all the steps required to write a basic test that connects to a `Git` repository and validates that the information in a `CloudFormation` template written in `JSON` (Only `JSON` supported for now) features the proper values.

Before taking this tutorial, you will need to follow some steps in other more generic tutorials:

1. First, let's [setup the `Prancer` environment](../common/01-setup-the-prancer-environment.md)
2. Next, let's [setup a `Prancer` project](../common/02-setup-a-prancer-project.md)

Then, you can follow these steps:

1. Setup the monitored GIT environment
2. Create the snapshot configuration
3. Create the test case
4. Run the tests
5. Trigger a failure
6. Cleanup and rejoice

## Setup the monitored `Git` environment

To run tests against a `Git` repository, well, you need a `Git` repository with files in it. This portion will create such as repository, commit files to it and then configure the `Git` connector for that specific repository and project.

First of all, create a project folder and copy the following code into a `JSON` file called `prancer-security-group-tutorial.json`:

> This part should not be done in your project folder, it should be in a discardable temporary directory.

    {
        "Resources" : {
            "PrancerTutorialVpc": {
                "Type": "AWS::EC2::VPC",
                "Properties": {
                    "CidrBlock": "172.16.0.0/16",
                    "EnableDnsSupport": true,
                    "EnableDnsHostnames": true,
                    "InstanceTenancy": "default"
                }
            },
            "PrancerTutorialSecGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupName": "prancer-tutorial-sg",
                    "GroupDescription": "Slightly more complex SG to show rule matching",
                    "VpcId": {
                        "Ref": "PrancerTutorialVpc"
                    },
                    "SecurityGroupIngress": [
                        {
                            "CidrIp" : "0.0.0.0/0",
                            "Description" : "Allow anyone to access this port",
                            "FromPort" : 80,
                            "IpProtocol" : "tcp",
                            "ToPort" : 80
                        },
                        {
                            "CidrIp" : "0.0.0.0/0",
                            "Description" : "Allow anyone to access this port from outside",
                            "FromPort" : 443,
                            "IpProtocol" : "tcp",
                            "ToPort" : 443
                        },
                        {
                            "CidrIp" : "172.16.0.0/16",
                            "Description" : "Allow anyone from the VPC to access SSH ports",
                            "FromPort" : 22,
                            "IpProtocol" : "tcp",
                            "ToPort" : 22
                        }
                    ]
                }
            }
        }
    }

This `CloudFormation` template creates a VPC with a security group that has special ingress rules allowing only traffic from certain places:

1. Traffic on the SSH port should only allow traffic from the internal VPC network
2. Traffic on port 80 and 443 should be allowed from the outside

Let's commit that file now:

    git add .
    git commit -m "Initial commit"

Next, we need to create a real `Git` repository that allows connection through username and password. The easiest way to do this is to open a free account on either `GitHub` or `BitBucket` or any other free `Git` service provider. Once that is done, copy the clone URL and do:

    git remote add origin <url>
    git push origin

This should push your files to the distant server, we can now configure the `Git` connector.

Copy the following information into a file named `gitConnector.json` at the base of your `Prancer` project directory:

    {
        "companyName": "<your name>",
        "gitProvider": "<https url of your repository>",
        "branchName":"master",
        "username":"<username to your repository>",
        "sshKeyFile":"<ssh-private-key-file-path>",
    }

> Remember to upload your public RSA key to your user that has access to this repository or the `git` connector won't be able to connect to your repository. If you don't know what is a public and private key, look it up on the web, it is pretty straight forward and well explained.

## Create the snapshot configuration

Now that we have our environment set up for testing, we'll need a snapshot configuration file. 

The snapshot configuration file is used to specify which resources we want to work on for the test suite. 

> Note: The `JSON` file we will be working with has multiple resources. Snapshots in `Prancer` are supposed to represent 1 specific resource. Problem is, none of our connectors to this day has filtering or transformation support. There are plans to add support for that in a not too long future, but for now, a `JSON` files content represents one big resource.

Copy the following content to a file named `validation/container1/snapshot.json`:

    {
        "snapshots": [
            {
                "source": "tutorial",
                "type": "custom",
                "testUser": "<username to your repository>",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "custom",
                        "collection": "security_groups",
                        "path": "prancer-security-group-tutorial.json"
                    }
                ]
            }
        ]
    }

> Our setup is simple, we do not have directories, just a single file. If you had put the `prancer-security-group-tutorial.json` file into a directory, you'd specify the additional directories in there as a relative path to the checkout.

> It is important to use strings as snapshot ids because the testing framework will not match the braced identifiers to snapshots if they are integers in your snapshot configuration file.

For more information on the structure of snapshot files, please refer to the [Snapshot documentation](http://www.prancer.io/documentation/?section=snapshot).

## Create the tests

The next step is to create the tests that will validate your snapshot. A test file is a `JSON` file that describes the tests that need to run on the snapshot you previously defined.

Copy the following content to a file named `validation/container1/test.json`:

    {
        "fileType": "test",
        "snapshot": "snapshot.json",
        "testSet": [
            {
                "testName ": "Ensure port 80 and 443 rules exists",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "
                            exists({1}.Resources.PrancerTutorialSecGroup
                            .Properties.SecurityGroupIngress['FromPort'=80])
                        "
                    },
                    {
                        "testId": "2",
                        "rule": "
                            exists({1}.Resources.PrancerTutorialSecGroup
                            .Properties.SecurityGroupIngress['FromPort'=443])
                        "
                    }
                ]
            },
            {
                "testName ": "Ensure port 22 rule exists and is only open to internal",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "3",
                        "rule": "
                            exists({1}.Resources.PrancerTutorialSecGroup
                            .Properties.SecurityGroupIngress['FromPort'=22])
                        "
                    },
                    {
                        "testId": "4",
                        "rule": "
                            {1}.Resources.PrancerTutorialSecGroup
                            .Properties.SecurityGroupIngress['FromPort'=22].CidrIp
                            = '172.16.0.0/16')
                        "
                    }
                ]
            }
        ]
    }

> Because these rules are very long, they have been broken down into multiple lines. **This is not possible in `JSON`**. You must put everything on one line!

This test set contains multiple tests and multiple cases. It uses the snapshot id 1 and digs into the data to ensure that the ports are is properly open and configured.

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

Now that we have passing tests, let's trigger a simple failure to see how everything fits together. To achieve this, we'll need to create a configuration drift, that is, change something in the `CloudFormation` template that doesn't match the expected infrastructure tests.

First, let's change our `CloudFormation` template. Change the block:

    {
        "CidrIp" : "172.16.0.0/16",
        "Description" : "Allow anyone from the VPC to access SSH ports",
        "FromPort" : 22,
        "IpProtocol" : "tcp",
        "ToPort" : 22
    }

To

    {
        "CidrIp" : "0.0.0.0/0",
        "Description" : "Allow anyone to access SSH ports",
        "FromPort" : 22,
        "IpProtocol" : "tcp",
        "ToPort" : 22
    }

The only thing that changed is the `CidrIp` to allow everyone in.

> Needless to say that this is a very bad practice?

Now, if you run the tests again

    validator container1

You should have a failing state proving that the drift was indeed detected.

## Cleanup your resources

Because this tutorial asked you to create a temporary `Git` repository on a public service, it would be good if you destroyed it since you won't need it anymore.

Apart from that, no other resources should have been created.

## Conclusion

That's it, you are done. You now know how to read `CloudFormation` files and check directly in them for changes that are unexpected.

Thank you for completing this tutorial on `Prancer`.

We hope to see you in the next tutorial!