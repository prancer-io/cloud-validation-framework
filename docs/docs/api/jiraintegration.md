**Jira Integration APIs**
===
Jira Integration APIs help in integrating Jira with Prancer at the collections level. The user can set project keys to view and create issues on the same.

**JiraIntegration API.**
---
  	This API is to initiate the integration by getting the details from the user. 

- **CURL Sample**

```curl 
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira' -H 'Authorization: Bearer <JWT Bearer Token>' -d '{"url": "https://accountname.atlassian.net","username": "User_Email","authtoken": "Authtoken","organisation": "User_Organisation ","project": "Project_Key",  "severity" : "Severity","container" : "Container_Name"}'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/jira>
- **Method:** POST
- **Header:**
  
``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```


- **Param:**

``` json
{
        "container":"Container Name"
	"url" : "https://accounname.atlassian.net",
	"username" : "Email to Jira login.",
	"authtoken" : "User's API token.",
	"organisation" : "Prancer",
	"project" : "Key of the project that has to be linked.",
	"severity" : "Severity that has to be set."

}
```
- **Explanation:**
    `All of the fields are required.`
    
    - **"container"**: Name of the container,
    - **“url"** : Jira URL of the user,
    - **"username"** : username for Jira URL,
    - **"authtoken"** : authtoken for Jira URL,
    - **"organisation"** : organisation of the user in Jira account,
    - **"project"** : project key to Jira,
    - **"severity"** : severity to be set.

- **Response:**

``` json
{
    "data": {},
    "error":""
    "error_list": [],
    "message": "Jira Integration is successful!Created the record.",
    "metadata": {},
    "status": 200
}
```

**JiraIssues API.**
===
   This API has  GET and POST methods. A user can list the issues available in the project he mentions. He can create a single or bulk issues with the POST method.

**GET method.**
---
   The GET method is to fetch all the issues that are in the given project key.
- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/issue' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/issue**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

``` json
{
    "container": "Container_Name",
    "project": "Project_Key"
}
```

- **Explanation:**
	`The Container field is mandatory. The Project field can be optional`

- **Response:**

``` json
{
    "data": {
        "results": [
            {
                "description": "Created by Jira Service Management",
                "id": "10000",
                "isAssigneeTypeValid": false,
                "name": "Active Directory",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10000"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10001",
                "isAssigneeTypeValid": false,
                "name": "Analytics and Reporting Service",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10001"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10002",
                "isAssigneeTypeValid": false,
                "name": "Billing Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10002"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10003",
                "isAssigneeTypeValid": false,
                "name": "Cloud Storage Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10003"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10004",
                "isAssigneeTypeValid": false,
                "name": "Data Center Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10004"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10005",
                "isAssigneeTypeValid": false,
                "name": "Email and Collaboration Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10005"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10006",
                "isAssigneeTypeValid": false,
                "name": "Financial Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10006"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10007",
                "isAssigneeTypeValid": false,
                "name": "HR Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10007"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10008",
                "isAssigneeTypeValid": false,
                "name": "Intranet",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10008"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10009",
                "isAssigneeTypeValid": false,
                "name": "Jira",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10009"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10010",
                "isAssigneeTypeValid": false,
                "name": "Office Network",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10010"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10011",
                "isAssigneeTypeValid": false,
                "name": "Payroll Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10011"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10012",
                "isAssigneeTypeValid": false,
                "name": "Printers",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10012"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10013",
                "isAssigneeTypeValid": false,
                "name": "Public Website",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10013"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10014",
                "isAssigneeTypeValid": false,
                "name": "VPN Server",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10014"
            },
            {
                "description": "Created by Jira Service Management",
                "id": "10015",
                "isAssigneeTypeValid": false,
                "name": "Webstore Purchasing Services",
                "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10015"
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
**POST method**
---
 - The POST method is to create a single or multiple issues.  If the user provided a single data set, it creates a single issue. Creates bulk incase of multiple data sets. 


**POST method-For creating a single issue**
---

- **CURL Sample**

```curl
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/issue' -H 'Authorization: Bearer <JWT Bearer Token>' -d {"container":"new_container","project":"IP","issues":{"title" : "title for the issue","tags"["test","label"]}}

```
 
- **URL: <https://portal.prancer.io/prancer-customer1/api/jira/issue>**
- **Method:POST**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>

```

 - **Param for creating a single issue:**
 
``` json
{
    "container":"new_container",
    "project":"IP",

    "issues":
     {
         "title" : "title for the issue",
         "tags":["test","label"]
     }
}
```
- **Response:**

```json
{
    "data": {
        "results": {
            "id": "10061",
            "key": "IP-44",
            "self": "https://abinayamahalingam.atlassian.net/rest/api/2/issue/10061"
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**POST method-For creating bulk issues**
---
  
   
- **CURL Sample**

```curl
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/issue' -H 'Authorization: Bearer <JWT Bearer Token>' -d {"container":"new_container","project":"IP","issues":{"title" : "title for the issue","tags"["test","label"]},"issues1":{"title" : "title for the issue1","tags":["test","label"]}}

```
 
- **URL: <https://portal.prancer.io/prancer-customer1/api/jira/issue>**
- **Method:POST**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>

```

- **Param for creating a multiple issues:**
 
``` json
{
    "container":"new_container",
    "project":"IP",

    "issues":
     {
         "title" : "title for the issue",
         "tags":["test","label"]
     },
    
     "issues1":
     {
         "title" : "title for the issue1",
         "tags":["test","label"]
     }
     
}
```

- **Response:**

``` json
{
    "data": {
        "results": {
            "errors": [],
            "issues": [
                {
                    "id": "10055",
                    "key": "IP-38",
                    "self": "https://abinayamahalingam.atlassian.net/rest/api/2/issue/10055"
                },
                {
                    "id": "10056",
                    "key": "IP-39",
                    "self": "https://abinayamahalingam.atlassian.net/rest/api/2/issue/10056"
                }
            ]
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```



