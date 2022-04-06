**Resources APIs**
===

- Resources are the actual configuration snapshot of cloud resource which generates after run the compliance.

**Resources - Search**
---

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/resource/search?count=3&index=0&collection=azure_crawler_demo&start_date=2020-10-26&end_date=2020-10-27' -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/search/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "index":0,
    "count":10,
    "collection": "azure_crawler_demo",
    "start_date":"2021-02-10",
    "end_date": "2021-02-10",
    "connector": "azure_crawler_structure",
    "account_id":155603667260,
    "subscription_id": "db3667b7-cef9-4523-8e45-e2d9ed4518ab",
    "branch_name": "master",
    "project_id" : "learning-269422",
    "user": "ajey.khanapuri@liquware.com",
    "resource_type": "Microsoft.ContainerRegistry/registries,Microsoft.Network/networkSecurityGroups",
    "region": "eastus,us-central",
    "services" : "Databases, Networking",
    "resource_search" : "acrprancertest01"
}
```
- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection which need to be filter.
    - **connector:** Name of the connector/structure which you want to filter.

    `Optional Fields`

    - **index:** determines from which index have to start populating of the data.
    - **count:** determines the number of records per page need to populate in response.
    - **start_date:** Start filtering from specified start date. Format of date is `yyyy-mm-dd`
    - **end_date:** Filter the collections upto specified end date. Format of date is `yyyy-mm-dd`
    - **user:** Name of the test user specified in snapshot file.
    - **resource_type:** Filter the resources based on Resource Type specified in snapshot node. You can pass multiple resource types seperated by comma.
    - **account_id:** Use this filter for search AWS resources. Specify AWS cloud Account Id for which you want to filter the resource.
    - **subscription_id:** Use this filter for search Azure resources. Specify Azure cloud Subscription Id for which you want to filter the resource.
    - **project_id:** Use this filter for search Azure resources. Specify Azure cloud Subscription Id for which you want to filter the resource.
    - **region:** Filter the resources based on specified region. You can pass multiple regions seperated by comma.
    - **services:** Filter the resources based on services, seprated by comma (,).
    - **resource_search:** Search resource by it's name.

 **NOTE:** 
 
 - `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.
 - `start_date` and `end_date` both must be pass, if you want to filter the resources between two dates. If no start date and end date defined then it will return the resources from last run output.

**Response:**
- _response with pagination of 3 records_

- Status Code: 200
- Response:
```
{
    "data": {
        "filter": {
            "collection": "azure_crawler_demo",
            "connector": "azure_crawler_structure",
            "end_date": "2020-11-05",
            "start_date": "2020-11-05",
            "subscription_id": "db3667b7-cef9-4523-8e45-e2d9ed4518ab",
            "user": "ajey.khanapuri@liquware.com"
        },
        "resource_type_list": [
            "Microsoft.KeyVault/vaults",
            "Microsoft.Network/networkSecurityGroups",
            "Microsoft.Network/networkWatchers",
            "Microsoft.Network/virtualNetworks",
            "Microsoft.Storage/storageAccounts"
        ],
        "results": [
            {
                "collection_name": "azureabc",
                "compliant": false,
                "resource_names": [
                    "ndev001"
                ],
                "resource_node_id": "AZRSNP_2313",
                "resource_paths": [
                    "/subscriptions/d34d6562-8a12-4458-ba02-b12s5df45gdd/resourceGroups/nprod-dev-eastus2-vnet-rg/providers/Microsoft.Network/networkSecurityGroups/ndev001"
                ],
                "resource_type": "Microsoft.Network/networkSecurityGroups"
            },
            {
                "collection_name": "azureabc",
                "compliant": false,
                "resource_names": [
                    "ndev-vnet01"
                ],
                "resource_node_id": "AZRSNP_2844",
                "resource_paths": [
                    "/subscriptions/d34d6562-8a12-4458-ba02-b12s5df45gdd/resourceGroups/nprod-dev-eastus2-vnet-rg/providers/Microsoft.Network/virtualNetworks/ndev-vnet01"
                ],
                "resource_type": "Microsoft.Network/virtualNetworks"
            },
            {
                "collection_name": "azureabc",
                "compliant": false,
                "resource_names": [
                    "cs710033fffad674856"
                ],
                "resource_node_id": "AZRSNP_3010",
                "resource_paths": [
                    "/subscriptions/d34d6562-8a12-4458-ba02-b12s5df45gdd/resourceGroups/cloud-shell-storage-southcentralus/providers/Microsoft.Storage/storageAccounts/cs710033fffad674856"
                ],
                "resource_type": "Microsoft.Storage/storageAccounts"
            },
            {
                "collection_name": "azureabc",
                "compliant": false,
                "resource_names": [
                    "NetworkWatcher_eastus2"
                ],
                "resource_node_id": "AZRSNP_2601",
                "resource_paths": [
                    "/subscriptions/d34d6562-8a12-4458-ba02-b12s5df45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkWatchers/NetworkWatcher_eastus2"
                ],
                "resource_type": "Microsoft.Network/networkWatchers"
            },
            {
                "collection_name": "azureabc",
                "compliant": false,
                "resource_names": [
                    "NetworkWatcher_westus2"
                ],
                "resource_node_id": "AZRSNP_2602",
                "resource_paths": [
                    "/subscriptions/d34d6562-8a12-4458-ba02-b12s5df45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkWatchers/NetworkWatcher_westus2"
                ],
                "resource_type": "Microsoft.Network/networkWatchers"
            },
            {
                "collection_name": "azureabc",
                "compliant": false,
                "resource_names": [
                    "mykv-01"
                ],
                "resource_node_id": "AZRSNP_2285",
                "resource_paths": [
                    "/subscriptions/d34d6562-8a12-4458-ba02-b12s5df45gdd/resourceGroups/prancer-nprod-dev-eastus2-aks-rg/providers/Microsoft.KeyVault/vaults/mykv-01"
                ],
                "resource_type": "Microsoft.KeyVault/vaults"
            }
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 3,
        "next_index": 3,
        "total": 12
    },
    "status": 200
}
```

