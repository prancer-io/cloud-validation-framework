# Files and Folders Structure
### Prancer project directory

The files to operate **Prancer** should be put into a project directory. It is recommended to have a source control mechanism for this folder to keep track of changes. All the **Prancer** files should be stored in a sub-directory of your choice, we recommend something like `tests/prancer/`. To create it, you can run something like:


    mkdir -p tests/prancer
    cd tests/prancer

> Most of these folder names and locations are configurable in `config.ini` file.

### Validation directory

The `validation` directory is the internal working directory for **Prancer**. This is where snapshot config files and tests will be created. All of them will be written inside a sub-directory of `validation`. Create the `validation` directory using:

    mkdir -p validation

Under the `validation` directory lives Collection directories. Each collection is a logical grouping for your test files and snapshot configuration files. Their sole purpose is to group and create a hierarchy to organize your tests better. Create a Collection directory like so:

    mkdir -p validation/container1

You can create as many as needed, and there is no specific naming convention. The only prerequisite is to respect your filesystem's requirements.

### Project configuration file

At the root of the **Prancer** project directory, you will be putting the `config.ini` file that tells **Prancer** how to behave for the current project. The configuration of **Prancer** is detailed in the next section. It consists of sections and key-value pairs, just like in any `INI` files. Here is an example:

    [section]
    key = value
    key = value

    [section2]
    key = value
    key = value

Look at the following sections to understand what you can put in this file.

### Reporting folder
**Prancer** requires you to specify a path where output files should be stored after running tests. You can use the same directory as your `TESTS`, but it will create a separate structure if you don't. Depending on your artifact-building approach, you might want to split them or keep them together.

### Collection folder
**Prancer** requires you to specify where your snapshot configuration files and test files are when using the filesystem storage-based approach. This section of the configuration defines where to find those files.

### Snapshot folder
When you are using Filesystem to store the result of snapshots, **Prancer** creates a folder inside the collection to store the snapshots.
