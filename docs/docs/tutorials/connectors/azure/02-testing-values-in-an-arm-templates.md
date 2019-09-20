This tutorial will show you all the steps required to write a basic test that connects to a **Git** repository and validates that the information in a **Azure ARM** template written in **JSON** features the proper values.

Before taking this tutorial, you will need to follow some steps in other more generic tutorials:

1. First, let's [setup the Prancer environment](../../../installation.md)
2. Next, let's [setup a Prancer project](../../../configuration/basics.md)

Then, you can follow these steps:

1. Setup the monitored GIT environment
2. Create the snapshot configuration file
3. Create the test case
4. Run the tests
5. Trigger a failure
6. Cleanup and rejoice

# Setup the monitored Git environment

To run tests against a **Git** repository, well, you need a **Git** repository with files in it. This portion will create such as repository, commit files to it and then configure the **Git** connector for that specific repository and project.

First of all, create a project folder and copy the following code into a **JSON** file called `prancer-security-group-tutorial.json`:

> <NoteTitle>Note</NoteTitle>
>
> This part should not be done in your project folder, it should be in a discardable temporary directory.

    {
        "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "resources": [
            {
                "type": "Microsoft.Network/networkSecurityGroups",
                "apiVersion": "2018-12-01",
                "name": "prancer-tutorial-nsg",
                "location": "westus",
                "properties": {
                    "securityRules": [
                        {
                            "name": "sshFromVnet",
                            "properties": {
                                "protocol": "*",
                                "sourcePortRange": "*",
                                "destinationPortRange": "22",
                                "sourceAddressPrefix": "VirtualNetwork",
                                "destinationAddressPrefix": "172.1.1.0/24",
                                "access": "Allow",
                                "priority": 100,
                                "direction": "Inbound"
                            }
                        },
                        {
                            "name": "httpFromPublic",
                            "properties": {
                                "protocol": "*",
                                "sourcePortRange": "*",
                                "destinationPortRange": "80",
                                "sourceAddressPrefix": "Internet",
                                "destinationAddressPrefix": "172.1.1.0/24",
                                "access": "Allow",
                                "priority": 110,
                                "direction": "Inbound"
                            }
                        },
                        {
                            "name": "httpsFromPublic",
                            "properties": {
                                "protocol": "*",
                                "sourcePortRange": "*",
                                "destinationPortRange": "443",
                                "sourceAddressPrefix": "Internet",
                                "destinationAddressPrefix": "172.1.1.0/24",
                                "access": "Allow",
                                "priority": 111,
                                "direction": "Inbound"
                            }
                        }
                    ]
                }
            }
        ]
    }

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> **Azure ARM** templates usually feature a `$schema` property. **MongoDB** doesn't allow keys to feature `$` in the name because it is a reserved character. Your parser will then escape the `$` character. If your tests expect this to exist (it should not) then remember to escape it too.

This **Azure ARM** template creates a Network Security Group that has special ingress rules allowing only traffic from certain places:

1. Traffic on the SSH port should only allow traffic from the internal network
2. Traffic on port 80 and 443 should be allowed from the outside

Let's commit that file now:

    git add .
    git commit -m "Initial commit"

Next, we need to create a real **Git** repository that allows connection through username and password. The easiest way to do this is to open a free account on either **GitHub** or **BitBucket** or any other free **Git** service provider. Once that is done, copy the clone URL and do:

    git remote add origin <url>
    git push origin

This should push your files to the distant server, we can now configure the **Git** connector.

Copy the following information into a file named `gitConnector.json` at the base of your **Prancer** project directory:

    {
        "fileType": "structure",
        "companyName": "Organization name",
        "gitProvider": "<ssh-or-https-url-to-public-repository>",
        "branchName": "<branch>",
        "private": false
    }

> <NoteTitle>Note</NoteTitle>
>
> Remember to upload your public RSA key to your user that has access to this repository or the **git** connector won't be able to connect to your repository. If you don't know what is a public and private key, look it up on the web, it is pretty straight forward and well explained.

# Create the snapshot configuration file

