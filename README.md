[![Build Status](https://ebizframework.visualstudio.com/whitekite/_apis/build/status/github-ci-pipeline?branchName=master)](https://ebizframework.visualstudio.com/whitekite/_build/latest?definitionId=8&branchName=master)

# What is prancer?

To move to the cloud, companies are using various methods to provision and deploy resources. That includes custom built scripts, manual provisioning from web-based interfaces, using of available provisioning engines and use of custom automation frameworks. Since the deployed resources in the cloud could grow exponentially over the time, Security Operators (SecOps) team should be equipped with the right tools for the cloud governance.

Prancer is a multi-cloud validation framework which can be used by any company Security Operators to validate and verify the cloud implementation after the deployment.
This post-deployment validation framework can connect to multiple cloud providers including Microsoft Azure, Amazon AWS and Google cloud to validate the resources you have deployed in the cloud. (other cloud providers are in development: Oracle, VMWare, Cloud Foundation, …)

Prancer engine has high capability to read out the configuration attributes from any text file or automation framework and use it as a blueprint to compare to the configuration values you have in your cloud implementation. It can read out the values from your cloud provisioning engine and compare it to the deployed resources to validate the implementation and find out any delta.

for more information you can check the website: http://www.prancer.io

## prancer installation
--  python3 package manager is pip3, install it for the system.
`sudo apt-get install python3-pip`

--  Will require the python mongo client library for interaction
`sudo pip3 install pymongo`

--  Will use requests library for http and https
`sudo pip3 install requests`

--  Need antlr runtime
`pip install antlr4-python3-runtime`

--  Parsing HCL
`pip install pyhcl==0.3.10`

-- install requirements
`pip install -r requirements.txt`

Mongo DB version used - 3.2.21 , can be upgraded to 3.4.18 or even ater 3.6.9. The latest current release is 4.0.4
Upgrade to 4.0.4 version and check the basic connections and query APIs.

TODO - Version selection and features involved.

### how to set the environment
`cd <project-folder>`
`export PYTHONPATH=`pwd`:$PYTHONPATH`
`echo $PYTHONPATH`
`antlr4 -Dlanguage=Python3 comparator.g4`

### how to start mongoDB
to start mongoDB at windows subsystem for linux
`screen -d -m mongod --config /etc/mongod.conf # start mongo server`
`screen -r # press ctrl+c to stop daemon`

### how to run the framework
`python3 validator.py container1`
`python3 validator.py container1 --db`

### how to run the unit tests
`py.test --cov=src/processor tests/ --cov-report term-missing`

