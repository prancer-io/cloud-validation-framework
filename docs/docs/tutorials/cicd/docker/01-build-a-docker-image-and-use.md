This tutorial will show you all the steps required to build a basic **Docker image** that can be used to run **Prancer** in any **Docker** based environment. This tutorial doesn't show how to use **Docker** nor **Prancer** but more how to use it in a CI/CD context that leverages **Docker** containers.

Before taking this tutorial, ensure the following:

1. You have the **Docker engine** [installed (Link to Ubuntu flavor)](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Then, you can follow these steps:

1. Create a **Prancer** image for **Docker**
2. Create a **Prancer** project
3. Run the tests
4. Trigger a failure
5. Cleanup and rejoice

# Create a **Prancer** image for **Docker**

First, we'll need to setup **Prancer** into a **Docker** image. Let's create the standard `Dockerfile` and add the following content to it:

**tests/prancer/docker/Dockerfile**

    FROM ubuntu

    RUN DEBIAN_FRONTEND=noninteractive apt update -y && \
        DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip mongodb git && \
        pip3 install prancer-basic

    CMD prancer
    WORKDIR /prancer/project

This creates a simple image that contains **Prancer**, **MongoDB** and **Git**. Depending on the configuration of your projet, you may need additional tools installed.

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

> <NoteTitle>Limitation</NoteTitle>
>
> There is a known limitation with the software right now, you cannot setup **MongoDB** anywhere else than on the machine you run **Prancer**. This is why we are installing **MongoDB** server directly into the container.
>
> There are workarounds such as reverse tunneling the port 27017 into a container or server but that makes it even more complex. We are actively working on a solution!

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

> <NoteTitle>Shortcut</NoteTitle>
>
> You can just use [https://github.com/prancer-io/prancer-docker-tutorial](https://github.com/prancer-io/prancer-docker-tutorial) if you want, it contains exactly the same thing.


# Run the tests

Once you are ready to execute your tests, you can run the following command to start a snapshot and a testing phase:

    docker run --rm -it -v "$(pwd)/tests/prancer/project:/prancer/project" prancer bash -c "service mongodb restart && prancer git"

Let's deconstruct this to understand each part:

1. `docker run --rm -it`

    The standard command that will run an image with terminal emulation, input support and kill the container once the process is done!

2. `-v "$(pwd)/tests/prancer/project:/prancer/project"`

    This part tells **Docker** to map the current directory's `/tests/prancer/project` folder to `/prancer/project` inside the container. This is necessary because **Prancer** is configured to execute from that directory. You can override the working directory using `-w <folder>` and map the project somewhere else but it won't give you any added benefit.

    Note that by binding this, your logs will be put in the mounted volume which means you won't lose them once the process is done. Because of the **MongoDB** limitation though, you will lose your **MongoDB** data if you don't add an additional `-v "$(pwd)/mongo:/data/db". This isn't critical but can be favorable depending on your testing approach.

3. `prancer`

    This is simply the image name. If you tagged the image name differently when you built it earlier, change this.

4. `bash -c "service mongodb restart && prancer git"`

    This is the command that we'll execute in the container. The command needs to be complex in this case because we have a limitation due to **MongoDB** needing to be started when the container gets activated. If you do not string the 2 commands back to back like this, **Prancer** will complain that it cannot connect to **MongoDB**.

    The last part of the command is the **Prancer** container to validate. In this case, we called it `git`. If you renamed the container in `tests/prancer/project/validation` then you need to change this here.

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

Apart from that, no other resources should have been created.

# Conclusion

That's it, you are done. You now know how to create a working **Docker** image with **Prancer** in it.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!