This tutorial will show you all the steps required to setup a basic **AWS CodeBuild** build project that could leverage **Prancer** in one of the build steps. This tutorial doesn't show how to use **Prancer** but more how to use it in a CI/CD setup such as **AWS CodeBuild**.

Before taking this tutorial, ensure the following:

1. You have an **AWS** account
2. You can create **VPC** and **EC2** resources on this account
3. You can create **AWS CodeCommit** repositories to store the copy of your code to test
4. You can create **AWS CodeBuild** jobs to test your infrastructure

Then, you can follow these steps:

1. Checkout example files
2. Create a **Prancer** project
3. Setup your **AWS** account
4. Setup the monitored **AWS** environment
5. Create an **AWS CodeBuild** build project
6. Run the build job
7. Trigger a failure
8. Cleanup and rejoice

# Checkout example files

We have all the files already prepared for you in a public read-only repository. 

We'll still show all the content of each files in this tutorial and explain some tweaks you can and should do. You can use your own repository and write the files yourself but it'll be easier and faster if you checkout ours:

    cd <working directory>
    git clone https://github.com/prancer-io/prancer-aws-codebuild-tutorial
    cd prancer-aws-codebuild-tutorial

# Create a **Prancer** project

First, we'll need a **Prancer** project. This is where all the configuration and test files will live. Here's the content of each file with a brief description.

## buildspec.yml

This file drives the AWS CodeBuild job that will test your virtual cloud infrastructure.

    version: 0.2
                
    phases:
        install:
            runtime-versions:
                python: 3.6
                docker: 18
            commands:
                - pip3 install prancer-basic
        pre_build:
            commands:
                - docker pull mongo
        post_build:
            commands:
                - docker run -d --name prancer_mongo -p 27017:27017 mongo
                - cd tests/prancer/project
                - prancer aws

## devops/aws/template.yml

This file is the AWS CloudFormation template used to provision a small virtual infrastructure that will be tested.

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

## tests/prancer/project/.gitignore