**Resources - Dashboard**
---

- API for get the stats view of the perticular resource object. It will return the resource status, configuration drifts in resource configuration and list of compliance testcases of resource.

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/resource/dashboard?collection=azure_nist_cloud_demo&resource_path=%2Fsubscriptions%2Fd34d6562-8a12-4458-ba02-b12345f45gdd%2FresourceGroups%2FNetworkWatcherRG%2Fproviders%2FMicrosoft.Network%2FnetworkSecurityGroups%2Fnsg-test-456&start_date=2021-02-20&end_date=2021-02-28' -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/dashboard
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "collection": "azure_crawler_demo",
    "resource_node_id" : "AZRSNP_22441",
    "start_date":"2020-10-19",
    "end_date": "2020-10-20"
}
```
- **Explanation:**

    `Required Fields`

    - **collection:** Name of the collection which need to be filter. It is `required` field.
    - **resource_node_id:** Uniquely identify the resource by id, it comes in the response of resource search api.

    `Optional Fields`

    - **start_date:** Start filtering from specified start date. Format of date is `yyyy-mm-dd`
    - **end_date:** Filter the collections upto specified end date. Format of date is `yyyy-mm-dd`
    
 **NOTE:** 
 - `start_date` and `end_date` both must be pass, if you want to filter the resources between two dates. If no start date and end date defined then it will return the resources from last run output.
 - Configuration Drift only come when resources are filtered based on `start_date` and `end_date`


**Response:**
```
{
    "data": {
        "compliant": "No",
        "configuration_drifts": [
            {
                "new_resource_id": "603604e7016161111cb46935",
                "new_resource_time": "2021-02-24 07:48:55",
                "old_resource_id": "603604345007f294c16c5fbe",
                "old_resource_time": "2021-02-24 07:45:56"
            },
            {
                "new_resource_id": "60362144fb687d817c6a7f4e",
                "new_resource_time": "2021-02-24 09:49:55",
                "old_resource_id": "60361e6c993b3f5e827caec5",
                "old_resource_time": "2021-02-24 09:37:47"
            },
            {
                "new_resource_id": "603630b61d855274b00c2a17",
                "new_resource_time": "2021-02-24 10:55:50",
                "old_resource_id": "60363058725937cae2eebfb9",
                "old_resource_time": "2021-02-24 10:54:16"
            },
            {
                "new_resource_id": "6036316a06689c4a72b54d42",
                "new_resource_time": "2021-02-24 10:58:50",
                "old_resource_id": "603630b61d855274b00c2a17",
                "old_resource_time": "2021-02-24 10:55:50"
            },
            {
                "new_resource_id": "603635b102a03c3ab4ed8c2d",
                "new_resource_time": "2021-02-24 11:17:05",
                "old_resource_id": "6036316a06689c4a72b54d42",
                "old_resource_time": "2021-02-24 10:58:50"
            },
            {
                "new_resource_id": "6036368064b6fd6ff8a3341f",
                "new_resource_time": "2021-02-24 11:20:32",
                "old_resource_id": "603635b102a03c3ab4ed8c2d",
                "old_resource_time": "2021-02-24 11:17:05"
            }
        ],
        "fail_count": 5,
        "first_crawl": "2021-01-19 09:14:12",
        "pass_count": 7,
        "resource_collection_name": "microsoftnetwork",
        "resource_path": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/nsg-test-456",
        "resource_status": "active",
        "resource_url": "https://portal.azure.com/#@f123456-a59f-478a-8457-54e8d12458d/resource/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/nsg-test-456",
        "testcases": [
            {
                "date": "2021-02-24 11:20:43",
                "result_id": "6036368b64b6fd6ff8a33429",
                "status": "passed",
                "test_id": "AZURE_TEST_229",
                "snapshot_id" : "AZRSNP_22229",
                "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22"
            },
            {
                "date": "2021-02-24 11:20:43",
                "result_id": "6036368b64b6fd6ff8a33429",
                "status": "passed",
                "test_id": "AZURE_TEST_230",
                "snapshot_id" : "AZRSNP_22230",
                "title": "Azure Network Security Group (NSG) allows traffic from internet on port 3389"
            },
            {
                "date": "2021-02-24 11:17:16",
                "result_id": "603635bc02a03c3ab4ed8c37",
                "status": "failed",
                "test_id": "AZURE_TEST_229",
                "snapshot_id" : "AZRSNP_22231",
                "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22"
            },
            {
                "date": "2021-02-24 11:17:16",
                "result_id": "603635bc02a03c3ab4ed8c37",
                "status": "failed",
                "test_id": "AZURE_TEST_230",
                "snapshot_id" : "AZRSNP_22232",
                "title": "Azure Network Security Group (NSG) allows traffic from internet on port 3389"
            },
            {
                "date": "2021-02-24 10:59:00",
                "result_id": "6036317406689c4a72b54d4c",
                "status": "passed",
                "test_id": "AZURE_TEST_229",
                "snapshot_id" : "AZRSNP_22233",
                "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22"
            },
            {
                "date": "2021-02-24 10:59:00",
                "result_id": "6036317406689c4a72b54d4c",
                "status": "passed",
                "test_id": "AZURE_TEST_230",
                "snapshot_id" : "AZRSNP_22234",
                "title": "Azure Network Security Group (NSG) allows traffic from internet on port 3389"
            },
            {
                "date": "2021-02-24 10:56:01",
                "result_id": "603630c11d855274b00c2a21",
                "status": "failed",
                "test_id": "AZURE_TEST_229",
                "snapshot_id" : "AZRSNP_22235",
                "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22"
            },
            {
                "date": "2021-02-24 10:56:01",
                "result_id": "603630c11d855274b00c2a21",
                "status": "failed",
                "test_id": "AZURE_TEST_230",
                "snapshot_id" : "AZRSNP_22236",
                "title": "Azure Network Security Group (NSG) allows traffic from internet on port 3389"
            },
            {
                "date": "2021-02-24 10:54:27",
                "result_id": "60363063725937cae2eebfc3",
                "status": "passed",
                "test_id": "AZURE_TEST_229",
                "snapshot_id" : "AZRSNP_22237",
                "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22"
            },
            {
                "date": "2021-02-24 10:54:27",
                "result_id": "60363063725937cae2eebfc3",
                "status": "passed",
                "test_id": "AZURE_TEST_230",
                "snapshot_id" : "AZRSNP_22238",
                "title": "Azure Network Security Group (NSG) allows traffic from internet on port 3389"
            },
            {
                "date": "2021-02-24 10:50:27",
                "result_id": "60362f73e20439143b65b8c7",
                "status": "failed",
                "test_id": "AZURE_TEST_229",
                "snapshot_id" : "AZRSNP_22239",
                "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22"
            },
            {
                "date": "2021-02-24 10:50:27",
                "result_id": "60362f73e20439143b65b8c7",
                "status": "passed",
                "test_id": "AZURE_TEST_230",
                "snapshot_id" : "AZRSNP_22240",
                "title": "Azure Network Security Group (NSG) allows traffic from internet on port 3389"
            }
        ],
        "total_test": 12
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Resources - Get**
---

- API for get the configuration details of latest resource object.

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/resource/detail?resource_path=%2Fsubscriptions%2Fd34d6562-8a12-4458-ba02-b12345f45gdd%2FresourceGroups%2FNetworkWatcherRG%2Fproviders%2FMicrosoft.Network%2FvirtualNetworks%2FNetworkWatcherRG-vnet&resource_collection_name=microsoftnetwork' -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/detail
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "resource_path" : "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg",
    "resource_collection_name" : "microsoftnetwork",
    "session_id": "session_1648443578974"
}
```
- **Explanation:**

    `Required Fields`

    - **resource_path:** Full path of the resource for which you want to get the detail information.
    - **resource_collection_name:** Collection name for the resource, it comes from response of Resource - Dashboard API.
    - **session_id:** Provide session id to get snapshot of specific session

**Response:**
```
{
    "data": {
        "etag": "W/\"7174e4bf-0571-4710-8791-343c365576ce\"",
        "id": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg",
        "location": "eastus2",
        "name": "automation-linux-nsg",
        "properties": {
            "defaultSecurityRules": [
                {
                    "etag": "W/\"7174e4bf-0571-4710-8791-343c365576ce\"",
                    "id": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg/defaultSecurityRules/AllowVnetInBound",
                    "name": "AllowVnetInBound",
                    "properties": {
                        "access": "Allow",
                        "description": "Allow inbound traffic from all VMs in VNET",
                        "destinationAddressPrefix": "VirtualNetwork",
                        "destinationAddressPrefixes": [],
                        "destinationPortRange": "*",
                        "destinationPortRanges": [],
                        "direction": "Inbound",
                        "priority": 65000,
                        "protocol": "*",
                        "provisioningState": "Succeeded",
                        "sourceAddressPrefix": "VirtualNetwork",
                        "sourceAddressPrefixes": [],
                        "sourcePortRange": "*",
                        "sourcePortRanges": []
                    },
                    "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
                }
            ],
            ...
        },
        "type": "Microsoft.Network/networkSecurityGroups"
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Resource - Testcase Detail**
---

- Get the full detail of single testcase

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/resource/testcase?result_id=6036368b64b6fd6ff8a33429&test_id=AZURE_TEST_229' -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/testcase
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "result_id": "5f97f7dcd94883dff55040e7",
    "test_id": "AZURE_TEST_229",
    "snapshot_id" : "AZRSNP_22229"
}
```
- **Explanation:**

    `Required Fields`

    - **result_id:** Result Id from which you want to read the testcases.
    - **test_id:** Testcase Id of perticular test from all testcases, it comes from response of Resource - Dashboard API.
    - **snapshot_id:** Snapshot Id for which the testcase was run.

**Response:**
```
{
    "data": {
        "content_version": "1.0.0.0",
        "date": "2020-10-27 10:35:08",
        "description": "Blocking SSH port 22 will protect users from attacks like Account compromise.",
        "log": "logs_20201027103457",
        "message": "",
        "rego_file": "package rule\ndefault rulepass = true\n\n# Azure Network Security Group (NSG) allows SSH traffic from internet on port ...",
        "result_id": "5f97f7dcd94883dff55040e7",
        "rule": "file(azure_network_security_229.rego)",
        "snapshotId": "AZRSNP_23118",
        "snapshot_name": "azure_crawler_snapshot_gen",
        "snapshots": [
            {
                "collection": "microsoftnetwork",
                "id": "AZRSNP_23118",
                "path": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg",
                "reference": "whitekite",
                "source": "azure_crawler_structure",
                "structure": "azure"
            }
        ],
        "status": "failed",
        "tags": [
            {
                "cloud": "Azure",
                "compliance": [
                    "PCI"
                ],
                "service": [
                    "Microsoft.Network",
                    "Networking"
                ]
            }
        ],
        "test_id": "AZURE_TEST_229",
        "test_name": "azure_crawler_test",
        "test_type": "mastertest",
        "title": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22",
        "type": "rego"
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Resource - configuration drift detail**
---

- Get the details of configuration drift

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/resource/configuration/drift?resource_collection_name=microsoftnetwork&new_resource_id=603604e7016161111cb46935&old_resource_id=603604345007f294c16c5fbe' -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/configuration/drift
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "resource_collection_name":"microsoftnetwork",
    "new_resource_id":"603604e7016161111cb46935",
    "old_resource_id":"603604345007f294c16c5fbe"
}
```
- **Explanation:**

    `Required Fields`

    - **resource_collection_name:** Collection name for the resource, it comes from response of Resource - Dashboard API.
    - **new_resource_id:** Resource Id of updated resource, it comes from response of Resource - Dashboard API.
    - **old_resource_id:** Resource Id of old resource, it comes from response of Resource - Dashboard API.

**Response:**
```
{
    "data": {
        "new_resource": {
            "etag": "W/\"7174e4bf-0571-4710-8791-343c365576ce\"",
            "id": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg",
            ...
        },
        "old_resource": {
            "etag": "W/\"57b928f0-c837-4552-9e93-9a7540a4ed1c\"",
            "id": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg",
            "location": "eastus2",
            "name": "automation-linux-nsg",
            ...
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Resource - filter save**
---

- Save the filter data for future use.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/resource/filter -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "collection": "azure_crawler_demo", "start_date" : "2020-10-19", "end_date" : "2020-10-20", "connector" : "aws_structure", "account_id": 155603667260, "user":"farshid_mahdavipour", "resource_type":"Microsoft.Network/networkSecurityGroups" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/filter
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "filter_id": "5f9804784cf7ad1bb583cece",
    "title" : "My Filter 1",
	"collection": "azure_crawler_demo",
	"start_date" : "2020-10-19",
	"end_date" : "2020-10-20",
	"connector" : "aws_structure",
	"account_id": 155603667260,
    "subscription_id": "db3667b7-cef9-4523-8e45-e2d9ed4518ab",
    "branch_name": "master",
    "project_id" : "learning-269422",
	"user" : "farshid_mahdavipour",
	"resource_type" : "Microsoft.Network/networkSecurityGroups",
    "query": "{"json.location" : {"$regex" : "^eastUS2$", "$options" : "i"}}",
    "query_collection" : "microsoftnetwork"
}
```
- **Explanation:**

    `Require Fields`

    - **title** Provide a title of the filter data.

    `Optional Fields`
    
    - **collection:** Name of the collection which need to be filter.
    - **connector:** Name of the connector/structure which you want to filter.
    - **user:** Name of the test user specified in snapshot file.
    - **account_id:** Use this filter for search AWS resources. Specify AWS cloud Account Id for which you want to filter the resource.
    - **subscription_id:** Use this filter for search Azure resources. Specify Azure cloud Subscription Id for which you want to filter the resource.
    - **project_id:** Use this filter for search Azure resources. Specify Azure cloud Subscription Id for which you want to filter the resource.
    - **branch_name:** Use this filter for search resources with Git provider.

    - **resource_type:** Filter the resources based on Resource Type specified in snapshot node.
    - **detail_methods:** Filter the resources based on Detail Methods specified in snapshot node. ( For AWS )
    - **start_date:** Start filtering from specified start date. Format of date is `yyyy-mm-dd`
    - **end_date:** Filter the collections upto specified end date. Format of date is `yyyy-mm-dd`
    - **filter_id:** A valid filter Id comes from response of save filter and get filters. If it is passed in request then it will update the existing filter.

    For Save filter in Query screen
    - **query:** Mongodb json query in String format.
    - **query_collection:** Database collection name on which the query will be execute.


**Response:**
```
{
    "data": {
        "filter_id": "5f9804784cf7ad1bb583cece"
    },
    "error": "",
    "error_list": [],
    "message": "Resource filter save successfully",
    "metadata": {},
    "status": 200
}
```


**Resource - filter get**
---

- Get the list of filters which are stored previously.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/resource/filter -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/filter
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
    "data": [
        {
            "filter_data": {
                "account_id": 155603667260,
                "collection": "azure_crawler_demo",
                "connector": "aws_structure",
                "end_date": "2020-10-20",
                "resource_type": "Microsoft.Network/networkSecurityGroups",
                "start_date": "2020-10-19",
                "user": "farshid_mahdavipour"
            },
            "filter_id": "5f9804784cf7ad1bb583cece",
            "title": "My Filter 1"
        }
    ],
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Resource - filter delete**
---

- delete the spacific filter

**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/resource/filter -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "filter_id": "5f9804784cf7ad1bb583cece" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/resource/filter
- **Method:** DELETE
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{ 
    "filter_id": "5f9804784cf7ad1bb583cece" 
}
```

- **Explanation:**

    `Required Fields`

    - **filter_id:** Valid filter Id which you want to delete.

**Success Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Resource filter deleted successfully",
    "metadata": {},
    "status": 200
}
```

**Failed Response:**
```
{
    "data": {},
    "error": "validation error",
    "message": "Invalid filter Id! No resource filter found with given filter Id",
    "metadata": {},
    "status": 400
}
```


**Resource - query**
---
- API for find the list of filtered resources based on it's configuration.

**CURL Sample**
```
curl -X GET ' https://portal.prancer.io/prancer-customer1/api/query/resources?query=Microsoft.Storage%2Fjson.properties.encryption.services.blob.keyType%3Daccount&start_date=2020-11-03&end_date=2020-11-04&count=10&index=50' -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/query/resources
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "query" : "{"json.location" : {"$regex" : "^eastUS2$", "$options" : "i"}}",
    "query_collection" : "microsoftnetwork",
    "start_date" : "2020-11-03",
    "end_date" : "2020-11-04",
    "count" : 10,
    "index" : 10
}
```

- **Explanation:**
    
    `Required Fields`

    - **query:** - Mongodb query for filter the resource in String format
    - **query_collection:** Database collection name on which the query will be execute.
    
    `Optional Fields`
    
    - **index:** determines from which index have to start populating of the data.
    - **count:** determines the number of records per page need to populate in response.
    
    - **start_date:** Start filtering from specified start date. Format of date is `yyyy-mm-dd`. It is optional.
    - **end_date:** Filter the resources upto specified end date. Format of date is `yyyy-mm-dd`. It is `required` if the start_date is passed. If no end date specified, only start date specified then it will return the last resource only.

 **NOTE:** 
 
 - `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.
 - `start_date` and `end_date` both must be pass, if you want to filter the resources between two dates. If no start date and end date defined then it will return the latest single resource.

**Response:**
```
{
    "data": {
        "results": [
            {
                "config": {
                     "name": "liqteststr01",
                     "location": "eastus2",
                     "properties": {
                         ...
                     }
                     ...
                },
                "resource_name": "liqteststr01",
                "date": "2020-11-05 06:33:22"
            },
            ...
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 10,
        "next_index": 20,
        "total": 56
    },
    "status": 200
}
```

**Resource - query sample**
---
- API for get sample queries for filter the resources.

**CURL Sample**
```
curl -X GET ' https://portal.prancer.io/prancer-customer1/api/query/samples' -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/query/samples
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
    "data": [
        {
            "collection": "microsoftcompute",
            "description": "Search for an Admin user in a Linux virtual Machine",
            "query": {
                "json.properties.osProfile.adminUsername": {
                    "$in": [
                        "user-1",
                        "user-2",
                        "user-3",
                    ]
                },
                "json.properties.storageProfile.osDisk.osType": {
                    "$eq": "Linux"
                },
                "json.type": {
                    "$eq": "Microsoft.Compute/virtualMachines"
                }
            },
            "title": "Admin Users for Linux Compute resources"
        },
        {
            "collection": "microsoftcompute",
            "description": "Find azure virtual machines by it's name",
            "query": {
                "json.name": {
                    "$in": [
                        "vm-instance-1",
                        "vm-instance-2",
                        "vm-instance-3"
                    ]
                },
                "json.type": {
                    "$eq": "Microsoft.Compute/virtualMachines"
                }
            },
            "title": "Azure virtual machine by name"
        },
        {
            "collection": "microsoftcompute",
            "description": "Search azure virtual machines which have disabled password authentication.",
            "query": {
                "json.properties.osProfile.linuxConfiguration.disablePasswordAuthentication": {
                    "$eq": true
                },
                "json.type": {
                    "$eq": "Microsoft.Compute/virtualMachines"
                }
            },
            "title": "Azure virtual machine with disabled password authentication"
        },
        {
            "collection": "microsoftstorage",
            "description": "Find microsoft storage by locations",
            "query": {
                "json.location": {
                    "$in": [
                        "eastus",
                        "eastus2"
                    ]
                },
                "json.type": {
                    "$eq": "Microsoft.Storage/storageAccounts"
                }
            },
            "title": "Mircrosoft storage with specific location"
        },
        {
            "collection": "aws_ec2",
            "description": "Find AWS ec2 instance by security group name",
            "query": {
                "json.SecurityGroups.GroupName": {
                    "$regex": ".*wizard-group-1.*"
                }
            },
            "title": "AWS ec2 instance by security group name"
        }
    ],
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Resource - exclusion create**
---

- Mark unwanted resources as excluded, so no compliance will execute on that resoruces.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/exclusions/resources/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "container": "azure_arm", "exclusions": [{ "exclusionType": "single", "masterTestID": "PR-AZR-ARM-AGW-001", "paths": [ "/APP_GW/appgw.azuredeploy.json", "/APP_GW/appgw.azuredeploy.parameters.json" ]}]}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/exclusions/resources/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**
```
{
    "container": "azure_arm",
    "exclusions": [
        {
            "exclusionType": "single",
            "masterTestID": "PR-AZR-ARM-AGW-001",
            "paths": [
                "/APP_GW/appgw.azuredeploy.json",
                "/APP_GW/appgw.azuredeploy.parameters.json",
            ]
        }
    ]
}
```
- **Explanation:**

    `Required Fields`

    - **container:** Name of the container
    - **exclusions:** List of the exclusions to be added. Check the available [excelusions](../exclusions/exclusion.md) for more details.

**Success Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Added exclusion successfully.",
    "metadata": {},
    "status": 200,
}
```

**Resource - exclusion get**
---

- Mark unwanted resources as excluded, so no compliance will execute on that resoruces.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/exclusions/resources/?container=azure_arm&count=10&index=0 -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/exclusions/resources/
- **Method:** GET
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**
```
{
    "container" : "azure_arm",
    "exclusionType": "single",
    "count": 10,
    "index": 0
}
```
- **Explanation:**

    `Required Fields`

    - **container:** Name of the collection to be filter.
    - **exclusionType:** Type of the exclution to filter.

    `Optional Fields`

    - **index:** determines from which index have to start populating of the data.
    - **count:** determines the number of records per page need to populate in response.

**Success Response:**
```
{
    "data": {
        "container": "azure_arm",
        "exclusions": [
            {
                "exclusionType": "single",
                "masterTestID": "PR-AZR-ARM-AGW-001",
                "paths": [
                    "/APP_GW/appgw.azuredeploy.json",
                    "/APP_GW/appgw.azuredeploy.parameters.json",
                ],
            }
        ],
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {"count": 10, "current_page": 1, "next_index": -1, "total": 1},
    "status": 200,
}
```

**Resource - exclusion delete**
---

- Delete the exclusion

**CURL Sample**
```
curl -X DELETE https://portal.prancer.io/prancer-customer1/api/exclusions/resources/?container=azure_arm&count=10&index=0 -H 'authorization: Bearer <JWT Bearer Token>' -d '{"container":"azure_arm","exclusions":[{"exclusionType":"single","masterTestID":"PR-AZR-ARM-AGW-001","paths":["/APP_GW/appgw.azuredeploy.json","/APP_GW/appgw.azuredeploy.parameters.json"]}]}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/exclusions/resources/
- **Method:** DELETE
- **Header:**
```
    - Authorization: Bearer <JWT Bearer Token>
```

- **Param:**
```
{
    "container": "azure_arm",
    "exclusions": [
        {
            "exclusionType": "single",
            "masterTestID": "PR-AZR-ARM-AGW-001",
            "paths": [
                "/APP_GW/appgw.azuredeploy.json",
                "/APP_GW/appgw.azuredeploy.parameters.json",
            ],
        }
    ],
}
```
- **Explanation:**

    `Required Fields`

    - **container:** Name of the collection from which exclusion need to be delete.
    - **exclusions:** List of exclusions to be delete.

**Success Response:**
```
{
    "data":{},
    "error":"",
    "error_list":[],
    "message":"Deleted exclusion successfully.",
    "metadata":{},
    "status":200
}
```