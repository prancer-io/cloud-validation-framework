This tutorial will show you all the steps required to setup a basic **Jenkins** CI server that could leverage **Prancer** as a step. This tutorial doesn't show how to use **Prancer** but more how to use it in a CI/CD setup such as **Jenkins**.

Before taking this tutorial, you will need to follow some more generic steps:

1. First, let's [install Docker](https://docs.docker.com/install/) to avoid installing **Jenkins** directly on our system

Then, you can follow these steps:

1. Setup a **Jenkins** server
2. Create a normal project that contains an **AWS CloudFormation** file to test
3. Create a basic **Prancer** project to get that **CloudFormation** and test it
4. Create a **Jenkins** job
5. Run the job
6. Trigger a failure
7. Cleanup and rejoice

# Setup a **Jenkins** server

To get our integration running, we need a **Jenkins** server. Let's start one using **Docker**:

    docker run -p 8080:8080 --name prancer-jenkins-tutorial \
        -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

Feel free to change the mapped ports or volume.

Once the server has started, look at the log for the administrator password. It should look something like:

    *************************************************************
    *************************************************************
    *************************************************************

    Jenkins initial setup is required. An admin user has been created and a password generated.
    Please use the following password to proceed to installation:

    e6013bfc6f034d2d8b47c7b56d129955

    This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

    *************************************************************
    *************************************************************
    *************************************************************

Copy this string in memory, you will need it in a few seconds.

