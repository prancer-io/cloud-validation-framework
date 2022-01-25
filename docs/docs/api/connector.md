**Connector APIs**
===

- Connector configuration contains the credentials using which connect to the cloud provider and use their services.

**Connector - get**
---
- Returns the list of available connectors in the system with some of its configuration details.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/customer1/api/connector/list -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/customer1/api/connector/list
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
                "_id": "5e62643a7e80f1cf4e2d78b9",
                "collection": "google_crawler_demo",
                "connector": "googleCrawlerStructure",
                "data": [
                    {
                        "project_id": "<GCP Project Id>",
                        "user": "<IAM user name>"
                    },
                    {
                        "project_id": "<GCP Project Id>",
                        "user": "<IAM user name>"
                    },
                    {
                        "project_id": "<GCP Project Id>",
                        "user": "<IAM user name>"
                    }
                ],
                "type": "google"
            },
            {
                "_id": "5e6f238eaec125f9450aec9c",
                "collection": "aws_crawler_demo",
                "connector": "aws_structure",
                "data": [
                    {
                        "account_id": "<AWS Account Id>",
                        "user": "<AWS Account User>"
                    }
                ],
                "type": "aws"
            },
            {
                "_id": "5e6f2862aec125f9450aecb5",
                "collection": "azure_crawler_demo",
                "connector": "azure_structure",
                "data": [
                    {
                        "subscription_id": "<Azure Subscription Id>",
                        "user": "<Azure Account User>"
                    }
                ],
                "type": "azure"
            },
            {
                "_id": "5f3a3f20d59395ccde16491c",
                "collection": "google_iac_demo",
                "connector": "google_template_structure",
                "data": [
                    {
                        "branch_name": "<git branch-name>",
                        "user": "<git username>"
                    }
                ],
                "type": "filesystem"
            }
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Response Explanation:**
Here in response you can see the list of connectors with different data in it.
- For connector type `GCP`, it will contain the `project_id` and `user` fields in data value.
- For connector type `Azure`, it will contain the `subscription_id` and `user` fields in data value.
- For connector type `AWS`, it will contain the `account_id` and `user` fields in data value.
- For connector type `filesystem/git`, it will contain the `branch_name` and `user` fields in data value.