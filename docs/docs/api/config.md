**Configuration APIs**
===

- Configuration APIs provide basic settings for specific collection like do only commit while remediation, not create any PR, Secret remediation vault settings etc. Also we can set global configuration like set logging level while run compliance.

**Collection Config - GET**
---

- API for set the configuration of a specific collection.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/collection_config/?collection=AWS_TF -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection_config/
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
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Collection Config - Create or Update**
---

- API for create or update the configuration of a specific collection.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/collection_config/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{collection: AWS_TF, configuration: {generate_pr: false}}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection_config/
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
    "error_list": [],
    "message": "Configuration updated",
    "metadata": {},
    "status": 200
}
```


**Configuration - Get**
---

- API for get global configuration of system.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/config/manage -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/config/manage
- **Method:** GET
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
```

**Response:**
```
{
    "data": {
        "config": {
            "LOGGING": {
                "level": "INFO",
                "space_id": "115"
            }
        },
        "modifiable_fields": {
            "LOGGING": [
                {
                    "name": "level",
                    "type": "option",
                    "values": [
                        "CRITICAL",
                        "ERROR",
                        "WARNING",
                        "INFO",
                        "DEBUG"
                    ]
                }
            ]
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

- **Explanation:**

    - **config:** The configuration map which defines the configuration of the specific feature. Here in the config it defines the level configuration of `LOGGING`.
    - **modifiable_fields:** It defines the list of field for specific features which can be modify.
        - **name:** Name of the editable field.
        - **type:** Type of the value which can be set for that field. It can be either `string` or `option`.
        - **values:** List of values can be set for this field. It will available only if type is `option`.


**Configuration - Update**
---

- API for update global configuration of system.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/config/manage -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "config" : { "LOGGING" : { "level": "INFO" }}}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/config/manage
- **Method:** POST
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
    - content-type: application/json
```

- **Param:**
```
{
	"config" : {
		"LOGGING" : {
			"level": "INFO"
		}	
	}
}
```
- **Explanation:**

    `Required Fields`

    - **config:** The configuration map with fields which requires to update.

 
**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Configuration updated successfully",
    "metadata": {},
    "status": 200
}
```