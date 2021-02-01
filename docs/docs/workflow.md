**Prancer** expects some configuration files to be available on your system, in order to complete its workflow.
We have two options to get up and running with prancer cloud validation framework:
    - Easy way
    - Hard way

# prancer workflow: easy way
The easiest way (recommended way) is to clone the `Hello World!` application and start building your project around that.

> you can find the detail of the `Hello World` application [here](https://www.prancer.io/guidance/)

Then after that you can put the required files at the same locations as the `Hello World` application. By doing this, you will up and running in minutes without dealing with all the details.

# prancer workflow: hard way
Based on the filing structure, you can start creating the required folders and putting the config files there.


# Setup the framework

Working with **Prancer** itself is a straightforward activity and needs only a few steps:

## Prancer Basic Workflow
1. Create a **Prancer** project directory in your application's project directory
2. Configure the connectors for each required providers
3. Create containers
4. Use existing `snapshot configuration` files
5. Use existing `test` files based on available compliance
6. Run the tests

## Prancer Enterprise Workflow
1. Create a **Prancer** project directory in your application's project directory
2. Configure the connectors for each required providers
3. Create containers
4. Use existing `master snapshot configuration` files and crawl your provider
5. Use existing `master test` files based on available compliance
6. Run the tests

Some of these steps are more involved than others but the general workflow is straightforward and simple to understand to keep the learning curve as simple as possible.

# Running tests

Running a test and gathering results was kept to the most simple steps possible so that integration into an existing continuous improvement/continuous deployment pipeline stays as simple as possible. The last thing you want is to use a tool that is cumbersome:

1. Checkout your application project
2. Go to the **Prancer** project directory
3. Run the prancer validation framework and act on return code
4. Save the outputs as artifacts for later viewing

Integrating with a CI/CD pipeline can be as simple as running a simple **BaSH** script in a folder with an `if` statement around it to catch potential failures. With the files written to disk, you can then dig into the results as you want by parsing the simple **JSON** files. Also for the Enterprise and Premium edition, API access is also available.

# The validation workflow

Each time the tool is ran, the test suite is executed in a sequential way:

1. Configuration files are read (Project configuration, Connector configuration, Snapshot configuration, Tests)
2. Providers are communicated with, snapshots are built and then saved to the database
3. Tests are ran against the snapshots
4. Reports are produced

![High-Level process](images/high-level-process.png)