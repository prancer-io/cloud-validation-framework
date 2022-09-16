**Jira Integration APIs**
===
Jira Integration APIs help in integrating Jira with Prancer at the collections level. The user can set project keys to view and create issues on the same.

**JiraIntegration API.**
---
  	This API is to initiate the integration by getting the details from the user. 

- **CURL Sample**

```curl 
curl -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST 'https://portal.prancer.io/prancer-customer1/api/jira?container=new_container' \
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
curl -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST 'https://portal.prancer.io/prancer-customer1/api/jira/issue?container=new_container&project=ip \'
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
               "self": "https://abinayamahalingam.atlassian.net/rest/api/2/component/10000", 
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
curl -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/jira/issue?container=new_container
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
    "container": "Container_Name",
    "Title" : "Title to be given on the issue",
    "Severity":"3",
    "Tags" : "[lables to be given by the user]"
  
    
}
```
- **Param for creating a multiple issues:**
 
``` json
{
    "container": "Container_Name",
    "Title" : "Title to be given on the issue",
    "Severity":"3",
    "Tags" : "[lables to be given by the user]",
    "Title1" : "Title to be given on the issue",
    "Severity1":"3",
    "Tags1" : "[lables to be given by the user]",
    "Title2" : "Title to be given on the issue",
    "Severity2":"3",
    "Tags2" : "[lables to be given by the user]"
  
    
}
```
- **Explanation:**
    `All of the fields are required.`
	  
     - **“Container”** : container name
     - **"Title"** : Title that has be provided as summary of the issue.
     - **"Severity"** : Severity that has to be set.
     - **"Tags"**: Lables that has to be given by the user.
 
 
- **Response for single issue creation:**
 

``` json
{
    "data": {},
    "results":{
        "id": "10034",
        "key","IP-17",
        "self":"https://abinayamahalingam.atlassian.net/rest/api/2/issue/10034"
    "error":""
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```



- **Response for bulk issues creation:**

``` json
{
    "data": {},
    "results":{
    "issues":[
     {
        "id": "10034",
        "key","IP-18",
        "self":"https://abinayamahalingam.atlassian.net/rest/api/2/issue/10035"
      },
        {
        "id": "10034",
        "key","IP-19",
        "self":"https://abinayamahalingam.atlassian.net/rest/api/2/issue/10036"
      },
        {
        "id": "10034",
        "key","IP-20",
        "self":"https://abinayamahalingam.atlassian.net/rest/api/2/issue/10037"
      }
     ]
    },
    "error":""
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```



