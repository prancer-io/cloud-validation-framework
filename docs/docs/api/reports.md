**Reports APIs**
===

- Report APIs are use for filter the reports.

**Resources - Search**
---

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/report/search -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "start_date":"2021-02-17", "end_date":"2021-02-17", "container": "azure_crawler_demo", "timestamp": 1613544407026, "provider" : "Azure", "compliances" : ["CIS","PCI"], "services" : ["Networking"], "status": "failed", "count" : 5, "index" : 0 }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/report/search
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"start_date":"2021-02-17",
	"end_date":"2021-02-17",
	"container": "azure_crawler_demo",
    "timestamp": 1613544407026,
    "provider" : "Azure",
	"compliances" : ["CIS","PCI"],
	"services" : ["Networking"],
    "status": "failed",
    "count" : 3,
    "index" : 0,
    "provider_type" : "cloud",
    "search" : <search_text>
}
```
- **Explanation:**

    All Fields are Optional.
    `Optional Fields`

    - **index:** determines from which index have to start populating of the data.
    - **count:** determines the number of records per page need to populate in response.
    - **start_date:** Start filtering from specified start date. Format of date is `yyyy-mm-dd`
    - **end_date:** Filter the reports upto specified end date. Format of date is `yyyy-mm-dd`
    - **container:** Name of the container, container name list will receive in response when call API without any filter or filter by startdate/enddate.
    - **timestamp:** Filter the report by timestamp, timestamp list will receive in response when call API without any filter or filter by startdate/enddate.
    - **provider:** Valid Provider name, See [Default - tags](/prancer-ent-apis/tags) API for get valid provider list.
    - **compliance:** A valid list of compliance for filter the policy. See [Default - tags](/prancer-ent-apis/tags) API for get valid compliance list.
    - **services:** A valid list of services for filter the services. See [Default - tags](/prancer-ent-apis/tags) API for get valid services list.
    - **status:** Filter the reports by report's result. ( "Passed" or "Failed" )
    - **provider_type:** Filter the reports by provider types. Valid values for provider types are `cloud` and `iac`. If the provider type not pass in request parameter then it will return report of last compliance run.
    - **search:** Search reports by title of the report.

 **NOTE:** 
 - `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.
 - `start_date` and `end_date` both must be pass, if you want to filter the resources between two dates. If no start date and end date defined then it will return the report from last run output.

**Response:**
- _response with pagination of 3 records_

