**Authentication API**
===

- Every APIs of Prancer Enterprise are secure with unique authentication token.
- Use the Login API for generate the authentication token.
- The expiration time of token is 7 days.

**Login API**
---

**CURL Sample**
```
curl -X POST \
  https://portal.prancer.io/prancer-customer1/api/login/ -H 'content-type: application/json' \
  -d '{
	"email" : "<Valid Email Address>",
	"password" : "<Valid Password>",
	"customer_id" : "<Valid CustomerId>"
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/login/
- **Method:** POST
- **Header:**
    - content-type: application/json
- **Param:**
```
    {
        "email" : "<Valid Email Address>",
        "password" : "<Valid Password>",
        "customer_id" : "<Valid CustomerId>"
    }
```

- **Explanation:**

    `Required Fields`

    - **email:** Valid email of user for login.
    - **password:** Valid password of user for login.
    - **customer_id:** It is in the format of `prancer-<company_name>`. For example, if your company name is `ABC`, the customer id would be `prancer-abc`.


**Success Response:**

- Status Code: 200
- Response:
```
{
    "data": {
        "refresh_token": "<JWT refresh Token>",
        "token": "<JWT Bearer Token>"
    },
    "error": "",
    "error_list": [],
    "message": "User Logged In Successfully",
    "metadata": {},
    "status": 200
}
```

**Failed Response:**

- Status Code: 400
- Response:
```
{
  "data": {},
  "error": "Authentication Failed",
  "message": "Invalid Email or Password",
  "metadata": {},
  "status": 400
}
```

- In Success Response you will receive `token` and `refresh_token`.
- Once you get the `token` using Login API, you can use that `token` for access other secure APIs.

## Create User Access Token

User Acceess Token can be use to authenticate the prancer enterprise API without email and password

**CURL Sample**
```
curl -X POST \
  https://portal.prancer.io/prancer-customer1/api/user/accesstoken/ -H 'content-type: application/json' \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -d '{
	"token_name" : "github pipeline token"
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/validate/accesstoken/
- **Method:** POST
- **Header:**
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
- **Param:**
```
    {
        "token_name" : "github pipeline token"
    }
```

- **Explanation:**

    `Required Fields`

    - **token_name:** Any name to identify the token reference.
    

**Success Response:**

- Status Code: 200
- Response:
```
{
    "data": {
        "token":"04c57a81fc034b16aa2d654f5d46fd59"
    },
    "error": "",
    "error_list": [],
    "message": "User access token set successfully",
    "metadata": {},
    "status": 200
}
```

## Get list of access token

Get the list of access token

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/user/accesstoken/ \
  -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/validate/accesstoken/
- **Method:** GET
- **Header:**
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
- **Param:**
```
- No Parameters
```

**Success Response:**

- Status Code: 200
- Response:
```
{
    "data": {
        "token_list": [{
            "token_id":"62752393b5079a7af37d490f",
            "token_name":"github pipeline token"
        }]
    },
    "error": "",
    "error_list": [],
    "message": "Token is Valid",
    "metadata": {},
    "status": 200
}
```

## Delete an access token

Delete a user access token

**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/user/accesstoken/ \
    -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/validate/accesstoken/
- **Method:** DELETE
- **Header:**
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
- **Param:**
```
{
    "token_id" : "62752393b5079a7af37d490f"
}
```
- **Explanation:**

    `Required Fields`

    - **token_id:** A valid token id returns from the get token list API.

**Success Response:**

- Status Code: 200
- Response:
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Token removed successfully",
    "metadata": {},
    "status": 200
}
```

## Validate Access Token

**CURL Sample**
```
curl -X POST \
  https://portal.prancer.io/prancer-customer1/api/validate/accesstoken/ -H 'content-type: application/json' \
  -d '{
	"token" : "<Valid User Access Token>",
	"customer_id" : "<Valid CustomerId>"
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/validate/accesstoken/
- **Method:** POST
- **Header:**
    - content-type: application/json
- **Param:**
```
    {
        "token" : "<Valid User Access Token>",
        "customer_id" : "<Valid CustomerId>"
    }
```

- **Explanation:**

    `Required Fields`

    - **token:** Valid User Access Token, generated from website.
    - **customer_id:** It is in the format of `prancer-<company_name>`. For example, if your company name is `ABC`, the customer id would be `prancer-abc`.


**Success Response:**

- Status Code: 200
- Response:
```
{
    "data": {
        "refresh_token": "<JWT refresh Token>",
        "token": "<JWT Bearer Token>"
    },
    "error": "",
    "error_list": [],
    "message": "Token is Valid",
    "metadata": {},
    "status": 200
}
```

**Failed Response:**

- Status Code: 400
- Response:
```
{
  "data": {},
  "error": "",
    "error_list": [],
  "message": "Invalid token or customer id",
  "metadata": {},
  "status": 400
}
```

- In Success Response you will receive `token` and `refresh_token`.
- Once you get the `token` using Validate Access Token API, you can use that `token` for access other secure APIs.

**Refresh Token**
---

- `token` comes from Login API has expire time of 7 days. After 7 days it cannot be use for access authenticated APIs.
- Refresh Token api is use for get new token without perform login.
- Pass the `refresh_token` in authorization header which comes from login API. It will create new token which can be use for next 24 hours.

**CURL Sample**
```
curl -X GET \
  https://portal.prancer.io/prancer-customer1/api/refresh/token/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/refresh/token/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

**Success Response:**

- Status Code: 200
- Response:
```
{
    "data": {
        "refresh_token": <JWT refresh Token>",
        "token": <JWT Bearer Token>
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Failed Response:**

- Status Code: 401
- Response:
```
{
    "data": {},
    "error": "Unauthorized",
    "message": "Please authenticate to access this API.",
    "metadata": {},
    "status": 401
}
```

**Logout API**
---

API for logout user. Once user gets logout the refresh token will also not work.

**CURL Sample**
```
curl -X POST \
  https://portal.prancer.io/prancer-customer1/api/logout/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/logout/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

**Success Response:**

- Status Code: 200
- Response:
```
{
  "data": {},
  "error": "",
  "error_list": [],
  "message": "User logged out successfully!",
  "metadata": {},
  "status": 200
}
```

**Failed Response:**

- Status Code: 401
- Response:
```
{
  "data": {},
  "error": "Unauthorized",
  "message": "Please authenticate to access this API.",
  "metadata": {},
  "status": 401
}
```