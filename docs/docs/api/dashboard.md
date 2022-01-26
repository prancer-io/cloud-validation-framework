**Dashboard APIs**
===

- API for create the different statstic componenets on dashboard.

**Dashboard - Get Components**
---
- Returns the list of available dashboard componenets.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/dashboard/view \
  -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/dashboard/view
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
                "container": "cloudformation_template_demo",
                "days": "7",
                "id": "5f6dfd0e3c83dfccd19083ee",
                "tag": {
                    "cloud": "AWS",
                    "compliances": [
                        "CIS"
                    ],
                    "services": [
                        "ec2"
                    ]
                },
                "title": "Title 1"
            },
            {
                "container": "",
                "days": "7",
                "id": "5f6dfd233c83dfccd19083fa",
                "tag": {
                    "cloud": "",
                    "compliances": [],
                    "services": []
                },
                "title": "Title 2"
            },
            {
                "container": "deployment_manager_demo",
                "days": "7",
                "id": "5f6dfd353c83dfccd19083ff",
                "tag": {
                    "cloud": "GCP",
                    "compliances": [
                        "CSA"
                    ],
                    "services": [
                        "Compute"
                    ]
                },
                "title": "Title 3"
            },
            {
                "container": "deployment_manager_git_demo",
                "days": "7",
                "id": "5f716508c2dc794a314887ec",
                "tag": {
                    "cloud": "",
                    "compliances": [],
                    "services": []
                },
                "title": "Title 4"
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

**Response Explanation:**
Here in response you can see the available statstic componenets of dashboard.
Once you get the componenet list, call the Dashboard - Stats API for get the stastic of each componenets



**Dashboard - stats**
---
- Returns the statstics of a dashboard componenet.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/dashboard/view -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "container": "", "days": "7", "tag": { "cloud": "", "compliances": [], "services": [] }}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/dashboard/view
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"container": "",
    "days": "7",
    "tag": {
        "cloud": "",
        "compliances": [],
        "services": []
    }
}
```

**Response:**
```
{
    "data": {
        "day_results": [
            "2021 Mar 03",
            "2021 Mar 01"
        ],
        "fail_results": [
            2,
            155
        ],
        "pass_results": [
            8,
            243
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```
- **Explanation:**

    `Optional Fields`
    - **container:** Pass the container name for which you want to get the statstics. 
    - **days:** Response will returns the stats till the number of days passed in request. Default value is 7.
    - **tag:** Pass the tags for filter the stats. 

    __NOTE: Check the response of 'Dashboard - Get Components' api. You have to pass same value which are returns in the response of dashboard get componenets api.__



**Dashboard - create component**
---
- Create a dashboard componenet.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/dashboard/manage \
  -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "container": "test", "days": "7","tag": { "cloud": "test", "compliances": [], "services": [] }}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/dashboard/manage
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "title" : "Title 1",
	"container": "azure_crawler_demo",
    "days": "7",
    "tag": {
        "cloud": "azure",
        "compliances": ["NIST 800"],
        "services": []
    }
}
```

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Dashboard configuration save successfully",
    "metadata": {},
    "status": 200
}
```
- **Explanation:**

    `Required Fields`
    - **container:** Pass the valid container name. You can get it from container list api.
    - **days:** Response will returns the stats till the number of days passed in request. Default value is 7.
    - **tag:** Pass the tags for filter the stats. You can get it from default tags api.



**Dashboard - delete component**
---
- Delete a dashboard componenet

**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/dashboard/manage -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "id": "6040ce75eb15c9f599e8cc9a" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/dashboard/manage
- **Method:** DELETE
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"id": "6040ce75eb15c9f599e8cc9a"
}
```

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Dashboard configuration save successfully",
    "metadata": {},
    "status": 200
}
```
- **Explanation:**

    `Required Fields`
    - **id:** Dashboard componenet id which you want to delete.
