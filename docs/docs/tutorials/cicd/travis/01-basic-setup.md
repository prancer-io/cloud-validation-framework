This tutorial will show you all the steps required to setup a basic **Travis CI** build project that could leverage **Prancer** in one of the build steps. This tutorial doesn't show how to use **Prancer** but more how to use it in a CI/CD setup such as **Travis CI**.

Before taking this tutorial, ensure the following:

1. You have a **GitHub** account
2. You have a public repository that you can put files in 
    1. If you have a commercial Travis CI account, you can use a private GitHub repository!

Then, you can follow these steps:

1. Checkout example files
2. Create your own GitHub repository for Travis
3. Create a **Prancer** project
4. Create a **Travis CI** build project
5. Run the build job
6. Trigger a failure
7. Cleanup and rejoice

# Checkout example files

We have all the files already prepared for you in a public read-only repository. 

We'll still show all the content of each files in this tutorial and explain some tweaks you can and should do. You can use your own repository and write the files yourself but it'll be easier and faster if you checkout ours:

    cd <working directory>
    git clone https://github.com/prancer-io/prancer-travis-tutorial
    cd prancer-travis-tutorial

# Create a **Prancer** project

First, we'll need a **Prancer** project. This is where all the configuration and test files will live. Here's the content of each file with a brief description.

## .travis.yml

This is the file **Travis** uses to run the building and testing process.

    language: python
    python:
       - "3.6"
    services:
       - docker
    install:
       - pip install prancer-basic
       - pip install --upgrade pyasn1-modules
    script:
       - docker run -d --name prancer_mongo -p 27017:27017 mongo
       - cd tests/prancer
       - prancer git-container

> If you copy paste this, you may have to reformat the file. YAML files use 2 spaces for each "tab".

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
    dburl = mongodb://localhost:27017/validator
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
        "gitProvider": "https://github.com/prancer-io/prancer-travis-tutorial.git",
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

# Create your own GitHub repository for Travis

Next, we need to indicate Travis which repository to watch to run the tests.

## Create a repository on GitHub and push your code

First, login to your GitHub account and create a repository named `prancer-travis-tutorial`. 

Then, in the file `tests/prancer/project/gitConnector.json`, change the `gitProvider` to use your own repository. Remember to use the **https** version if you don't have ssh access to that repository as you won't have a key on **Travis**. The file should now look like:

    {
        "fileType": "structure",
        "companyName": "prancer-test",
        "gitProvider": "https://github.com/crazycodr/prancer-travis-tutorial.git",
        "branchName":"master",
        "private": false
    }

Finally, push the files you have on disk to that repository. Remember to commit your changes to `tests/prancer/project/gitConnector.json` before your push your files. You should run:

    git remote rm origin
    git remote add origin <your-github-clone-url>
    git add .
    git commit -m "Adjust configuration for my repository"
    git push

This should push your files to your repository. Refresh the **GitHub** page to confirm your files are there!

## Create a **Travis CI** build project

The next part is to bind **Travis CI** to your repository:

