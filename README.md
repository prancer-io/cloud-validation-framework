
## Introduction
Prancer is a pre-deployment and post-deployment multi-cloud security platform for your Infrastructure as Code (IaC) and live cloud resources. It shifts the security to the left and provides end-to-end security scanning based on the Policy as Code concept. DevOps engineers can use it for static code analysis on IaC to find security drifts and maintain their cloud security posture with continuous compliance features. you can get more information from our website at : https://www.prancer.io

## prerequisites
- Linux-based OS
- Python 3.6.8 / 3.8 or 3.9
- mongo database (optional)


 > Note: mongo database is not a hard requirement to run prancer basic platform. It is possible to run the framework and write all the outputs to the file system. To learn more, you can review [prancer documentation](https://docs.prancer.io/configuration/config/)

# Running Prancer from the code
You can run Prancer Basic Platform from your file system or the database. There are three modes available:
 - `--db NONE` It means all the files are expected to be on the file system, and the results also will be written on the file system.
 - `--db SNAPSHOT` It means all the configuration files and output files will be written on the filesystem. but the resource snapshots are being kept in the database
 - `--db FULL` It means all the configuration files and snapshots are stored in the database
  
## Running Prancer with no database

- Clone the Prancer repository at `https://github.com/prancer-io/cloud-validation-framework.git`
- `cd cloud-validation-framework`
- Install the dependent packages as present in requirements.txt `pip3 install -r requirements.txt`
- export the following variables:

  ```
  export BASEDIR=`pwd`
  export PYTHONPATH=$BASEDIR/src
  export FRAMEWORKDIR=$BASEDIR
  ```
  
- Run the sample scenario from the filesystem: `python3 utilities/validator.py gitScenario --db NONE`
- Review the result `cat realm/validation/gitScenario/output-test.json`

> For more scenarios, visit our `Hello World` application at : https://github.com/prancer-io/prancer-hello-world

## Running Prancer with no database in a virtual environment
  `git clone https://github.com/prancer-io/cloud-validation-framework.git`

  `cd cloud-validation-framework`
  
  make sure python virtual environment is installed and set up. (https://docs.python.org/3/tutorial/venv.html)

  `python3 -m venv tutorial-env`

  `source tutorial-env/bin/activate`

  `pip install -r requirements.txt`
  
  export the following variables:

  ```
  export BASEDIR=`pwd`
  export PYTHONPATH=$BASEDIR/src
  export FRAMEWORKDIR=$BASEDIR
  ```

Run the sample scenario from the filesystem: `python utilities/validator.py gitScenario --db NONE`

Review the result `cat realm/validation/gitScenario/output-test.json`

## How to run `crawler`
Whenever you have the master snapshot configuration files available, you need to first run the `crawler`. Crawler finds individual objects from the target provider based on the master snapshot configuration file guidance. And generate snapshot configuration files that contains the reference to individual objects. You can crawl a target environment by specifying `--crawler` to your command.

`python utilities/validator.py gitScenario --db NONE --crawler`

To understand more about the crawling, check our documentation at : https://docs.prancer.io/crawler/crawler-definition/

## How to upload files to database and run prancer from database
First, make sure you have the MongoDB up and running. you can refer to this documentation from MongoDB: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/ 

Edit config.ini and add these lines if they are not already there
```
  [MONGODB]
  dburl = mongodb://localhost:27017/validator
  dbname = validator
  COLLECTION = resources
  SNAPSHOT = snapshots
  TEST = tests
  STRUCTURE = structures
  MASTERSNAPSHOT = mastersnapshots
  MASTERTEST = mastertests
  OUTPUT = outputs
  NOTIFICATIONS = notifications
```

You can use `populate_json.py` file in the `utilities` folder to upload files from filesystem to mongodb: 

**upload connectors**

`python utilities/populate_json.py scenario-pass --file connector.json`

Check the DB's `structures` collection to make sure the connector is uploaded successfully.

**upload snapshots**

`python utilities/populate_json.py scenario-pass --file snapshot.json`

Check the DB's `snapshots` collection to make sure the snapshot is uploaded successfully.

**upload tests**

`python utilities/populate_json.py scenario-pass --file test.json`

Check the DB's tests collection to make sure the test is uploaded successfully.

> Note: You can do the same for the scenario fail.

Now you can run the framework from the database:
`python utilities/validator.py scenario-fail --db FULL`

Check the DB's `webserver` and `outputs` collection in mongoDB to see the results.


## what are the environment variables
We have three environment variables that need to be set before running the code.

```
export BASEDIR=`pwd`
export PYTHONPATH=$BASEDIR/src
export FRAMEWORKDIR=$BASEDIR
```
`BASEDIR` is the base directory for the codebase. It is the folder you have cloned your git repository to.

`PYTHONPATH` is where the code resides. It is in the `src` folder inside the cloned directory.

`FRAMEWORKDIR` is where the configuration files available. We expect `config.ini` available in this directory. other folders are referenced in the `config.ini`

# Debugging with VSCode
Make sure these files exists under `.vscode` folder
 - launch.json
 - settings.json

The content of these files are as follows:

`launch.json`
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "env": {
                "BASEDIR": "${workspaceFolder}",
                "PYTHONPATH": "${workspaceFolder}/src",
                "FRAMEWORKDIR": "${workspaceFolder}"
            },
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "python": "${command:python.interpreterPath}",
            "args": [
                "gitScenario"
            ]
        }
    ]
}
```
In the `args` attribute, you will put the name of the `collection` you want to run the code for. For example, we have a `gitScenario` you can use for testing purposes.

`settings.json`
```
{
    "python.pythonPath": "testenv/bin/python"
}
```
In `python.pythonPath` file you put the path to your python. In the above example, we are using a virtual python environment `testenv`

> Note : These files already available in our repository and you can modify them based on your requirements.

This document helps you how to do debugging of Python applications in VSCode : https://code.visualstudio.com/docs/python/debugging

## Further documentation
To learn more about the Prancer Platform, review our [documentation site](https://docs.prancer.io)