Now that we have our environment set up for testing, we'll need a snapshot configuration file. 

The snapshot configuration file is used to specify which resources we want to work on for the test suite. 

> <NoteTitle>Notes: Limitations</NoteTitle>
>
> Note: The **JSON** file we will be working with has multiple resources. Snapshots in **Prancer** are supposed to represent 1 specific resource. Problem is, none of our connectors to this day has filtering or transformation support. There are plans to add support for that in a not too long future, but for now, a **JSON** files content represents one big resource.

Copy the following content to a file named `validation/container1/snapshot.json`:

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "type": "git",
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

> <NoteTitle>Note</NoteTitle>
>
> Our setup is simple, we do not have directories, just a single file. If you had put the `prancer-security-group-tutorial.json` file into a directory, you'd specify the additional directories in there as a relative path to the checkout.

For more information on the structure of snapshot configuration files, please refer to the [Snapshot documentation](../../../snapshots/json.md).

# Create the tests

The next step is to create the tests that will validate your snapshot. A test file is a **JSON** file that describes the tests that need to run on the snapshot you previously defined.

Copy the following content to a file named `validation/container1/test.json`:

    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Ensure port 80 and 443 rules exists and are reachable using the Internet",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "exist({1}.resources['name'='prancer-tutorial-nsg'].properties.securityRules['name'='httpFromPublic'])"
                    },
                    {
                        "testId": "2",
                        "rule": "exist({1}.resources['name'='prancer-tutorial-nsg'].properties.securityRules['name'='httpsFromPublic'])"
                    },
                    {
                        "testId": "3",
                        "rule": "{1}.resources['name'='prancer-tutorial-nsg'].properties.securityRules['name'='httpFromPublic'].properties.sourceAddressPrefix='Internet'"
                    },
                    {
                        "testId": "4",
                        "rule": "{1}.resources['name'='prancer-tutorial-nsg'].properties.securityRules['name'='httpsFromPublic'].properties.sourceAddressPrefix='Internet'"
                    }
                ]
            },
            {
                "testName ": "Ensure port 22 rule exists and is only open to internal",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "5",
                        "rule": "{1}.resources['name'='prancer-tutorial-nsg'].properties.securityRules['name'='sshFromVnet'].properties.sourceAddressPrefix = 'VirtualNetwork'"
                    }
                ]
            }
        ]
    }

This test set contains multiple tests and multiple cases. It uses the snapshot id 1 and digs into the data to ensure that the ports are is properly open and configured.

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

Now that we have passing tests, let's trigger a simple failure to see how everything fits together. To achieve this, we'll need to create a configuration drift, that is, change something in the **Azure ARM** template that doesn't match the expected infrastructure tests.

First, let's change our **Azure ARM** template. Change the block:

    {
        "name": "sshFromVnet",
        "properties": {
            "protocol": "*",
            "sourcePortRange": "*",
            "destinationPortRange": "22",
            "sourceAddressPrefix": "VirtualNetwork",
            "destinationAddressPrefix": "172.1.1.0/24",
            "access": "Allow",
            "priority": 100,
            "direction": "Inbound"
        }
    }

To

    {
        "name": "sshFromVnet",
        "properties": {
            "protocol": "*",
            "sourcePortRange": "*",
            "destinationPortRange": "22",
            "sourceAddressPrefix": "Internet",
            "destinationAddressPrefix": "172.1.1.0/24",
            "access": "Allow",
            "priority": 100,
            "direction": "Inbound"
        }
    }

The only thing that changed is the `sourceAddressPrefix` to allow everyone in.

> <NoteTitle>Notes: Good practices</NoteTitle>
>
> Needless to say that this is a very bad practice? You should never open port 22 to everyone!

Now, if you run the tests again

    prancer container1

You should have a failing state proving that the drift was indeed detected.

# Cleanup your resources

Because this tutorial asked you to create a temporary **Git** repository on a public service, it would be good if you destroyed it since you won't need it anymore.

Apart from that, no other resources should have been created.

# Conclusion

That's it, you are done. You now know how to read **Azure ARM** files and check directly in them for changes that are unexpected.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!