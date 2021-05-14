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
- No Parameters
```

**Response:**
```
{
    "data": {
        "results": [
            {
                "collection": "default_container",
                "connectors": [
                    "default_connector"
                ]
            },
            {
                "collection": "google_crawler_demo",
                "connectors": [
                    "googleCrawlerStructure"
                ]
            },
            {
                "collection": "aws_crawler_demo",
                "connectors": [
                    "aws_structure"
                ]
            },
            {
                "collection": "azure_demo",
                "connectors": []
            },
            {
                "collection": "azure_crawler_demo",
                "connectors": [
                    "azure_structure",
                    "azure_crawler_structure"
                ]
            },
            {
                "collection": "git_google_demo_db",
                "connectors": [
                    "git_connector",
                    "googleCrawlerStructure"
                ]
            },
            {
                "collection": "google_iac_demo",
                "connectors": [
                    "google_template_structure"
                ]
            },
            {
                "collection": "aws_iac_demo",
                "connectors": [
                    "aws_template_structure"
                ]
            }
        ]
    },
    "error": "",
    "message": "",
    "metadata": {},
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