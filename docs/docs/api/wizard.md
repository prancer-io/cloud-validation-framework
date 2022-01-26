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

** Wizard Status API - container created using wizard.**
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

** Wizard Status API - container not created using wizard.**
---
- API to get the wizard creation status for a container which was not created using wizard.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/wizardstatus?name=git_azure_customer1_161757129442"
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

** Wizard Collection check  API - collection existence check.**
---
- API to check if a collection exists in the system.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/collection?collection=git_azure_customer1_1617571294420"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection
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
    "exists": true
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```

** Wizard Collection check  API - collection existence check.**
---
- API to check if a collection exists in the system.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-customer1/api/collection?collection=git_azure_customer1_16175712944"
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/collection
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
    "exists": false
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

** Google Wizard create API.**
---
- API to create google collection which is already present.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizard"  -d'{"customer":"customer1"    ,"provider":"GCP","projects":[{"projectName": "<GCP Project Name>","projectId": "<GCP Project Id>","checked":true}],"name":"google-test2","remediate":true}'
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

** Kubernetes Wizard create API.**
---
- API to create Kubernetes collection which is already present.

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST "https://portal.prancer.io/prancer-customer1/api/wizard"  -d'{"customer":"customer1","provider":"kubernetes", "clusterName": "<cluster name>", "clusterUrl": "<cluster url>", "secret": "<Secret Token>", "namespaces": [{"name": "default", "namespaceId": "<namespace Id>"}], "name": "< collection name like kube-test>", "remediate": true}'
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

**Wizard Redirect API for google - Wizard Redirect API for a provider like google.**
---
- API to get the redirect URL for google provider

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" https://portal.prancer.io/prancer-customer1/api/wizardredirect?provider=google&state=customer1
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
- provider: google
- state: <customer1, customer2>
```

**Response:**
```
{
  "data": {
    "data": {
      "provider": "google",
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


**Wizard provider API for google - Wizard provider API for a provider viz. google.**
---
- API to get the provider URL for google projects

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST https://portal.prancer.io/prancer-customer1/api/wizardproviders -d'{"provider": "google", "code": "<callback received>", "customer": "customer1"}'
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
- customer: <customer1>
- provider: google
- code: <callback receivedi code>
```

**Response:**
```
{
  "data": {
    "results": [{"projectName": "Abcd1", "projectId": "12df34"]
    "error": null
  },
  "error": "",
    "error_list": [],
  "message": "",
  "metadata": {},
  "status": 200
}
```



**Wizard Redirect API for git - Wizard Redirect API for a provider like github.**
---
- API to get the redirect URL for github provider

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" https://portal.prancer.io/prancer-customer1/api/wizardredirect?provider=github&state=customer1
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
- state: <customer1, customer2>
```

**Response:**
```
{
  "data": {
    "data": {
      "provider": "github",
      "url": "https://github.com/login/oauth/authorize?state=customer1&client_id=0f19f9f77715d9c49466"
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

**Wizard Provider - List of subscriptions for Azure, list of projects for aws or google**
---
- API to get the list of subscriptions or projects or accounts to pick for creating connector and configuration files.

**CURL Sample**
```
curl -H "space-id: 101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST https://portal.prancer.io/prancer-customer1/api/wizardproviders -d'{"provider": "azure", "tenant": "<tenant-id>", "name": "<spn-name>", "client_id": "<client-key>", "client_secret": "<client secret for spn>"}'
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
- tenant: <tenant-id>
- name: <spn-name>
- client_id: <client-id of the spn>
- client_secret: <client secret of the spn>
```

**Response:**
```
{
   "message" : "",
   "error" : "",
   "metadata" : {},
   "status" : 200,
   "data" : {
      "results" : [
         {
            "name" : "<subscription name>",
            "subscription" : "<subscription id>"
         }
      ],
      "error" : null
   }
}
```

- **URL git:** https://portal.prancer.io/prancer-customer1/api/wizardproviders
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
- state: <customer1 or customer2 or whichever customer>
- code: <code in the callback provided by github>
```

**Response:**
```
{
  "data": {
    "error": null,
    "results": [
      "git@github.com:<username>/<rpository_name>.git", 
      "git@github.com:<organization>/<rpository_name>.git"
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


**Wizard Creation Status - Wizard creation status for a cloud provider.**
---
- API to query the status of a wizard creation for a cloud provider

**CURL Sample**
```
curl -H "space-id:101" -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" https://portal.prancer.io/prancer-customer1/api/wizardstatus?name=git_azure_customer1_1613610032528
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
- name: <Container name>
```

**Response:**
```
{
   "message" : "",
   "error" : "",
   "metadata" : {},
   "status" : 200,
   "data" : {
      "results" : [
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
      "error" : null
   }
}
```

