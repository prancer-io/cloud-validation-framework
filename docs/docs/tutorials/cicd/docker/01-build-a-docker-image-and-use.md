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
                "type": "git",
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

This file describes the tests we want to achieve on the information we took a snapshot of. This is related to the previous file!

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

Before running the tests, we'll need a **MongoDB** server. If you are using your own and updated the configuration files in the previous section, perfect, skip to **Running a prancer test**. On the other hand, if you need a server, the best solution is to just start one in a **Docker** container. This will make it easily discardable!

## Starting a MongoDB in a Docker container

Starting a **MongoDB** server using **Docker** is easy but because we want to have multiple containers communicating together, we'll need to create a network to link both of them together. Once created, we can start the **MongoDB** server inside that network:

    docker network create prancer
    docker run -d --name prancer-mongodb-server -it --network prancer mongo

Thats it, you now have a dockerized **MongoDB** server.

## Running a Prancer test

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase. If you are using a container for the **MongoDB** server run the second version of the **Prancer** command:

    # First ensure you are in the root of the repository / the folder containing the `tests/prancer`:
    cd "root-of-whole-project"

    # Run Prancer WITHOUT the dockerized MongoDB server
    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" prancer prancer git

    # Run Prancer WITH the dockerized MongoDB server
    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" --network prancer prancer prancer git

Let's deconstruct this to understand each part:

1. `docker run --rm -it`

    The standard command that will run an image with terminal emulation, input support and kill the container once the process is done!

2. `-v "$(pwd)/tests/prancer/project:/prancer/project"`

    This part tells **Docker** to map the current directory's `/tests/prancer/project` folder to `/prancer/project` inside the container. This is necessary because **Prancer** is configured to execute from that directory. You can override the working directory using `-w <folder>` and map the project somewhere else but it won't give you any added benefit.

    Note that by binding this, your logs will be put in the mounted volume which means you won't lose them once the process is done. Because of the **MongoDB** limitation though, you will lose your **MongoDB** data if you don't add an additional `-v "$(pwd)/mongo:/data/db". This isn't critical but can be favorable depending on your testing approach.

3. `--network prancer`

    This optional part tells **Docker** to use a special network to link all containers together. This has the advantage of allowing you to resolve special hostnames within containers that could refer to other containers. Those names are the name that you give to a container. For example, if you use the containerized **MongoDB**, we suggest to call this container `--name prancer-mongodb-server` so the hostname would be `prancer-mongodb-server` when you are in the **Prancer** container.

4. `prancer`

    This is simply the image name. If you tagged the image name differently when you built it earlier, change this.

5. `prancer git`

    This is the command that we'll execute in the container. It tells the **Prancer** which container to validate, in this case, we called it `git`. If you renamed the container in `tests/prancer/project/validation` then you need to change this here.

Once this has run, you can find a `tests/prancer/project/validation/git/output-test.json` in the container folder and a log file in the `log/` folder. The exit code of the tool (`echo ?$`) should return 0 stating that everything went well. The log should look something like:

    2019-07-22 18:04:47,533(rule_interpreter: 169) - LHS: 80, OP: =, RHS: 80
    2019-07-22 18:04:47,533(rundata_utils:  92) - END: Completed the run and cleaning up.
    2019-07-22 18:04:47,533(rundata_utils: 102) -  Run Stats: {
        "start": "2019-07-22 18:04:46",
        "end": "2019-07-22 18:04:47",
        "errors": [],
        "host": "3eb17c24a573",
        "timestamp": "2019-07-22 18:04:46",
        "log": "/prancer/project/log/20190722-180445.log",
        "duration": "1 seconds"
    }

Which shows that the test ran fine trying to compare port 80 to port 80.

## Checking the MongoDB server did record information

If you used a container for **MongoDB**, it would be nice to check if the data did make it in there. To do so, we'll need to run the client as a container connecting to it:

    docker run -it --network prancer --rm mongo mongo --host prancer-mongodb-server validator

This will get you in the MongoDB server, you can then list the collections which should show `security_groups`. If you find all content in there, you should see our snapshots:

    show collections;
    db.security_groups.find().pretty();

# Triggering a failure

## Using our repository

Because our repository is read-only, you can't create a real configuration drift. Therefore, we'll adjust the command you use to run **Prancer** and use a different test that is already programmed to fail by default. Simply run:

    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" --network prancer prancer prancer git-fail

You should have a failing state proving that the drift was indeed detected. The log should look something like:

    2019-07-22 18:08:58,837(rule_interpreter: 169) - LHS: 80, OP: =, RHS: 443
    2019-07-22 18:08:58,837(rundata_utils:  92) - END: Completed the run and cleaning up.
    2019-07-22 18:08:58,838(rundata_utils: 102) -  Run Stats: {
        "start": "2019-07-22 18:08:57",
        "end": "2019-07-22 18:08:58",
        "errors": [],
        "host": "8531f1a4c4f0",
        "timestamp": "2019-07-22 18:08:57",
        "log": "/prancer/project/log/20190722-180857.log",
        "duration": "1 seconds"
    }

Which shows that the test ran fine trying to compare port 80 to port 443, which obviously fails!

## Using your own repository

Now that we have passing tests, let's trigger a simple failure to see how everything fits together. To achieve this, we'll need to create a configuration drift, that is, change something in the `data/config.json` file that doesn't match the expected tests.

1. Change the port `80` in there for `443`
2. Save and push the changes to your git repository

Now, if you run the tests again:

    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" prancer bash -c "service mongodb restart && prancer git"

You should have a failing state proving that the drift was indeed detected. The log should look something like:

    2019-07-22 18:08:58,837(rule_interpreter: 169) - LHS: 443, OP: =, RHS: 80
    2019-07-22 18:08:58,837(rundata_utils:  92) - END: Completed the run and cleaning up.
    2019-07-22 18:08:58,838(rundata_utils: 102) -  Run Stats: {
        "start": "2019-07-22 18:08:57",
        "end": "2019-07-22 18:08:58",
        "errors": [],
        "host": "8531f1a4c4f0",
        "timestamp": "2019-07-22 18:08:57",
        "log": "/prancer/project/log/20190722-180857.log",
        "duration": "1 seconds"
    }

Which shows that the test ran fine trying to compare port 443 to port 80, which obviously fails!

# Cleanup your resources

Depending on your choices, you will have different cleanup steps:

1. If you used your own **Git** repository, then feel free to destroy it if you want.
2. If you used a **Docker** container for **MongoDB**, then you need to stop it and drop the network:

        docker stop prancer-mongodb-server
        docker rm prancer-mongodb-server
        docker network remove prancer

# Conclusion

That's it, you are done. You now know how to create a working **Docker** image with **Prancer** in it.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!