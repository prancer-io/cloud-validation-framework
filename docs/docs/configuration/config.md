# Project configuration - config.ini

At the root of the **Prancer** project directory, you will be putting the `config.ini` file that tells **Prancer** how to behave for the current project. The configuration of **Prancer** is detailed in the following sections. It consists of sections and key-value pairs, just like in any `INI` files. Here is an example:

    [section]
    key = value
    key = value

    [section2]
    key = value
    key = value

# [Default] section

**Prancer** supports a variety of APIs in the enterprise edition. To access these APIs, some extra parameters need to be set.

The `INI` section to use in the configuration file is `[DEFAULT]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| space_id | *string* | space_id of the customer (required to access enterprise APIs for the particular customer) |

Example:

    [DEFAULT]
    space_id = 50973a54-16a7-4590-bcc0-755d0e83c7c9

# [Azure] section

**Prancer**  it is possible to specify where Prancer searches for Azure connectors.

Example:

    [AZURE]
    azureStructureFolder = realm/

# [Database] section

We use **MongoDB** to store data. You must configure the server's location through this section plus a few other behaviors.

The `INI` section to use in the configuration file is `[MONGODB]`, and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|-----------|
| dburl | *string* | The connection string to the mongodb server. If none, **Prancer** will connect to localhost on port 27017. Also used when reading configuration files using the `--db` switch |
| dbname | *string* | The name of the database to connect to when storing snapshots. Also used when reading configuration files using the `--db` switch |
| NOTIFICATIONS | *string* | Name of the collection where notifications are stored in database driven mode |
| SNAPSHOT | *string* | Name of the collection where snapshot configuration files are stored in database driven mode |
| MASTERSNAPSHOT | *string* | Name of the collection where master snapshot configuration files are stored in database driven mode |
| TEST | *string* | Name of the collection where test configurations are stored in database driven mode |
| MASTERTEST | *string* | Name of the collection where master test configurations are stored in database driven mode |
| STRUCTURE | *string* | Name of the collection where connector configurations are stored in database driven mode |
| OUTPUT | *string* | Name of the collection where test results are stored in database driven mode |

Example:

    [MONGODB]
    dburl = mongodb://localhost:27017/prancer
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

# [Logging] section

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

# [Notification] section

**Prancer** supports notifications when using the [Enterprise edition documentation](../enterprise/basics.md). This section allows you to turn on or off the notifications engine.

The `INI` section to use in the configuration file is `[NOTIFICATION]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| enabled | *boolean* | Are notifications active or not? |

Example:

    [NOTIFICATION]
    enabled = false

# [Reporting] section

**Prancer** requires you to specify where it should output its output files after tests are running. You can use the same directory as your `TESTS`, but it will create a separate structure if you don't. Depending on your artifact-building approach, you might want to split them or keep them together.

The `INI` section to use in the configuration file is `[REPORTING]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| reportOutputFolder | directory | Name of the directory to write reports into |

Example:

    [REPORTING]
    reportOutputFolder = validation

# [Vault] section

**Prancer** supports **Azure key vaults** or **CyberArk** (<http://www.cyberark.com>) Application Access Manager to store secrets that you might need for your infrastructure inspections.

The `INI` section to use in the configuration file is `[VAULT]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| type | azure | Name of the vault to use, right now, only **azure** is supported |
| tenant_id | *azure tenant id* | The Tenant ID where the Azure Vault is located |
| client_id | *azure spn client id* | Client id for the SPN that will connect to the vault |
| keyvault | *string* | Name of the vault to use |

* Note: The service principal name (SPN) should have access to read secrets from the keyvault. The client secret for the SPN will be prompted when running in interactive mode. Non-interactive Azure vault are possible through setting the environment variables or Managed Identities in Azure.

Example:

    [VAULT]
    type = azure
    tenant_id = oigdsa5-9u5jrgoi-sndroughs985-tu093h4tosnhgb
    client_id = gimwioj-n945hyw0-84h5tgwoerh6-08w4o58ghyqw04
    keyvault = vaultname

# [Tests] section

**Prancer** requires you to specify where your containers, snapshot configuration files, and test files are when using the filesystem storage-based approach. This section of the configuration defines where to find those.

The `INI` section to use in the configuration file is `[TESTS]` and here are all the possible configurations you can use:

| Key | Possible values | Explanation |
|------|:-------:|----------|
| containerFolder | directory | Name of the directory to look into for snapshot configuration files and test files |
| database | *string* | Could be `NONE` , `SNAPSHOT` or `FULL` you can also set this behavior at the runtime by `--db` argument. If it set to `NONE` then all the data will be read and written to the filesystem. if it is `SNAPSHOT` then the configuration files (snapshot config / compliance tests) will be read from filesystem, output file will be written to filesystem, but the snapshots will be kept in the database. if set to `FULL` then all the configuration files, snapshots and outputs will be read and written to database |

Example:

    [TESTS]
    containerFolder = validation
    database = FULL

# [Indexes] section

Specify which attributes could be indexed in the database.

Example:

    [INDEXES]
    OUTPUT = name, container, timestamp

# [RESULT] section

Specify result related configurations

Example:

    [RESULT]
    console_min_severity_error=Low

    # which is used to filter out result according to minimum level of failing.
    for example:
    - if console_min_severity_error is High, then only High level severity cases will fail the result
    - if console_min_severity_error is Medium, then only Medium and High severity level testcases will fail the result.
    - if console_min_severity_error is Low, then all(Low, Medium, and High) severity level testcases will fail the result.
