> Target Platform : Basic Edition

**Prancer** uses the popular **Python 3** language interpreter. Read on to learn how to install the dependencies for **Prancer** but also the framework itself. You can install **Prancer** using the source code available on **GitHub** or using the **Pip** package manager.

# Installing Prerequisites

    - Python 3.6
    - pip3

Installing **Python3** is fairly simple on most OS' as they will provide you with either a package manager or, for `Windows`, you will be able to find an installer on the official **Python3** [download page](https://www.python.org/downloads/).

Assuming you are using a popular Linux distribution that is **Debian** or **Red hat** based, it should be as simple as running the following command from your terminal:

    sudo apt install python3 python3-pip

or

    sudo yum install python3 python3-pip

> Please refer to the **Python3** [download page](https://www.python.org/downloads/) for instructions if you can't seem to install **Python3**, we cannot give support for this.

# Installing Prancer using Pip

To install **Prancer**, you just need to run a command using **Pip** (the **Python 3** package manager) to install the packaged version:

    sudo -H pip3 install prancer-basic

To test that everything works fine, run the following command:

    prancer --version

If you see something like:

    Prancer 1.0.4

Then it means everything worked fine.

> Note that if you are a **Python** developer and use an environment switcher or if you are a power user that played around with the aliases, you might need to just use `pip` instead of `pip3`. In the same optic, if you changed the alias, the `prancer` alias might not work properly as it expects `python3`.

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

    2019-04-12 09:47:18,556(cli_validator:  23) - Command: 'python3 /usr/local/bin/prancer --help'
    usage: Prancer Basic Functionality [-h] [-v] [--db {NONE,SNAPSHOT,FULL}]
                                   [--crawler] [--test TEST]
                                   [--customer CUSTOMER]
                                   container

    positional arguments:
        container             Container tests directory.

    optional arguments:
        -h, --help            show this help message and exit
        -v, --version         Show prancer version
        --db {NONE,SNAPSHOT,FULL}
                                NONE - Mongo database not used, SNAPSHOT - for storing
                                snapshots, FULL - Tests, configurations, outputs and
                                snapshots in database
        --crawler             Crawl and generate snapshot files only
        --test TEST           Run a single test in NODB mode
        --customer CUSTOMER   customer name for config

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