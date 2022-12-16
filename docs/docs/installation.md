# Prancer Basic CLI installation

**Prancer** uses the popular **Python3** language interpreter. You can run **Prancer** platform using the source code available on **GitHub** or the **Pip** package manager. Read on to learn how to install the dependencies for **Prancer** and the framework itself.

# Installing Prerequisites

    - Python 3.6.8 / 3.8 or 3.9
    - pip3

Installing **Python3** is relatively simple on most OS' as they will provide you with either a package manager, or for `Windows`, you will be able to find an installer on the official [**Python3** download page](https://www.python.org/downloads/).

Assuming you are using a popular Linux distribution that is **Debian** or **Red hat** based, it should be as simple as running the following command from your terminal:

    sudo apt install python3 python3-pip

or

    sudo yum install python3 python3-pip

> Please refer to the [**Python3** download page](https://www.python.org/downloads/) for instructions if you can't seem to install **Python3**, we cannot give support for this.

# Installing Prancer using Pip

To install **Prancer**, you just need to run a command using **Pip** (the **Python 3** package manager) to install the packaged version:

    sudo -H pip3 install prancer-basic

To test that everything works fine, run the following command:

    prancer --version

If you see something like:

    Prancer 2.1.46

Then it means everything worked fine.

> Note that if you are a **Python** developer and use an environment switcher or if you are a power user that played around with the aliases, you might need to just use `pip` instead of `pip3`. If you changed the alias, the `prancer` alias might not work properly as it expects `python3`.

# Running Prancer from source code

The complete walkthrough to run the Prancer Platform from source code is available in our GitHub repository at: [https://github.com/prancer-io/cloud-validation-framework](https://github.com/prancer-io/cloud-validation-framework)
 
 # Installing Prancer from source

If you want to run **Prancer** using its source code, then you can checkout the source code from our public **Git** repository on **GitHub**. This is a community available tool, anyone can download the source code, look at it, report bugs and even contribute to it provided the contribution rules have been observed properly.

Go to a directory of your choice, but not in your web application's project directory and then checkout the source code there. Assuming you have [Git](https://git-scm.com/downloads) installed, just run:

    git clone https://github.com/prancer-io/cloud-validation-framework.git

Then change directory to the cloned directory:

    cd cloud-validation-framework

You will also need to install the requirements for the framework to ensure proper usage:

    pip3 install -r requirements.txt

export the following variables:


    export BASEDIR=`pwd`
    export PYTHONPATH=$BASEDIR/src
    export FRAMEWORKDIR=$BASEDIR

From that point on, you can run the tool manually using:

    python3 utilities/validator.py <arguments>

If you see something like:

    usage: prancer [-h] [-v] [--db {NONE,SNAPSHOT,FULL,REMOTE}] [--crawler] [--compliance] [--file_content FILE_CONTENT] [--mastertestid MASTERTESTID] [--mastersnapshotid MASTERSNAPSHOTID]
                [--snapshotid SNAPSHOTID] [--env {DEV,QA,PROD,LOCAL}] [--apitoken APITOKEN] [--gittoken GITTOKEN] [--company COMPANY] [--createsnapshot] [--mastersnapshotfile MASTERSNAPSHOTFILE]
                [collection]

    positional arguments:
    collection            The name of the folder which contains the collection of files related to one scenario

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         Show prancer version
    --db {NONE,SNAPSHOT,FULL,REMOTE}
                            NONE - Database will not be used, all the files reside on file system, SNAPSHOT - Resource snapshots will be stored in db, everything else will be on file system, FULL - tests,
                            configurations, outputs and snapshots will be stored in the database REMOTE - Connect to Prancer Enterprise solution to get the configuration files and send the results back.
    --crawler             Crawls the target environment and generates snapshot configuration file
    --compliance          Run only compliance tests based on the available snapshot configuration file
    --file_content FILE_CONTENT
    --mastertestid MASTERTESTID
                            Run the framework only for the master test Ids or compliance Ids mentioned here
    --mastersnapshotid MASTERSNAPSHOTID
                            Run the framework only for the master snapshot Ids mentioned here
    --snapshotid SNAPSHOTID
                            Run the framework only for the snapshot Ids mentioned here
    --env {DEV,QA,PROD,LOCAL}
                            DEV - API server is in dev environment, QA - API server is in qa environment, PROD - API server is in prod environment LOCAL - API server is in local environment.
    --apitoken APITOKEN   API token to access prancer saas solution. (This argument is needed only when the --db is REMOTE).
    --gittoken GITTOKEN   github/enterprise/internal github API token to access repositories. (This argument is optional only when the --db is REMOTE)
    --company COMPANY     company name of the prancer saas solution (This argument is needed only when the --db is REMOTE)
    --createsnapshot      To generate all the snapshots after crawler is completed.
    --mastersnapshotfile MASTERSNAPSHOTFILE
                            To run crawler for the specific mastersnapshot file.

Then it means everything worked fine.

# Installing MongoDB

**MongoDB** server is an optional installation to run prancer framework. It is possible to store all the output files on the filesystem. You need a **MongoDB** server to store snapshots of your resources but also, some of the configurations can be stored on it instead of in filesystem. 

> <NoteTitle>Optional dependency</NoteTitle>
>
> You can specify a remote **MongoDB** server url in your configuration files. Therefore, you do not need to install it on your system. We will assume, in all examples, that you have such a server installed locally. 
>
> If you don't and want to use a distant server, remember to configure the `dburl` setting. See this in the [configuration page](configuration/basics.md).
You can use the community edition of **MongoDB** and provided you are on a popular **Linux** distribution, it should be as simple as:

    sudo apt install mongodb

or

    sudo yum install mongodb

To ensure **MongoDB** works fine, run:

    mongo

If you see the **Mongo shell** start, everything works fine, you can exit it.

> Refer to the official [MongoDB Installation](https://docs.mongodb.com/manual/installation/) for more information.

# Upgrading Prancer Platform basic edition

You can use `pip3` to upgrade `prancer-basic` executables on your computer.
First, you need to know, which version you want to upgrade. You can browse different versions and find the latest available one. [click here](https://github.com/prancer-io/cloud-validation-framework/releases)

The command to upgrade is:
    `pip3 install -U prancer-basic==<latest-version>`

For example, if you want to upgrade to version `2.1.46`, you should run:
    `pip3 install -U prancer-basic==2.1.46`

<iframe width="560" height="315" src="https://www.youtube.com/embed/lvEdvAQm80Y" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>