This is a simple .gitignore file that ensures we are not commiting files we don't want in our project. Prancer will output many files such as logs and reports, you want to have such a file.

    log/*
    *.log
    output-*json

## tests/prancer/project/config.ini

This is the configuration file. You can change many things in here but the default configuration we provide should suffice. If you want to use your own **MongoDB** server then you should change the `dburl` property.

    [LOGGING]
    level = DEBUG
    propagate = true
    logFolder = log
    dbname = whitekite

    [MONGODB]
    dburl = mongodb://localhost:27017/validator
    dbname = validator

    [REPORTING]
    reportOutputFolder = validation

    [TESTS]
    containerFolder = validation
    database = false



## tests/prancer/project/awsConnector.json

> <NoteTitle>Setup beforehand</NoteTitle>
>
> If you haven't done it yet, you'll need to follow the steps in [AWS Connector](/connectors/aws) to setup your basic IAM user. If you change the username, remember to update the `prancer_ro` in this file and the following!

    {
        "organization": "organization",
        "fileType": "structure",
        "organization-unit": [
            {
                "name": "unit",
                "accounts": [
                    {
                        "account-name": "prancer-io",
                        "account-description": "account description",
                        "account-id": "<account-id>",
                        "users": [
                            {
                                "name": "prancer_ro",
                                "access-key": "<console-access-key>",
                                "secret-access": "<console-secret-key>",
                                "region":"<account-region>",
                                "client": "EC2"
                            }
                        ]
                    }
                ]
            }
        ]
    }

You to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| `account-id` | Your **AWS** account id, find this in the **AWS console** account menu drop-down |
| `console-access-key` | The programmatic **access key** associated to that user |
| `console-secret-key` | The programmatic **secret** associated to the access key |
| `account-region` | The region that you are operating from, for example: `us-east-1` |

> If you do not have access to an **access key** or to the **secret** you will have to create a new access key and decommission the old one.

## tests/prancer/project/validation/aws/snapshot.json

This file describes the information we want to test, you shouldn't need to change anything here.

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "awsConnector",
                "type": "aws",
                "testUser": "prancer_ro",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "security_groups",
                        "collection": "security_groups",
                        "id": {
                            "Filters": [
                                {
                                    "Name": "tag:aws:cloudformation:stack-name",
                                    "Values": ["PrancerCodeBuildTutorial"]
                                },
                                {
                                    "Name": "tag:aws:cloudformation:logical-id",
                                    "Values": ["PrancerTutorialSecGroup"]
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

## tests/prancer/project/validation/aws/test.json

This file describes the tests we want to achieve on the information we took a snapshot of.

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

# Setup your **AWS** account

Next, you need to create the infrastructure to observe, then push your code to **AWS CodeCommit** and finally create the build job on **AWS CodeBuild**.

## Launch your virtual infrastructure

To run these tests, you need a virtual infrastructure. This step will instruct you how to do so using a **CloudFormation** template provided with this tutorial.

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `Create stack`.
2. Upload the template using: `Template is ready` -> `Upload a template file` -> `Choose file`. The file to upload is in `devops/aws/template.yml`.
3. Click `Next`.
4. Name your stack `PrancerCodeBuildTutorial` and click `Next`.
5. Skip to the bottom and click `Next`.
6. Skip to the bottom and click `Create stack`.
7. Wait for **CloudFormation** to finish it's job. Once you see that the stack has been created, you can move on.

## Create a repository on CodeCommit and push your code

Now you need to store your code on **AWS CodeCommit**:

1. Visit [CodeCommit](https://console.aws.amazon.com/codesuite/codecommit/repositories) and click `Create repository`.
2. Name your repository `prancer-aws-codebuild-tutorial` and click `Create`.
3. Copy the proper clone URL (HTTPS or SSH) at your convienience. If you use SSH, you will need special SSH configuration. All instructions are present on the SSH tab. This is the recommended approach.
4. Next the checked out files to your **AWS CodeCommit** repository instead of **Prancer's**:

        git remote rm origin
        git remote add origin <your-aws-codecommit-clone-url>
        git add .
        git commit -m "Adjust configuration for my repository"
        git push

This should push your files to your repository. Refresh the **AWS CodeCommit** page to confirm your files are there!

## Create an **AWS CodeBuild** build project

The last part is to create your **AWS CodeBuild** build job to run **Prancer** tests.

1. Visit [CodeBuild](https://console.aws.amazon.com/codesuite/codebuild/projects) and click `Create build project`.
2. Name your project `prancer-aws-codebuild-tutorial`
3. Configure the source provider to the **AWS CodeCommit** and point it to the repository `prancer-aws-codebuild-tutorial`
4. Select the `master` branch
5. Configure the environment to use the `Ubuntu` operating system, use the `Standard` runtime and select the `aws/codebuild/standard:2.0` image. 

    > **Very important: Check the box about elevated privileges**.

    ![CodeBuild project name](/images/codebuild-environment.png)

6. If you do not already have a codebuild service role, create one with default settings. We already had one created when we built this example.

7. Leave the option to use the default `buildspec.yml` file

    ![CodeBuild project name](/images/codebuild-buildspec.png)

8. Skip to the bottom and click `Create build project`

# Run the build job

Now let's run the job to ensure the test works:

1. Go to the job's page (Something like [https://console.aws.amazon.com/codesuite/codebuild/projects/prancer-aws-codebuild-tutorial/history](https://console.aws.amazon.com/codesuite/codebuild/projects/prancer-aws-codebuild-tutorial/history))

2. Clicking on the "Start build" button in the navigation bar at the top right:

    ![Job navbar](/images/codebuild-navbar.png)

3. Use the default for everything and click `Start build` at the bottom

This will trigger the build. It can take a few seconds to complete as there are a lot of things going on in there:

1. It will install **Docker** and **Python 3** using **AWS CodeBuild's** runtime support
2. It will install the **Prancer** tool
3. It will pull the **MongoDB** docker image
4. It will start a **MongoDB** container
5. It will run the **Prancer** tests

You should see a log of all this as it goes, and it should look something like:

    2019-09-01 19:16:39,687(interpreter: 209) - ########################################################################### 
    2019-09-01 19:16:39,687(interpreter: 210) - Actual Rule: count({1}.SecurityGroups[0].IpPermissions[0].IpRanges)=2 
    2019-09-01 19:16:39,704(interpreter: 219) - ************************************************** 
    2019-09-01 19:16:39,705(interpreter: 220) - All the parsed tokens: ['count', '(', '{1}.SecurityGroups[0].IpPermissions[0].IpRanges', ')', '=', '2'] 
    2019-09-01 19:16:39,706(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}} 
    2019-09-01 19:16:39,706(rule_interpreter:  36) - <class 'dict'> 
    2019-09-01 19:16:39,708(rule_interpreter:  78) - Regex match- groups:('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), regex:\{(\d+)\}(\..*)*, value: {1}.SecurityGroups[0].IpPermissions[0].IpRanges, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f379b2fc208>>  
    2019-09-01 19:16:39,708(rule_interpreter: 121) - matched grps: ('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), type(grp0): <class 'str'> 
    2019-09-01 19:16:39,710(rule_interpreter: 150) - Number of Snapshot Documents: 1 
    2019-09-01 19:16:39,711(rule_interpreter:  78) - Regex match- groups:('2', None), regex:(\d+)(\.\d+)?, value: 2, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f379b2fc208>>  
    2019-09-01 19:16:39,711(rule_interpreter: 169) - LHS: 2, OP: =, RHS: 2 
    2019-09-01 19:16:39,712(rundata_utils:  92) - END: Completed the run and cleaning up.

Which shows that the test ran fine trying to compare port `80` to port `80`.

# Trigger a failure

Now that we have a working example, let's simulate a failure by changing the security group and removing one of the 2 rules in it.

1. Go to the [EC2 console's security group page](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SecurityGroups:sort=groupId)
2. Find the proper security group that matches the previously created stack

    ![Job navbar](/images/codebuild-ec2.png)
    
3. Go to the Inbound tab and click `Edit`
4. Delete one of the two lines and save

    ![Job navbar](/images/codebuild-sg-rules.png)

Now let's run the job again to ensure the test fails:

1. Go to the job's page (Something like [https://console.aws.amazon.com/codesuite/codebuild/projects/prancer-aws-codebuild-tutorial/history](https://console.aws.amazon.com/codesuite/codebuild/projects/prancer-aws-codebuild-tutorial/history))

2. Clicking on the "Start build" button in the navigation bar at the top right:

    ![Job navbar](/images/codebuild-navbar.png)

3. Use the default for everything and click `Start build` at the bottom

    You should see a log of all this as it goes. Once the build is complete, it should be in a failed state. The log will end with something like:

        2019-09-01 19:20:44,293(interpreter: 209) - ########################################################################### 
        2019-09-01 19:20:44,294(interpreter: 210) - Actual Rule: count({1}.SecurityGroups[0].IpPermissions[0].IpRanges)=2 
        2019-09-01 19:20:44,310(interpreter: 219) - ************************************************** 
        2019-09-01 19:20:44,311(interpreter: 220) - All the parsed tokens: ['count', '(', '{1}.SecurityGroups[0].IpPermissions[0].IpRanges', ')', '=', '2'] 
        2019-09-01 19:20:44,311(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}} 
        2019-09-01 19:20:44,312(rule_interpreter:  36) - <class 'dict'> 
        2019-09-01 19:20:44,313(rule_interpreter:  78) - Regex match- groups:('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), regex:\{(\d+)\}(\..*)*, value: {1}.SecurityGroups[0].IpPermissions[0].IpRanges, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7ff511e581d0>>  
        2019-09-01 19:20:44,314(rule_interpreter: 121) - matched grps: ('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), type(grp0): <class 'str'> 
        2019-09-01 19:20:44,315(rule_interpreter: 150) - Number of Snapshot Documents: 1 
        2019-09-01 19:20:44,316(rule_interpreter:  78) - Regex match- groups:('2', None), regex:(\d+)(\.\d+)?, value: 2, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7ff511e581d0>>  
        2019-09-01 19:20:44,317(rule_interpreter: 169) - LHS: 1, OP: =, RHS: 2 

    As you can see here, the rule interpreter ran the rule ok but found a mismatch where `1` did not equal `2`. Therefore, **Prancer** fails the build!

# Cleanup and rejoice

If you followed this tutorial without altering the resources to create, then nothing should cost you anything over time, but let's just go back to **CloudFormation** and destroy the stack to make sure. *(It is a good habit when testing things)*

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `PrancerCodeBuildTutorial` stack.
2. Click on the `Delete` button.
3. Confirm the deletion.
4. Wait for the operation to complete.

Then you might also want to:

1. Delete the **AWS CodeBuild** project
2. Delete the code **AWS CodeCommit** repository

# Conclusion

That's it, you are done. You now know how to setup a basic `Prancer` test in **AWS CodeCommit**.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!