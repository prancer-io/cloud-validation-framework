**Collection APIs**
===

- Collection is the combinations of Snapshots configuration, Connectors configuration, Compliances configuration, and rego files.

**Collection - get**
---
- This API is for get the list of available collections with connectors list available in each collection.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/api/collection/list -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/api/collection/list
- **Method:** GET
- **Header:**

```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
- detail= <show details of collection>
- search= <search by collection name>
```

**Response:**

`detail=true`

```
{
    "data": {
        "results": [
            {
                "connectors": [
                    {
                        "name": "aws_test_1_connector_aws",
                        "type": "filesystem"
                    },
                    {
                        "name": "git_prancer-liquware_connector",
                        "type": "filesystem"
                    }
                ],
                "containerId": 105,
                "masterSnapshots": [
                    {
                        "name": "mastersnapshot_aws_test_1"
                    }
                ],
                "masterTests": [
                    {
                        "name": "mastertest_aws_test_1"
                    }
                ],
                "name": "aws_test_1",
                "others": [],
                "snapshots": [],
                "status": "active",
                "tests": []
            }
        ]
    },
    "error": "",
    "message": "",
    "metadata": {
        "count": 1,
        "current_page": 1,
        "next_index": 1,
        "total": 63
    },
    "status": 200
}
```

`detail=false`

```
{
    "data": {
        "results": [
            {
                "collection": "aws_test_2",
                "connectors": [
                    "aws_test_2_connector_aws",
                    "git_prancer-liquware_connector"
                ]
            }
        ]
    },
    "error": "",
    "message": "",
    "metadata": {
        "count": 1,
        "current_page": 1,
        "next_index": 1,
        "total": 62
    },
    "status": 200
}
```


**Collection - get by name of the collection**
---

- This API is to check if a collection exists.

**CURL Sample**
```
curl -H "space-id:101"  -H 'authorization: Bearer <JWT Bearer Token>' -X GET "https://portal.prancer.io/customer1/api/collection?collection=git_azure_customer1_1617571294420"
```

- **URL:** https://portal.prancer.io/api/collection
- **Method:** GET
- **Header:**

```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
- collection: <name of the collection>
```

**Response:**

```
{
  "data":{
    "exists":true
  },
  "error":"",
  "message":"",
  "metadata":{},
  "status":200
}
```


**Database Collection - get**
---
- This API is for get the list of available database collections which are set in snapshot nodes.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/customer1/api/database/collection -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/customer1/api/database/collection
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
- No Parameters
```

**Response:**
```
{
    "data": {
        "results": [
            "armtemplate",
            "cloudformation",
            "cloudformationtemplate",
            "cloudtrail",
            "ec2",
            "ecs",
            "elb",
            "lambda",
            "microsoftcompute",
            "microsoftcontainerregistry",
            "microsoftcontainerservice",
            "microsoftnetwork",
            "microsoftsqlserversalertpolicies",
            "microsoftstorage",
            "rds",
            "s3",
            "sqs"
        ]
    },
    "error": "",
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Get Collection manage config items**
---

- This API is for get getting json data of config item like connector, snapshot, mastersnapshot, test, and mastertest

**CURL Sample**
```
curl -X GET https://portal.prancer.io/customer1/api/manage/config -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/customer1/api/manage/config
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
- resource_type - <Type of the resource available types: "connector", "snapshot", "mastersnapshot", "test", "mastertest">
- resource_name - <Name of the resource>
- container_name - <Name of the container>
```

**Response:**
```
{
    "data": [
        {
            "json": {
                "autoRemediate": true,
                "branchName": "sensitive_extension",
                "companyName": "prancer",
                "fileType": "structure",
                "gitProvider": "https://github.com/prancer-io/prancer-cloudy.git",
                "httpsUser": "vatsalgit5118",
                "private": false,
                "type": "filesystem",
                "username": "vatsalgit5118"
            },
            "name": "aws_iac_structure"
        }
    ],
    "error": "",
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Update Collection manage config items**
---

- This API is for updating json data of config item like connector, snapshot, mastersnapshot, test, and mastertest

**CURL Sample**
```
curl -X POST https://portal.prancer.io/customer1/api/manage/config -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/customer1/api/manage/config
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Data:**

```
- resource_type - <Type of the resource available types: "connector", "snapshot", "mastersnapshot", "test", "mastertest", "collection_config">
- resource_name - <Name of the resource><for collection config use "collection_config">
- container_name - <Name of the container>
- data - <Updated data>
```

**Response:**
```
{
    "data": [
        {
            "json": {
                "autoRemediate": true,
                "branchName": "sensitive_extension",
                "companyName": "prancer",
                "fileType": "structure",
                "gitProvider": "https://github.com/prancer-io/prancer-cloudy.git",
                "httpsUser": "vatsalgit5118",
                "private": false,
                "type": "filesystem",
                "username": "vatsalgit5118"
            },
            "name": "aws_iac_structure"
        }
    ],
    "error": "",
    "message": "",
    "metadata": {},
    "status": 200
}
```