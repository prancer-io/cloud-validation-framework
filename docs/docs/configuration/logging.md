Nowadays, generating comprehensive log information is a must, and **Prancer** doesn't stray away from this. Every single operation is captured by the logging system and is timestamped when caught.

# Configuration

To configure the logging behavior, consult the [Configuration](config.md) section and read on for detailed information.

# Logging level

**Prancer** supports the classic five levels of logging:

* ERROR
* WARNING
* INFO
* DEBUG
* CRITICAL

Each level is more verbose than the other. Using a mode such as `DEBUG` will print all the logging information possible while `ERROR` prints only the bare minimum.

# Database, filesystem and console logging

**Console logging**

Console logging is active by default, you can turn it off by setting `propagate` to `false` in the configuration.

**Filesystem logging**

Filesystem logging is always on, you cannot turn it off. `logFolder` (which defaults to `log`) will be the location where the log files are created. This location is always relative to the **Prancer** project directory.

All log files are named `log_<dateofrun>.log`

**Database logging**

If you provide a `dbname` in the configuration, the system will log everything to the database as well as the filesystem. The connection used to store logs will be the same as defined in the database configuration section.

The `logFolder` will be used by the database logger to create the collection name where the log entries will be put. For example, if logFolder = `logez`:

    db.logez_20190101120000.find()
    
Will return the data for that log.

# Example of log files and database logs

Log files are stored in the file system as a text file. Here is the example of the log file:

    2019-02-27 20:53:50,211(restapi_azure: 186) - Get Azure token REST API invoked!
    2019-02-27 20:53:50,213(http_utils:  96) - HTTP POST https://login.microsoftonline.com/@f123456-a59f-478a-8457-54e8d12458d/oauth2/token  .......
    2019-02-27 20:53:50,999(http_utils:  50) - HTTP POST: status: 401, ex:HTTP Error 401: Unauthorized 
    2019-02-27 20:53:51,005(restapi_azure: 193) - Get Azure token returned invalid status: 401
    2019-02-27 20:53:51,009(vault:  60) - Secret Value: None
    2019-02-27 20:53:51,012(snapshot_azure:  87) - Secret: None
    2019-02-27 20:53:51,015(snapshot_azure:  89) - No client secret in the snapshot to access azure resource!...
    2019-02-27 20:53:51,017(validation: 109) - Starting validation tests
    2019-02-27 20:53:51,023(validation: 112) - /home/whitekite/realm/validation//container6
    2019-02-27 20:53:51,027(validation: 114) - /home/whitekite/realm/validation/container6/test6.json

When you configure the system to log in to the database, **Prancer** will convert the data to a `JSON` format like below and then store it in the database. Here is an example of a log file in the database :

    {
        "_id": {
            "$oid": "5c526ba47456213b793728ec"
        },
        "timestamp": {
            "$numberLong": "1548905380239"
        },
        "level": "INFO",
        "module": "populate_json",
        "line": 100,
        "asctime": "2019-01-31 08:59:40,239",
        "msg": "Command: 'python3 utilities/populate_json.py lq --file ./realm/awsStructure.json --type structure'"
    }
    {
        "_id": {
            "$oid": "5c526ba47456213b793728ed"
        },
        "timestamp": {
            "$numberLong": "1548905380565"
        },
        "level": "INFO",
        "module": "populate_json",
        "line": 114,
        "asctime": "2019-01-31 08:59:40,564",
        "msg": "Namespace(container='lq', dir=None, file='./realm/awsStructure.json', type='structure')"
    }
    {
        "_id": {
            "$oid": "5c526ba47456213b793728ef"
        },
        "timestamp": {
            "$numberLong": "1548905380600"
        },
        "level": "INFO",
        "module": "populate_json",
        "line": 62,
        "asctime": "2019-01-31 08:59:40,599",
        "msg": "Populating ./realm/awsStructure.json json file."
    }
    {
        "_id": {
            "$oid": "5c526ba47456213b793728f0"
        },
        "timestamp": {
            "$numberLong": "1548905380601"
        },
        "level": "INFO",
        "module": "populate_json",
        "line": 72,
        "asctime": "2019-01-31 08:59:40,601",
        "msg": "Storing file:./realm/awsStructure.json"
    }
    {
        "_id": {
            "$oid": "5c526ba47456213b793728f2"
        },
        "timestamp": {
            "$numberLong": "1548905380641"
        },
        "level": "INFO",
        "module": "populate_json",
        "line": 79,
        "asctime": "2019-01-31 08:59:40,641",
        "msg": "********************************************************************************"
    }
    {
        "_id": {
            "$oid": "5c526ba47456213b793728f3"
        },
        "timestamp": {
            "$numberLong": "1548905380645"
        },
        "level": "INFO",
        "module": "rundata_utils",
        "line": 96,
        "asctime": "2019-01-31 08:59:40,645",
        "msg": "\u001b[92m Run Stats: {\n  \"start\": \"2019-01-31 08:59:40\",\n  \"end\": \"2019-01-31 08:59:40\",\n  \"errors\": [],\n  \"host\": \"HP-Notebook\",\n  \"timestamp\": \"2019-01-31 08:59:40\",\n  \"log\": \"/home/log/20190131-085940.log\",\n  \"duration\": \"0 seconds\"\n}\u001b[00m"
    }