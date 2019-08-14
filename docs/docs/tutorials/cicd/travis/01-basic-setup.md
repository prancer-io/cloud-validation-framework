This tutorial will show you all the steps required to setup a basic **Travis CI** build project that could leverage **Prancer** in one of the build steps. This tutorial doesn't show how to use **Prancer** but more how to use it in a CI/CD setup such as **Travis CI**.

Before taking this tutorial, ensure the following:

1. You have a **GitHub** account
2. You have a public repository that you can put files in 
    1. If you have a commercial Travis CI account, you can use a private GitHub repository!

Then, you can follow these steps:

1. Create a **Prancer** project
2. Create a **Travis CI** build project
3. Run the build job
4. Trigger a failure
5. Cleanup and rejoice

# Create a **Prancer** project

First, we'll need a **Prancer** project. We'll store all of our **Prancer** project file in what would be a standard web application project. We'll add to that a JSON file that contains data to validate and our **Travis CI** `.travis.yml` file.

> <NoteTitle>Shortcut</NoteTitle>
>
> You can use [https://github.com/prancer-io/prancer-travis-tutorial](https://github.com/prancer-io/prancer-travis-tutorial) if you want, it contains exactly the same thing that you will be creating below but you still need to change some configuration in it.

Create an empty directory and copy all the following files in their proper location as indicated by the filenames:

**.travis.yml**

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

**data/json/valid-file.json**

    {
        "someobject": {
            "configuration": {
                "hello": "world"
            }
        }
    }

**data/json/invalid-file.json**

    {
        "someobject": {
            "configuration": {
                "hello": "hell"
            }
        }
    }

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

**tests/prancer/gitConnector.json**

    {
        "fileType": "structure",
        "companyName": "Organization name",
        "gitProvider": "https://github.com/prancer-io/prancer-travis-tutorial.git",
        "branchName": "master",
        "private": false
    }

Remember to substitute the `gitProvider` for your own repository.

**tests/prancer/validation/git-container/snapshot.json**

    {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "gitConnector",
                "type": "git",
                "testUser": "git",
                "branchName": "master",
                "nodes": [
                    {
                        "snapshotId": "1",
                        "type": "json",
                        "collection": "json_data",
                        "path": "data/json/valid-file.json"
                    }
                ]
            }
        ]
    }

**tests/prancer/validation/git-container/test.json**

    {
        "fileType": "test",
        "snapshot": "snapshot",
        "testSet": [
            {
                "testName ": "Ensure salutes the world",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "1",
                        "rule": "{1}.someobject.configuration.hello = 'world'"
                    }
                ]
            }
        ]
    }

Then commit this setup to a repository that is accessible using git such as on **GitHub** or **CodeCommit**. Note that you must create the repository beforehand.

    git init
    git remote add origin git@github.com:your-user/some-repo.git
    git add .
    git commit -m "Tutorial on Travis CI"
    git push

Following this, you should be able to see your code on your repository.

# Create a **Travis CI** build project

The next part is to create your **Travis CI** project to run **Prancer** tests.

