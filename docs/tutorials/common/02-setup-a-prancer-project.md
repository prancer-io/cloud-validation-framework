# Tutorial - Setup a Prancer project

This tutorial will show you how to create a project directory for `Prancer`.

## Prancer directory

The files to operate `Prancer` should be put into your project and commited with it. All the `Prancer` files should be stored into a directory of your choice. You should avoid mixing files unrelated to `Prancer` within this directory.

Now, let's create the directory to store those files. Go to your project directory and create a directory for `Prancer` there. You can put it into a sub directory if you want, for example:

    mkdir -p tests/prancer
    cd tests/prancer

## The validation directory

The `validation` directory is the internal test directory. This is where tests will be created. All of your tests will be written inside a sub-directory of `validation` such as `container1`.

First you need to create the `validation` directory using:

    mkdir -p validation

Then you must create additional directories that will contain your test cases. These directories are called containers. They contain snapshot files and test files. For now, let's just create one:

    mkdir -p validation/container1

You can create as many as needed but all tutorials you will be following in this site will require, most of the time, only one container and it should be named: `container1`.

## Configuring the validation engine

Next, we need to configure the validation engine. The configuration file must be created at the root of the `Prancer` directory. Create a configuration file named `config.ini` and copy the following content into it:

    [TESTS]
    directory = validation/

    [REPORTING]
    directory = validation/

    [LOGGING]
    level = DEBUG
    maxbytes = 10
    backupcount = 10
    propagate = true
    directory = log
    dbname = whitekite

    [MONGODB]
    dbname1 = mongodb://localhost:27017/validator
    dbname = validator
    COLLECTION = resources
    SNAPSHOT = snapshots
    TEST = tests
    STRUCTURE = structures
    OUTPUT = outputs
    NOTIFICATIONS = notifications

    [INDEXES]
    OUTPUT = name, container, timestamp

Most of these settings are self explanatory, adjust them to fit your needs. If you need more information, visit the [Configuration documentation](http://www.prancer.io/documentation/?section=configuration)

## Conclusion

That's it, you are done.

You can now go back to the previous tutorial that brought you here to continue looking at the tutorials on [Prancer's Guidance section](http://www.prancer.io/guidance/)