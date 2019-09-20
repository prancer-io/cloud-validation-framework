# Enterprise scenario use-case: Parallelization

**Prancer** enterprise edition proposes interresting features that compensate's the basic editions scalability. If you have a very big infrastructure to manage, you might want to use a distributed approach when running tests so you don't have to wait for too long. 

# Containers

The reason containers exist in the first place is to help you better structure your test files and snapshot configuration files. At the same time, containers play another role: **They help with parallelization of your testing**. 

When you have a large infrastructure, you'll need multiple runners to query your infrastructure and run tests. You can do this without enterprise support and even without database storage but it will be a complex task.

# Database setup

If you want to leverage parallelization of your **Prancer** setup, you will need multiple runners, they could be **AWS** or **Azure** virtual machines or just multiple developer machines. You will need a common **MongoDB** server that all will connect to and then feed that database with the configuration that everyone will share.

This setup can be done in a CI/CD pipeline scenario as a temporary setup/tear-down scenario or more permanent solution. 

# Permanent setup

A permanent setup, with or without enterprise support would look like this:

1. Setup a **MongoDB** server as a permanent solution
2. Feed the **MongoDB** server with the configuration files using the **utilities** presented in the [last chapter](basics.md)

Then, manually or through a CI/CD process:

1. Start/Bring up/Install **prancer** on multiple runners
2. On each runner, start the validation tool, each with it's own container `prancer <container>`

# Non-permanent setup

A non-permanent setup would be used in a complete setup/tear-down solution on every run of your CI/CD pipeline. You should use this setup **only in a basic edition scenario**. If you have enterprise support, instead, you should opt for a permanent solution. 

> <NoteTitle>Notes: Edition differences</NoteTitle>
>
> We strongly recommend using a permanent setup and the enterprise edition once you need parallelization.

1. Setup a **MongoDB** server as a temporary solution
2. Feed the **MongoDB** server with the configuration files using the **utilities** presented in the [last chapter](basics.md)
3. Start/Bring up/Install **prancer** on multiple runners, you cannot use more runners than you have containers
4. On each runner, start the validation tool, each with it's own container `prancer <container>`
5. Export the test-output if you need it
6. Tear-down the **MongoDB** server

# Post run data

If you use the database storage approach, you should always consider doing some backups of your data. This is especially true in **non-permanent setups** or you will run your tests and then lose the data once the pipeline cleans up everything.

In all cases, it is a good approach to always export your test data to a build artifact. In the next section you will see how to backup your **MongoDB** server or export your test results or more to send them to build artifacts.