**Webhook APIs**
===

**Webhook - save**
---
- Enable or Disable github webhook autofix feature for a collection

**CURL Sample**
```
curl -X POST https://portal.prancer.io/customer1/api/webhook/github/create -H 'authorization: Bearer <JWT Bearer Token>' -d '{ "collection" : "azure_arm", "enable" : true }'
```

- **URL:** https://portal.prancer.io/customer1/api/webhook/github/create
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{ 
    "collection" : "azure_arm", 
    "enable" : true 
}
```

**Explanation**

- collection: Name of the collection for which configure the webhook
- enable: Boolean value to specify enable or disable the webhook.

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Successfully updated configuration",
    "metadata": {},
    "status": 200
}
```
