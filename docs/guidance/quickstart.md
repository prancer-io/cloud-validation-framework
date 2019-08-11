This document provides a set of quick start guidelines for running **Prancer** on your system. This quick start assumes the use of an **Azure** environment but you should be able to substitute easily for **AWS** or any other provider of your choice. 

The test cases ran in this quick start scenario are extremely simple and are only figured here as a means to quickly grasp the features of **Prancer**. If you want more detailed explanations, read on the reference documentation or continue down to the **Connector tutorials** section.

# Overview

Here are the steps we will go through:

1. Setup **Prancer** on your machine
2. Create a project folder with basic configuration
3. Configure the connector to **Azure**
4. Configure the resources to inspect
5. Configure the tests
6. Run and view the reports

# Prerequisites

We expect/assume a few things in this quick start to keep it simple:

1. You must have an **Azure** subscription
2. You must have an **Azure** Service Principal Name (SPN) to access your resources
3. We assume you use a Linux based system

    > <NoteTitle>Supported systems</NoteTitle>
    >
    > This tutorial is based off **Ubuntu**. We currently support the following systems but not limited to:
    >
    > * **Ubuntu** 16.04 +
    > * **Redhat**

4. You must have a **MongoDB** server installed on the machine

    > See [installation](http://docs.prancer.io/installation) for instructions on installing a basic MongoDB server

# Step 1 - Setup **Prancer** on your machine

Setting up **Prancer** is as easy as running an `apt` command to ensure **Python 3** installed and then using **Pip** to install **Prancer**:

    sudo apt install python3 python3-pip
    sudo -H pip3 install prancer-basic

Check the [installation](http://docs.prancer.io/installation) section if you want more detailed instructions on installing **Prancer**.

# Step 2 - Create a project folder with basic configuration

Before using **Prancer**, you will need a project folder where all the configuration will be created:

    mkdir prancer-quickstart
    cd prancer-quickstart
    mkdir validation
    mkdir validation/container1
    cat <<EOT >> config.ini
    [AZURE]
    api = azureApiVersions.json

    [LOGGING]
    level = DEBUG
    propagate = true
    logFolder = log
    dbname = whitekite

    [MONGODB]
    dbname = validator

    [REPORTING]
    reportOutputFolder = validation

    [TESTS]
    containerFolder = validation
    database = false
    EOT

> <notetitle>Important</notetitle>
>
> Replace the values in **CAPITAL** in the last commands or the example won't work. If you need help finding this information, checkout the [Azure connector](http://docs.prancer.io/connectors/azure) reference.

Check the [configuration](http://docs.prancer.io/configuration/basics) section if you want more detailed instructions on configuring a **Prancer** project.
    
# Step 3 - Configure the connection to **Azure**

Next we need to setup a connection to your Azure environment. This requires the creation of an api versions file and a structure file:

    cat <<EOT >> azureApiVersions.json
    {
        "Microsoft.Compute/availabilitySets": {
            "version": "2018-06-01"
        },
        "Microsoft.Network/virtualNetworks": {
            "version": "2018-07-01"
        },
        "Microsoft.Storage/storageAccounts": {
            "version": "2018-07-01"
        },
        "Microsoft.KeyVault/vaults": {
            "version": "2015-06-01"
        },
        "Microsoft.Network/networkSecurityGroups": {
            "version": "2018-11-01"
        },
        "fileType": "structure",
        "type": "others"
    }
    EOT
    cat <<EOT >> azureConnector.json
    {
        "companyName": "Company Name",
        "tenant_id": "REPLACE THIS WITH YOUR TENANT ID",
        "accounts": [
            {
                "department": "Unit/Department name",
                "subscription": [
                    {
                        "subscription_name": "Subscription (Account) name",
                        "subscription_description": "Subscription (Account) description",
                        "subscription_id": "REPLACE THIS WITH YOUR SUBSCRIPTION ID",
                        "users": [
                            {
                                "name":"prancer-quickstart",
                                "client_id": "REPLACE THIS WITH YOUR SPN CLIENT ID",
                                "client_secret": "REPLACE THIS WITH YOUR SPN CLIENT SECRET"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    EOT

> <notetitle>Important</notetitle>
>
> Replace the values in **CAPITAL** in the last commands or the example won't work. If you need help finding this information, checkout the [Azure connector](http://docs.prancer.io/connectors/azure) reference.

# Step 4 - Configure the resources to inspect

Next, we need to define which resources we want to inspect in our tests. 

We assume here that you have a **Virtual Network** in your **Azure** subscription for this test. If you don't have one, create one right now, it is cost free. Once done, run the following commands to create your snapshot file:

    cat <<EOT >> validation/container1/snapshot.json
    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "azureConnector",
                "type": "azure",
                "testUser": "prancer-quickstart",
                "subscriptionId": "REPLACE THIS WITH YOUR SUBSCRIPTION ID",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "Microsoft.Network/virtualNetworks",
                        "collection": "Microsoft.Networks",
                        "path": "/resourceGroups/REPLACE THIS WITH RESOURCE GROUP NAME/providers/Microsoft.Network/virtualNetworks/REPLACE THIS WITH VIRTUAL NETWORK NAME"
                    }
                ]
            }
        ]
    }
    EOT

> <notetitle>Important</notetitle>
>
> Replace the values in **CAPITAL** in the last commands or the example won't work. If you need help finding this information, checkout the [Azure snapshot](http://docs.prancer.io/snapshots/azure) reference.

# Step 5 - Configure the tests

Finally, the last step before we can run **Prancer** is to write a test:

    cat <<EOT >> validation/container1/test.json
    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Test",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "exists({1}.location)"
                    },
                    {
                        "testId": "2",
                        "rule": "{1}.location='REPLACE THIS WITH YOUR AZURE LOCATION CODE'"
                    }
                ]
            }
        ]
    }
    EOT

