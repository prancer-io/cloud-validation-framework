# SSO APIs

## SSO Azure Connect API

### Description

- Connect to Azure Account using authentication credentials and fetch related user details

### Curl Sample

```curl
curl --location --request POST 'https://portal.prancer.io/prancer-customer1/api/sso/azure/connect' \
--header 'Authorization: Bearer <JWT Bearer Token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tenant_id": "f997f2f9-a48f-xxxx-xxxx-xxxxxxxxxxxx",
    "client_id": "db57053a-7bce-xxxx-xxxx-xxxxxxxxxxxx",
    "client_secret": "EnM7Q~52qpx67LcMDQpxxxxxxxxxxxxxxx",
    "group_id": "12345678-a1b1-xxxx-xxxx-xxxxxxxxxxxx"
}'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/sso/azure/connect>
- **Method:** POST
- **Header:**

```text
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```json
    "tenant_id": "f997f2f9-a48f-xxxx-xxxx-xxxxxxxxxxxx",
    "client_id": "db57053a-7bce-xxxx-xxxx-xxxxxxxxxxxx",
    "client_secret": "EnM7Q~52qpx67LcMDQpxxxxxxxxxxxxxxx",
    "group_id": "12345678-a1b1-xxxx-xxxx-xxxxxxxxxxxx"
```

- **Explanation:** provide given parameter and the API will return list of available users with invitation status

- **Response:**

```json
{
    "data": {
        "results": [
            {
                "email": "farshid@liquware.com",
                "group_id": "12345678-a1b1-c1d1-1234-123456abc1",
                "is_invited": false,
                "username": "Farshid Mahdavipour"
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

## SSO Azure Add User For Corporate Login

### Description

- Add users in prancer with corporate login

### Curl Sample

```curl
curl --location --request POST 'https://portal.prancer.io/prancer-customer1/api/sso/provision' \
--header 'Authorization: Bearer <JWT Bearer Token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "provision_emails": ["vatsal.thaker.p@Liquwareus.onmicrosoft.com", "ajey.khanapuri@liquware.com"],
    "group_id": "12345678-a1b1-c1d1-1234-123456abc1"
}'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/sso/provision>
- **Method:** POST
- **Header:**

```text
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

```json
{
    "provision_emails": ["farshid@liquware.com"],
    "group_id": "12345678-a1b1-xxxx-xxxx-xxxxxxxxxxx"
}
```

- **Explanation:** Provide list of email and group Id to register user with prancer

- **Response:**

```json
{
    "data": {
        "results": [
            {
                "email": "farshid@liquware.com",
                "group_id": "12345678-a1b1-c1d1-1234-123456abc1",
                "is_invited": false,
                "username": "Farshid Mahdavipour"
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
