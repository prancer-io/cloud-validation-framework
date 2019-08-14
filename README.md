[![Build Status](https://ebizframework.visualstudio.com/whitekite/_apis/build/status/github-ci-pipeline?branchName=master)](https://ebizframework.visualstudio.com/whitekite/_build/latest?definitionId=8&branchName=master)

# What is prancer?

To move to the cloud, companies are using various methods to provision and deploy resources. That includes custom built scripts, manual provisioning from web-based interfaces, using of available provisioning engines and use of custom automation frameworks. Since the deployed resources in the cloud could grow exponentially over the time, Security Operators (SecOps) team should be equipped with the right tools for the cloud governance.

Prancer is a multi-cloud validation framework which can be used by any company Security Operators to validate and verify the cloud implementation after the deployment.
This post-deployment validation framework can connect to multiple cloud providers including Microsoft Azure, Amazon AWS and Google cloud to validate the resources you have deployed in the cloud. (other cloud providers are in development: Oracle, VMWare, Cloud Foundation, …)

Prancer engine has high capability to read out the configuration attributes from any text file or automation framework and use it as a blueprint to compare to the configuration values you have in your cloud implementation. It can read out the values from your cloud provisioning engine and compare it to the deployed resources to validate the implementation and find out any delta.

for more information you can check the website: http://www.prancer.io

## prancer installation
For the current release the installation has to be done from github. Following are the steps:
- Clone the cloud validation framework
- Create virtual environment using `virtualenv --python=python3 cloudenv`. The cloud validation has been tested and continuously integrated with python > 3.5
- Set the virtual environment. `source cloudenv/bin/activate`
- Upgrade the package manager `pip install -U pip`
- Install the dependent packages as present in requirements.txt `pip install -r requirements.txt`
- Install mongo server and start the service. (The mongoDB could be local or remote and you can set it in config.ini file "dburl")
- Update config.ini to reflect the database server settings.
- Run the tests from the filesystem. `python3 validator.py container3`
- Populate snapshot, test and structure json and then run the tests from database. `python3 validator.py container3 --db`

