This tutorial will show you all the steps required to build a basic **Docker image** that can be used to run **Prancer** in any **Docker** based environment. This tutorial doesn't show how to use **Docker** nor **Prancer** but more how to use it in a CI/CD context that leverages **Docker** containers.

Before taking this tutorial, ensure the following:

1. You have the **Docker engine** [installed (Link to Ubuntu flavor)](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Then, you can follow these steps:

1. Checkout example files
2. Create a **Prancer** image for **Docker**
3. Create a **Prancer** project
4. Run the tests
5. Trigger a failure
6. Cleanup and rejoice

# Checkout example files

We have all the files already prepared for you in a public read-only repository. 

We'll still show all the content of each files in this tutorial and explain some tweaks you can and should do. You can use your own repository and write the files yourself but it'll be easier and faster if you checkout ours:

    cd <working directory>
    git clone https://github.com/prancer-io/prancer-docker-tutorial
    cd prancer-docker-tutorial

# Create a **Prancer** image for **Docker**

The first step is to create the `Dockerfile` that will generate the **Docker** image that we'll use to run **Prancer**.

**tests/prancer/docker/Dockerfile**

    FROM ubuntu

    RUN DEBIAN_FRONTEND=noninteractive apt update -y && \
        DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip git && \
        pip3 install prancer-basic

    CMD prancer
    WORKDIR /prancer/project

This file describes how to build a basic **Ubuntu** image that contains **Prancer** and **Git**. Now let's build the image by running:

     cd tests/prancer
     docker build docker --tag prancer

Once **Docker** is done building the image, you'll have a new image in your local Docker image repository tagged with the name `prancer`. If you list your images, you should see it in the list:

    docker images

    REPOSITORY      TAG         IMAGE ID            CREATED              SIZE
    prancer         latest      b34102a2985a        About a minute ago   1.12GB

We can now build our **Prancer** project.

# Create a **Prancer** project

Next, we'll need a **Prancer** project. This is where all the configuration and test files will live. Here's the content of each file with a brief description.

## data/config.json

This file contains the data that we want to test using **Prancer**.

    {
        "webserver": {
            "port": 80
        }
    }

## data/config-fails.json

This file contains the data that we want to test using **Prancer**. This file is used in the failure scenario!

    {
        "webserver": {
            "port": 443
        }
    }

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
    dburl = mongodb://prancer-mongodb-server/validator
    dbname = validator

    [REPORTING]
    reportOutputFolder = validation

    [TESTS]
    containerFolder = validation
    database = false

## tests/prancer/project/gitConnector.json

This is the configuration file that leads to the files **Prancer** will need to check out when running tests. It is currently pointing to our public read-only repository. If you want to use your own, feel free to remap the remote once you checked out our files and push the files somewhere else.

    {
        "fileType": "structure",
        "companyName": "prancer-test",
        "gitProvider": "https://github.com/prancer-io/prancer-docker-tutorial.git",
        "branchName":"master",
        "private": false
    }

## tests/prancer/project/validation/git/snapshot.json

This file describes the information we want to test, you shouldn't need to change anything here.

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "type": "filesystem",
                "testUser": "git",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "json",
                        "collection": "security_groups",
                        "path": "data/config.json"
                    }
                ]
            }
        ]
    }

## tests/prancer/project/validation/git/test.json

This file describes the tests we want to achieve on the information we took a snapshot of.

    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Ensure configuration uses port 80",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "{1}.webserver.port=80"
                    }
                ]
            }
        ]
    }

## tests/prancer/project/validation/git-fails/snapshot.json

This file describes the information we want to test, you shouldn't need to change anything here. This file is used in the failure scenario!

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "type": "filesystem",
                "testUser": "git",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "json",
                        "collection": "security_groups",
                        "path": "data/config.json"
                    }
                ]
            }
        ]
    }

## tests/prancer/project/validation/git-fails/test.json

This file describes the tests we want to achieve on the information we took a snapshot of. This file is used in the failure scenario!

    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Ensure configuration uses port 80",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "{1}.webserver.port=80"
                    }
                ]
            }
        ]
    }

# Run the tests

Before running the tests, we'll need a **MongoDB** server. If you are using your own and updated the configuration files in the previous section, perfect, skip to **Running a Prancer test** but remove the `--network prancer` in the **Docker** call. On the other hand, if you need a server, the best solution is to just start one in a **Docker** container. This will make it easily discardable!

## Starting a MongoDB in a Docker container

