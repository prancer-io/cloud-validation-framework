[![Build Status](https://ebizframework.visualstudio.com/whitekite/_apis/build/status/github-ci-pipeline?branchName=master)](https://ebizframework.visualstudio.com/whitekite/_build/latest?definitionId=8&branchName=master)

# What is prancer?

To move to the cloud, companies are using various methods to provision and deploy resources. That includes custom built scripts, manual provisioning from web-based interfaces, use of available provisioning engines and use of custom automation frameworks. Since the deployed resources in the cloud could grow exponentially over the time, the Security Operators (SecOps) team should be equipped with the right tools to ensure cloud compliance.

Prancer is a multi-cloud validation framework which can be used by any company Security Operators to validate and verify cloud implementation before and after the deployment.

This pre-deployment and post-deployment validation framework can connect to multiple cloud providers including Microsoft Azure, Amazon AWS and Google cloud to validate the resources you have deployed in the cloud. (Note: other cloud providers are in development: Oracle, VMWare, Cloud Foundation, etc.)

Prancer engine has the capability to read out the configuration attributes from any parameter file or automation framework and use it as a blueprint to compare to the configuration values you have in your cloud implementation. It can read out the values from your cloud provisioning engine and compare it to the deployed resources to validate the implementation and find out any configuration drift.

Prancer cloud validation framework is equipped with industry compliance tests (HIPPA, PCI, SCI,etc,) to automatically initiate a compliance scan of your infrastructure as code (IaC) and cloud deployed resources to make sure you are in compliance.

for more information you can check the website: http://www.prancer.io

## prerequisites
- Linux based OS
- Python 3.6
- virtualenv
- mongo database 

*Note:* virtualenv is not a hard requirement. it is better to run the python code in a virtual environment. To understand more about python virtual environment, [check python website](https://docs.python.org/3/library/venv.html)

*Note:* mongo database is not a hard requirement to run prancer cloud validation framework. It is possible to run the framework and write all the outputs to the file system. To learn more, you can review [prancer documentations](https://docs.prancer.io/configuration/basics/#database-configuration)

## prancer installation
- Clone the cloud validation framework repository at `https://github.com/prancer-io/cloud-validation-framework.git`
- `cd cloud-validation-framework`
- Create virtual environment using `virtualenv --python=python3 cloudenv`. The cloud validation has been tested and continuously integrated with python > 3.5
- Set the virtual environment. `source cloudenv/bin/activate`
- Upgrade the package manager `pip install -U pip`
- Install the dependent packages as present in requirements.txt `pip install -r requirements.txt`
- Install mongo server and start the service. (The mongoDB could be local or remote and you can set it in config.ini file "dburl")
- Update config.ini to reflect the database server settings.
- export the following variables:
  ```
  export BASEDIR=`pwd`
  export PYTHONPATH=$BASEDIR/src
  export FRAMEWORKDIR=$BASEDIR
  ```
- Run the tests from the filesystem: `python utilities/validator.py gitScenario`
