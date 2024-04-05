# Run Prancer CLI
Prancer CLI provides different arguments for the configuration of the run. On this page, we are reviewing all the available arguments for Prancer CLI.
We are providing different examples of running the Crawler and Compliance of Prancer Framework. 
To start, make sure you have installed Prancer CLI and clone the Hello World application.

- Clone this repository, [https://github.com/prancer-io/prancer-hello-world](https://github.com/prancer-io/prancer-hello-world)
- Check the file `config.ini`, here you can see the value of `containerFolder` in `TESTS` section is `./validation/`(i.e. All the test cases are stored inside the `validation` directory).

Run the prancer help

```
prancer -h
```

#### usage: 

&emsp;&emsp;prancer  [-h]  
&emsp;&emsp;[-v]  
&emsp;&emsp;[--db {NONE,SNAPSHOT,FULL,REMOTE}]  
&emsp;&emsp;[--crawler]  
&emsp;&emsp;[--compliance]  
&emsp;&emsp;[--file_content FILE_CONTENT]  
&emsp;&emsp;[--mastertestid MASTERTESTID]   
&emsp;&emsp;[--mastersnapshotid MASTERSNAPSHOTID]  
&emsp;&emsp;[--snapshotid SNAPSHOTID]   
&emsp;&emsp;[--env {DEV,QA,PROD,LOCAL}]   
&emsp;&emsp;[--apitoken APITOKEN]   
&emsp;&emsp;[--gittoken GITTOKEN]  
&emsp;&emsp;[--company COMPANY]  
&emsp;&emsp;[--createsnapshot]  
&emsp;&emsp;[--mastersnapshotfile MASTERSNAPSHOTFILE]  
&emsp;&emsp;[collection]  

#### positional arguments:
 
| Argument   | Description |
|------------|-------------|
| collection | The name of the folder which contains the collection of files related to one scenario |

#### optional arguments:

|    |  Argument   | Description |
|----|-------------|-------------|
| -h | --help | Show this help message and exit |
| -v | --version| Show prancer version |
|    | --db {*NONE*, *SNAPSHOT*, *FULL*, *REMOTE*} | *NONE* - Database will not be used, all the files reside on filesystem <br/> <br/>*SNAPSHOT* - Resource snapshots will be stored in db, everything else will be on filesystem<br/> <br/>*FULL* - tests, configurations, outputs and snapshots will be stored in the database<br/> <br/>*REMOTE* - Connect to Prancer Enterprise solution to get the configuration files and send the results back.|
|    | --crawler | Crawls the target environment and generates snapshot configuration file |
|    | --compliance | Run only compliance tests based on the available snapshot configuration file |
|    | --file_content FILE_CONTENT | The path of the file to be used as snapshost |
|    | --mastertestid MASTERTESTID | Run the framework only for the master test Ids or compliance Ids mentioned here |
|    | --mastersnapshotid MASTERSNAPSHOTID | Run the framework only for the master snapshot Ids mentioned here |
|    | --snapshotid SNAPSHOTID | Run the framework only for the snapshot Ids mentioned here |
|    | --env {*DEV*, *QA*, *PROD*, *LOCAL*} | *DEV* - API server is in dev environment<br/><br/>*QA* - API server is in qa environment<br/><br/>*PROD* - API server is in prod environment<br/><br/>*LOCAL* - API server is in local environment. |
|    | --apitoken APITOKEN | API token to access prancer saas solution. (This argument is needed only when the --db is REMOTE). |
|    | --gittoken GITTOKEN | github/enterprise/internal github API token to access repositories. (This argument is optional only when the --db is REMOTE) |
|    | --company COMPANY | company name of the prancer saas solution (This argument is needed only when the --db is REMOTE) |
|    | --createsnapshot | To generate all the snapshots after crawler is completed.|
|    | --mastersnapshotfile MASTERSNAPSHOTFILE | To run crawler for the specific mastersnapshot file. |


#### 1) Run Crawler Only

```
prancer scenario-arm-pass --crawler --db=NONE
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection which contains master-snapshot and master-test files. |
| --crawler | Specifies that you want to run crawler only on given collection. |
| --db=None | It defines that the prancer have to find the collection of master-snapshot and master-test from local filesystem. |

- On completion of crawler, it generates the snapshot file inside the collection with name `<mastersnapshot_name>_gen.json`.

#### 2) Run Compliance Only

```
prancer scenario-arm-pass --compliance --db=NONE
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection on which you want to run the compliance. |
| --compliance | Specifies that you want to run compliance only on given collection. |
| --db=None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |

- On completion of compliance, it generates the `snapshots` folder inside the collection which contains the actual snapshot files of your cloud resources or templates files for IaC. It also creates the outputs file named `output-<mastertest_name>.json` which contains the <strong style="color: green;">passed</strong> and <strong style="color: red; ">failed</strong> results of compliance.

#### 3) Run both crawler and compliance

```
prancer scenario-arm-pass --db=NONE
prancer scenario-arm-pass --crawler --compliance --db=NONE
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection on which you want to run the compliance. |
| --db None | It defines that the prancer have to find the collection of snapshot and mastertest files from local filesystem. |

- If neither `--crawler` nor `--compliance` is specified, then the default option is to run both processes. First it crawls the collection and generates the snapshot file. After that, it runs the compliance for the generated snapshot and generates the output file.


#### 4) Run compliance for a file

```
prancer --db NONE --file-content /tmp/deploy.yaml <collection>
```

| Parameters | Description |
|------------|-------------|
| collection |  Name of the collection on which you want to run the compliance. |
| --db None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |
| --file-content /tmp/deploy.yaml |  This the snapshot data and compliance is run for this as per the compliance tests in the collection. |


#### 5) Run compliance for one(or more) of the specific mastertestIDs

```
prancer --db NONE --mastertestid TEST_S3_14 <collection>
prancer --db NONE --mastertestid TEST_S3_14,TEST_EC2_1 <collection>
```

| Parameters | Description |
|------------|-------------|
| collection |  Name of the collection on which you want to run the compliance. |
| --db None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |
| --mastertestid TEST_S3_14|  The compliance is run only the specified masterTestID or comma separated masterTestIDs or compliance Ids. |


#### 6) Run compliance for one(or more) of the specific masterSnapshotIDs

```
prancer --db NONE --mastersnapshotid CFR_TEMPLATE_SNAPSHOT <collection>
prancer --db NONE --mastersnapshotid CFR_TEMPLATE_SNAPSHOT,EC2_TEMPLATE_SNAPSHOT <collection>
```

| Parameters | Description |
|------------|-------------|
| collection |  Name of the collection on which you want to run the compliance. |
| --db None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |
| --mastersnapshotid CFR_TEMPLATE_SNAPSHOT|  The compliance is run only the specified masterSnapshotID or comma separated masterSnapshotIDs. |


#### 7) Run compliance for one(or more) of the specific snapshots

```
prancer --db NONE --snapshotid K8S_TEMPLATE_SNAPSHOT7,K8S_TEMPLATE_SNAPSHOT6 <collection>
```

| Parameters | Description |
|------------|-------------|
| collection |  Name of the collection on which you want to run the compliance. |
| --db None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |
| --snapshotid K8S_TEMPLATE_SNAPSHOT7|  The compliance is run only the specified SnapshotID or comma separated SnapshotIDs. |

- If you doesn't defines the `--crawler` or `--compliance` then it runs both proceesses. First it crawls the collection and generates the snapshot file.After it runs the compliance on it and generates the output file.

#### 8) Run Specific compliance on all resources

```
prancer scenario-arm-pass --db=NONE --mastertestid `mastertestid_of_master_compliance_test`
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection on which you want to run the compliance. |
| --db=None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |
| mastertestid | [masterTestId](https://github.com/prancer-io/prancer-compliance-test/blob/7b57c2538d0ef1784b388c262ba9831393b4593f/azure/iac/master-compliance-test.json#L8) provided in master-compliace-test |


#### 9) Run all compliances on specific resources

```
prancer scenario-arm-pass --db=NONE --mastersnapshotid `generated_mastersnapshotid`
```

| Parameters | Description |
|------------|-------------|
| scenario-arm-pass |  Name of the collection on which you want to run the compliance. |
| --db=None | It defines that the prancer have to find the collection of snapshot and master-test files from local filesystem. |
| mastersnapshotid | snapshot id generated after running crawler looks like `ARM_TEMPLATE_SNAPSHOT1` |


#### 10) Run crawler and compliance remotely

```
prancer "GCP Collection" --db=REMOTE --apitoken=e734c17a1f5********************* --gittoken=ghp_************************************ --company=prancer
```


| Parameters | Description |
|------------|-------------|
| GCP Collection |  Name of the collection exists on the Prancer portal. |
| --db=REMOTE | It defines that the prancer have to find the collection of snapshot and master-test files remotely. |
| --apitoken | User access token to access the prancer saas solution. |
| --gittoken | github/enterprise/internal github API token to access the repositories. |
| --company | company name of the prancer saas solution |
