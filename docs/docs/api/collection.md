**Collection APIs**
===

- Collection is the combinations of Snapshots configuration, Connectors configuration, Compliances configuration, and rego files.

**Collection - create**
---
- Create new collection with given name of type IAC("infrastructure") and PAC("application")

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/collection -H 'authorization: Bearer <JWT Bearer Token>' -d '{ "collection" : "azure_iac", "collection_type" : "infrastructure" }
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection
- **Method:** POST
- **Header:**

```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
{
	"collection" : "<name of the collection>",
	"collection_type" : "infrastructure"
}
```

- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection to be created.

    `Optional Fields`

    - **collection_type:** Valid values are "infrastructure", "application". Default value is "infrastructure". Invalid or missing values default to "infrastructure"


**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Collection created successfully.",
    "metadata": {},
    "status": 200
}
```

**Collection - get**
---
- This API is for get the list of available collections with connectors list available in each collection.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/collection/list -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection/list
- **Method:** GET
- **Header:**

```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
- search: <search by collection name>
```

**Response:**

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
                "tests": [],
                "notifications" : [
                    {
                        "name": "notifications_azure_iac_31"
                    }
                ]
            }
        ]
    },
    "error": "",
    "error_list": [],
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

**Collection - Archive/Delete**
---
- This API is for archiving old collection and deleting new collections

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/collection -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection
- **Method:** DELETE
- **Header:**

```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
- "collection": "collection_name",
- "status": "delete" [available status: "archive", "unarchive", "delete"]
```

**Response:**

```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Collection collection_name deleted successfully",
    "metadata": {},
    "status": 200
}
```

**Collection - exists**
---

- This API is to check if a collection exists.

**CURL Sample**
```
curl -H "space-id:101"  -H 'authorization: Bearer <JWT Bearer Token>' -X GET "https://portal.prancer.io/prancer-customer1/api/collection?collection=git_azure_customer1_1617571294420"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection
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
- This API is for get the list of available database collections in which the actual cloud/IaC snapshot JSON file is stored.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/database/collection -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/database/collection
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
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Get Collection config items**
---

- This API is for get getting json data of config item like connector, snapshot, mastersnapshot, test, mastertest, and collection_configuration

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/manage/config -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/manage/config
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
Required Fields
    - resource_type - <Type of the resource available types: "connector", "snapshot", "mastersnapshot", "test", "mastertest", "collection_configuaration">
    - resource_name - <Name of the resource>
    - container_name - <Name of the container>
```

**Response:**
```
{
    "data": {
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
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Update Collection config items**
---

- This API is for updating json data of config item like connector, snapshot, mastersnapshot, test, mastertest, and collection_configuration, notifications

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/manage/config -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/manage/config
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Data:**

```
{
	"resource_type" : "connector",
	"container_name" : "aws_iac",
	"resource_name" : "aws_iac_structure",
	"data" : {
		"json": {
            "autoRemediate": false,
            "branchName": "sensitive_extension",
            "companyName": "prancer",
            "fileType": "structure",
            "gitProvider": "https://github.com/prancer-io/prancer-cloudy.git",
            "httpsUser": "vatsalgit5118",
            "private": false,
            "type": "filesystem",
            "username": "vatsalgit5118"
        }
	}
}
```

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Connector updated successsfully",
    "metadata": {},
    "status": 200
}
```


**Archive/Unarchive a collection**
---

- This API is for updating json data of config item like connector, snapshot, mastersnapshot, test, mastertest, and collection_configuration

**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/collection -H 'authorization: Bearer <JWT Bearer Token>' -d '{ "collection" : "azure_iac", "status" : "inactive" }
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection
- **Method:** DELETE
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```
{
	"collection" : "azure_iac",
	"status" : "inactive"
}
```

- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection for which you want to change the status.
    - **status:** Status of collection `active` or `inactive`.


**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Collection azure_iac archived successfully",
    "metadata": {},
    "status": 200
}
```

**Upload collection manage config files**
---

- This API is for uploading json files of config item like connector, snapshot, mastersnapshot, test, mastertest, and collection_configuration, notifications

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/manage/config/upload -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/manage/config/upload
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **form-data:**

```
- files - <Multiple files: "connector", "snapshot", "mastersnapshot", "test", "mastertest", "collection_configuration">
- container_name - <Name of the container>
```

**Response Success:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "All files added successfully",
    "metadata": {},
    "status": 200
}
```

**Response Error:**
```
{
    "data": {},
    "error": "",
    "error_list": [
        "Invalid JSON - masterSnapshot field is missing or empty"
    ],
    "message": "",
    "metadata": {},
    "status": 400
}
```