Once **Jenkins** is ready (you should see a "Jenkins is fully up and running" in the log), visit the [server](http://localhost:8080). It will ask you to unlock your **Jenkins** server. Paste in the code you copied from the log. Then, following the instructions below:

1. Click on `Install suggested plugins`
2. Create an `admin` user (Keep it simple for this demo, we suggest to use `admin` for both username and password)
3. Set the proper URL if not properly set
4. Confirm the start of **Jenkins**

The final step to setting up your instance is to install **Prancer** on the master node (The **Jenkins** server). We named our node `prancer-jenkins-tutorial` using the `--name` switch so we can now execute simple root commands to install **Prancer** on that container. We also need to install MongoDB and start it.

	docker exec -itu 0 prancer-jenkins-tutorial apt update -y
    docker exec -itu 0 prancer-jenkins-tutorial apt install -y python3 python3-pip mongodb
    docker exec -itu 0 prancer-jenkins-tutorial pip3 install prancer-basic
    docker exec -itu 0 prancer-jenkins-tutorial service mongodb start
    docker exec -itu 0 prancer-jenkins-tutorial pip3 install --upgrade pyasn1-modules

At this point, your master node should be setup properly to run Prancer!

> <NoteTitle>Alternatives</NoteTitle>
>
> There are other ways to install **Prancer** and **MongoDB** on your master node but this is a straighforward and easy to undertand way. 
>
> In fact, the better approach is to use slave nodes which we'll cover in a later tutorial.

# Create a normal code project

Next, we'll need a normal code project where we store our **AWS CloudFormation** template. Note that it is not required to be a **CloudFormation** template, it can be any json file of your choice.

Open a new directory and create the sub directories and the `template.json` file with the following content:

**devops/cf/mytemplate.json**

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

Then commit this setup to a repository that is accessible using git such as on GitHub. Note that you must create the repository beforehand.

    git init
    git remote add origin git@github.com:your-user/some-repo.git
    git add .
    git commit -m "Tutorial on jenkins"
    git push

Following this, you should be able to see your code on your repository.

> <NoteTitle>Shortcut</NoteTitle>
>
> You can just use [https://github.com/prancer-io/prancer-tests](https://github.com/prancer-io/prancer-tests) if you want, it contains exactly the same thing alongside other templates.

# Create a basic **Prancer** project to test previous repository

Now that we have a repository with some code, let's get some **Prancer** tests in there. Note that you could setup both in the same repository. The tutorial shows you how to do this in 2 different repositories but this is not a requirement at all.

Create a project folder, refer to the [Configuration documentation](../../../configuration/basics.md) for more details:

    mkdir prancer-tutorial
    cd prancer-tutorial
    mkdir -p tests/validation/git-tutorial

And then copy all the following files to the different folders:

**tests/.gitignore**

    log/*
    *.log
    output-*json

**tests/config.ini**

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

**tests/gitConnector.json**

    {
        "fileType": "structure",
        "companyName": "prancer-test",
        "gitProvider": "https://github.com/your-user/prancer-tests.git",
        "branchName":"master",
        "private": false
    }

**tests/validation/git-tutorial/snapshot.json**

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "type": "git",
                "testUser": "git",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "json",
                        "collection": "security_groups",
                        "path": "devops/cf/mytemplate.json"
                    }
                ]
            }
        ]
    }

**tests/validation/git-tutorial/test.json**

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
                        "rule": "{1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=80].CidrIp= '0.0.0.0/0'"
                    },
                    {
                        "testId": "2",
                        "rule": "{1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=443].CidrIp= '0.0.0.0/0'"
                    }
                ]
            },
            {
                "testName ": "Ensure port 22 rule exists and is only open to internal",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "3",
                        "rule": "{1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=22].CidrIp= '172.16.0.0/16'"
                    }
                ]
            }
        ]
    }

Then commit this setup to a repository that is accessible using git such as on **GitHub**. Note that you must create the repository beforehand.

    git init
    git remote add origin git@github.com:your-user/prancer-cicd-tutorial.git
    git add .
    git commit -m "Tutorial on jenkins"
    git push

Following this, you should be able to see your code on your repository.

> <NoteTitle>Shortcut</NoteTitle>
>
> You can just use [https://github.com/prancer-io/prancer-cicd-tutorial](https://github.com/prancer-io/prancer-cicd-tutorial) if you want, it contains exactly the same thing.

# Create a **Jenkins** job

Back to **Jenkins**, you can now create your first job. A job is what runs a certain set of operations. In our case, we'll make it very simple and only run **Prancer** on some checked out code but in a more complex scenario, you'd have many other steps to run before hand. 

Let's create a job:

1. Visit the [Jenkins server](http://localhost:8080)
2. Login if necessary
3. Click on "Create new jobs"

    ![Jenkins home](../../../images/jenkins-dashboard.png)

4. Name your job something like "prancer-jenkins-tutorial" and select the "Pipeline" type and click "Ok"
5. Skip down to the last section and paste the following pipeline script into the pipeline box:

    ![Jenkins pipeline script setup](../../../images/jenkins-pipeline.png)

**Pipeline script**

    pipeline { 
        agent any 
        options {
            skipStagesAfterUnstable()
        }
        stages {
            stage('Build') { 
                steps { 
                    git url: 'https://github.com/your-user/prancer-cicd-tutorial.git'
                }
            }
            stage('Test'){
                steps {
                    dir("tests") {
                        sh "prancer git-tutorial"
                    }
                }
            }
        }
    }

Remember to update the git url with the url to your repository! Once done, save the job and you should be back to the job dashboard!

# Run the job

Now let's run the job to ensure the test works:

1. Go to the job's page (Something like [http://localhost:8080/job/prancer-jenkins-tutorial/](http://localhost:8080/job/prancer-jenkins-tutorial/))
2. Clicking on the "Build now" button on the side bar

    ![Job sidebar](../../../images/jenkins-job.png)

This will trigger a build and within seconds, thanks to our very simple project, you should have a passing build. Let's check the logs!

1. Click on the date beside the last build you ran in the build history

    ![Job sidebar](../../../images/jenkins-build-history.png)

2. Click on "Console Output"

    ![Job sidebar](../../../images/jenkins-build-sidebar.png)

3. Look at the log

It should show the same log as if you ran **Prancer** from your machine but instead it was run as a CI job on your **Jenkins** server.

    2019-06-10 14:23:47,962(interpreter: 209) - ###########################################################################
    2019-06-10 14:23:47,963(interpreter: 210) - Actual Rule: {1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=22].CidrIp= '172.16.0.0/16'
    2019-06-10 14:23:47,965(interpreter: 219) - **************************************************
    2019-06-10 14:23:47,966(interpreter: 220) - All the parsed tokens: ["{1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=22].CidrIp", '=', "'172.16.0.0/16'"]
    2019-06-10 14:23:47,967(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}}
    2019-06-10 14:23:47,967(rule_interpreter:  36) - <class 'dict'>
    2019-06-10 14:23:47,967(rule_interpreter:  78) - Regex match- groups:('1', ".Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=22].CidrIp"), regex:\{(\d+)\}(\..*)*, value: {1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=22].CidrIp, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f023e7f0d30>> 
    2019-06-10 14:23:47,968(rule_interpreter: 121) - matched grps: ('1', ".Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=22].CidrIp"), type(grp0): <class 'str'>
    2019-06-10 14:23:47,969(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-06-10 14:23:47,969(rule_interpreter:  78) - Regex match- groups:(), regex:\'.*\', value: '172.16.0.0/16', function: <bound method RuleInterpreter.match_string of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f023e7f0d30>> 
    2019-06-10 14:23:47,970(rule_interpreter: 169) - LHS: 172.16.0.0/16, OP: =, RHS: 172.16.0.0/16

You can see here, in the last rule interpreted, that the LHS is **172.16.0.0/16** so the comparison between **172.16.0.0/16** and **172.16.0.0/16** passes and so the test succeeds.

# Trigger a failure

Now that we have a working example, let's simulate a failure by changing the test that is run with another that cannot succeed:

1. Go to the job's page (Something like [http://localhost:8080/job/prancer-jenkins-tutorial/](http://localhost:8080/job/prancer-jenkins-tutorial/))
2. Click on the `Configure` option in the sidebar

    ![Job sidebar](../../../images/jenkins-job.png)

3. Go down to the pipeline script and change it to:

**Pipeline script**

    pipeline { 
        agent any 
        options {
            skipStagesAfterUnstable()
        }
        stages {
            stage('Build') { 
                steps { 
                    git url: 'https://github.com/your-user/prancer-cicd-tutorial.git'
                }
            }
            stage('Test'){
                steps {
                    dir("tests") {
                        sh "prancer git-tutorial-fails"
                    }
                }
            }
        }
    }


Now let's run the job to ensure the test fails:

1. Go to the job's page (Something like [http://localhost:8080/job/prancer-jenkins-tutorial/](http://localhost:8080/job/prancer-jenkins-tutorial/))
2. Clicking on the "Build now" button on the side bar

    ![Job sidebar](../../../images/jenkins-job.png)

This will trigger a build and within seconds, thanks to our very simple project, you should have a passing build. Let's check the logs!

1. Click on the date beside the last build you ran in the build history

    ![Job sidebar](../../../images/jenkins-build-history-fails.png)

2. Click on "Console Output"

    ![Job sidebar](../../../images/jenkins-build-sidebar.png)

3. Look at the log

It should show the same log as if you ran **Prancer** from your machine but instead it was run as a CI job on your **Jenkins** server.

    2019-06-10 14:46:54,713(interpreter: 209) - ###########################################################################
    2019-06-10 14:46:54,714(interpreter: 210) - Actual Rule: {1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=99].CidrIp= '0.0.0.0/0'
    2019-06-10 14:46:54,731(interpreter: 219) - **************************************************
    2019-06-10 14:46:54,732(interpreter: 220) - All the parsed tokens: ["{1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=99].CidrIp", '=', "'0.0.0.0/0'"]
    2019-06-10 14:46:54,732(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}}
    2019-06-10 14:46:54,733(rule_interpreter:  36) - <class 'dict'>
    2019-06-10 14:46:54,734(rule_interpreter:  78) - Regex match- groups:('1', ".Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=99].CidrIp"), regex:\{(\d+)\}(\..*)*, value: {1}.Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=99].CidrIp, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7fbba8a7f240>> 
    2019-06-10 14:46:54,734(rule_interpreter: 121) - matched grps: ('1', ".Resources.PrancerTutorialSecGroup.Properties.SecurityGroupIngress['FromPort'=99].CidrIp"), type(grp0): <class 'str'>
    2019-06-10 14:46:54,735(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-06-10 14:46:54,736(rule_interpreter:  78) - Regex match- groups:(), regex:\'.*\', value: '0.0.0.0/0', function: <bound method RuleInterpreter.match_string of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7fbba8a7f240>> 
    2019-06-10 14:46:54,737(rule_interpreter: 169) - LHS: None, OP: =, RHS: 0.0.0.0/0

You can see here that the LHS is **none** because it couldn't find that line in the snapshot so the comparison between **0.0.0.0/0** and **None** failed.

# Cleanup and rejoice

If you followed this tutorial without altering the resources to create, then it should be relatively easy to cleanup, here is a list:

1. Kill the docker container, you can simply `CTRL+C` out of it
2. Destroy the docker container: `docker rm prancer-jenkins-tutorial`
3. Destroy the docker volume: `docker volume rm jenkins_home`
4. Destroy the useless repositories such as `prancer-tests` and `prancer-cicd-tutorial` if you used your own

# Conclusion

That's it, you are done. You now know how to setup a basic `Prancer` test in **Jenkins**.

Things to remember:

1. **Prancer** exits with a proper exit code regarding success or failure. This means that any CI server, not just **Jenkins**, will catch the error code and stop right there if it receives an exit code that is not 0.
2. Running **Prancer** from a CI doesn't do anything else than if you ran it from your machine, you still need to build your tests and ensure they work beforehand.
3. Running tests without saving the artifacts of the tests, mostly when there are failures, will make it harder to figure out what failed. Read on the next tutorials to learn how to save your artifacts for later review.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!