Starting a **MongoDB** server using **Docker** is easy but because we want to have multiple containers communicating together, we'll need to create a network to link both of them together. Once created, we can start the **MongoDB** server inside that network:

    docker network create prancer
    docker run --rm -it --name prancer-mongodb-server --network prancer mongo

Thats it, you now have a dockerized **MongoDB** server.

## Running a Prancer test

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase.

    cd "root-of-whole-project"
    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" --network prancer prancer prancer git

Once this has run, you can find a `tests/prancer/project/validation/git/output-test.json` in the container folder and a log file in the `log/` folder. The exit code of the tool (`echo ?$`) should return 0 stating that everything went well. The log should look something like:

    2019-09-01 16:16:19,142(interpreter: 209) - ###########################################################################
    2019-09-01 16:16:19,143(interpreter: 210) - Actual Rule: {1}.webserver.port=80
    2019-09-01 16:16:19,158(interpreter: 219) - **************************************************
    2019-09-01 16:16:19,158(interpreter: 220) - All the parsed tokens: ['{1}.webserver.port', '=', '80']
    2019-09-01 16:16:19,158(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}}
    2019-09-01 16:16:19,158(rule_interpreter:  36) - <class 'dict'>
    2019-09-01 16:16:19,160(rule_interpreter:  78) - Regex match- groups:('1', '.webserver.port'), regex:\{(\d+)\}(\..*)*, value: {1}.webserver.port, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f50d65cc5f8>> 
    2019-09-01 16:16:19,160(rule_interpreter: 121) - matched grps: ('1', '.webserver.port'), type(grp0): <class 'str'>
    2019-09-01 16:16:19,161(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-09-01 16:16:19,162(rule_interpreter:  78) - Regex match- groups:('80', None), regex:(\d+)(\.\d+)?, value: 80, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f50d65cc5f8>> 
    2019-09-01 16:16:19,162(rule_interpreter: 169) - LHS: 80, OP: =, RHS: 80
    2019-09-01 16:16:19,163(rundata_utils:  92) - END: Completed the run and cleaning up

Which shows that the test ran fine trying to compare port `80` to port `80`.

# Triggering a failure

Because our repository is read-only, you can't create a real configuration drift. Therefore, we'll adjust the command you use to run **Prancer** and use a different test that is already programmed to fail by default. Simply run:

    cd "root-of-whole-project"
    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" --network prancer prancer prancer git-fails

You should have a failing state proving that the drift was indeed detected. The log should look something like:

    2019-09-01 16:17:56,492(interpreter: 209) - ###########################################################################
    2019-09-01 16:17:56,492(interpreter: 210) - Actual Rule: {1}.webserver.port=80
    2019-09-01 16:17:56,502(interpreter: 219) - **************************************************
    2019-09-01 16:17:56,502(interpreter: 220) - All the parsed tokens: ['{1}.webserver.port', '=', '80']
    2019-09-01 16:17:56,502(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}}
    2019-09-01 16:17:56,502(rule_interpreter:  36) - <class 'dict'>
    2019-09-01 16:17:56,504(rule_interpreter:  78) - Regex match- groups:('1', '.webserver.port'), regex:\{(\d+)\}(\..*)*, value: {1}.webserver.port, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f27d5d8a5c0>> 
    2019-09-01 16:17:56,504(rule_interpreter: 121) - matched grps: ('1', '.webserver.port'), type(grp0): <class 'str'>
    2019-09-01 16:17:56,505(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-09-01 16:17:56,505(rule_interpreter:  78) - Regex match- groups:('80', None), regex:(\d+)(\.\d+)?, value: 80, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f27d5d8a5c0>> 
    2019-09-01 16:17:56,505(rule_interpreter: 169) - LHS: 443, OP: =, RHS: 80
    2019-09-01 16:17:56,506(rundata_utils:  92) - END: Completed the run and cleaning up.

Which shows that the test ran fine trying to compare port `443` to port `80`, which obviously fails!

> If you are using your own repository, you can create a true configuration drift by changing the test or the config file and push the changes to your repo. You don't need to use the `git-fails` container in the validation call.

# Cleanup your resources

Here is a list of things to cleanup if you followed the tutorial without any changes:

1. In the terminal windows that runs the **MongoDB** server, press `CTRL+C` to shut it down and destroy the container
2. Destroy the network: `docker network rm prancer`
3. You may also want to delete the prancer image: `docker rmi prancer`

# Conclusion

That's it, you are done. You now know how to create a working **Docker** image with **Prancer** in it.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!