**Users APIs**
===

**Users - get**
---
- API for get loggedIn user's information.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/user/get/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/user/get/
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



**Users - update tour status**
---
- API to update the status of a page tour

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/user/tour/ -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/user/tour/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
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
```
{
    "data": "Tour status updated successfully",
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```
