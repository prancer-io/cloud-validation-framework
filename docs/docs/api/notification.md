**Notification APIs**
===

**Notification - List**
---

- **CURL Sample**

``` curl
curl --location --request GET 'https://portal.prancer.io/prancer-customer1/api/manage/notification/?container=test_collection&index=0&count=2' \
--header 'Authorization: Bearer <JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/manage/notification>
- **Method:** GET
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

``` json
{
    "container": "Container Name",
    "count" : 3,
    "index" : 0,
    "search" : <search_text>
}
```

- **Explanation:**

    `Required Fields`
    - **container:** Name of the container,

    `Other Fields`
    - **search:** Search the notification by name.

 **NOTE:**

- `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.

**Response:**

- _response with pagination of 2 records_

- Status Code: 200
- Response:

``` json
{
    "data": [
        {
            "id": "62f08ba3d6104952c348827d",
            "name": "aws_cloud_notification7",
            "timestamp": "2022-08-08T04:05:55.000Z"
        }
    ],
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 2,
        "current_page": 1,
        "next_index": -1,
        "total": 1
    },
    "status": 200
}
```


**Notification - Delete**
---

- **CURL Sample**

``` curl
curl --location --request DELETE 'https://portal.prancer.io/prancer-customer1/api/manage/notification/?notification_name=sample_notification_file&container=check_notification' \
--header '<JWT Bearer Token>'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/manage/notification>
- **Method:** DELETE
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

``` json
{
    "container": "check_notification",
    "notification_name": "sample_notification_file"
}
```

- **Explanation:**

    All Fields are Required.
  - **container:** Name of the container in which notification file is present.
  - **notification_name:** Name of the notification file which you want to delete.


**Response:**

- Status Code: 200
- Response:

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Notification deleted successfully.",
    "metadata": {},
    "status": 200
}
```