> <notetitle>Important</notetitle>
>
> Replace the values in **CAPITAL** in the last commands or the example won't work.

# Step 6 - Run and view the reports

Now that we have a project with a snapshot and a test, we can run the tool and check out the results:

    prancer container1

This will generate a bit of content in the console but if you execute:

    echo $?

You should see a return value of `0` hopefully, meaning that the test did work fine. If you get anything else such as `1`, this probably means you have not properly configured your structure file, snapshot file or test file. Check the documentation on how to properly configure everything or seek help from the community.

If you do get a `0`, then you should see a `output-test.json` in the `validation/container1` directory. If you open this, you should see something like this:

    {
        "fileType": "output",
        "timestamp": 1551281031487,
        "snapshot": "snapshot.json",
        "container": "testcontainer",
        "test": "test.json",
        "results": [
            {
                "result": "passed",
                "snapshots": [
                    {
                        "id": "1",
                        "path": "/resourceGroups/xyz/providers/Microsoft.Network/virtualNetworks/abc",
                        "structure": "azure",
                        "source": "azureConnector"
                    }
                ],
                "testId": "1",
                "rule": "exist({1}.location)"
            },
            {
                "result": "passed",
                "snapshots": [
                    {
                        "id": "1",
                        "path": "/resourceGroups/xyz/providers/Microsoft.Network/virtualNetworks/abc",
                        "structure": "azure",
                        "source": "azureConnector"
                    }
                ],
                "testId": "2",
                "rule": "{1}.location='eastus2'"
            }
        ]
    }

This shows that all of your tests passed properly, or if one of the 2 tests failed, it will show you which one and you can easily troubleshoot from there.

# Conclusion

That's it, you are done. You now know how to write a basic **Prancer** test related to an existing **Azure** infrastructure.

If you have any more questions don't hesitate to:

1. Read on the rest of the [documentation](http://docs.prancer.io/)
2. Checkout the [connector tutorials](http://docs.prancer.io/) at the end of the documentation
3. Communicate with the community