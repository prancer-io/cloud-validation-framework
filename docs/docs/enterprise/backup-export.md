# Backup and export of enterprise data

When you use **Prancer** enterprise edition or a manual setup of **basic** edition with **MongoDB** based storage, you should always take great care in backing up your data and also exporting it from time to time. 

Reasons for this are:

* Backup your snapshots
* Backup your configurations
* Backup your test reports
* Prepare for a failure/restore scenario

Let's look at a few ways and use-cases!

# Exporting data

From time to time, you should execute a full or incremental backup of your **MongoDB** server. The [MongoDB Back up and restore](https://docs.mongodb.com/manual/tutorial/backup-and-restore-tools/) page offers different solutions, we'll look at the simplest ones here.

**Exporting all documents**

You can export documents by using `mongoexport`. This tool requires a database and collection, so you can't export everything at once but you can automate your incremental or full backups using this:

    mongoexport -d validator -c security_groups > security_groups.json

This would export the whole collection to a file called `security_groups.json`.

**Importing all documents**

 If you needed to restore the previous backup, you could simply use:

    mongoimport -d validator --mode upsert -c security_groups < security_groups.json

> The `upsert` mode is used to replace documents if they already exist

**Exporting documents incrementally**

If you want to only export recent items you can use a query. Each **Prancer** snapshot has a `timestamp` set so you could keep the last timestamp you exported and use it in a query like this:

    mongoexport -d validator -c security_groups -q '{timestamp:{$gt:1555340917380}}'

If you do not have the timestamp on hand but have the latest backup, you can extract this using **jq** to retrieve it:

    lastTimestamp=$(cat security_groups.json | jq -n '[inputs] | map(.timestamp."$numberLong" | tonumber) | max')
    mongoexport -d validator -c security_groups -q "{timestamp:{\$gt:$lastTimestamp}}"

# Backup of data

Another approach, as stated in the [MongoDB Back up and restore](https://docs.mongodb.com/manual/tutorial/backup-and-restore-tools/) page is to use `mongodump` and `mongorestore`.

Running a simple:

    mongodump

Will create a `dump` directory in your current working directory with all the data you have in your database. You can easily call:

    mongorestore

Which expects the exact same setup to restore your whole mongodb server. This is the best approach to a complete setup/teardown scenario.

# Build artifact generation

In a CI/CD scenario, you will usually want to keep an artifact of everything that gets produced by your system. Not only the final version of your application but test results, docker images, and so many more items. **Prancer** is no exception, you should store artifacts of the **MongoDB** server on each run. This applies only if you use the `--db` switch.

**Backup of the test results**

The test results are stored in the main database, you have to look at the `dbname` in the configuration file in the `[mongodb]` section. To know in which collection the test results are stored, look at the `output` value in the `[mongodb]` section.

The best approach is to simply output that collection using a method similar to before to export incrementally:

    mongoexport -d validator -c $outputCollection -q '{timestamp:{$gt:1555340917380}}' > build_xyz_results.json

And then you can just flag this file as an artifact.

**Backup of the logs**

The logs are stored in the logging database, you have to look at the `dbname` in the configuration file in the `[logging]` section. To know in which collection the logs are stored, you have to list the collections and export the content of the one that matches the runtime. For example:

    logs_20190508150809

The best approach is to simply output that collection using a method similar to before. No need for a query since the logs are already split into collections:

    mongoexport -d validator -c logs_20190508150809 > build_xyz_logs.json

And then you can just flag this file as an artifact.