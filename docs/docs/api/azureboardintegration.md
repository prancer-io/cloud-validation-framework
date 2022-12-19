**Azure board Integration APIs**
===
Azure board Integration APIs help in integrating Azure Board with Prancer at the collections level. The user can set project keys to view and create issues on the same.

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
        "azureboard": "not-integrated",
        "jira": "integrated"
    },
    "error": "",
    "error_list": [],
    "message": "Configuration data.",
    "metadata": {},
    "status": 200
}
```


**AzureBoard Integration API.**
---
  	This API is to initiate the integration by getting the details from the user. 

- **CURL Sample**

```curl 
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/azboard' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{
    "url": "https://dev.azure.com/<organisationname>",
    "container":"<container_name",
    "username":"<useremail>",
    "authtoken":"<access_token>",
    "project":"<project_name",
    "severity":"high",
    "organisation":"prancer"
}'
```

- **URL:** <https://portal.prancer.io/prancer-customer1/api/azboard>
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
	"url" : "User’s url to connect to Azureboard",
	"username" : "Email to AzureBoard login.",
	"authtoken" : "User's API token.",
	"organisation" : "Prancer",
	"project" : "Name of the project.",
	"severity" : "Severity that has to be set."

}
```
- **Explanation:**
    `All of the fields are required.`
    
 - **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Azure DevOps Board integration is sucessfull! Created the record",
    "metadata": {},
    "status": 200
}
```

**Get Project List API.**
---
  	This API is to list the projects available in the mentioned account. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/azboard/project?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/project**
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
        "projects": [
            "NextGen Cloud",
            "Project B",
            "Project Red"
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
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/azboard/status?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/status**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

``` json
    "container": "Container_Name",
    "workitem" : "workitemtype"
