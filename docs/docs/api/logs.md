**Logs APIs**
===

**Logs - List**
---

- **CURL Sample**

``` curl
curl --location --request GET 'https://portal.prancer.io/prancer-customer1/api/logs/?index=0&count=10&container=aws_cloud&compliance=mastertest_aws_cloud&search=test' \
--header 'Authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/logs>
- **Method:** GET
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

``` json
{
    "container": "Container Name",
    "compliance": "Mastertest file name/ compliance name",
    "count" : 3,
    "index" : 0,
    "search" : <search_text>
}
```

- **Explanation:**

    All Fields are Optional.
    `Optional Fields`

  - **container:** Name of the container, container name list will receive in response when call API without any filter or filter by startdate/enddate.
  - **compliance:** A valid list of compliance for filter the policy. See [Default - tags](/prancer-ent-apis/tags) API for get valid compliance list.
  - **search:** Search reports by title of the report.

 **NOTE:**

- `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.

**Response:**

- _response with pagination of 3 records_

- Status Code: 200
- Response:

``` json
{
    "data": [
        {
            "_id": "626107fc8b0d8f64092782f5",
            "container": "aws_cloud",
            "json": {
                "log": "logs_20220421130000_jwlyh_3384",
                "master_snapshot_list": [
                    {
                        "id": "61b1ae694af4483b84901c34",
                        "name": "mastersnapshot_aws_cloud"
                    }
                ],
                "master_test_list": [
                    {
                        "id": "61b1ae694af4483b84901c35",
                        "name": "mastertest_aws_cloud"
                    }
                ],
                "snapshot": "",
                "status": "Completed",
                "test": "Crawlertest_aws_cloud"
            },
            "timestamp": 1650526204830,
            "type": "crawlerOutput"
        },
        {
            "_id": "625fd60f31e347261daeec5e",
            "container": "aws_cloud",
            "json": {
                "log": "logs_20220420151443_dunvd_0528",
                "master_snapshot_list": [
                    {
                        "id": "61b1ae694af4483b84901c34",
                        "name": "mastersnapshot_aws_cloud"
                    }
                ],
                "master_test_list": [
                    {
                        "id": "61b1ae694af4483b84901c35",
                        "name": "mastertest_aws_cloud"
                    }
                ],
                "snapshot": "",
                "status": "Completed",
                "test": "Crawlertest_aws_cloud"
            },
            "timestamp": 1650447887765,
            "type": "crawlerOutput"
        },
        {
            "_id": "625fd45ca74a17d8ad86841f",
            "container": "aws_cloud",
            "json": {
                "log": "logs_20220420150728_kjlzr_3603",
                "master_snapshot_list": [
                    {
                        "id": "61b1ae694af4483b84901c34",
                        "name": "mastersnapshot_aws_cloud"
                    }
                ],
                "master_test_list": [
                    {
                        "id": "61b1ae694af4483b84901c35",
                        "name": "mastertest_aws_cloud"
                    }
                ],
                "snapshot": "",
                "status": "Completed",
                "test": "Crawlertest_aws_cloud"
            },
            "timestamp": 1650447452811,
            "type": "crawlerOutput"
        }
    ],
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 3,
        "current_page": 1,
        "next_index": 3,
        "total": 756
    },
    "status": 200
}
```


**Logs - Details**
---

- **CURL Sample**

``` curl
curl --location --request GET 'http://localhost:4200/api/logs/details/?index=0&count=10&log_name=logs_20220421130000_jwlyh_3384' \
--header '<JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/logs/details/>
- **Method:** GET
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

``` json
{
    "log_name": "logs_20220421130000_jwlyh_3384",
    "count" : 3,
    "index" : 0,
}
```

- **Explanation:**

    All Fields are Required.
  - **log_name:** Name of the log file to check details.

 **NOTE:**

- `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.

**Response:**

- _response with pagination of 3 records_

- Status Code: 200
- Response:

``` json
{
    "data": [
        {
            "asctime": "2022-04-21 13:00:04,049",
            "level": "INFO",
            "line": 348,
            "log_type": "DEFAULT",
            "module": "cli_validator",
            "msg": "2022-04-21 13:00:04,049(cli_validator: 348) - START: Argument parsing and Run Initialization. Version 2.1.20",
            "timestamp": 1650506404050
        },
        {
            "asctime": "2022-04-21 13:00:04,812",
            "level": "INFO",
            "line": 359,
            "log_type": "DEFAULT",
            "module": "cli_validator",
            "msg": "2022-04-21 13:00:04,812(cli_validator: 359) - Command: 'python /home/swan-24/Documents/projects/prancer/git-repo/prancer-enterprise/adv/venv/bin/prancer --db FULL aws_cloud'",
            "timestamp": 1650506404812
        },
        {
            "asctime": "2022-04-21 13:00:04,815",
            "level": "INFO",
            "line": 370,
            "log_type": "DEFAULT",
            "module": "cli_validator",
            "msg": "2022-04-21 13:00:04,815(cli_validator: 370) - Using Framework dir: /home/swan-24/Documents/projects/prancer/git-repo/prancer-enterprise",
            "timestamp": 1650506404815
        }
    ],
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 3,
        "current_page": 1,
        "next_index": 3,
        "total": 3167
    },
    "status": 200
}
```