- Status Code: 200
- Response:
```
{
    "data": {
        "container_list": [
            "azure_crawler_demo"
        ],
        "results": [
            {
                "result_item": {
                    "auto_remediate": false,
                    "container_name": "azure_crawler_demo",
                    "content_version": "1.0.0.0",
                    "date": "2021-02-17 06:46:47",
                    "description": "Blocking SSH port 22 will protect users from attacks like Account compromise.",
                    "function": "",
                    "id": "602cbbd77c49350c2b0bd081",
                    "log": "logs_20210217064616",
                    "message": "",
                    "remediation_description": "",
                    "remediation_id": "",
                    "rule": "file(azure_network_security_229.rego)",
                    "snapshot_name": "azure_crawler_snapshot_gen",
                    "snapshots": [
                        {
                            "collection": "microsoftnetwork",
                            "id": "AZRSNP_23113",
                            "path": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/nsg-test-456",
                            "reference": "whitekite",
                            "region": "eastus",
                            "source": "azure_crawler_structure",
                            "structure": "azure",
                            "type": "Microsoft.Network/networkSecurityGroups"
                        }
                    ],
                    "status": "passed",
                    "tags": [
                        {
                            "cloud": "Azure",
                            "compliance": [
                                "CIS v1.0 (Azure)-6.2",
                                "CSA CCM v3.0.1-DSI-02",
                                "CSA CCM v3.0.1-IAM-07",
                                "CSA CCM v3.0.1-IVS-06",
                                "CSA CCM v3.0.1-IVS-08",
                                "HIPAA-164.312(e)(2)(i)",
                                "NIST 800-53 Rev4-SC-7 (19)",
                                "NIST 800-53 Rev4-SI-4 (4)",
                                "PCI DSS v3.2-1.2.1",
                                "CIS",
                                "CSA",
                                "HIPAA",
                                "NIST",
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
                }
            },
            {
                "result_item": {
                    "auto_remediate": false,
                    "container_name": "azure_crawler_demo",
                    "content_version": "1.0.0.0",
                    "date": "2021-02-17 06:46:47",
                    "description": "Blocking SSH port 22 will protect users from attacks like Account compromise.",
                    "function": "",
                    "id": "602cbbd77c49350c2b0bd081",
                    "log": "logs_20210217064616",
                    "message": "",
                    "remediation_description": "",
                    "remediation_id": "",
                    "rule": "file(azure_network_security_229.rego)",
                    "snapshot_name": "azure_crawler_snapshot_gen",
                    "snapshots": [
                        {
                            "collection": "microsoftnetwork",
                            "id": "AZRSNP_23114",
                            "path": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/uxmachine-nsg",
                            "reference": "whitekite",
                            "region": "eastus2",
                            "source": "azure_crawler_structure",
                            "structure": "azure",
                            "type": "Microsoft.Network/networkSecurityGroups"
                        }
                    ],
                    "status": "passed",
                    "tags": [
                        {
                            "cloud": "Azure",
                            "compliance": [
                                "CIS v1.0 (Azure)-6.2",
                                "CSA CCM v3.0.1-DSI-02",
                                "CSA CCM v3.0.1-IAM-07",
                                "CSA CCM v3.0.1-IVS-06",
                                "CSA CCM v3.0.1-IVS-08",
                                "HIPAA-164.312(e)(2)(i)",
                                "NIST 800-53 Rev4-SC-7 (19)",
                                "NIST 800-53 Rev4-SI-4 (4)",
                                "PCI DSS v3.2-1.2.1",
                                "CIS",
                                "CSA",
                                "HIPAA",
                                "NIST",
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
                }
            },
            {
                "result_item": {
                    "auto_remediate": false,
                    "container_name": "azure_crawler_demo",
                    "content_version": "1.0.0.0",
                    "date": "2021-02-17 06:46:47",
                    "description": "This policy identifies Azure Network Security Groups (NSGs) which are overly permissive to open UDP traffic from any source. A network security group contains a list of security rules that allow or deny inbound or outbound network traffic based on source or destination IP address, port, and protocol. As a best practice, it is recommended to configure NSGs to restrict traffic from known sources, allowing only authorized protocols and ports.",
                    "function": "",
                    "id": "602cbbd77c49350c2b0bd081",
                    "log": "logs_20210217064616",
                    "message": "",
                    "remediation_description": "",
                    "remediation_id": "",
                    "rule": "file(azure_network_security_232.rego)",
                    "snapshot_name": "azure_crawler_snapshot_gen",
                    "snapshots": [
                        {
                            "collection": "microsoftnetwork",
                            "id": "AZRSNP_23112",
                            "path": "/subscriptions/d34d6562-8a12-4458-ba02-b12345f45gdd/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkSecurityGroups/automation-linux-nsg",
                            "reference": "whitekite",
                            "region": "eastus2",
                            "source": "azure_crawler_structure",
                            "structure": "azure",
                            "type": "Microsoft.Network/networkSecurityGroups"
                        }
                    ],
                    "status": "passed",
                    "tags": [
                        {
                            "cloud": "Azure",
                            "compliance": [
                                "COSTUM"
                            ],
                            "service": [
                                "Microsoft.Network",
                                "Networking"
                            ]
                        }
                    ],
                    "test_id": "AZURE_TEST_232",
                    "test_name": "azure_crawler_test",
                    "test_type": "mastertest",
                    "title": "Azure Network Security Group (NSG) dose not having Inbound rule overly permissive to all UDP traffic from any source",
                    "type": "rego"
                }
            }
        ],
        "timestemp_list": [
            {
                "container": "azure_crawler_demo",
                "timestamp": 1613544407026,
                "timestamp_str": "2021-02-17 06:46:47"
            },
            {
                "container": "azure_crawler_demo",
                "timestamp": 1613544379577,
                "timestamp_str": "2021-02-17 06:46:19"
            }
        ]
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 3,
        "next_index": 3,
        "total": 13
    },
    "status": 200
}
```