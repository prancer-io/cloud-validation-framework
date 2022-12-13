# Prancer Basic CLI installation

**Prancer** uses the popular **Python 3** language interpreter. You can run **Prancer** platform using the source code available on **GitHub** or the **Pip** package manager. Read on to learn how to install the dependencies for **Prancer** and the framework itself.

# Installing Prerequisites

    - Python 3.6.8 / 3.8 or 3.9
    - pip3

Installing **Python3** is relatively simple on most OS' as they will provide you with either a package manager or, for `Windows`, you will be able to find an installer on the official **Python3** [download page](https://www.python.org/downloads/).

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

    Prancer 2.0.5

Then it means everything worked fine.

> Note that if you are a **Python** developer and use an environment switcher or if you are a power user that played around with the aliases, you might need to just use `pip` instead of `pip3`. If you changed the alias, the `prancer` alias might not work properly as it expects `python3`.

# Running Prancer from source code

The complete walkthrough to run the Prancer Platform from source code is available in our GitHub repository at: https://github.com/prancer-io/cloud-validation-framework
 
# Upgrading Prancer Platform basic edition

You can use `pip3` to upgrade `prancer-basic` executables on your computer.
First, you need to know to which version you want to upgrade. You can browse different versions here and find the latest available one. [click here](https://github.com/prancer-io/cloud-validation-framework/releases)

The command to upgrade is:
    pip3 install -U prancer-basic==<latest-version>

For example, if you want to upgrade to version `2.0.5`, you should run:
    pip3 install -U prancer-basic==2.0.5

<iframe width="560" height="315" src="https://www.youtube.com/embed/lvEdvAQm80Y" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
