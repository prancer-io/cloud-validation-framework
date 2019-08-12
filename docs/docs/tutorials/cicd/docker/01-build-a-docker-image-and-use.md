This tutorial will show you all the steps required to build a basic **Docker image** that can be used to run **Prancer** in any **Docker** based environment. This tutorial doesn't show how to use **Docker** nor **Prancer** but more how to use it in a CI/CD context that leverages **Docker** containers.

Before taking this tutorial, ensure the following:

1. You have the **Docker engine** [installed (Link to Ubuntu flavor)](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Then, you can follow these steps:

1. Create a **Prancer** image for **Docker**
2. Create a **Prancer** project
3. Run the tests
4. Trigger a failure
5. Cleanup and rejoice

> <NoteTitle>Shortcut</NoteTitle>
>
> You can use [https://github.com/prancer-io/prancer-docker-tutorial](https://github.com/prancer-io/prancer-docker-tutorial) instead of writting the files yourself. This repository contains exactly the same file structure and content.

# Create a **Prancer** image for **Docker**

**tests/prancer/docker/Dockerfile**

    FROM ubuntu

    RUN DEBIAN_FRONTEND=noninteractive apt update -y && \
        DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip git && \
        pip3 install prancer-basic

    CMD prancer
    WORKDIR /prancer/project

This creates a simple image that contains **Prancer** and **Git**. Depending on the configuration of your projet, you may need additional tools installed.

Now let's build the image:

     cd tests/prancer
     docker build docker --tag prancer

Once this is done, you'll have the image built and tagged into your system. It should output a log that looks like this:

    Sending build context to Docker daemon  22.53kB
    Step 1/4 : FROM ubuntu
    ---> 4c108a37151f
    Step 2/4 : RUN DEBIAN_FRONTEND=noninteractive apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip mongodb git && pip3 install prancer-basic
    ---> Using cache
    ---> d8f616cda4d4
    Step 3/4 : CMD prancer
    ---> Using cache
    ---> 48cae0b129df
    Step 4/4 : WORKDIR /prancer/project
    ---> Using cache
    ---> b34102a2985a
    Successfully built b34102a2985a
    Successfully tagged prancer:latest

If you list your images, you should see the **Prancer** image we just built:

    docker images

    REPOSITORY      TAG         IMAGE ID            CREATED              SIZE
    prancer         latest      b34102a2985a        About a minute ago   1.12GB

We can now build our **Prancer** project.

# Create a **Prancer** project

Next, we'll need a **Prancer** project. To run tests against a **Git** repository, well, you need a **Git** repository with files in it. This portion will create such as repository along with the files for the **Prancer** project. We'll commit files to it and then configure the **Git** connector for that specific repository and project.

**data/config.json**

    {
        "webserver": {
            "port": 80
        }
    }

**tests/prancer/project/.gitignore**

    log/*
    *.log
    output-*json

**tests/prancer/project/config.ini**

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

**tests/prancer/project/gitConnector.json**

    {
        "fileType": "structure",
        "companyName": "prancer-test",
        "gitProvider": "https://github.com/prancer-io/prancer-docker-tutorial.git",
        "branchName":"master",
        "private": false
    }

> <NoteTitle>Changes</NoteTitle>
>
> Remember to substitute the **gitProvider** with your own!

**tests/prancer/project/validation/git/snapshot.json**

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

**tests/prancer/project/validation/git/test.json**

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

Then commit this setup to a repository that is accessible using git such as on **GitHub**. Note that you must create the repository beforehand.

    git init
    git remote add origin git@github.com:your-user/prancer-docker-tutorial.git
    git add .
    git commit -m "Tutorial on jenkins"
    git push

Following this, you should be able to see your code on your repository.

# Run the tests

Before running the tests, we'll need a **MongoDB** server. If you are using your own and properly updated the configuration files, perfect. On the other hand, if you need a server, the best solution is to just start one in a **Docker** container. Skip the next step if you already have a server that is reachable.

## Starting a MongoDB in a docker container

Starting a **MongoDB** server is easy but because you want to have multiple containers communicating, you'll need to create a network to link both of them together.

    docker network create prancer

Then we can start the MongoDB server in that network:

    docker run -d --name prancer-mongodb-server -it --network prancer mongo

Now that you have a docker container with **MongoDB** running in it, you can add, to your next docker command line, the network, using:

    docker ... --network prancer ...

And you can set the `dburl` in your configuration file to:

    dburl=mongodb://prancer-mongodb-server:27017/validator

Thats it, you now have a dockerized **MongoDB** server.

## Running a Prancer test

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase. If you are using a connected container for **MongoDB**, add the `--network prancer` argument to it before the `prancer` image name.

    # First ensure you are in the root of the repository / the folder containing the `tests/prancer`:
    cd "root-of-whole-project"

    # Without dockerized mongodb server
    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" prancer prancer git

    # or with dockerized mongodb server
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

Because this tutorial asked you to create a temporary **Git** repository on a public service, it would be good if you destroyed it since you won't need it anymore.

Furthermore, if you have used the containerized **MongoDB**, it would be wise to drop it and the related network using:

    docker stop prancer-mongodb-server
    docker rm prancer-mongodb-server
    docker network remove prancer

# Conclusion

That's it, you are done. You now know how to create a working **Docker** image with **Prancer** in it.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!