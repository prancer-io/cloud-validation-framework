**Compliance APIs**
===

**Compliance - Run Compliance**
---
- API for running the compliance on provided collection.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/compliance/run/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "collection" : "azure_cloud" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/compliance/run/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "collection" : "azure_cloud"
}
```

- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection for which you want to run the compliance.
    

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Compliance started running successfully.",
    "metadata": {},
    "status": 200
}
```

**Compliance - Run Crawler**
---
- API for running the crawler on provided collection.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/compliance/crawler/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "collection" : "azure_cloud" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/compliance/crawler/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "collection" : "azure_cloud"
}
```

- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection for which you want to run the compliance.
    

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Crawler started running successfully.",
    "metadata": {},
    "status": 200
}
```

**Compliance - Add Schedulers**
---
- API for adding a new Scheduler.

**CURL Sample**
```
curl -X POST \
  https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json' \
  -d '{
    "collection":"azure_cloud",
    "schedule":"Daily@01:00 date@13/05/2021",
    "name":"Test",
    "description":"test ",
    "recur":"1",
    "test":"CRAWLER",
    "crawler":true
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "collection":"azure_cloud",
    "schedule":"Daily@01:00 date@13/05/2021",
    "name":"Test",
    "description":"test ",
    "recur":"1",
    "test":"CRAWLER",
    "crawler":true,
    "config_id" : "62186dd3c1d0e47a312b9f45"
}
```

- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection for which you want to scheduler a Job.
    - **schedule:** We can schedule the following types of Schedulers.
        - Once ( Ex. `once@11:00 date@10/26/2019` )
        - Hourly ( Ex. `hourly@11:00 date@10/26/2019` )
        - Daily ( Ex. `daily@11:00 date@10/26/2019` )
        - Weekly ( Ex. `weekly@11:00 date@10/26/2019` )
        - Monthly ( Ex. `monthly@11:00 date@10/26/2019` )
    - **name:** Name of the Scheduler Job.
    - **description:** Description about the Scheduler Job.
    - **recur:** It defines the Job will run after no. of recuring defined.
        ( Ex. recur is 2, then Job will run after every 2 hours )
    - **test** : Valid value for this field is `TEST`, `CRAWLER` and `BOTH`.
        - `TEST:` Run the only compliance on specified collection.
        - `CRAWLER:` Run only crawler on specified collection.
        - `BOTH:` Run both Crawler and then compliance on specified collection.
    - **crawler** : Require to set this field to `true` if the `test` value is `CRAWLER` or `BOTH`.

    `Optional Fields`

    - **config_id** : Any Id to use it as reference at time of running the scheduler.

**Response:**
```
{
    "data": {
        "jobs": [
            {
                "id": "azure_cloud_nbyrl_9441",
                "name": "azure_cloud",
                "next_run_time": "2021-05-14 01:00:00"
            }
        ]
    },
    "error": "",
    "error_list": [],
    "message": "Job scheduled successfully",
    "metadata": {},
    "status": 200
}
```

**Compliance - Get scheduler list**
---
- API for getting the list of scheduled jobs.

**CURL Sample**
```
curl -X GET \
  https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/
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
        "jobs": [
            {
                "collection": "azure_cloud",
                "crawler": true,
                "config_id": "",
                "description": "Wizard Created azure_cloud scheduled",
                "id": "azure_cloud_nbyrl_9441",
                "name": "Scheduled azure_cloud",
                "next_run_time": "2021-05-13 15:30:00",
                "recur": "2",
                "schedule": "Hourly@15:00 date@12/05/2021",
                "test": "BOTH"
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

**Compliance - Get a scheduler**
---
- API for get a scheduled job.

**CURL Sample**
```
curl -X GET \
  https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/?scheduler_id=azure_cloud_nbyrl_9441 \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "scheduler_id" : "azure_cloud_nbyrl_9441"
}
```
- **Explanation:**

    `Required Fields`

    - **scheduler_id:** Id of the Scheduled Job.

**Response:**
```
{
    "data": {
        "collection": "azure_cloud",
        "crawler": true,
        "config_id": "",
        "description": "Wizard Created azure_cloud scheduled",
        "id": "azure_cloud_nbyrl_9441",
        "name": "Scheduled azure_cloud",
        "next_run_time": "2021-05-13 15:30:00",
        "recur": "2",
        "schedule": "Hourly@15:00 date@12/05/2021",
        "test": "BOTH"
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Compliance - Delete scheduler**
---
- API for deleting a scheduled job.

**CURL Sample**
```
curl -X DELETE \
  https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/ \
  -H 'authorization: Bearer <JWT Bearer Token>' \
  -H 'content-type: application/json' \
  -d '{
    "id" : "azure_cloud_nbyrl_9441"
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/compliance/scheduler/
- **Method:** DELETE
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "id" : "azure_cloud_nbyrl_9441"
}
```
- **Explanation:**

    `Required Fields`

    - **id:** Id of the Scheduled Job.

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Job deleted successfully",
    "metadata": {},
    "status": 200
}
```