1. Visit the [GitHub Marketplace](https://github.com/marketplace) and search for the **Travis** application

    ![Travis CI project name](/images/travis-search-app.png)

2. Select the **Travis** Application and then scroll down to the bottom to select the `Open source` plan

    ![Travis CI project name](/images/travis-add-app.png)

3. Click `Install it for free`
4. Visit the [repositories](https://travis-ci.com/account/repositories) page on **Travis** and click the `Settings` button on the repository where your code is stored

    ![Travis CI project name](/images/travis-repositories.png)

5. Ensure the `Build pushed branches` is turned on, alternatively, if you want to work with a pull request, ensure that one is also turned on

    ![Travis CI project name](/images/travis-configure-project.png)

# Run the build job

Now let's run the job to ensure the test works:

1. Go to the job's page (Something like [https://travis-ci.com/prancer-io/prancer-travis-tutorial](https://travis-ci.com/prancer-io/prancer-travis-tutorial)

2. Click on the button `More options` in the top right and select `Trigger build`. Alternatively, you can just commit something on your branch and push it.

    ![Travis CI - Build options](/images/travis-build-options.png)

This will trigger the build. It can take a few seconds to complete as there are a lot of things going on in there:

1. It will activate the **Docker** service
2. It will install the **Prancer** tool
3. It will pull the **MongoDB** docker image and start the container
4. It will run the **Prancer** tests

You should see a log of all this as it goes, and it should look something like:

    Worker information
    Build system information
    docker stop/waiting
    resolvconf stop/waiting
    0.01s$ sudo service docker start
    0.58s$ git clone --depth=50 --branch=master https://github.com/prancer-io/prancer-travis-tutorial.git prancer-io/prancer-travis-tutorial
    0.01s$ source ~/virtualenv/python3.6/bin/activate
    $ python --version
    Python 3.6.3
    $ pip --version
    pip 9.0.1 from /home/travis/virtualenv/python3.6.3/lib/python3.6/site-packages (python 3.6)
    install.1
    15.61s$ pip install prancer-basic
    0.60s$ pip install --upgrade pyasn1-modules
    11.17s$ docker run -d --name prancer_mongo -p 27017:27017 mongo
    Unable to find image 'mongo:latest' locally
    latest: Pulling from library/mongo
    Status: Downloaded newer image for mongo:latest
    5b1004b33d219bb0a7bdc4b73984b533ee2ab1777283382afb690ca11b0d5e30
    The command "docker run -d --name prancer_mongo -p 27017:27017 mongo" exited with 0.
    0.00s$ cd tests/prancer
    The command "cd tests/prancer" exited with 0.
    1.88s$ prancer git-container
    2019-06-20 01:07:27,646(cli_validator: 170) - START: Argument parsing and Run Initialization.
    2019-06-20 01:07:27,722(cmd: 722) - Popen(['git', 'version'], cwd=/home/travis/build/prancer-io/prancer-travis-tutorial/tests/prancer, universal_newlines=False, shell=None)
    2019-06-20 01:07:27,726(cmd: 722) - Popen(['git', 'version'], cwd=/home/travis/build/prancer-io/prancer-travis-tutorial/tests/prancer, universal_newlines=False, shell=None)
    2019-06-20 01:07:27,993(cli_validator: 181) - Comand: 'python /home/travis/virtualenv/python3.6.3/bin/prancer git-container'
    2019-06-20 01:07:27,995(cli_validator: 189) - Args: Namespace(container='git-container', db=None)


If the build passes, the log will end with something like:

    2019-06-20 01:07:28,419(interpreter: 209) - ###########################################################################
    2019-06-20 01:07:28,419(interpreter: 210) - Actual Rule: {1}.someobject.configuration.hello = 'world'
    line 1:37 no viable alternative at input '{1}.someobject.configuration.hello='world''
    2019-06-20 01:07:28,432(interpreter: 219) - **************************************************
    2019-06-20 01:07:28,432(interpreter: 220) - All the parsed tokens: ['{1}.someobject.configuration.hello', '=', "'world'"]
    2019-06-20 01:07:28,432(rule_interpreter:  35) - {'dbname': 'prancer', 'snapshots': {'1': 'json_data'}}
    2019-06-20 01:07:28,433(rule_interpreter:  36) - <class 'dict'>
    2019-06-20 01:07:28,434(rule_interpreter:  78) - Regex match- groups:('1', '.someobject.configuration.hello'), regex:\{(\d+)\}(\..*)*, value: {1}.someobject.configuration.hello, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7ff512a1ca20>> 
    2019-06-20 01:07:28,435(rule_interpreter: 121) - matched grps: ('1', '.someobject.configuration.hello'), type(grp0): <class 'str'>
    2019-06-20 01:07:28,436(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-06-20 01:07:28,437(rule_interpreter:  78) - Regex match- groups:(), regex:\'.*\', value: 'world', function: <bound method RuleInterpreter.match_string of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7ff512a1ca20>> 
    2019-06-20 01:07:28,437(rule_interpreter: 169) - LHS: world, OP: =, RHS: world
    2019-06-20 01:07:28,438(rundata_utils:  92) - END: Completed the run and cleaning up.
    2019-06-20 01:07:28,439(rundata_utils: 102) -  Run Stats: {
        "start": "2019-06-20 01:07:27",
        "end": "2019-06-20 01:07:28",
        "errors": [],
        "host": "travis-job-586d94e0-203d-4dfa-bb4e-83ea3bf2e309",
        "timestamp": "2019-06-20 01:07:27",
        "log": "/home/travis/build/prancer-io/prancer-travis-tutorial/tests/prancer/log/20190620-010727.log",
        "duration": "0 seconds"
    }
    The command "prancer git-container" exited with 0.
    Done. Your build exited with 0.

As you can see here, the rule interpreter ran fine:

    2019-06-20 01:07:28,437(rule_interpreter: 169) - LHS: world, OP: =, RHS: world

Which ended up as a success!

# Trigger a failure

Now that we have a working example, let's simulate a failure by changing the file we are inspecting and use the wrong file instead.

1. In `tests/prancer/validation/git-container/snapshot.json`, change the reference of `valid-file.json`  to `invalid-file.json`:

        {
            "snapshotId": "1",
            "type": "json",
            "collection": "json_data",
            "path": "data/json/invalid-file.json"
        }

2. Commit and push to the repository

This should automatically start a build. Once the build is complete, it should be in a failed state. The log will end with something like:

    2019-06-21 13:08:27,698(interpreter: 209) - ###########################################################################
    2019-06-21 13:08:27,699(interpreter: 210) - Actual Rule: {1}.someobject.configuration.hello = 'world'
    line 1:37 no viable alternative at input '{1}.someobject.configuration.hello='world''
    2019-06-21 13:08:27,712(interpreter: 219) - **************************************************
    2019-06-21 13:08:27,712(interpreter: 220) - All the parsed tokens: ['{1}.someobject.configuration.hello', '=', "'world'"]
    2019-06-21 13:08:27,712(rule_interpreter:  35) - {'dbname': 'prancer', 'snapshots': {'1': 'json_data'}}
    2019-06-21 13:08:27,712(rule_interpreter:  36) - <class 'dict'>
    2019-06-21 13:08:27,714(rule_interpreter:  78) - Regex match- groups:('1', '.someobject.configuration.hello'), regex:\{(\d+)\}(\..*)*, value: {1}.someobject.configuration.hello, function: <bound method RuleInterpreter.match_attribute_array of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f607ddc09e8>> 
    2019-06-21 13:08:27,714(rule_interpreter: 121) - matched grps: ('1', '.someobject.configuration.hello'), type(grp0): <class 'str'>
    2019-06-21 13:08:27,716(rule_interpreter: 150) - Number of Snapshot Documents: 1
    2019-06-21 13:08:27,716(rule_interpreter:  78) - Regex match- groups:(), regex:\'.*\', value: 'world', function: <bound method RuleInterpreter.match_string of <processor.comparison.comparisonantlr.rule_interpreter.RuleInterpreter object at 0x7f607ddc09e8>> 
    2019-06-21 13:08:27,717(rule_interpreter: 169) - LHS: hell, OP: =, RHS: world
    2019-06-21 13:08:27,717(rundata_utils:  92) - END: Completed the run and cleaning up.
    2019-06-21 13:08:27,718(rundata_utils: 102) -  Run Stats: {
        "start": "2019-06-21 13:08:27",
        "end": "2019-06-21 13:08:27",
        "errors": [],
        "host": "travis-job-f31bb1f6-b9ea-4835-8d57-cde1ddeb50c1",
        "timestamp": "2019-06-21 13:08:27",
        "log": "/home/travis/build/prancer-io/prancer-travis-tutorial/tests/prancer/log/20190621-130826.log",
        "duration": "0 seconds"
    }
    The command "prancer git-container" exited with 1.
    Done. Your build exited with 1.

As you can see here, the rule interpreter ran the rule ok but found a mismatch:

    2019-06-21 13:08:27,717(rule_interpreter: 169) - LHS: hell, OP: =, RHS: world

Therefore, **Prancer** fails the build!

# Cleanup and rejoice

None of the resources created should cost anything to keep unless you used a team github organization and a commercial Travis license. If you want to cleanup everything, here is a quick list of what you need to think about:

1. Visit [Travis CI repositories](https://travis-ci.com/account/repositories) and disconnect your `prancer-travis-tutorial` project
2. Visit [GitHub](https://github.com/) to delete the `prancer-travis-tutorial` repository

# Conclusion

That's it, you are done. You now know how to setup a basic `Prancer` test in **Travis CI**.

Things to remember:

1. **Prancer** exits with a proper exit code regarding success or failure. This means that any CI server, not just **Travis CI**, will catch the error code and stop right there if it receives an exit code that is not 0.
2. Running **Prancer** from a CI doesn't do anything else than if you ran it from your machine, you still need to build your tests and ensure they work beforehand.
3. Running tests without saving the artifacts of the tests, mostly when there are failures, will make it harder to figure out what failed. Read on the next tutorials to learn how to save your artifacts for later review.

Thank you for completing this tutorial on **Prancer**.

We hope to see you in the next tutorial!