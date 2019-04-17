# Tutorial - Setup the Prancer environment

This tutorial will direct you through all the steps required to setup your environment to properly run `Prancer`.

> **These steps only need to be done once**
>
> If you have already followed this tutorial, you can skip it and go back to the original tutorial that sent you here.

## Prepare your OS

This tutorial assumes a few things:

1. You use the popular [Ubuntu](https://ubuntu.com) Linux operating system
2. You have the [Git](https://git-scm.org) version control tools installed

Let's first update your system and then install the `python3` package manager `pip`:

    sudo apt update
    sudo apt install python3-pip

Then, let's install the `Prancer` validation tools using `pip`:

    sudo -H pip3 install prancer-basic

> The -H switch to `sudo` sets the HOME environment variable to the HOME of the current user.

Finaly, let's test the installation by running the `validator` utility:

    validator --help

If you see something like:

    2019-04-12 09:47:18,556(cli_validator:  23) - Comand: 'python3 /usr/local/bin/validator --help'
    usage: Validator functional tests. [-h] [--db] container

    positional arguments:
    container   Container tests directory.

    optional arguments:
    -h, --help  show this help message and exit
    --db        Mongo to be used for input and output data.

Then it means everything worked fine. 

Let's move on!

## Install MongoDB

> If you already have `MongoDB` installed, then you can skip this.

Next up, let's install a `MongoDB` server on your system:

    sudo apt install mongodb

This should be more than enough to get the `MongoDB` database server running. Test it out with:

    mongo

It should get you into a prompt to manipulate your `MongoDB` server and show you some log lines. You can CTRL-C out of it.

> You could also use a [MongoDB Docker container](https://hub.docker.com/_/mongo) instead and set the data to be stored in a data volume. As long as your configuration points to the right port, it will work fine.

## Check out the Prancer framework

Next, we need to check out the `Prancer` framework into a directory. This framework contains different tools that help you create configuration files with ease and utilities used by the `validator`.

You do not need to check out the framework to a directory that is used by your project. In fact, you should put it somewhere outside of your project directory or, at least, in a vendor directory that is not commited with your project.

    git clone https://github.com/prancer-io/cloud-validation-framework.git

## Tell the validator tool where to find the framework

The `validator` needs to be told where to find the framework that you just downloaded with GIT. Everytime you start a new console terminal, you should export an environment variable with the following:

    export FRAMEWORKDIR="<path to framework parent>"

> This environment variable should contain the path to the directory containing your folder "cloud-validation-framework" not directly into the framework folder.

## Conclusion

That's it, you are done.

You can now go back to the previous tutorial that brought you here to continue looking at the tutorials on [Prancer's Guidance section](http://www.prancer.io/guidance/)