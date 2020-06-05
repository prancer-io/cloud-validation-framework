# Files and Folders Structure
## Prancer project directory

The files to operate **Prancer** should be put into a project directory. It is recommended to have a source control mechanism for this folder to keep track of changes. All the **Prancer** files should be stored into a sub-directory of your choice, we recommend something like `tests/prancer/`. To create it, you can run something like:

> Most of these folder names and locations are configurable in `config.ini` file

    mkdir -p tests/prancer
    cd tests/prancer

### Validation directory

The `validation` directory is the internal working directory for **Prancer**. This is where snapshot config files and tests will be created. All of them will be written inside a sub-directory of `validation`. Create the `validation` directory using:

    mkdir -p validation

Under the `validation` directory lives container directories. Each container is a logical grouping for your test files and snapshot configuration files. Their sole purpose is to group and create a hierarchy to better organize your tests. Create a container directory like so:

    mkdir -p validation/container1

You can create as many as needed and there are no specific naming convention. The only requirement is to respect your filesystem's requirements.

### Project configuration file

At the root of the **Prancer** project directory, you will be putting the `config.ini` file that tells **Prancer** how to behave for the current project. The configuration of **Prancer** is detailed in the next section. It consists of sections and key value pairs just like in any `INI` files. Here is an example:

    [section]
    key = value
    key = value

    [section2]
    key = value
    key = value

Look at the next sections to understand what you can put in this file.

### Azure api version file
**Prancer** requires a special configuration to support calling the **Azure** apis. Each **Azure** api needs a specific version that the software should support and instead of baking this into the application we went for a description file that everyone can contribute to. Usually the name of the file is `azureApiVersions.json`


> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `azureApiVersions.json`

    {
        "Microsoft.Compute/availabilitySets": {
            "version": "2018-06-01"
        },
        "Microsoft.Network/virtualNetworks": {
            "version": "2018-07-01"
        },
        "Microsoft.Storage/storageAccounts": {
            "version": "2018-07-01"
        },
        "Microsoft.KeyVault/vaults": {
            "version": "2015-06-01"
        },
        "Microsoft.Network/networkSecurityGroups": {
            "version": "2018-11-01"
        },
        "fileType": "structure",
        "type": "others"
    }

### Google resource file
**Prancer** requires a special configuration to support calling the **Google cloud** apis. **Prancer** stores these information in `googleParamsVersions.json`



### Reporting folder
**Prancer** requires you to specify where it should output it's output files after tests are ran. You can use the same directory as your `TESTS` but if you don't, it will create a separate structure. Depending on your artifact building approach, you might want to split them or keep them together.


### Container folder
**Prancer** requires you to specify where your snapshot configuration files and test files are when using the filesystem storage based approach. This section of the configuration defines where to find those.

### Snapshot folder
When you are using Filesystem to store the result of snapshots, **Prancer** creates a folder inside the container to store the snapshots.
