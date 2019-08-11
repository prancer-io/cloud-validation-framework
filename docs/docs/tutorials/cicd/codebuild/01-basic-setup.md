This tutorial will show you all the steps required to setup a basic **AWS CodeBuild** build project that could leverage **Prancer** in one of the build steps. This tutorial doesn't show how to use **Prancer** but more how to use it in a CI/CD setup such as **AWS CodeBuild**.

Before taking this tutorial, ensure the following:

1. You have an **AWS** account
2. You can create **VPC** and **EC2** resources on this account

Then, you can follow these steps:

1. Create a **Prancer** project
2. Setup the monitored **AWS** environment
3. Create an **AWS CodeBuild** build project
4. Run the build job
5. Trigger a failure
6. Cleanup and rejoice

# Create a **Prancer** project

First, we'll need a **Prancer** project. We'll store all of our **Prancer** project file in what would be a standard web application project. We'll add to that our **AWS CloudFormation** template and our **AWS CodeBuild** `buildspec.yml` file.

> <NoteTitle>Shortcut</NoteTitle>
>
> You can use [https://github.com/prancer-io/prancer-code-build-tutorial](https://github.com/prancer-io/prancer-code-build-tutorial) if you want, it contains exactly the same thing that you will be creating below but you still need to setup the security in it.

Create an empty directory and copy all the following files in their proper location as indicated by the filenames:

**buildspec.yml**

    version: 0.2
                
    phases:
        install:
            runtime-versions:
                python: 3.7
                docker: 18
            commands:
                - pip3 install prancer-basic
        pre_build:
            commands:
                - docker pull mongo
        post_build:
            commands:
                - docker run -d --name prancer_mongo -p 27017:27017 mongo
                - cd tests/prancer
                - prancer aws-container

**devops/aws/template.yaml**

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

**tests/prancer/config.ini**

    [MONGODB]
    dbname = prancer

    [LOGGING]
    level = DEBUG
    logFolder = log

    [REPORTING]
    reportOutputFolder = validation

    [TESTS]
    containerFolder = validation
    database = false

**tests/prancer/awsConnector.json**

> <NoteTitle>Setup beforehand</NoteTitle>
>
> If you haven't done it yet, you'll need to follow the steps in [AWS Connector](/connectors/aws) to setup your basic IAM user.

    {
        "organization": "Organization name",
        "fileType": "structure",
        "organization-unit": [
            {
                "name": "Unit/Department name",
                "accounts": [
                    {
                        "account-name": "Account name",
                        "account-description": "Description of account",
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

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| account-id | Your **AWS** account id, find this in the **AWS console** account menu drop-down |
| iam-user | Name of the **IAM** user, we suggest `prancer_ro` |
| iam-access-key | The programmatic **access key** associated to that user |
| secret-access-key | The programmatic **secret** associated to the access key |

If you do not have access to an **access key** or to the **secret** you will have to create a new access key and decommission the old one.

**tests/prancer/validation/aws-container/snapshot.json**

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

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| iam-user | Name of the **IAM** user, we suggest `prancer_ro` |

**tests/prancer/validation/aws-container/test.json**

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

Then commit this setup to a repository that is accessible using git such as on **GitHub** or **CodeCommit**. Note that you must create the repository beforehand.

    git init
    git remote add origin git@github.com:your-user/some-repo.git
    git add .
    git commit -m "Tutorial on AWS CodeBuild"
    git push

Following this, you should be able to see your code on your repository.

# Setup the monitored AWS environment

To run tests against an environment, well, you need an environment. To create the environment that we'll work with, we'll use a simple custom **CloudFormation** template.

> <NoteTitle>Note</NoteTitle>
>
> The **CloudFormation** template is available in the previous files we created under `devops/aws/template.yml`. You should use that one or adjust the snapshot and test files based on your modifications if any.

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `Create a new stack`.
2. Upload the file we created by choosing `Upload a template to Amazon S3` and click `Next`.
3. Give your stack a simple name such as `PrancerCodeBuildTutorial` and click `Next`.
4. Skip to the bottom and click `Next`.
5. Skip to the bottom and click `Create`.
6. Wait for **CloudFormation** to finish it's job. Once you see that the stack has been created, you can move on.

# Create an **AWS CodeBuild** build project

The next part is to create your **CodeBuild** project to run **Prancer** tests.

1. Visit [CodeBuild](https://console.aws.amazon.com/codesuite/codebuild/projects) and click `Create build project`.
2. Name your project as you wish, we named it "prancer-aws-codebuild-tutorial"

    ![CodeBuild project name](/images/codebuild-name.png)

3. Configure the source provider to the repository that you uploaded your code into. Here we used CodeCommit.

    ![CodeBuild project name](/images/codebuild-source.png)

4. Configure the environment to use the "Ubuntu Standard 2.0" image. **Very important: Check the box about elevated privileges**. We already had a role created but you probably will need to create one!

    ![CodeBuild project name](/images/codebuild-environment.png)

5. Leave the option to use the default `buildspec.yml` file

    ![CodeBuild project name](/images/codebuild-buildspec.png)

6. Click the `Create build project` at the bottom

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

    [Container] 2019/06/19 15:10:51 Waiting for agent ping 
    [Container] 2019/06/19 15:10:53 Waiting for DOWNLOAD_SOURCE 
    [Container] 2019/06/19 15:10:55 Phase is DOWNLOAD_SOURCE 
    [Container] 2019/06/19 15:10:55 CODEBUILD_SRC_DIR=/codebuild/output/src977770363/src/git-codecommit.us-east-1.amazonaws.com/v1/repos/prancer_test 
    [Container] 2019/06/19 15:10:55 YAML location is /codebuild/output/src977770363/src/git-codecommit.us-east-1.amazonaws.com/v1/repos/prancer_test/buildspec.yml 
    [Container] 2019/06/19 15:10:55 Processing environment variables 
    [Container] 2019/06/19 15:10:55 Moving to directory /codebuild/output/src977770363/src/git-codecommit.us-east-1.amazonaws.com/v1/repos/prancer_test 
    [Container] 2019/06/19 15:10:55 Registering with agent 
    [Container] 2019/06/19 15:10:55 Phases found in YAML: 3 
    [Container] 2019/06/19 15:10:55  PRE_BUILD: 1 commands 
    [Container] 2019/06/19 15:10:55  POST_BUILD: 3 commands 
    [Container] 2019/06/19 15:10:55  INSTALL: 1 commands 
    [Container] 2019/06/19 15:10:55 Phase complete: DOWNLOAD_SOURCE State: SUCCEEDED 
    [Container] 2019/06/19 15:10:55 Phase context status code:  Message:  
    [Container] 2019/06/19 15:10:55 Entering phase INSTALL 
    [Container] 2019/06/19 15:10:55 Running command echo "Installing Docker version 18 ..." 
    Installing Docker version 18 ... 
    
    [Container] 2019/06/19 15:10:55 Running command echo "Installing Python version 3.7 ..." 
    Installing Python version 3.7 ... 
    
    [Container] 2019/06/19 15:10:55 Running command pip3 install prancer-basic 
    Collecting prancer-basic 
    Downloading https://files.pythonhosted.org/packages/d6/97/fd4c18564dce23e648e2a6e25aaad738267ba54d214fa70aa30f896fa7f0/prancer_basic-0.1.2-py3-none-any.whl (65kB) 
    Collecting ply==3.10 (from prancer-basic) 
    Downloading https://files.pythonhosted.org/packages/ce/3d/1f9ca69192025046f02a02ffc61bfbac2731aab06325a218370fd93e18df/ply-3.10.tar.gz (150kB) 
    Collecting pymongo==3.7.2 (from prancer-basic) 
    Downloading https://files.pythonhosted.org/packages/99/18/b50834fbfd557eaf07985c2a657b03efc691462ecba62d03e32c2fc4f640/pymongo-3.7.2-cp37-cp37m-manylinux1_x86_64.whl (406kB) 


If the build passes, the log will end with something like:

    2019-06-19 15:11:27,526(interpreter: 209) - ########################################################################### 
    2019-06-19 15:11:27,527(interpreter: 210) - Actual Rule: count({1}.SecurityGroups[0].IpPermissions[0].IpRanges)=2 
    2019-06-19 15:11:27,542(interpreter: 219) - ************************************************** 
    2019-06-19 15:11:27,543(interpreter: 220) - All the parsed tokens: ['count', '(', '{1}.SecurityGroups[0].IpPermissions[0].IpRanges', ')', '=', '2'] 
    2019-06-19 15:11:27,543(rule_interpreter:  35) - {'dbname': 'prancer', 'snapshots': {'1': 'security_groups'}} 
    2019-06-19 15:11:27,543(rule_interpreter:  36) - <class 'dict'> 
    2019-06-19 15:11:27,543(rule_interpreter:  78) - Regex match- groups:('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), regex:\{(\d+)\}(\..*)*, value: {1}.SecurityGroups[0].IpPermissions[0].IpRanges, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f0597f28fd0>>  
    2019-06-19 15:11:27,544(rule_interpreter: 121) - matched grps: ('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), type(grp0): <class 'str'> 
    2019-06-19 15:11:27,545(rule_interpreter: 150) - Number of Snapshot Documents: 1 
    2019-06-19 15:11:27,545(rule_interpreter:  78) - Regex match- groups:('2', None), regex:(\d+)(\.\d+)?, value: 2, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f0597f28fd0>>  
    2019-06-19 15:11:27,545(rule_interpreter: 169) - LHS: 2, OP: =, RHS: 2 
    2019-06-19 15:11:27,545(rundata_utils:  92) - END: Completed the run and cleaning up. 
    2019-06-19 15:11:27,546(rundata_utils: 102) - ·[92m Run Stats: { 
    "start": "2019-06-19 15:11:27", 
    "end": "2019-06-19 15:11:27", 
    "errors": [], 
    "host": "88023f46b7d2", 
    "timestamp": "2019-06-19 15:11:27", 
    "log": "/codebuild/output/src977770363/src/git-codecommit.us-east-1.amazonaws.com/v1/repos/prancer_test/tests/prancer/log/20190619-151126.log", 
    "duration": "0 seconds" 
    }·[00m 
    
    [Container] 2019/06/19 15:11:27 Phase complete: POST_BUILD State: SUCCEEDED 
    [Container] 2019/06/19 15:11:27 Phase context status code:  Message:

As you can see here, the rule interpreter ran fine:

    2019-06-19 15:11:27,545(rule_interpreter: 169) - LHS: 2, OP: =, RHS: 2

Which ended up as a success!

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

    2019-06-19 15:20:05,834(interpreter: 209) - ########################################################################### 
    2019-06-19 15:20:05,834(interpreter: 210) - Actual Rule: count({1}.SecurityGroups[0].IpPermissions[0].IpRanges)=2 
    2019-06-19 15:20:05,850(interpreter: 219) - ************************************************** 
    2019-06-19 15:20:05,850(interpreter: 220) - All the parsed tokens: ['count', '(', '{1}.SecurityGroups[0].IpPermissions[0].IpRanges', ')', '=', '2'] 
    2019-06-19 15:20:05,850(rule_interpreter:  35) - {'dbname': 'prancer', 'snapshots': {'1': 'security_groups'}} 
    2019-06-19 15:20:05,850(rule_interpreter:  36) - <class 'dict'> 
    2019-06-19 15:20:05,851(rule_interpreter:  78) - Regex match- groups:('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), regex:\{(\d+)\}(\..*)*, value: {1}.SecurityGroups[0].IpPermissions[0].IpRanges, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f33478ab668>>  
    2019-06-19 15:20:05,851(rule_interpreter: 121) - matched grps: ('1', '.SecurityGroups[0].IpPermissions[0].IpRanges'), type(grp0): <class 'str'> 
    2019-06-19 15:20:05,852(rule_interpreter: 150) - Number of Snapshot Documents: 1 
    2019-06-19 15:20:05,852(rule_interpreter:  78) - Regex match- groups:('2', None), regex:(\d+)(\.\d+)?, value: 2, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f33478ab668>>  
    2019-06-19 15:20:05,852(rule_interpreter: 169) - LHS: 1, OP: =, RHS: 2 
    2019-06-19 15:20:05,853(rundata_utils:  92) - END: Completed the run and cleaning up. 
    2019-06-19 15:20:05,853(rundata_utils: 102) - ·[92m Run Stats: { 
    "start": "2019-06-19 15:20:05", 
    "end": "2019-06-19 15:20:05", 
    "errors": [], 
    "host": "0442a12b2e16", 
    "timestamp": "2019-06-19 15:20:05", 
    "log": "/codebuild/output/src651938574/src/git-codecommit.us-east-1.amazonaws.com/v1/repos/prancer_test/tests/prancer/log/20190619-152005.log", 
    "duration": "0 seconds" 
    }·[00m 
    
    [Container] 2019/06/19 15:20:06 Command did not exit successfully prancer aws-container exit status 1 
    [Container] 2019/06/19 15:20:06 Phase complete: POST_BUILD State: FAILED 
    [Container] 2019/06/19 15:20:06 Phase context status code: COMMAND_EXECUTION_ERROR Message: Error while executing command: prancer aws-container. Reason: exit status 1 

As you can see here, the rule interpreter ran the rule ok but found a mismatch:

    2019-06-19 15:20:05,852(rule_interpreter: 169) - LHS: 1, OP: =, RHS: 2 

Therefore, **Prancer** fails the build!

# Cleanup and rejoice

If you followed this tutorial without altering the resources to create, then nothing should cost you anything over time, but let's just go back to **CloudFormation** and destroy the stack to make sure. *(It is a good habit when testing things)*

1. Visit [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and click `PrancerCodeBuildTutorial` stack.
2. Click on the `Delete` button.
3. Confirm the deletion.
4. Wait for the operation to complete.

Then you might also want to:

1. Delete the **AWS CodeBuild** project
2. Delete the code repository (Such as on **CodeCommit** or **GitHub**)

# Conclusion

That's it, you are done. You now know how to setup a basic `Prancer` test in **AWS CodeCommit**.

Things to remember:

1. **Prancer** exits with a proper exit code regarding success or failure. This means that any CI server, not just **AWS CodeCommit**, will catch the error code and stop right there if it receives an exit code that is not 0.
2. Running **Prancer** from a CI doesn't do anything else than if you ran it from your machine, you still need to build your tests and ensure they work beforehand.
3. Running tests without saving the artifacts of the tests, mostly when there are failures, will make it harder to figure out what failed. Read on the next tutorials to learn how to save your artifacts for later review.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!