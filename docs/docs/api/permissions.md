**Permissions APIs**
===

- APIs for creating different user roles and assigning user roles to the users.

**Permissions - Get**
---
- Returns the list of available permissions which can add to the role.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/permission/ \
  -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/permission/
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
                "codename": "api_full_control",
                "id": 63,
                "name": "Full control on api"
            },
            {
                "codename": "collection_full_control",
                "id": 34,
                "name": "Full control on collection"
            },
            {
                "codename": "collection_read",
                "id": 33,
                "name": "Can view collection"
            },
            ...
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Permissions Role - create**
---
- Create a new user role

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/permission/role/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{"permissions": [ "collection_full_control", "compliance_full_control", "configuration_full_control", "crawler_full_control", "dashboard_full_control"],"role_name" : "QC"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/permission/role/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "permissions": [
        "collection_full_control",
        "compliance_full_control",
        "configuration_full_control",
        "crawler_full_control",
        "dashboard_full_control"
    ],
    "id" : 10,
    "role_name" : "QC"
}
```

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Role saved successfully",
    "metadata": {},
    "status": 200
}
```
- **Explanation:**

    `Required Fields`
    - **permissions:** List of permissions that will apply to the role.
    - **role_name:** Name of the user role.

    `Optional Fields`
    
    - **id:** Role id, which returns from the "Permissions - Role Get" API response. If you want to update the existing permissions of a role, it is required. If it is not passed, then it will create a new role.


**Permissions - Role Get**
---
- Returns the list of available user roles.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/permission/role/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/permission/role/
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
                "id": 10,
                "permissions": [
                    {
                        "codename": "dashboard_full_control",
                        "name": "Full control on dashboard"
                    },
                    {
                        "codename": "collection_full_control",
                        "name": "Full control on collection"
                    },
                    {
                        "codename": "crawler_full_control",
                        "name": "Full control on crawler"
                    },
                    {
                        "codename": "compliance_full_control",
                        "name": "Full control on compliance"
                    },
                    {
                        "codename": "configuration_full_control",
                        "name": "Full control on configuration"
                    }
                ],
                "role_name": "QC"
            },
            ...
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```