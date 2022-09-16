**Jira Integration APIs**
===
Jira Integration APIs help in integrating Jira with Prancer at the collections level. The user can set project keys to view and create issues on the same.

**JiraIntegration API.**
---
  	This API is to initiate the integration by getting the details from the user. 

- **CURL Sample**

```curl 
curl --location --request POST 'https://portal.prancer.io/prancer-customer1/api/jira' \
--header 'Authorization: Bearer <JWT Bearer Token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "https://accountname.atlassian.net",
    "username": "User_Email",
    "authtoken": "Authtoken",
    "organisation": "User_Organisation ",
    "project": "Project_Key",
    "severity" : "Severity",
    "container" : "Container_Name"
}'
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
curl --location --request POST 'https://portal.prancer.io/prancer-customer1/api/jira/issue' \
 --header 'Authorization: Bearer <JWT Bearer Token>' \
 --header 'Content-Type: application/json' \
 --data-raw '{
     "container" : "Container_Name",
     "project" : "Project_Key"
 }'
```

- **URL: https://portal.prancer.io/prancer-customer1/api/jira**
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
    "data": {"results": 
               "self": "https://accountname.atlassian.net/rest/api/2/component/{issueid}", 
                "id": "10000", 
               "name": "Active Directory", 
               "description": "Created by Jira Service Management"},
    "error":""
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
 
```

**POST method.**
---
   - The POST method is to create a single or multiple issues.  If the user provided a single data set, it creates a single issue. Creates bulk incase of multiple data sets. 
   
- **CURL Sample**

```curl
curl --location --request GET 'https://portal.prancer.io/prancer-customer1/api/jira/issue' \
 --header 'Authorization: Bearer <JWT Bearer Token>' \
 --header 'Content-Type: application/json' \
 --data-raw '{
     "container" : "Container_Name",
     "project" : "Project_Key"
}'

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
	"container":"Container_Name"
}
{
	"fields": {
		"summary": "Title for the issue",
		"issuetype": {
			"id": "Task/Epic/Story/Bug"
		},
		"project": {
			"key": "Project_key"
		},

		"labels": [
			"Labels",
			"blitz_test"
		]
	}
}
```
- **Param for creating a multiple issues:**
 
``` json
{
	"container":"Container_Name"
}
{
	"issueUpdates": [{
			"fields": {
				"summary": "Title for the issue",
				"issuetype": {
					"id": "Task/Epic/Story/Bug"
				},
				"project": {
					"key": "Project_key"
				},

				"labels": [
					"Labels",
					"blitz_test"
				]
			}
		},
		{
			"fields": {
				"summary": "Title for the issue",
				"issuetype": {
					"id": "Task/Epic/Story/Bug"
				},
				"project": {
					"key": "Project_key"
				},

				"labels": [
					"Labels",
					"blitz_test"
				]
			}
		}
	]
}
```



