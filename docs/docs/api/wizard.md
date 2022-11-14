**Wizard APIs**
===

- Wizard is single step process to create connector and testcases for github, azure, aws and google providers.

** Google Wizard Redirection API.**
---
- API to get the google redirect URL for dev, qa or prod google oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/wizardredirect?provider=GCP&state=customer1"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardredirect
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: GCP (or gcp, google)
- state: <customer>
```

**Response:**
```
{
  "data": {
    "data": {
      "provider": "GCP",
      "url": "https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/cloud-platform&include_granted_scopes=true&response_type=code&state=customer1&redirect_uri=https%3A//portaldev.prancer.io/callback/gcp&client_id=785412359856-9667ctjtbp7fbijb00kvblaotjd50d0f.apps.googleusercontent.com"
     },
     "error": null
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Google Wizard Provider API.**
---
- API to get the google projects in the account the permission has been granted.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "GCP", "state": "customer1", "code": "<GOOGLE ACCESS CODE>"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: GCP (or gcp, google)
- state: <customer>
- code: <code passed by google's oauth app>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      {
        "projectId": "<GCP Project Id>",
        "projectName": "<GCP Project Name>"
      },
      {
        "projectId": "<GCP Project Id>",
        "projectName": "<GCP Project Name>"
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

** Github Wizard Redirection API.**
---
- API to get the github redirect URL for dev, qa or prod github oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/wizardredirect?provider=github&state=customer1"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardredirect
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: github
- state: <customer>
```

**Response:**
```
{
  "data": {
    "data": {
      "provider": "github",
      "url": "https://github.com/login/oauth/authorize?state=customer1&client_id=85df68d715d9c49877"
     },
     "error": null
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Gitlab Wizard Redirection API.**
---
- API to get the gitlab redirect URL for dev, qa or prod gitlab oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/wizardredirect?provider=gitlab&state=customer1"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardredirect
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: gitlab
- state: <customer>
```

**Response:**
```
{
  "data": {
    "data": {
      "provider": "gitlab",
      "url": "https://gitlab.com/oauth/authorize?client_id=714be9e110cc8a4cb5b**&redirect_uri=https%3A%2F%2Fportaldev.prancer.io%2Fcallback%2Fgitlab&response_type=code&state=customer1&scope=read_api%20write_repository"
     },
     "error": null
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```
** Bitbucket Wizard Redirection API.**
---
- API to get the bitbucket redirect URL for dev, qa or prod github oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/wizardredirect?provider=bitbucket&state=customer1"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardredirect
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: bitbucket
- state: <customer>
```

**Response:**
```
{
    "data": {
        "data": {
            "provider": "bitbucket",
            "url": "https://bitbucket.org/site/oauth2/authorize?client_id=TVXMH4WGZhUttqa5mw&response_type=code&state=None"
        },
        "error": null
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```
** Github Wizard provider API.**
---
- API to get the github list of repositories using github oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "git", "type": "github", "state": "customer1", "code": "<Github Access Code>"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: git
- type: github
- state: <customer>
- code: <code in the callback from github>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      "git@github.com:<gituser>/<repository_name>.git",
      "git@github.com:<organization>/<repository_name>.git",
    ]
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```
** Gitlab Wizard provider API.**
---
- API to get the gitlab list of repositories using gitlab oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "git", "type": "gitlab", "state": "customer1", "code": "<gitlab Access Code>"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: git
- type: gitlab
- state: <customer>
- code: <code in the callback from gitlab>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      "git@gitlab.com:<gituser>/<repository_name>.git",
      "git@gitlab.com:<organization>/<repository_name>.git",
    ]
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```
** Bitbucket Wizard provider API.**
---
- API to get the bitbucket list of repositories using bitbucket oauth app. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "git", "type": "bitbucket", "state": "customer1", "code": "<bitbucket Access Code>"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: git
- type: bitbucket
- state: <customer>
- code: <code in the callback from bitbucket>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      "git@bitbucket.com:<gituser>/<repository_name>.git",
      "git@bitbucket.com:<organization>/<repository_name>.git",
    ]
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Azure Wizard provider API.**
---
- API to get the azure subscriptions API.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "azure", "tenant": "<Azure Tenant Id>", "client_id": "<Azure Client Id>", "client_secret": "<Azure Client Secret>", "customer": "customer1"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: azure
- tenant: <azure tenant Id>
- client_id: <azure client Id>
- client_secret: <azure client secret>
- customer: <customer_id>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      {
        "name": "<subscription_name>",
        "subscription": "<subscription_id>"
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

** Aws Wizard provider API.**
---
- API to get the aws accounts API.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "aws", "accessKey": "<AWS accesskey>", "accessSecret": "<AWS Secret Key>"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: azure
- accessKey: <access key of the aws account>
- accessSecret: <access secret for the key>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      {
        "accountId": "<AWS Account Id>",
        "name": "<AWS Account Name>",
        "region": "<region like us-east-2>"
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

** Gitlab Wizard Branch list API.**
---
- API to get the gitlab list of branches in the respository. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "'http://localhost:8080/api/wizard/branches?provider=gitlab&repo=git@gitlab.com:<gituser>/<repository_name>.git'"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizard/branches
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: gitlab
- repo: <git@gitlab.com:<gituser>/<repository_name>.git>
```

**Response:**
```
{
    "data": {
        "error": null,
        "results": [
            "main",
            "testbranch1",
            "testbranch2"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

** Bitbucket Wizard Branch list API.**
---
- API to get the bitbucket list of branches in the respository. 

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "'http://localhost:8080/api/wizard/branches?provider=bitbucket&repo=git@bitbucket.com:<gituser>/<repository_name>.git'"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizard/branches
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: bitbucket
- repo: <git@bitbucket.com:<gituser>/<repository_name>.git>
```

**Response:**
```
{
    "data": {
        "error": null,
        "results": [
            "main",
            "testbranch1",
            "testbranch2"
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

** Wizard Status API.**
---
- API to get the wizard creation status for a container.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/wizardstatus?name=git_azure_customer1_1617571294420"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardstatus
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- name: <name of the collection>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      "Creating wizard...", 
      "Creating azure connector.....Done", 
      "Creating git connector to get compliance tests.....Done", 
      "Creating resources for the subscription.....Done", 
      "Creating resource compliance for the subscription.....Done", 
      "Creating master resource for the subscription.....Done", 
      "Creating master resource complaince for the subscription.....Done", 
      "Updating resources for the collection.....Done", 
      "Successfully added complaince tests for the subscription."
    ],
    "wizardstatus": 0
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

**Failed response if container not created using wizard:**
```
{
  "data": {
    "error": null,
    "results": [
      "Did not find any messages for this wizard!"
    ],
    "wizardstatus": 0
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Google Wizard create API.**
---
- API to create google collection for a project.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizard"  -d'{"customer":"customer1"    ,"provider":"GCP","projects":[{"projectName":"<GCP Project Name>","projectId":"<GCP Project Id>","checked":true}],"name":"<Collection Name like google-test2>","remediate":true}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizard
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: GCP (or gcp, google)
- customer: <customer>
- projectName: <Name of the project>
- projectId: <id of the project>
- name: <name of the collection>
- remediate: true
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": {
      "name": "google-test2"
    }
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

**Failed Response:**
```
{
  "data": {
    "error": "google-test2 exists, cannot create container with the same name!",
    "results": {},
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Kubernetes Wizard create API.**
---
- API to create kubernetes collection for a namespace.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizard"  -d'{"customer":"customer1","provider":"kubernetes", "clusterName": "<Cluster Name>", "clusterUrl": "<cluster url>", "secret": "<Secret Token>", "namespaces": [{"name": "default", "namespaceId": "<namespace_id>"}], "name": "< collection name like kube-test>", "remediate": true}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizard
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: kubernetes
- customer: <customer>
- clusterName: <Name of the cluster>
- clusterUrl: <URL of the cluster>
- secret: <bearer token to connect to the URL>
- name: <name of the collection>
- remediate: true/false
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": {
      "name": "kube-test"
    }
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

**Failed Response:**

```
{
  "data": {
    "error": "kube-test exists, cannot create container with the same name!",
    "results": {},
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Kubernetes Wizard Provider API.**
---
- API to get the kubernetes namespaces in the api server.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizardproviders" -d'{"provider": "kubernetes", "customer": "customer1", "clusterName": "<Cluster Name>", "clusterUrl": "<Cluster Url>", "secret": "<Secret Token>"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: kubernetes
- customer: <customer>
- clusterName: <Name of the cluster>
- clusterUrl: <URL of the cluster>
- secret: <bearer token to connect to the URL>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      {
        "name": "<namespace name>",
        "namespaceId": "<namespace id>"
      },
      {
        "name": "<namespace name>",
        "namespaceId": "<namespace id>"
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

**Wizard Creation - Creation of a wizard for cloud provider.**
---
- API to create a wizard for the cloud provider

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST https://portal.prancer.io/prancer-customer1/api/wizard -d'{"customer": "customer1", "tenantId": "<tenant-id>", "clientId": "<client Id>", "subscriptionName": "<subscription name>", "subscriptionId": "<subscription Id>", "provider": "azure"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/wizard
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - space-id: 101
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- provider: azure
- tenant: <tenant-id>
- subscriptionId: <Subscription Id>
- subscriptionName: <Subscription name>
- client_id: <client-id of the spn>
- customer: <customer name viz. customer1>
```

**Response:**
```
{
   "message" : "",
   "status" : 200,
   "metadata" : {},
   "error" : "",
   "data" : {
      "results" : {
         "name" : "git_azure_customer1_1613610032528"
      },
      "error" : null
   }
}
```
