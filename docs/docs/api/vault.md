**Vault APIs**
===

- Vault APIs are used to save the secrets to the vault and get the value from the vault whenever required.

**Vault - get**
---

- API returns the value of a specific key, which the user sets in the vault.

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/secret/vault/?key_name=secret-key' -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/secret/vault/?key_name=secret-key
- **Method:** GET
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
```
 
**Response:**
```
{
    "data": {
        "value": "secret-value"
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Vault - save key**
---

- API for saving the secret value into the vault.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/secret/vault/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "key_name" : "secret-key", "vault_value" : "secret-value" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/secret/vault/
- **Method:** POST
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
    - content-type: application/json
```

- **Param:**
```
{ 
    "key_name" : "secret-key", 
    "vault_value" : "secret-value"
}
```
 
**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Key saved successfully in keyvault",
    "metadata": {},
    "status": 200
}
```

**Vault - update**
---

- API for updating the secret value into the vault.

**CURL Sample**
```
curl -X PUT https://portal.prancer.io/prancer-customer1/api/secret/vault/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "key_name" : "secret-key", "vault_value" : "secret-updated-value" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/secret/vault/
- **Method:** POST
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
    - content-type: application/json
```

- **Param:**
```
{ 
    "key_name" : "secret-key", 
    "vault_value" : "secret-updated-value"
}
```
 
**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Key saved successfully in keyvault",
    "metadata": {},
    "status": 200
}
```

**Vault - delete key**
---

- API for deleting the secret value from the vault.

**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/secret/vault/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "key_name" : "secret-key" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/secret/vault/
- **Method:** POST
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
    - content-type: application/json
```

- **Param:**
```
{ 
    "key_name" : "secret-key", 
}
```
 
**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Key deleted successfully from keyvault",
    "metadata": {},
    "status": 200
}
```