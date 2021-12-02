**Collection Config APIs**
===

- Collection Config is feature to provide basic settings for specific collection like generate only commit not PR, Secret remediation vault settings etc.

**Collection Config - GET**
---

**CURL Sample**
```
curl -X GET https://portal.prancer.io/customer1/api/collection_config/?collection=AWS_TF -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/customer1/api/collection_config/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"collection": "AWS_TF"
}
```
- **Explanation:**

    `Required Fields`

    - **collection:** The name of the collection to get configuration.

 
**Response:**
```
{
    "data": {
        "collection_config": {
            "generate_pr": false
        }
    },
    "error": "",
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Collection Config - Create or Update**
---

**CURL Sample**
```
curl -X POST https://portal.prancer.io/customer1/api/collection_config/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{collection: AWS_TF, configuration: {generate_pr: false}}'
```

- **URL:** https://portal.prancer.io/customer1/api/collection_config/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"collection": "AWS_TF",
    "configuration": {
        "generate_pr": false
    }
}
```
- **Explanation:**

    `Required Fields`

    - **collection:** The name of the collection to get configuration.
    - **configuration:** updated configuration data

 
**Response:**
```
{
    "data": {},
    "error": "",
    "message": "Configuration updated",
    "metadata": {},
    "status": 200
}
```