1. Visit the [GitHub Marketplace](https://github.com/marketplace) and search for the **Travis** application

    ![Travis CI project name](/images/travis-search-app.png)

2. Select the **Travis** Application and then scroll down to the bottom to select the `Open source` plan

    ![Travis CI project name](/images/travis-add-app.png)

3. Click `Install it for free`

    > If you already installed it before for other projects, it will be impossible to install. Just skip to the next step!

4. Visit the [repositories](https://travis-ci.com/account/repositories) page on **Travis** and click the `Settings` button on the repository where your code is stored

    ![Travis CI project name](/images/travis-repositories.png)

5. Ensure the `Build pushed branches` is turned on, alternatively, if you want to work with a pull request, ensure that one is also turned on

    ![Travis CI project name](/images/travis-configure-project.png)

# Run the build job

Now let's run the job to ensure the test works:

1. Go to the job's page (Something like [https://travis-ci.com/prancer-io/prancer-travis-tutorial](https://travis-ci.com/prancer-io/prancer-travis-tutorial) but for your repository

2. Click on the button `More options` in the top right and select `Trigger build`. Alternatively, you can just commit something on your branch and push it.

    ![Travis CI - Build options](/images/travis-build-options.png)

This will trigger the build. It can take a few seconds to complete as there are a lot of things going on in there:

1. It will activate the **Docker** service
2. It will install the **Prancer** tool
3. It will pull the **MongoDB** docker image and start the container
4. It will run the **Prancer** tests

You should see a log of all this as it goes, and it should look something like in the end:

    2019-09-01 17:24:04,864(interpreter: 209) - ###########################################################################
    2019-09-01 17:24:04,865(interpreter: 210) - Actual Rule: {1}.webserver.port=80
    2019-09-01 17:24:04,877(interpreter: 219) - **************************************************
    2019-09-01 17:24:04,878(interpreter: 220) - All the parsed tokens: ['{1}.webserver.port', '=', '80']
    2019-09-01 17:24:04,879(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}}
    2019-09-01 17:24:04,880(rule_interpreter:  36) - <class 'dict'>
    2019-09-01 17:24:04,883(rule_interpreter:  78) - Regex match- groups:('1', '.webserver.port'), regex:\{(\d+)\}(\..*)*, value: {1}.webserver.port, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f91e6a700f0>> 
    2019-09-01 17:24:04,884(rule_interpreter: 121) - matched grps: ('1', '.webserver.port'), type(grp0): <class 'str'>
    2019-09-01 17:24:04,886(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-09-01 17:24:04,887(rule_interpreter:  78) - Regex match- groups:('80', None), regex:(\d+)(\.\d+)?, value: 80, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f91e6a700f0>> 
    2019-09-01 17:24:04,889(rule_interpreter: 169) - LHS: 80, OP: =, RHS: 80
    2019-09-01 17:24:04,890(rundata_utils:  92) - END: Completed the run and cleaning up.

As you can see here, the rule interpreter ran fine and compared `80` to `80` which ended up as a success!

# Trigger a failure

Now that we have a working example, let's simulate a failure by changing the file we are inspecting and use a wrong value.

1. In `data/config.json`, change the port value for `443` instead of `80`, it should look like this instead:

        {
            "webserver": {
                "port": 443
            }
        }

2. Commit and push to your repository. **Travis** will build this new commit and it will end in an error with something like this:

        2019-09-01 17:32:27,480(interpreter: 209) - ###########################################################################
        2019-09-01 17:32:27,481(interpreter: 210) - Actual Rule: {1}.webserver.port=80
        2019-09-01 17:32:27,493(interpreter: 219) - **************************************************
        2019-09-01 17:32:27,494(interpreter: 220) - All the parsed tokens: ['{1}.webserver.port', '=', '80']
        2019-09-01 17:32:27,495(rule_interpreter:  35) - {'dbname': 'validator', 'snapshots': {'1': 'security_groups'}}
        2019-09-01 17:32:27,496(rule_interpreter:  36) - <class 'dict'>
        2019-09-01 17:32:27,499(rule_interpreter:  78) - Regex match- groups:('1', '.webserver.port'), regex:\{(\d+)\}(\..*)*, value: {1}.webserver.port, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7ff2722d2c18>> 
        2019-09-01 17:32:27,500(rule_interpreter: 121) - matched grps: ('1', '.webserver.port'), type(grp0): <class 'str'>
        2019-09-01 17:32:27,502(rule_interpreter: 150) - Number of Snapshot Documents: 1
        2019-09-01 17:32:27,503(rule_interpreter:  78) - Regex match- groups:('80', None), regex:(\d+)(\.\d+)?, value: 80, function: <bound method RuleInterpreter.match_number of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7ff2722d2c18>> 
        2019-09-01 17:32:27,504(rule_interpreter: 169) - LHS: 443, OP: =, RHS: 80
        2019-09-01 17:32:27,506(rundata_utils:  92) - END: Completed the run and cleaning up.

    As you can see here, the rule interpreter ran fine and compared `443` to `80` which ended up as a failure!

# Cleanup and rejoice

None of the resources created should cost anything to keep unless you used a team github organization and a commercial Travis license. If you want to cleanup everything, here is a quick list of what you need to think about:

1. Visit [Travis CI repositories](https://travis-ci.com/account/repositories) and disconnect your `prancer-travis-tutorial` project
2. Visit [GitHub](https://github.com/) to delete the `prancer-travis-tutorial` repository

# Conclusion

That's it, you are done. You now know how to setup a basic `Prancer` test in **Travis CI**.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!