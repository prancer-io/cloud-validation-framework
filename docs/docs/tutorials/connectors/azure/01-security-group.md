This tutorial will show you all the steps required to write a basic test that connects to **Azure** and validates that a network security group's subnet hasn't changed.

Before taking this tutorial, you will need to follow some more generic steps:

1. First, let's [install Prancer](../../../installation.md)
2. Next, let's [configure a project](../../../configuration/basics.md)
3. Finaly, let's [connect to Azure](../../../connectors/azure.md)

Then, you can follow these steps:

1. Setup the monitored **Azure** environment
2. Create the snapshot configuration
3. Create the test case
4. Run the tests
5. Trigger a failure
6. Cleanup and rejoice

# Setup the monitored Azure environment

To run tests against an environment, well, you need an environment. To create the environment that we'll work with, we'll use a simple custom **Azure ARM** template.

Copy the following code in memory, we'll paste it into the online **Azure ARM** template editor:

    {
        "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "resources": [
            {
                "type": "Microsoft.Network/virtualNetworks",
                "apiVersion": "2018-12-01",
                "name": "prancer-tutorial-vnet",
                "location": "westus",
                "properties": {
                    "addressSpace": {
                        "addressPrefixes": [
                            "172.1.1.0/24"
                        ]
                    }
                }
            },
            {
                "type": "Microsoft.Network/virtualNetworks/subnets",
                "apiVersion": "2018-12-01",
                "name": "prancer-tutorial-vnet/prancer-tutorial-snet",
                "dependsOn": [
                    "prancer-tutorial-vnet",
                    "prancer-tutorial-nsg"
                ],
                "properties": {
                    "addressPrefix": "172.1.1.0/24",
                    "networkSecurityGroup": {
                        "id": "[resourceId('Microsoft.Network/networkSecurityGroups', 'prancer-tutorial-nsg')]"
                    }
                }
            },
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
            },
            {
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "apiVersion": "2018-12-01",
                "name": "prancer-tutorial-nsg/sshFromVnet",
                "dependsOn": [
                    "prancer-tutorial-nsg"
                ],
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
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "apiVersion": "2018-12-01",
                "name": "prancer-tutorial-nsg/httpFromPublic",
                "dependsOn": [
                    "prancer-tutorial-nsg"
                ],
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
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "apiVersion": "2018-12-01",
                "name": "prancer-tutorial-nsg/httpsFromPublic",
                "dependsOn": [
                    "prancer-tutorial-nsg"
                ],
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

Now, let's deploy that **ARM** template:

1. Visit [Custom deployment](https://portal.azure.com/#create/Microsoft.Template) and click `Build your own template in the editor`
2. Copy the content above into the editor and click `Save`
3. Select the subscription, resource-group (we recommend you create one such as `prancer-sg-tutorial`)
4. Accept the agreement and click `Purchase` (We are not using any paying resources, so don't worry about that **purchase** button)
5. Wait for your deployment to be complete

# Create the snapshot configuration

Now that we have our environment set up for testing, we'll need a snapshot configuration file. 

The snapshot configuration file is used to specify which resources we want to work on for the test suite. You might have a lot of resources already created and not everything is meant to be validated.

Copy the following content to a file named `validation/container1/snapshot.json` and replace the `<spn-username>`, `<subscription-id>` and the `<resource-group-name>` with the proper values that you can find in the **Azure** portal:

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "azureConnector",
                "type": "azure",
                "testUser": "<spn-username>",
                "subscriptionId": "<subscription-id>",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "Microsoft.Network/networkSecurityGroups",
                        "collection": "security_groups",
                        "path": "/resourceGroups/<resource-group-name>/providers/Microsoft.Network/networkSecurityGroups/prancer-tutorial-nsg"
                    }
                ]
            }
        ]
    }

For more information on the structure of snapshot files, please refer to the [Snapshot documentation](../../../snapshots/azure.md).

# Create the tests

The next step is to create the tests that will validate your snapshot. A test file is a **JSON** file that describes the tests that need to run on the snapshot you previously defined.

Copy the following content to a file named `validation/container1/test.json`:

    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Ensure subnet",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "count({1}.subnets)=1"
                    }
                ]
            }
        ]
    }

This test set contains only 1 test called "Ensure subnet" exists. It uses the snapshot id 1 and digs into the data to ensure that the subnet count is still 1.

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

1. Login to your [Azure portal](https://portal.azure.com/#home)
2. Find the security group named `prancer-tutorial-nsg` in [All resources](https://portal.azure.com/#blade/HubsExtension/BrowseAllResourcesBlade/resourceType/Microsoft.Resources%2Fresources)
3. Go to the `Subnets`
4. Dissociate the subnet from the network security group
5. Run the tests again using `prancer container1`
6. Check the results: `echo $?`

You should have a failing state proving that the drift was indeed detected.

# Cleanup your Azure resources

If you followed this tutorial without altering the resources to create, then nothing should cost you anything over time, but let's just go to **Resource groups** and destroy the resource group we created to make sure. *(It is a good habit when testing things)*

1. Visit [Resource groups](https://portal.azure.com/#blade/HubsExtension/BrowseResourceGroupBlade/resourceType/Microsoft.Resources%2Fsubscriptions%2FresourceGroups) and click the `prancer-sg-tutorial` resource group
2. Click on the `Delete resource group` button
3. Confirm the deletion
4. Wait for the operation to complete

# Conclusion

That's it, you are done.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!