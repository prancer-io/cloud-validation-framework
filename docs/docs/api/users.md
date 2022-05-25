**Users APIs**
===

**Users - Send Invitation**
---

- API for sending user invitation for prancer.

**CURL Sample**

```curl
curl -X GET https://portal.prancer.io/prancer-customer1/api/user/invite/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/user/invite/>
- **Method:** POST
- **Header:**

```text
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```json
{
    "email": "test.login319@gmail.com",
    "resend": false
}
```

**Response:**

```json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "User invitation link sent successfully",
    "metadata": {},
    "status": 200
}
```

**Explanation**

- Email field is required
- If user invitation is sending for first time then set `resend` value to `false`
- If user invitation is resending to the user then set `resend` value to `true`


**Users - get**
---

- API for get loggedIn user's information.

**CURL Sample**

```curl
curl -X GET https://portal.prancer.io/prancer-customer1/api/user/get/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/user/get/>
- **Method:** GET
- **Header:**

```text
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```text
- No Parameters
```

**Response:**

```json
{
    "data": {
        "email": "useremail@gmail.com",
        "id": 2,
        "is_staff": false,
        "is_superuser": false,
        "is_admin": true,
        "name": " ",
        "permissions": [
            "dashboard_full_control",
            "dashboard_read",
            "query_full_control",
            "query_read",
            "resource_full_control",
            "resource_read",
            "policy_full_control",
            "policy_read",
            "report_full_control",
            "report_read"
        ],
        "tours": {
            "/wc/dashboard": false,
            "/wc/exclusion/search": false,
            "/wc/resource/search": true
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Explanation**

- Response contains the user role `is_staff`, `is_superuser` and `is_admin`.
- If the user type is either `is_admin` or `is_superuser` then user have full control on all services.
- For Staff users need to verify permissions on web interface.

**Users - list**
---

**CURL Sample**

```curl
curl -X GET https://portal.prancer.io/prancer-customer1/api/user/manage/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/user/manage/>
- **Method:** GET
- **Header:**

```text
content-type: application/json
Authorization: Bearer <JWT Bearer Token>
```

**Param:**

```text
- No Parameters
```

**Response:**

```json
{
    "data": {
        "users": [
            {
                "date_joined": "Fri, 20 Mar 2020 05:50:56 GMT",
                "email": "prancer@gmail.com",
                "first_name": "",
                "id": 1,
                "is_active": true,
                "is_staff": true,
                "is_superuser": true,
                "last_login": "Fri, 01 Apr 2022 09:44:17 GMT",
                "last_name": "",
                "password": "pbkdf2_sha256$120000$csNVo2wtSbVa$yGEM7dVeQkWbsCvM641GgASxFk2p0VqU5lw4raw5UGc=",
                "status": "Registered",
                "user_groups": [
                    "Owner"
                ],
                "username": "prancer@gmail.com"
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

**Users - Delete**
---

**CURL Sample**

```curl
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/user/manage/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/user/manage/>
- **Method:** DELETE
- **Header:**

```text
content-type: application/json
Authorization: Bearer <JWT Bearer Token>
```

**Param:**

```json
{
    "email": "test@gmail.com"
}
```

**Response:**

```json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "User does deleted successfully!",
    "metadata": {},
    "status": 200
}
```

**Users - update tour status**
---

- API to update the status of a page tour

**CURL Sample**

```curl
curl -X POST https://portal.prancer.io/prancer-customer1/api/user/tour/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/user/tour/>
- **Method:** POST
- **Header:**

```text
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```json
{
 "tour_path" :  "/wc/resource/search",
 "status" : true
}
```

**Explanation**

`Required Fields`

    - **tour_path:**  Tour path which is come from response of get users API.
    - **status:** Boolean field to set the status of a tour.

**Response:**

```json
{
    "data": "Tour status updated successfully",
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```
