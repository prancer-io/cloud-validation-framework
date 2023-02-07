**Drift detection APIs**
===
**Drift detection - Output detail**
---
- API for drift detection output detail.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/drift_detection/report/detail/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{"drift_output_id": "63aad93b76780fb0b1913033","drift_result_id": "awsdrifttf_TEST_IAM_050_1672141115","container": "aws_drift_tf"}
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/report/detail/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "drift_output_id": "63aad93b76780fb0b1913033",
    "drift_result_id": "awsdrifttf_TEST_IAM_050_1672141115",
    "container": "aws_drift_tf"
}
```

- **Explanation:**

    `Required Fields`

    - **container:** Name of the cloud container for which you want drift detection output detail.
    - **drift_output_id:** Output id of the drift detection output record.
    - **drift_result_id:** Result id of the drift detection output result.

    
**Response:**
```
{
    "data": {
        "cloud_snapshot": {
            "name": "prancerWebApp",
            "properties": {
                "httpsOnly": true,
                "siteConfig": {
                    "minTlsCipherSuite": null,
                    "minTlsVersion": null,
                    "linuxFxVersion": "DOTNETCORE|3.0"
                }
            },
            "type": "Microsoft.Web/sites"
        },
        "cloud_type": "azure",
        "container": "azure_drift_tf",
        "iac_snapshot": {
            "name": "prancerWebApp",
            "properties": {
                "httpsOnly": false,
                "siteConfig": {
                    "minTlsCipherSuite": null,
                    "minTlsVersion": 1.1,
                    "linuxFxVersion": "PYTHON|3.10"
                }
            },
            "type": "Microsoft.Web/sites"
        },
        "iac_type": "terraform",
        "resource_type": "azurerm_app_service",
        "result": "drifted",
        "result_id": "azuredrifttf_AZRSNP_100171_1673936853",
        "tags": {
            "prancer_unique_id": "9b0b53c1-6619-47ac-b646-599b6bc5ae02",
            "resource_type": "azurerm_app_service"
        },
        "timestamp": 1673936853888
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Drift detection - Upload Drift configuration**
---
- API to manage drift detection configuration of a container. This API has Three methods GET, POST and DELETE.

**POST method.**
---
  	POST method to submit the drift detection configuration. 
	
- **CURL Sample**

``` curl 
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/drift_detection/config/' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{
    "container": "container_name",
    "is_drift_detection_active": false,
    "iac_mastersnapshot": "master_iac_snapshot_name",
    "cloud_mastersnapshot": "master_cloud_snapshot_name"
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/config/
- **Method:** POST
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```	

- **Param:**

``` json
{
    "container": "container_name",
    "is_drift_detection_active": false,
    "iac_mastersnapshot": "master_iac_snapshot_name",
    "cloud_mastersnapshot": "master_cloud_snapshot_name"
}
```
- **Explanation:**
    `All of the fields are required.`
    - **is_drift_detection_active**: To run drift detection whenever we run crawl and compliance. Valid values are true or false,
    - **iac_mastersnapshot** : Name of the IAC mastersnapshot,
    - **cloud_mastersnapshot** : Name of the cloud mastersnapshot.
    - **container** : Name of the container.

- **Response:**

``` json
{
    "data": {
        "cloud_mastersnapshot": "master_iac_snapshot_name",
        "iac_mastersnapshot": "master_cloud_snapshot_name",
        "is_drift_detection_active": false
    },
    "error": "",
    "error_list": [],
    "message": "Drift detection configuration is succesfully added.",
    "metadata": {},
    "status": 200
}
```

**DELETE method.**
---
  	DELETE method to delete the existing drift detection configuration. 
	
**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/drift_detection/config/?container=container_name -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' 
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/config/
- **Method:** DELETE
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

```
    "container": "container_name"
```
- **Explanation:**
    `All of the fields are required.`
    - **container** : Name of the container.

- **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Drift detection configuration deleted successfully.",
    "metadata": {},
    "status": 200
}
```

**GET method.**
---
  	GET method to fetch the existing drift detection configuration. 
	
**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/drift_detection/config/?container=container_name -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' 
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/config/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

```
    "container": "container_name"
```
- **Explanation:**
    `All of the fields are required.`
    - **container** : Name of the container.

- **Response:**

``` json
{
    "data": {
        "cloud_mastersnapshot": "mastersnapshot_aws_cloud",
        "iac_mastersnapshot": "master-snapshot",
        "is_drift_detection_active": true
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Drift detection - mastersnapshot list**
---
- API to get mastersnapshot list for a container..

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/mastersnapshot/list/?container=container_name -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/mastersnapshot/list/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "container": "container_name"
}
```

- **Explanation:**

    `Required Fields`

    - **container:** Name of the container.

    
**Response:**
```
{
    "data": {
        "cloud_snapshots": [
            "mastersnapshot_aws_cloud"
        ],
        "iac_snapshots": [
            "master-snapshot"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Drift detection - Get tag**
---
- API for getting the prancer_unique_id tags.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/drift_detection/get_tag -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/get_tag/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

**Response:**
```
{
    "data": {
        "prancer_unique_id": "1e08eaab-666d-4d4c-bf3b-88ffcd3e8af5"
    },
    "error": "",
    "error_list": [],
    "message": "Tag received successfully.",
    "metadata": {},
    "status": 200
}
```
