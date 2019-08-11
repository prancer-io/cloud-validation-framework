# Features

**Prancer**'s enterprise edition adds various additional features such as:

* Database storage for configuration files, snapshots and test reports
* A web interface to manage all this
* Everything is managed in your own infrastructure (On premise)

The difference with the **SaSS** offering is that you install the enterprise edition on your servers while the SaSS manages it for you on **Prancer**'s infrastructure.

# Database storage in the basic edition

Database storage **is not a locked feature**. It exists even in the basic edition but isn't really useful unless you create a large set of tools around it to manage the input and output. This is exactly what the enterprise edition solves by offering a managed web interface that you can install on premise.

If you want to use **Prancer** in database mode, ensure you have configured the following settings in the `[mongodb]` section in the projecy configuration file:

| Key | Possible values | Explanation |
|------|:-------:|-----------|
| SNAPSHOT | *string* | Name of the collection where snapshot configurations are stored |
| TEST | *string* | Name of the collection where test configurations are stored |
| STRUCTURE | *string* | Name of the collection where connector configurations are stored |
| OUTPUT | *string* | Name of the collection where test results are stored |

These settings are optional if you use file based storage but necessary when you use the database storage. Each additional collection will receive different documents, you can insert the documents yourself or use the utilities to push file based documents into the database.

# Database management utilities

**Prancer** comes with a tool that will help you push your documents to the database. This is particularly useful when migrating to the enterprise edition or if you want to store everything yourself in the **MongoDB** database without the enterprise edition support.

> <NoteTitle>Notes: Edition differences</NoteTitle>
>
> Note that this tool doesn't come with the `prancer-basic` package, you need to work with the source version.

For example, to import document you can use:

    python3 utilities/populate_json.py lq --file azureApiVersions.json --type structure
    python3 utilities/populate_json.py lq --file awsStructure.json --type structure
    python3 utilities/populate_json.py lq --file azureStructure.json --type structure
    python3 utilities/populate_json.py lq --file azureStructure1.json --type structure
    python3 utilities/populate_json.py lq --file parameterStructure.json --type structure
    python3 utilities/populate_json.py lq --file parameterStructure1.json --type structure
    python3 utilities/populate_json.py lq --file notifications/notifications_slack_wk.json --type notifications
    python3 utilities/populate_json.py lq --file notifications/notifications_email_gm.json --type notifications
    python3 utilities/populate_json.py lq --file notifications/notifications_email_sg.json --type notifications
    python3 utilities/populate_json.py container1 --dir validation/container1
    python3 utilities/populate_json.py container3 --dir validation/container3
    python3 utilities/populate_json.py container4 --dir validation/container4
    python3 utilities/populate_json.py container5 --dir validation/container5
    python3 utilities/populate_json.py container6 --dir validation/container6

These are a few examples of how you can use `populate_json.py` to load the files into the **MongoDB** database. 

# Running tests using the database

If you want **Prancer** to run the tests using the database configuration, the only thing you need will be a `config.ini` on disk and then issue the following:

    prancer --db <container-name>

This will run the tool using the database instead of the filesystem.