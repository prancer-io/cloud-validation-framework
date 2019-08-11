# Prancer project directory

The files to operate **Prancer** should be put into your web application's project directory and commited with it. All the **Prancer** files should be stored into a sub-directory of your choice, we recommend something like `tests/prancer/`. To create it, you can run something like:

    mkdir -p tests/prancer
    cd tests/prancer

# Validation directory

The `validation` directory is the internal test directory for **Prancer**. This is where tests will be created. All of your tests will be written inside a sub-directory of `validation`. Create the `validation` directory using:

    mkdir -p validation

Under the `validation` directory lives container directories. Each container is a logical grouping for your test files and snapshots. Their sole purpose is to group and create a hierarchy to better organize your tests. Create a container directory like so:

    mkdir -p validation/container1

You can create as many as needed and there are no specific naming convention. The only requirement is to respect your filesystem's requirements.

# Project configuration

At the root of the **Prancer** project directory, you will be putting the `config.ini` file that tells **Prancer** how to behave for the current projet. The configuration of **Prancer** is detailed in the following sections. It consists of sections and key value pairs just like in any `INI` files. Here is an example:

    [section]
    key = value
    key = value

    [section2]
    key = value
    key = value

Look at the next sections to understand what you can put in this file.

# Azure api configuration

**Prancer** requires a special configuration to support calling the **Azure** apis. Each **Azure** api needs a specific version that the software should support and instead of baking this into the application we went for a description file that everyone can contribute to.

The `INI` section to use in the configuration file is `[AZURE]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| api | filename | Name of the file to use to load the **Azure** api versions |

Example:

    [AZURE]
    api = azureApiVersions.json

# Database configuration

We use **MongoDB** for the No-SQL storage solution. You must configure the location of the server through this section.

The `INI` section to use in the configuration file is `[MONGODB]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|-----------|
| dbname | *string* | The name of the database to connect to when storing snapshots or when reading configuration files using the `--db` switch |
| NOTIFICATIONS | *string* | Name of the collection where notifications are stored in database driven mode |
| SNAPSHOT | *string* | Name of the collection where snapshot configurations are stored in database driven mode |
| TEST | *string* | Name of the collection where test configurations are stored in database driven mode |
| STRUCTURE | *string* | Name of the collection where connector configurations are stored in database driven mode |
| OUTPUT | *string* | Name of the collection where test results are stored in database driven mode |

Example:

    [MONGODB]
    dbname = myprancerdatabase
    NOTIFICATIONS = prancernotifications
    SNAPSHOT = prancersnapshot
    TEST = prancertest
    STRUCTURE = prancerstructure
    OUTPUT = pranceroutput

> <NoteTitle>Notes: Collection configurations</NoteTitle>
>
> All of the previous collection name configurations are optional if you use filesystem storage for your configuration.
>
> If you want to use the `--db` switch when testing, you need to provide the other values such as: `SNAPSHOT`, `NOTIFICATIONS`, `TEST`, `STRUCTURE` and `OUTPUT`. More on this feature in the [Enterprise edition documentation](../enterprise/basics.md)

# Logging configuration

You can configure logging to use either **MongoDB** or the filesystem. 

The `INI` section to use in the configuration file is `[LOGGING]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|-----------|
| level | `DEBUG`, `INFO`, `WARNING`, `ERROR` | This sets the minimum level for the logger, if you set `DEBUG`, everything is logged, if you set `ERROR`, only errors will be logged |
| propagate | *boolean* | Will the log be shown to the console (`True`) or will the tool be silent (`False`), defaults to `True` |
| logFolder | *string* | The name of the directory where logs are stored, defaults to `log`. This is also the collection name when logging to the database  |
| dbname | *string* | The name of the database to connect to when logging, uses the database configuration below to know which server to connect to |

Visit the section on [Logging configuration](logging.md) to know more.

Example:

    [LOGGING]
    level = DEBUG
    propagate = true
    logFolder = logs
    dbname = logs

# Notification configuration

**Prancer** supports notifications when using the [Enterprise edition documentation](../enterprise/basics.md). This section allows you to turn on or off the notifications engine.

The `INI` section to use in the configuration file is `[NOTIFICATION]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| enabled | *boolean* | Are notifications active or not? |

Example:

    [NOTIFICATION]
    enabled = false

# Reporting configuration

**Prancer** requires you to specify where it should output it's output files after tests are ran. You can use the same directory as your `TESTS` but if you don't, it will create a separate structure. Depending on your artifact building approach, you might want to split them or keep them together.

The `INI` section to use in the configuration file is `[REPORTING]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| reportOutputFolder | directory | Name of the directory to write reports into |

Example:

    [REPORTING]
    reportOutputFolder = validation

# Secrets

**Prancer** supports **Azure key vaults** to store secrets that you might need for you infrastructure inspections. We might add more vaults in the future but for now, this is the only supported one. If you use the **Git** or **AWS** connector, you can skip this section.

The `INI` section to use in the configuration file is `[VAULT]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| type | azure | Name of the vault to use, right now, only **azure** is supported |
| tenant_id | *azure tenant id* | The Tenant ID where the Azure Vault is located |
| client_id | *azure spn client id* | Client id for the SPN that will connect to the vault |
| keyvault | *string* | Name of the vault to use |

* Note: The service principal name (SPN) should have access granted to read secrets from the keyvault. The client secret for the SPN will be prompted when running in interactive mode. Non-interactive Azure vault are impossible for now.

Example:

    [VAULT]
    type = azure
    tenant_id = oigdsa5-9u5jrgoi-sndroughs985-tu093h4tosnhgb
    client_id = gimwioj-n945hyw0-84h5tgwoerh6-08w4o58ghyqw04
    keyvault = vaultname

# Tests configuration

**Prancer** requires you to specify where your containers, snapshots and test files are when using the filesystem storage based approach. This section of the configuration defines where to find those.

The `INI` section to use in the configuration file is `[TESTS]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| containerFolder | directory | Name of the directory to look into for snapshots and tests |
| database | *boolean* | `True` by default, if `True`, assumes tests are ran from the database like if you provided `--db` on the command line, set to `False` to run from the filesystem. |

Example:

    [TESTS]
    containerFolder = validation
    database = false
