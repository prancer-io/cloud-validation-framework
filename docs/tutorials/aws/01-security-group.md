# Tutorial - Security group monitoring in AWS

This tutorial will show you all the steps required to start from scratch a Prancer project, connect it to an AWS environment and write basic tests to ensure everything works fine.

The steps to accomplish this are the following:

1. Setup the environment
2. Setup the `AWS` connector
3. Create the snapshot configuration
4. Create the test case
5. Run the tests
6. Trigger a failure
7. Cleanup and rejoice

## Step 1 - Setup the environment

The first step to using `Prancer` will be to setup a proper environment. There are 5 steps to this:

1. Setup the [Prancer](https://prancer.io) environment
2. Setup a [MongoDB](https://www.mongodb.com/download-center/community) database server to store snapshot data
3. Get a copy of the Prancer framework
4. Create the working directory
5. Setup the monitored AWS environment

This tutorial assumes a few things:

1. You use the popular [Ubuntu](https://ubuntu.com) Linux operating system
2. You have the [Git](https://git-scm.org) version control tools installed
3. You have an [AWS](https://aws.amazon.com/) account
4. Your `AWS console user` has enough rights to create `EC2` resources

### Step 1.1 - Setup the Prancer environment

This step is a **one time only step** where you will update your system and install the dependencies to run [Prancer](https://prancer.io). 

Let's first update your system and then install the `python3` package manager:

    sudo apt update
    sudo apt install python3-pip

Then, let's install the `Prancer` validation framework using the `python3 package manager`:

    sudo -H pip3 install prancer-basic

> The -H switch to `sudo` sets the HOME environment variable to the HOME of the current user.

Finaly, let's test the installation by running the `validator` utility:

    validator --help

If you see something like:

    2019-04-12 09:47:18,556(cli_validator:  23) - Comand: 'python3 /usr/local/bin/validator --help'
    usage: Validator functional tests. [-h] [--db] container

    positional arguments:
    container   Container tests directory.

    optional arguments:
    -h, --help  show this help message and exit
    --db        Mongo to be used for input and output data.

Then it means everything worked fine. 

Let's move on!

### Step 1.2 - Install a MongoDB server to store results

Next up, installing a `MongoDB` server on your system. If you already installed it, then you can skip this:

    sudo apt install mongodb

This should be more than enough to get the `MongoDB` database server running. Test it out with:

    mongo

It should get you into a prompt to manipulate your `MongoDB` server and show you some log lines. You can CTRL-C out of it.

> You could also use a [MongoDB Docker](https://hub.docker.com/_/mongo) container instead and set the data to be stored in a data volume. As long as your configuration points to the right port, it will work fine.

### Step 1.3 - Checkout the Prancer framework

Next, we need to check out the `Prancer` framework into a directory. This framework contains different tools that help you create configuration files with ease and utilities used by the `validator`.

    git clone https://github.com/prancer-io/cloud-validation-framework.git

The `validator` needs to be told where to find the framework that you just downloaded with GIT. Export an environment variable with the following:

    export FRAMEWORKDIR="$(pwd)"

> This environment variable should contain the path to the directory containing your folder "cloud-validation-framework" not directly into that folder.

**IMPORTANT**: You do not need to put the framework at the same place as your test files. In a typical scenario, you would create your `Prancer` files in your project in a devops structure. The framework could be checked out into another folder that contains non-commited files like a vendor directory.

Here is an example structure:

    - Your project
        - src
            - /* Source code of application */
        - devops
            - cloudformation
            - prancer
                - /* Prancer test files go here */
        - vendor
            - .gitignore
            - cloud-validation-framework

In this scenario, you would export something like:

    export FRAMEWORKDIR="<...>/project/vendor"

And run your tests from
    
    cd "<...>/devops/prancer"

### Step 1.4 - Create the working directory

The configuration files that you will create requires a few additional folders and files. In the previous case, we suggested to store your files under `devops/prancer` in your project but you can put them where you want.

    mkdir -p devops/prancer
    cd devops/prancer

Then you need to create a few more folders that will contain the different test scenarios:

    mkdir -p validation/container1
    mkdir -p validation/test2
    mkdir -p validation/test3athing
    mkdir -p validation/test4something_else

> You can create as many as needed but this tutorial requires only the first one: `container1`.

The `validation` folder is your base folder where tests will exist. All of your tests will be written inside a sub-folder of this folder such as `container1`.

Next, we need to configure the validation engine. Create a configuration file named `config.ini` and copy the following content into it:

    [TESTS]
    containerFolder = validation/

    [REPORTING]
    reportOutputFolder = validation/

    [LOGGING]
    level = DEBUG
    maxbytes = 10
    backupcount = 10
    propagate = true
    logFolder = log
    dbname = whitekite

    [MONGODB]
    dbname1 = mongodb://localhost:27017/validator
    dbname = validator
    COLLECTION = resources
    SNAPSHOT = snapshots
    TEST = tests
    STRUCTURE = structures
    OUTPUT = outputs
    NOTIFICATIONS = notifications

    [INDEXES]
    OUTPUT = name, container, timestamp

### Step 1.5 - Setup the monitored AWS environment

Once you are done setting up the `Prancer` environment, you will need to setup an `AWS` environment.

To create the environment to work with, we'll use a simple custom CloudFormation template. Copy the following code into a `YAML` file called `prancer-security-group-tutorial.yml`. It will create a `VPC` with a `security group` in it.

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
2. Upload your template by choosing `Upload a template to Amazon S3` and click `Next`.
3. Give your stack a simple name such as `tutorial` and click `Next`.
4. Skip to the bottom and click `Next`.
5. Skip to the bottom and click `Create`.
6. Wait for `CloudFormation` to finish it's job. Once you see that the stack has been created, you can move on.

## Step 2 - Create and configure the AWS connector

This section will show you how to create the configuration file used to connect `Prancer` to your `AWS` account using the usual access keys and secrets that the `AWS CLI` would use.

> You will need the **`Access key`** and **`Secret`** that are provided when you create an `IAM` user on `AWS`. 
> 
> Ensure that this user only has the necessary credentials to read `EC2` components. You don't want to commit to your code base a token and secret that has elevated privileges. In a later tutorial, we'll show you how to share those secrets with `Prancer` through different means.

### Step 2.1 - Create an IAM user with basic privileges

> If you already have an `IAM` user configured and have access to it's access key and secret, skip to the next section.

This section will focus on creating the user that will be used to take snapshots of the `AWS` infrastructure.

1. Visit the [IAM console](https://console.aws.amazon.com/iam/home)
2. Click on the `Users` section on the left menu
3. Click on `Add user`
4. Name the user anything you want, we suggest `prancer_ro`
5. Only enable `Programmatic access`
6. Click `Next: Permissions`
7. Click `Attach existing policies directly`
8. Search for the `AmazonEC2ReadOnlyAccess` policy and check it
9. Click `Next: Tags`
10. Click `Next: Review`
11. Click `Create user`
12. Note down the `Access key ID`
13. Note down the `Secret access key`
14. Click `Close`

### Step 2.2 - Configure the connector

Create a configuration file named `awsStructure.json` and copy the following content in it:

    {
        "organization": "prancer-test",
        "fileType": "structure",
        "organization-unit": [
            {
                "name": "prancer-test",
                "accounts": [
                    {
                        "account-name": "prancer-test",
                        "account-description": "prancer-test",
                        "account-id": "<account-id>",
                        "users": [
                            {
                                "name": "<iam-user>",
                                "access-key": "<iam-access-key>",
                                "secret-access": "<secret-access-key>",
                                "region":"<region>",
                                "client": "EC2"
                            }
                        ]
                    }
                ]
            }
        ]
    }

Remember to replace all values in this file that looks like a tag such as:

| tag | What to put there |
|-----|-------------------|
| account-id | Your AWS account id, find this in the `AWS console` account menu drop-down |
| iam-user | Name of the `IAM` user, we previously suggested `prancer_ro` |
| iam-access-key | The `access key` that you took note of in the previous section |
| secret-access-key | The `secret` associated to the access key that you took note of in the previous section |

## Step 3 - Create the snapshot configuration

Now that we have our system setup for testing, we'll first need a snapshot configuration file. The snapshot configuration file is used to specify which resources we want to work on for this test suite. You might have a lot of resources already created and not everything is meant to be validated. 

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

### Step 3.1 - How does id actually work for the AWS Connector?

Have you ever used the `AWS CLI`? If not, head to the [latest AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference) documentation to learn more about it.

`Prancer` uses the `AWS CLI/api` to communicate with your `AWS` infrastructure. Anything you can pass to those commands can be passed into the id object:

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

## Step 3.2 - Understanding how to use filters with tags

You can also use the `id` object to refer to tags instead of specific ids. Beware though that the result of a snapshot resource **`must always be 1 item`**.

Here is an example of a tag based research:

    "id": {
        "Filters": [
            {
                "Name": "tag:aws:cloudformation:stack-name",
                "Values": ["tutorial"]
            }
        ]
    }

This is the equivalent of calling the same command on the command line:

    aws ec2 describe-security-groups --filters Name=tag:aws:cloudformation:stack-name,Values=tutorial

And it will return the security group that is part of that tutorial. 

In a more evolved scenario, you will want to use more tags to pin point one exact resource. For example, in a multi security group scenario generate using a complex CloudFormation template, you could use the following approach:

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

## Step 4 - Create the tests

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

### Step 4.1 - Rule structure

A rule is the most important part of the test. It specifies what to use to run the test.

A test rule is usually a comparison operator such as `=` and should feature a `left hand side` operator (`LHS`) and a `right hand side` operator (`RHS`). The system will parse this rule and create references to the items that are represented in braces such as `{1}`.

These `{1}{2}{3}{4}...` are references to the snapshot ids that you set in the `snapshot.json` file that lives beside the `test.json` file.

> Mentioning this again, in the `snapshot.json` files, ensure you are using `string` based snapshot ids.

### Step 4.2 - Fields you can use in rules

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

### Step 4.3 - Rule functions and operators

Rules are not only about comparing for equality. You can use rules in a rather complex way using functions. For example:

| function | note |
| -------- | ---- |
| exists(x) | Checks that the operand exists, returns a boolean |
| count(x) | Returns the count of the operand when it is an `Array` |

Another thing you can do is use operators to create mathematical expressions. You can add, subtract, multiply, divide. For example:

    {1}.somevalue + {2}.somevalue = 20

That is a perfectly valid rule!

## Step 5 - Run the tests

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase:

    validator container1

Once this has run, you can find a `validation/container1/output-test.json` in the container folder and a log file in the `log/` folder.

The exit code of the validator should reflect the status of the tests. 

* If any test fail, the validator will return an exit code of 1. 
* If all tests pass, it will return an exit code of 0.

### Step 5.1 - Test output file

If you end up with failed tests, you can look at the `validation/container1/output-test.json` to figure out what went wrong. The output file is again another `JSON` file and it will contain details of each test.

Most of the time, the file will contain sensibly the same information that you would have had in a test file. If you re-run the test, the `validation/container1/output-test.json` file is lost.

In a continuous improvement scenario, you should store all `validation/*/output-test.json` into an artifact system for later reference. This is especialy important in failure scenarios to ensure you keep a track of what failed.

## Step 6 - Triggering a failure

Now that we have passing tests, let's trigger a simple failure to see how everything fits together. To achieve this, we'll need to create a configuration drift, that is, change something in the infrastructure that doesn't match the expected infrastructure tests.

### Step 6.1 - Drift your AWS setup

First, let's change our infrastructure to create a configuration drift.

1) Login to your [EC2 AWS console](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SecurityGroups)
2) Find the security group named `prancer-tutorial-sg`
3) Change it's name to `prancer-tut-sg`
4) Run the tests again

        validator container1

5) Check the results

        echo $?

You should have a failed state proving that the drift was indeed detected.

## Step 7 - Cleanup your AWS resources

If you followed this tutorial without altering the resources to create, then nothing should cost you anything over time, but let's just go back to `CloudFormation` and destroy the stack to make sure. *(It is a good habit when testing things)*

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `tutorial` stack.
2. Click on the `Actions` drop down and click `Delete stack`.
3. Confirm the deletion.
4. Wait for the operation to complete.

Thank you for completing this tutorial on `Prancer`.

We hope to see you in the [next tutorial](/docs/tutorials/aws/02-next-aws-tutorial)!