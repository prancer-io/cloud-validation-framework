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
  https://portal.prancer.io/customer1/api/login/ -H 'content-type: application/json' \
  -d '{
	"email" : "<Valid Email Address>",
	"password" : "<Valid Password>",
	"customer_id" : "<Valid CustomerId>"
}'
```

- **URL:** https://portal.prancer.io/api/login/
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
    - **customer_id:** Valid customer Id of user.


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

**Refresh Token**
---

- `token` comes from Login API has expire time of 7 days. After 7 days it cannot be use for access authenticated APIs.
- Refresh Token api is use for get new token without perform login.
- Pass the `refresh_token` in authorization header which comes from login API. It will create new token which can be use for next 24 hours.

**CURL Sample**
```
curl -X GET \
  https://portal.prancer.io/api/refresh/token/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/api/refresh/token/
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
  https://portal.prancer.io/api/logout/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/api/logout/
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