```

- **Explanation:**
	`All the fields are mandatory.`

- **Response:**

``` json
{
    "data": {
        "statuslist": [
            "To Do",
            "Doing",
            "Done"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Get Workitem type API.**
---
  	This API is to list the workitem types available for the user. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/azboard/witype?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/witype**
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
        "workitemtype": [
            "Issue",
            "Epic",
            "Issue",
            "Test Case",
            "Shared Steps",
            "Shared Parameter",
            "Code Review Request",
            "Code Review Response",
            "Feedback Request",
            "Feedback Response",
            "Test Plan",
            "Test Suite",
            "Task",
            "Code Review Request"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Get Workitem field API.**
---
  	This API is to list the fields available for workitem choosen. . 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/azboard/wifield?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/wifield**
- **Method: GET**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**

``` json
    "container": "Container_Name",
    "workitem" : "workitemtype"
```
- **Explanation:**
	`All the fields are mandatory.`

- **Response:**

``` json

    "data": {
        "workitemtype": [
            "Iteration Path",
            "Iteration ID",
            "External Link Count",
            "Iteration Level 7",
            "Iteration Level 6",
            "Iteration Level 5",
            "Iteration Level 4",
            "Iteration Level 3",
            "Iteration Level 2",
            "Iteration Level 1",
            "Area Level 7",
            "Area Level 6",
            "Area Level 5",
            "Area Level 4",
            "Area Level 3",
            "Area Level 2",
            "Area Level 1",
            "Team Project",
            "Parent",
            "Remote Link Count",
            "Comment Count",
            "Hyperlink Count",
            "Attached File Count",
            "Node Name",
            "Area Path",
            "Revised Date",
            "Changed Date",
            "ID",
            "Area ID",
            "Authorized As",
            "Title",
            "State",
            "Authorized Date",
            "Watermark",
            "Rev",
            "Changed By",
            "Reason",
            "Assigned To",
            "Work Item Type",
            "Created Date",
            "Created By",
            "Description",
            "History",
            "Related Link Count",
            "Tags",
            "Board Column",
            "Board Column Done",
            "Board Lane",
            "State Change Date",
            "Activated Date",
            "Activated By",
            "Closed Date",
            "Closed By",
            "Priority",
            "Stack Rank",
            "Effort",
            "Resolved By",
            "Resolved Date"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**AzureBoard Configuration API.**
---
  	This API has three methods,POST,GET and PUT. This API is to collect data from user input, save and fetch when required and also can be edited. The fields are, workitem,project,fields,status and container. The detailed explanation are below: 

**POST method.**
---
  	This method is to post the data received. 
	
- **CURL Sample**

``` curl 
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/azboard/configuration' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{
    "workitem": "Task","project": "<projectname","fields": "Priority","status": "To Do","container":"<container_name"}'
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/configuration**
- **Method: POST**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```	

- **Param:**

``` json
{
    "workitem": "Task",
    "project": "NextGen Cloud",
    "fields": "Priority",
    "status": "To Do",
    "container":"aws_tf_rds"
}
```
- **Explanation:**
    `All of the fields are required.`
    - **"workitem"**: Workitem type that the user wish to create,
    - **“project"** :Name of the project to create workitems,
    - **"fields"** : Workitem fields that has to be set while creating the workitems,
    - **"status"** : Status that has to be set initially,
    - **"container"** : Name of the container.

- **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Azure Board configuration as added.",
    "metadata": {},
    "status": 200
}
```

**GET method.**
---
  	This API is to fetch the data, which were set by the user. 

- **CURL Sample**

``` curl 
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/azboard/configuration?container=<container_name>' -H 'Authorization: Bearer <JWT Bearer Token>' 
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/configuration**
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
        "configid": "623af301f57e72ac44239d91",
        "container": "aws_tf_rds",
        "fields": "Priority",
        "project": "NextGen Cloud",
        "status": "To Do",
        "url": "https://dev.azure.com/wildkloud",
        "workitem": "Task"
    },
    "error": "",
    "error_list": [],
    "message": "Azureboard configuration as added.",
    "metadata": {},
    "status": 200
}
```
**PUT method.**
---
  	This method is to be able to edit the data. 
	
- **CURL Sample**

``` curl 
curl -X PUT 'https://portal.prancer.io/prancer-customer1/api/azboard/configuration' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{
    "workitem": "Task","project": "<projectname","fields": "Priority","status": "To Do","container":"<container_name"}'
```

- **URL: https://portal.prancer.io/prancer-customer1/api/azboard/configuration**
- **Method: PUT**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```	
- **Param:**

``` json
{
    "workitem": "Task",
    "project": "NextGen Cloud",
    "fields": "Priority",
    "status": "To Do",
    "container":"aws_tf_rds"
}
```
- **Explanation:**
    `The container name is required. All other fields are optional and can be used accordingly.`
    - **"workitem"**: Workitem type that the user wish to create,
    - **“project"** :Name of the project to create workitems,
    - **"fields"** : Workitem fields that has to be set while creating the workitems,
    - **"status"** : Status that has to be set initially,
    - **"container"** : Name of the container.

- **Response:**

``` json
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Azure Board configuration is modified.",
    "metadata": {},
    "status": 200
}
```
   
    
**AzureBoard Issues API.**
===
   This API has POST and PATCH methods.Creating a single or bulk workitems can be done with this API.


**POST method**
---
 - The POST method is to create a single workitem. 

- **CURL Sample**

```curl
curl -X POST 'https://portal.prancer.io/prancer-customer1/api/azboard/ticket/create/' -H 'Authorization: Bearer <JWT Bearer Token>'  --data-raw '{"container":"aws_cloud_specific", "pac_alert_ids": ["62b59d9105c659f779127df4", "62b9af0d0f8908d3969b39b6", "62b9af0d0f8908d3969b39f0"]}

```
 
- **URL: <https://portal.prancer.io/prancer-customer1/api/azboard/ticket/create>**
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
            "_links": {
                "fields": {
                    "href": "https://dev.azure.com/wildkloud/27ab1504-3280-41e1-920a-7a3685a75d6d/_apis/wit/fields"
                },
                "workItemType": {
                    "href": "https://dev.azure.com/wildkloud/27ab1504-3280-41e1-920a-7a3685a75d6d/_apis/wit/workItemTypes/Issue"
                }
            },
            "fields": {
                "Microsoft.VSTS.Common.Priority": 2,
                "Microsoft.VSTS.Common.StateChangeDate": "1753-01-01T00:00:00Z",
                "System.AreaPath": "NextGen Cloud",
                "System.ChangedBy": {
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/wildkloud/_apis/GraphProfile/MemberAvatars/aad.NjE4MjEyMGItOWNjMC03OTk0LTlkZTctNTVhZDM1MGY2NGI5"
                        }
                    },
                    "descriptor": "aad.NjE4MjEyMGItOWNjMC03OTk0LTlkZTctNTVhZDM1MGY2NGI5",
                    "displayName": "Abinaya Mahalingam",
                    "id": "6182120b-9cc0-6994-9de7-55ad350f64b9",
                    "imageUrl": "https://dev.azure.com/wildkloud/_apis/GraphProfile/MemberAvatars/aad.NjE4MjEyMGItOWNjMC03OTk0LTlkZTctNTVhZDM1MGY2NGI5",
                    "uniqueName": "Abinaya.Mahalingam@prancer.io",
                    "url": "https://spsprodcus5.vssps.visualstudio.com/A08567b08-9a09-4fe8-a99f-6275a2f140da/_apis/Identities/6182120b-9cc0-6994-9de7-55ad350f64b9"
                },
                "System.CreatedBy": {
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/wildkloud/_apis/GraphProfile/MemberAvatars/aad.NjE4MjEyMGItOWNjMC03OTk0LTlkZTctNTVhZDM1MGY2NGI5"
                        }
                    },
                    "descriptor": "aad.NjE4MjEyMGItOWNjMC03OTk0LTlkZTctNTVhZDM1MGY2NGI5",
                    "displayName": "Abinaya Mahalingam",
                    "id": "6182120b-9cc0-6994-9de7-55ad350f64b9",
                    "imageUrl": "https://dev.azure.com/wildkloud/_apis/GraphProfile/MemberAvatars/aad.NjE4MjEyMGItOWNjMC03OTk0LTlkZTctNTVhZDM1MGY2NGI5",
                    "uniqueName": "Abinaya.Mahalingam@prancer.io",
                    "url": "https://spsprodcus5.vssps.visualstudio.com/A08567b08-9a09-4fe8-a99f-6275a2f140da/_apis/Identities/6182120b-9cc0-6994-9de7-55ad350f64b9"
                },
                "System.IterationPath": "NextGen Cloud",
                "System.Reason": "Added to backlog",
                "System.State": "To Do",
                "System.TeamProject": "NextGen Cloud",
                "System.WorkItemType": "Issue"
            },
            "url": "https://dev.azure.com/wildkloud/27ab1504-3280-41e1-920a-7a3685a75d6d/_apis/wit/workItems"
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**PATCH method-For creating bulk issues**
---
     
- **CURL Sample**

```curl
curl -X PATCH 'https://portal.prancer.io/prancer-customer1/api/azboard/issue' -H 'Authorization: Bearer <JWT Bearer Token>' --data-raw '{"container": "aws_tf_rds","issues": [{"title": "Bulk issue creation 3"},{"title": "Bulk issue creation 4"},{"title": "Bulk issue creation 10"},{"title": "Bulk issue creation 12 "}]}'
```
 
- **URL: <https://portal.prancer.io/prancer-customer1/api/azboard/issue>**
- **Method:PATCH**
- **Header:**

``` code
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>

```

- **Param for creating a multiple issues:**
 
``` json
{
    "container": "aws_tf_rds",
    "issues": [
        {
            "title": "Bulk issue creation 3"
        },
        {
            "title": "Bulk issue creation 4"
        },
        {
            "title": "Bulk issue creation 10"
        },
        {
            "title": "Bulk issue creation 12 "
        }
    ]
}
```

- **Explanation:**
	`The Container and issues fields are mandatory.`


- **Response:**

``` json
{
    "data": {
        "results": {
            "count": 4,
            "value": [
                {
                    "body": "{\"id\":81,\"rev\":1,\"fields\":{\"System.AreaPath\":\"Project B\",\"System.TeamProject\":\"Project B\",\"System.IterationPath\":\"Project B\",\"System.WorkItemType\":\"Task\",\"System.State\":\"To Do\",\"System.Reason\":\"New task\",\"System.CreatedDate\":\"2022-11-09T11:12:44.217Z\",\"System.CreatedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.ChangedDate\":\"2022-11-09T11:12:44.217Z\",\"System.ChangedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.CommentCount\":0,\"System.Title\":\"Bulk issue creation 3\",\"Microsoft.VSTS.Common.StateChangeDate\":\"2022-11-09T11:12:44.217Z\",\"Microsoft.VSTS.Common.Priority\":2},\"_links\":{\"self\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/81\"},\"workItemUpdates\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/81/updates\"},\"workItemRevisions\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/81/revisions\"},\"workItemComments\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/81/comments\"},\"html\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_workitems/edit/81\"},\"workItemType\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_apis/wit/workItemTypes/Task\"},\"fields\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/fields\"}},\"url\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/81\"}",
                    "code": 200,
                    "headers": {
                        "Content-Type": "application/json; charset=utf-8"
                    }
                },
                {
                    "body": "{\"id\":82,\"rev\":1,\"fields\":{\"System.AreaPath\":\"Project B\",\"System.TeamProject\":\"Project B\",\"System.IterationPath\":\"Project B\",\"System.WorkItemType\":\"Task\",\"System.State\":\"To Do\",\"System.Reason\":\"New task\",\"System.CreatedDate\":\"2022-11-09T11:12:44.217Z\",\"System.CreatedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.ChangedDate\":\"2022-11-09T11:12:44.217Z\",\"System.ChangedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.CommentCount\":0,\"System.Title\":\"Bulk issue creation 4\",\"Microsoft.VSTS.Common.StateChangeDate\":\"2022-11-09T11:12:44.217Z\",\"Microsoft.VSTS.Common.Priority\":2},\"_links\":{\"self\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/82\"},\"workItemUpdates\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/82/updates\"},\"workItemRevisions\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/82/revisions\"},\"workItemComments\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/82/comments\"},\"html\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_workitems/edit/82\"},\"workItemType\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_apis/wit/workItemTypes/Task\"},\"fields\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/fields\"}},\"url\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/82\"}",
                    "code": 200,
                    "headers": {
                        "Content-Type": "application/json; charset=utf-8"
                    }
                },
                {
                    "body": "{\"id\":83,\"rev\":1,\"fields\":{\"System.AreaPath\":\"Project B\",\"System.TeamProject\":\"Project B\",\"System.IterationPath\":\"Project B\",\"System.WorkItemType\":\"Task\",\"System.State\":\"To Do\",\"System.Reason\":\"New task\",\"System.CreatedDate\":\"2022-11-09T11:12:44.217Z\",\"System.CreatedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.ChangedDate\":\"2022-11-09T11:12:44.217Z\",\"System.ChangedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.CommentCount\":0,\"System.Title\":\"Bulk issue creation 10\",\"Microsoft.VSTS.Common.StateChangeDate\":\"2022-11-09T11:12:44.217Z\",\"Microsoft.VSTS.Common.Priority\":2},\"_links\":{\"self\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/83\"},\"workItemUpdates\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/83/updates\"},\"workItemRevisions\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/83/revisions\"},\"workItemComments\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/83/comments\"},\"html\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_workitems/edit/83\"},\"workItemType\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_apis/wit/workItemTypes/Task\"},\"fields\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/fields\"}},\"url\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/83\"}",
                    "code": 200,
                    "headers": {
                        "Content-Type": "application/json; charset=utf-8"
                    }
                },
                {
                    "body": "{\"id\":84,\"rev\":1,\"fields\":{\"System.AreaPath\":\"Project B\",\"System.TeamProject\":\"Project B\",\"System.IterationPath\":\"Project B\",\"System.WorkItemType\":\"Task\",\"System.State\":\"To Do\",\"System.Reason\":\"New task\",\"System.CreatedDate\":\"2022-11-09T11:12:44.217Z\",\"System.CreatedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.ChangedDate\":\"2022-11-09T11:12:44.217Z\",\"System.ChangedBy\":\"Abinaya Mahalingam <Abinaya.Mahalingam@prancer.io>\",\"System.CommentCount\":0,\"System.Title\":\"Bulk issue creation 12 \",\"Microsoft.VSTS.Common.StateChangeDate\":\"2022-11-09T11:12:44.217Z\",\"Microsoft.VSTS.Common.Priority\":2},\"_links\":{\"self\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/84\"},\"workItemUpdates\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/84/updates\"},\"workItemRevisions\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/84/revisions\"},\"workItemComments\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/84/comments\"},\"html\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_workitems/edit/84\"},\"workItemType\":{\"href\":\"https://dev.azure.com/wildkloud/618632a1-db64-4649-ae0e-ae1524eec7a0/_apis/wit/workItemTypes/Task\"},\"fields\":{\"href\":\"https://dev.azure.com/wildkloud/_apis/wit/fields\"}},\"url\":\"https://dev.azure.com/wildkloud/_apis/wit/workItems/84\"}",
                    "code": 200,
                    "headers": {
                        "Content-Type": "application/json; charset=utf-8"
                    }
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



