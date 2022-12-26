**Jira Integration APIs**
===
Jira Integration APIs help in integrating Jira with Prancer at the collections level. The user can set project keys to view and create issues on the same.

**Collection Configuration API.**
---
  	This API is to check the existing integrations status. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/collection/configuration?container=<container_name' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/collection/configuration**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

``` json
    "container": "Container_Name",

```

- **Explanation:**
	`The Container field is mandatory.`

- **Response:**

``` json
{
    "data": {
        "jira": "integrated"
    },
    "error": "",
    "error_list": [],
    "message": "Configuration data.",
    "metadata": {},
    "status": 200
}
```


**Jira Integration API.**
---
  	It contains two method POST and DELETE. POST API is to initiate the integration by getting the details from the user and DELETE API for deleting the existing Jira integration if any. 

**POST method.**
---
API to initiate the Jira integration

- **CURL Sample**

```curl 
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/integration/' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{"url": "https://accountname.atlassian.net","username": "User_Email","authtoken": "Authtoken","organisation": "User_Organisation ","project": "Project_Key",  "severity" : "Severity","container": "Container_Name"}'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/jira/integration/>
- **Method:** POST
- **Header:**
  
``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```


- **Param:**

``` json
{
    "container":"Container Name",
	"url" : "https://accounname.atlassian.net",
	"username" : "Email to Jira login.",
	"authtoken" : "User's API token.",
	"organisation" : "Prancer",
	"project" : "Project Name",
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
    "message": "Jira integration is sucessfull! Created a new record.",
    "metadata": {},
    "status": 200
}
```

**DELETE method.**
---
API to delete the existing Jira integration

- **CURL Sample**

```curl 
curl -X DELETE 'https://portal.prancer.io/prancer-customer1/api/jira/integration/?container=aws_cloud_specific' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw ''
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/jira/integration/>
- **Method:** DELETE
- **Header:**
  
``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```


- **Param:**

```
    "container":"Container Name"
```
- **Explanation:**
    `The Container field is mandatory.`
    - **container**: Name of the container

- **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Jira configuration deleted successfully.",
    "metadata": {},
    "status": 200
}
```

**Get Projects API.**
---
  	This API is to list all the projects available. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/project/?url=https://accounname.atlassian.net/&username=<user_email>&authtoken=<token>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/project/**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

```   
    url : https://accounname.atlassian.net/.
	username : Email to Jira login.
	authtoken : User's API token.

