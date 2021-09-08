**Exclusion APIs**
===

- Prancer supports crawl and compliance execution for cloud and IAC resources. The process runs for all resources. Exclusions enables to exclude resources during the processes. Exclusions are applied at the collection level, not globally for all compliances across different types like azure, aws etc. Eg: for a given type of collection could be IAC, azure cloud etc, the resources, tests or a combination of test and resource can be excluded.

# For a container (that exists) get the list of exclusions
# param ==> container = <Container/Collection name>
curl -X GET https://portaldev.prancer.io/prancer-shahin/api/exclusions/resources/?container=Aws -H "authorization: Bearer $tk" -H 'content-type: application/json'

** List of the exclusions for a container **
---
- API to get the list of exclusions for a container. 

**CURL Sample**
```
curl -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X GET "https://portal.prancer.io/prancer-liquware/api/exclusions/resources/?container=aws"
```

- **URL:** https://portal.prancer.io/api/exclusions/resources/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- container: <container name>
```

**Response:**
```
{
   "status" : 200,
   "message" : "",
   "error" : "",
   "data" : {
      "container" : "Aws",
      "exclusions" : [
         {
            "paths" : [
               "/crawler-test/service-definition.yaml"
            ],
            "exclusionType" : "resource"
         },
         {
            "masterTestID" : "TEST_POD_2",
            "exclusionType" : "test"
         },
         {
            "masterTestID" : "TEST_POD_1",
            "paths" : [
               "/crawler-test/pod-creation.yaml"
            ],
            "exclusionType" : "single"
         }
      ]
   },
   "metadata" : {}
}
```

** API to Exclude Resource for  all tests API.**
---
- API to exclude a specific resource (either not ready or low-risk resource) for all tests in the compliance suite.

**CURL Sample**
```
curl -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X POST https://portal.prancer.io/prancer-liquware/api/exclusions/resources/  -d'{"container": "Aws", "exclusions": [{"exclusionType": "resource", "paths": ["/crawler-test/service-definition.yaml"]}]}'

```

- **URL:** https://portal.prancer.io/prancer-liquware/api/exclusions/resources/
- **Method:** POST

- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- container: <container name>
- exclusions: [{"exclusionType": "resource", "paths": ["<resource path>"]}, {}]
```

**Response:**
```
{
   "status" : 200,
   "message" : "Added exclusion successfully.",
   "error" : "",
   "metadata" : {}
}
```

** API to delete an Excluded Resource for  all tests API.**
---
- API to delete an excluded resource for all tests in the compliance suite.

**CURL Sample**
```
curl -H "Authorization: Bearer <JWT Bearer Token>" -H "Content-Type:application/json" -X DELETE https://portal.prancer.io/prancer-liquware/api/exclusions/resources/  -d'{"container": "Aws", "exclusions": [{"exclusionType": "resource", "paths": ["/crawler-test/service-definition.yaml"]}]}'

```

- **URL:** https://portal.prancer.io/prancer-liquware/api/exclusions/resources/
- **Method:** DELETE

- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
- container: <container name>
- exclusions: [{"exclusionType": "resource", "paths": ["<resource path>"]}, {}]
```

**Response:**
```
{
   "status" : 200,
   "message" : "Deleted exclusion successfully.",
   "error" : "",
   "metadata" : {}
}
```