```

- **Explanation:**
	`All of the fields are required.`
    - **url** : Jira URL of the user.
    - **username** : username for Jira URL.
    - **authtoken** : authtoken for Jira URL.

- **Response:**

``` json
{
    "data": {
        "projects": [
            "API"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Get Issuetypes API.**
---
  	This API is to list the issue types available. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/issuetype/?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/issuetype/**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

``` 
    "container": "Container_Name"
```

- **Explanation:**
	`The Container field is mandatory.`

- **Response:**

``` json
{
    "data": {
        "issuetypes": [
            "Task",
            "Epic",
            "Subtask"
       ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```
**Get Status API.**
---
  	This API is to list the statuses available for the user. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/status/?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/status/**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

``` json
    "container": "Container_Name",

```

- **Explanation:**
	`The Container field is mandatory.`

- **Response:**

``` json
{
    "data": {
        "status": [
            "IN_PROGRESS",
            "DONE",
            "TODO"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```
**Get Labels API.**
---
  	This API is to list the labels available for the user. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/label/?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/label/**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

``` json
    "container": "Container_Name",

```

- **Explanation:**
	`The Container field is mandatory.`

- **Response:**

``` json
{
    "data": {
        "Labels": [
            "blitz_test",
            "bugfix",
            "cspm",
            "iac",
            "label",
            "new_release",
            "pentest",
            "sample-space",
            "test"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Jira Configuration API.**
---
  	This API has three methods, POST, GET and PUT. This API is to collect data from user input, save it and fetch when required and also can be edited. The fields are, issuetype, openstatus, closestatus, labels. The detailed explanation are below: 

**POST method.**
---
  	This method is to post the data received. 
	
- **CURL Sample**

``` curl 
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/configuration/' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw {
    "issuetype": "Task","openstatus": "TODO","closestatus": "InProgress","labels": ["testfix"],"container":<container_name}'
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/configuration/**
- **Method: POST**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```	

- **Param:**

``` json
{
    "issuetype": "Task",
    "openstatus": "TODO",
    "closestatus": "DONE",
    "labels": ["testjira", "IAC"],
    "container":"container_name"
}
```
- **Explanation:**
    `All of the fields are required.`
    - **"issuetype"**: Issue type as set by the user,
    - **“openstatus"** : Openstatus value as set by the user,
    - **"closestatus"** : Closestatus value as set by the user,
    - **"labels"** : Label values as set by the user,
    - **"container"** : Name of the container.

- **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Jira configuration is added.",
    "metadata": {},
    "status": 200
}
```

**GET method.**
---
  	This API is to fetch the data, which were set by the user. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/configuration/?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/configuration/**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

```
    "container": "Container_Name",
```
- **Explanation:**
	`The Container field is mandatory.`

- **Response:**

``` json
{
    "data": {
        "closestatus": "DONE",
        "configid": "632ad6c37dd27c6b720fb751",
        "container": "new_container",
        "issuetype": "Task",
        "labels": ["testjira", "IAC"],
        "openstatus": "TODO",
        "project": "INT",
        "url": "https://abinayamahalingam.atlassian.net"
    },
    "error": "",
    "error_list": [],
    "message": "Jira configuration as added.",
    "metadata": {},
    "status": 200
}
```
**PUT method.**
---
  	This method is to be able to edit the data. 
	
- **CURL Sample**

``` curl 
curl -X PUT 'https://portal.prancer.io/prancer-customer1/api/jira/configuration/' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw {
    "issuetype": "Task","openstatus": "TODO","closestatus": "DONE","labels": ["testfix"],"container":<container_name>}'
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/configuration/**
- **Method: PUT**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```	

- **Param:**

``` json
{
    "issuetype": "Task",
    "openstatus": "TODO",
    "closestatus": "DONE",
    "labels": ["testjira"],
    "container":"new_container"
}
```
- **Explanation:**
    `The container field is required. All other fields are optional.`
    - **"issuetype"**: Issue type as set by the user from the specified project,
    - **“openstatus"** : Openstatus value as set by the user from the specified project,
    - **"closestatus"** : Closestatus value as set by the user from the specified project,
    - **"labels"** : Label values as set by the user,
    - **"container"** : Name of the container.

- **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Jira configuration is modified.",
    "metadata": {},
    "status": 200
}
```


    
    
**JiraIssues API.**
===
   This API has  GET and POST methods. A user can list the issues available in the project mentioned. Creating a single or bulk issues can be done with the POST method.

**GET method.**
---
   The GET method is to fetch all the issues that are in the given project key.
- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/jira/ticket/create/?container=<container_name>&project=<project_key>'' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira/ticket/create/**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**

``` json
    "container": "Container_Name",
    "project": "Project_Key"
```

- **Explanation:**
	`The Container field is mandatory. The Project field can be optional.`

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
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/ticket/create/' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{"container":"aws_cloud_specific", "pac_alert_ids": ["62b59d9105c659f779127df4", "62b9af0d0f8908d3969b39b6", "62b9af0d0f8908d3969b39f0"]}

```
 
- **URL: <https://portal.prancer.io/prancer-customer1/api/jira/ticket/create/>**
- **Method:POST**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>

```

 - **Param for creating a single issue:**
 
``` json
{
    "container":"aws_cloud_specific",
    "pac_alert_ids": [
        "62b59d9105c659f779127df4",
        "62b9af0d0f8908d3969b39b6",
        "62b9af0d0f8908d3969b39f0"
        ]
}
```

- **Explanation:**

    `Required Fields`

    - **container:** Name of the cloud container for which you want want to create Jira tickets.

    **For Creating Ticket for Infra findings:**
    - **result_id:** Result id of the infra output.
    - **output_id:** Output id of the infra output.
    - **test_id:** Test id of the failed testcase of the infra output.
    - **snapshot_id:** Snapshot id of the failed testcase in infra output.
    
    **For Creating Ticket for App findings:**
    - **pac_alert_ids:** Alert id list for which ticket needs to be created.


    `Optional Fields`

    - **matching_testcase:** : Valid values are `true` and `false`. To create the a single ticket for all similar failed testcases on the Infra findings if `true`


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
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/issue' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{
    "container":"new_container",
    "project":"IP","issues":[{ "title" : "title for the issue","tags":["test","label"]},{ "title" : "title for the issue1","tags":["test","label"]}]}'
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
    "issues":[
     {
         "title" : "title for the issue",
         "tags":["test","label"]
    },
    {
         "title" : "title for the issue1",
         "tags":["test","label"]
    }]
     
}
```

- **Explanation:**
	`The Container and issues fields are mandatory. The title in the issues is a required field.Tags and issuetype are optional.The Project field can be optional.`


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



