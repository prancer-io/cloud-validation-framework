**Policy APIs**
===

**Policy - Filter**
---
- API for find the compliance policies based on applied filter parameters.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/policy/filter -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "provider": "Azure", "compliance" : [], "resource_type" : [], "policy_name" : "Network Security Group should not exposed RDP and SSH ports", "count" : 100, "index" : 0 }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/policy/filter
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"provider": "Azure",
	"compliance" : ["CIS", "CSA", "HIPAA"],
	"resource_type" : ["Networking"],
	"policy_name" : "Azure Network Security",
	"count" : 10,
	"index" : 0,
	"collection":""
}
```

- **Explanation:**

    `Required Fields`
    
    - **provider:** A valid cloud provider name ( Azure, AWS, GCP, git ) for filter the policies. See [Default - tags](/prancer-ent-apis/tags) API for get valid provider list.
    - pass the follwing parameters if you want to apply the pagination or 
    - **index:** determines from which index have to start populating of the data. First index should be 0.
    - **count:** determines the number of records per page need to populate in response.
    `Optional Fields`

    - **compliance:** A valid list of policy standards for filter the policy. See [Default - tags](/prancer-ent-apis/tags) API for get valid compliance list.
    - **resource_type:** A valid list of services which are supported by each of the providers. Services list should be pass based on provider value.  See [Default - tags](/prancer-ent-apis/tags) API for get list the services supported by each of the providers.
    - **policy_name:** A string value for filter the policy based on policy name.
    - **collection:** Pass the collection name for which you want to filter the policies.
    

**Response:**
```
{
    "data": [
        {
            "collection_name": "azure_cloud",
            "compliance": [
                "CIS",
                "CSA-CCM",
                "HIPAA",
                "NIST 800",
                "PCI-DSS"
            ],
            "container_name": "azure_cloud",
            "evals": [
                {
                    "eval": "data.rule.rulepass",
                    "id": "PR-AZR-0020",
                    "message": "data.rule.rulepass_err",
                    "remediation_description": "1. Login to Azure Portal. \n 2. Click on All services. \n 3. Under Networking, click on Network security groups. \n 4. Click on reported Network security group. \n  5. Under settings, click on Inbound security rules. \n 6. Click on reported row (22 PORT). \n 7. Set Action to Deny. \n 8. Click on OK.",
                    "remediation_function": "PR_AZR_0020.py"
                }
            ],
            "mastersnapshot_id": "AZRSNP_231",
            "mastertestcase_id": "608414064648517532cfe2ab",
            "policy_description": "Blocking SSH port 22 will protect users from attacks like Account compromise.",
            "policy_id": "AZURE_TEST_229",
            "policy_name": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22",
            "policy_rule": "file(PR_AZR_0020.rego)",
            "policy_type": "rego",
            "provider": "Azure",
            "resource_type": [
                "Networking"
            ],
            "severity": "Medium",
            "status": true
        },
        {
            "collection_name": "azure_cloud",
            "compliance": [
                "CIS",
                "CSA-CCM",
                "HIPAA",
                "NIST 800",
                "PCI-DSS"
            ],
            "container_name": "azure_cloud",
            "evals": [
                {
                    "eval": "data.rule.rulepass",
                    "id": "PR-AZR-0021",
                    "message": "data.rule.rulepass_err",
                    "remediation_description": "1. Login to Azure Portal. \n 2. Click on All services. \n 3. Under Networking, click on Network security groups. \n 4. Click on reported Network security group. \n  5. Under settings, click on Inbound security rules. \n 6. Click on reported row (3389 PORT). \n 7. Set Action to Deny. \n 8. Click on OK.",
                    "remediation_function": "PR_AZR_0021.py"
                }
            ],
            "mastersnapshot_id": "AZRSNP_231",
            "mastertestcase_id": "608414064648517532cfe2ab",
            "policy_description": "Blocking RDP port 3389 will protect users from attacks like account compromise, Denial of service and ransomware.",
            "policy_id": "AZURE_TEST_230",
            "policy_name": "Azure Network Security Group (NSG) allows traffic from internet on port 3389",
            "policy_rule": "file(PR_AZR_0021.rego)",
            "policy_type": "rego",
            "provider": "Azure",
            "resource_type": [
                "Networking"
            ],
            "severity": "Medium",
            "status": true
        }
    ],
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {
        "count": 10,
        "next_index": -1,
        "total": 2
    },
    "status": 200
}
```

**Get policy Rego**
---
- API for get the detail about rego file.

**CURL Sample**
```
curl -X GET 'https://portal.prancer.io/prancer-customer1/api/policy/rego?container_name=azure_cloud&policy_rule=file(PR_AZR_0020.rego)' -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/policy/search
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"container_name" : "azure_cloud",
    "policy_rule" : "file(PR_AZR_0020.rego)"
}
```

- **Explanation:**
    
    `Required Fields`

    - **container_name:** The `container_name` which you received from the response of Policy filter API.
    - **policy_rule:** The `policy_rule` which contains the rego file name. Pass the same policy rule which you received from the response of Policy filter API.

**Response:**
```
{
    "data": {
        "rego_file": "#\n# PR-AZR-0020\n#\n\npackage rule\ndefault rulepass = true\n\n# Azure Network Security Group (NSG) allows SSH traffic from internet on port \"22\"\n# If NSG dose not allows SSH traffic from internet on port \"22\"\n\n# https://docs.microsoft.com/en-us/rest/api/virtualnetwork/networksecuritygroups/get\n# https://resources.azure.com/subscriptions/db3667b7-cef9-4523-8e45-e2d9ed4518ab/resourceGroups/hardikResourceGroup/providers/Microsoft.Network/networkSecurityGroups/hardikVM-nsg\n\nrulepass = false {\n    lower(input.type) == \"microsoft.network/networksecuritygroups\"\n    count(public_security_rules_any) > 0\n}\nrulepass = false {\n    lower(input.type) == \"microsoft.network/networksecuritygroups\"\n    count(public_security_rules_Internet) > 0\n}\n# Method for check rule\nget_access[security_rule] {\n    security_rule := input.properties.securityRules[_]\n    security_rule.properties.access == \"Allow\"\n    security_rule.properties.direction == \"Inbound\"\n}\n\n# Method for check rule\nget_source_port[security_rule] {\n    get_access[security_rule]\n    security_rule.properties.sourcePortRange == \"22\"\n}\n\n# Method for check rule\nget_destination_port[security_rule] {\n    get_access[security_rule]\n    security_rule.properties.destinationPortRange == \"22\"\n}\n# Method for check rule\nget_source_PortRanges[security_rule] {\n    get_access[security_rule]\n    security_rule.properties.sourcePortRanges[_] == \"22\"\n}\n# Method for check rule\nget_destination_PortRanges[security_rule] {\n    get_access[security_rule]\n    security_rule.properties.destinationPortRanges[_] == \"22\"\n}\n# Method for check rule\nget_source_PortRange_Any[security_rule] {\n    get_access[security_rule]\n    security_rule.properties.sourcePortRange == \"*\"\n}\n# Method for check rule\nget_destination_PortRange_Any[security_rule] {\n    get_access[security_rule]\n    security_rule.properties.destinationPortRange == \"*\"\n}\n\n\n# \"securityRules[?(@.access == 'Allow' && @.direction == 'Inbound' && @.sourceAddressPrefix == '*'\n# @.sourcePortRange == '22')].destinationPortRange contains _Port.inRange(22)\npublic_security_rules_any[\"internet_on_PortRange_22_any_source\"] {\n    some security_rule\n    get_source_port[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"*\"\n}\n\npublic_security_rules_any[\"internet_on_PortRange_22_any_source\"] {\n    some security_rule\n    get_destination_port[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"*\"\n}\n\n# or \"securityRules[?(@.access == 'Allow' && @.direction == 'Inbound' && @.sourceAddressPrefix == '*'\n# @.sourcePortRanges[*] == '22')].destinationPortRanges[*] contains _Port.inRange(22)\npublic_security_rules_any[\"internet_on_PortRanges_22_any_source\"] {\n    some security_rule\n    get_source_PortRanges[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"*\"\n}\npublic_security_rules_any[\"internet_on_PortRanges_22_any_source\"] {\n    some security_rule\n    get_destination_PortRanges[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"*\"\n}\n\n# or \"securityRules[?(@.access == 'Allow' && @.direction == 'Inbound' && @.sourceAddressPrefix == '*'\n# @.sourcePortRanges[*] == '*')].destinationPortRanges[*] contains _Port.inRange(22)\npublic_security_rules_any[\"internet_on_Any_PortRange_any_source\"] {\n    some security_rule\n    get_source_PortRange_Any[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"*\"\n}\npublic_security_rules_any[\"internet_on_Any_PortRange_any_source\"] {\n    some security_rule\n    get_destination_PortRange_Any[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"*\"\n}\n\n# or securityRules[?(@.access == 'Allow' && @.direction == 'Inbound' && @.sourceAddressPrefix = 'Internet'\n# @.sourcePortRange == '22')]‌.destinationPortRange contains _Port.inRange(22)\npublic_security_rules_Internet[\"internet_on_PortRange_22_Internet_source\"] {\n    some security_rule\n    get_source_port[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"Internet\"\n}\npublic_security_rules_Internet[\"internet_on_PortRange_22_Internet_source\"] {\n    some security_rule\n    get_destination_port[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"Internet\"\n}\n# or \"securityRules[?(@.access == 'Allow' && @.direction == 'Inbound' && @.sourceAddressPrefix == 'Internet'\n#  @.sourcePortRanges[*] == '22')].destinationPortRanges[*] contains _Port.inRange(22)\npublic_security_rules_Internet[\"internet_on_PortRanges_22_Internet_source\"] {\n    some security_rule\n    get_source_PortRanges[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"Internet\"\n}\npublic_security_rules_Internet[\"internet_on_PortRanges_22_Internet_source\"] {\n    some security_rule\n    get_destination_PortRanges[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"Internet\"\n}\n# or \"securityRules[?(@.access == 'Allow' && @.direction == 'Inbound' && @.sourceAddressPrefix == 'Internet'\n# @.sourcePortRanges[*] == '*')].destinationPortRanges[*] contains _Port.inRange(22)\npublic_security_rules_Internet[\"internet_on_Any_PortRange_Internet_source\"] {\n    some security_rule\n    get_source_PortRange_Any[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"Internet\"\n}\npublic_security_rules_Internet[\"internet_on_Any_PortRange_Internet_source\"] {\n    some security_rule\n    get_destination_PortRange_Any[security_rule]\n    security_rule.properties.sourceAddressPrefix == \"Internet\"\n}\n"
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```

**Save Policy**
---
- Update existing policy

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/policy -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' \
  -d '{
	"mastertestcase_id": "608414064648517532cfe2ab",
    "collection_name": "azure_cloud",
    "compliance": [
        "CIS",
        "CSA-CCM",
        "HIPAA",
        "NIST 800",
        "PCI-DSS"
    ],
    "evals": [
        {
            "eval": "data.rule.rulepass",
            "id": "PR-AZR-0020",
            "message": "data.rule.rulepass_err",
            "remediation_description": "1. Login to Azure Portal. \n 2. Click on All services. \n 3. Under Networking, click on Network security groups. \n 4. Click on reported Network security group. \n  5. Under settings, click on Inbound security rules. \n 6. Click on reported row (22 PORT). \n 7. Set Action to Deny. \n 8. Click on OK.",
            "remediation_function": "PR_AZR_0020.py"
        }
    ],
    "mastersnapshot_id": "AZRSNP_231",
    "policy_description": "Blocking SSH port 22 will protect users from attacks like Account compromise.",
    "policy_id": "AZURE_TEST_229",
    "policy_name": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22",
    "policy_rule": "file(PR_AZR_0020.rego)",
    "policy_type": "rego",
    "provider": "Azure",
    "resource_type": [
        "Networking"
    ],
    "status": true,
    "severity": "Medium",
    "rego_file": "#\n# PR-AZR-0020\n#\n\npackage rule\ndefault rulepass = true\n\n# Azure Network Security Group (NSG) allows SSH traffic "
}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/policy
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
Save Policy with basic type
{
	"collection_name": "aws_cloud",
    "compliance": [
        "CSA-CCM",
        "GDPR",
        "HITRUST",
        "ISO 27001",
        "NIST 800",
        "NIST CSF",
        "PCI-DSS",
    ],
    "container_name": "aws_cloud",
    "evals": [],
    "mastersnapshot_id": "AWS_S3_01",
    "mastertestcase_id": "608419564648517532cfe31f",
    "policy_description": "This policy identifies the S3 buckets which have Object Versioning disabled. S3 Object Versioning is an important capability in protecting your data within a bucket. Once you enable Object Versioning, you cannot remove it; you can suspend Object Versioning at any time on a bucket if you do not wish for it to persist. It is recommended to enable Object Versioning on S3.",
    "policy_id": "AWS_S3_02",
    "policy_name": "AWS S3 Object Versioning is disabled",
    "policy_rule": "{AWS_REDSHIFT_01}.Versioning.Status=Enabled",
    "policy_type": "simple",
    "provider": "AWS",
    "remediation_description": "Steps for manual remediate ...",
    "resource_type": ["redshift"],
    "severity": "Medium",
	"status" : true
}

Save Policy with rego rules

```
{
	"mastertestcase_id": "608414064648517532cfe2ab",
    "collection_name": "azure_cloud",
    "compliance": [
        "CIS",
        "CSA-CCM",
        "HIPAA",
        "NIST 800",
        "PCI-DSS"
    ],
    "evals": [
        {
            "eval": "data.rule.rulepass",
            "id": "PR-AZR-0020",
            "message": "data.rule.rulepass_err",
            "remediation_description": "1. Login to Azure Portal. \n 2. Click on All services. \n 3. Under Networking, click on Network security groups. \n 4. Click on reported Network security group. \n  5. Under settings, click on Inbound security rules. \n 6. Click on reported row (22 PORT). \n 7. Set Action to Deny. \n 8. Click on OK.",
            "remediation_function": "PR_AZR_0020.py"
        }
    ],
    "mastersnapshot_id": "AZRSNP_231",
    "policy_description": "Blocking SSH port 22 will protect users from attacks like Account compromise.",
    "policy_id": "AZURE_TEST_229",
    "policy_name": "Azure Network Security Group (NSG) allows SSH traffic from internet on port 22",
    "policy_rule": "file(PR_AZR_0020.rego)",
    "policy_type": "rego",
    "provider": "Azure",
    "resource_type": [
        "Networking"
    ],
    "status": true,
    "severity": "Medium",
    "rego_file": "#\n# PR-AZR-0020\n#\n\npackage rule\ndefault rulepass = true\n\n# Azure Network Security Group (NSG) allows SSH traffic "
}
```

- **Explanation:**

    `Required Fields`

    - **policy_id:** Policy Id.
    - **collection_name:** Name of the collection.
    - **policy_name:** `Title` of the policy testcases.
    - **policy_description:** `Description` of the policy testcases.
    - **policy_rule:** Either it should be rego file reference or actual policy rule.
    - **provider:** Valid provider name for the testcase it should be in Azure, AWS, GCP, Git, Kubernetes.
    - **compliance:** List of valid compliances, See [Default - tags](/prancer-ent-apis/tags) API for get valid compliance list.
    - **service:** List of valid services. See [Default - tags](/prancer-ent-apis/tags) API for get valid service list.
    - **mastertestcase_id:** Mastertest Id, defined in policy testcases. If the Mastertest Id already exist in master testcase configuration file then it will update it otherwise it will create new policy testcase.
    - **type:** Type of policy testcase it will be either `rego` or `basic`.
    - **severity:** Set the severity of the policy. Allowed values are "Medium", "Low" and "High".

    `Required if type is rego`

    - **evals:** List of evel, the value of each evel object should be as follow:
        - **eval:** Field value which is presents in rego file. Final value of that field will be use for eveluate testcase is passed or not.
        - **message": Field value which is presents in rego file. Value of that field can be use as error message display for fail testcase.
        - **id": Valid remediation Id.
        - **remediation_description:** Manual steps for remediate the failed testcase.
        - **remediation_function:** Valid function name for remediation.
    - **rego_file:** The rego file in a string format.

    `Optional Fields`
    - **status:** Status of policy testcase, it is either "enable" or "disable".

**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Policy save successfully",
    "metadata": {},
    "status": 200
}
```

**Policy - Dashboard**
---
- API for get the dashboard statstics of Policy

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/policy/dashboard -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "mastertest_id": "AZURE_TEST_224", "collection_name" : "azure_crawler_demo" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/policy/dashboard
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	"mastertest_id": "AZURE_TEST_229",
	"collection_name" : "azure_cloud",
	"start_date" : "2021-05-01",
	"end_date" : "2021-05-05"
}
```

- **Explanation:**
    
    `Required Fields`

    - **collection_name:** The `collection_name` in which the master testcase is exist, it returns in response of Policy search API.
    - **mastertest_id:** The `mastertest_id` for which you want to get the detail information, which returns in response of Policy search API (`policy_id`).

**Response:**
```
{
    "data": {
        "fail_count": 1,
        "pass_count": 4,
        "testcases": [
            {
                "date": "2020-12-21 13:44:47",
                "resource_collection_name": "microsoftcontainerregistry",
                "resource_path": "/subscriptions/<subscription_id>/resourceGroups/prancer-resources-rg/providers/Microsoft.ContainerRegistry/registries/prancertest01",
                "result_id": "5fe0a6cf06297db2b0e8b14e",
                "status": "passed",
                "test_id": "AZURE_TEST_224",
                "title": "Azure Container Registry using the deprecated not classic registry"
            },
            {
                "date": "2020-12-21 13:39:37",
                "resource_collection_name": "microsoftcontainerregistry",
                "resource_path": "/subscriptions/<subscription_id>/resourceGroups/prancer-resources-rg/providers/Microsoft.ContainerRegistry/registries/prancertest01",
                "result_id": "5fe0a599194736822ddc0d2e",
                "status": "failed",
                "test_id": "AZURE_TEST_224",
                "title": "Azure Container Registry using the deprecated not classic registry"
            },
            {
                "date": "2020-12-21 13:24:34",
                "resource_collection_name": "microsoftcontainerregistry",
                "resource_path": "/subscriptions/<subscription_id>/resourceGroups/prancer-resources-rg/providers/Microsoft.ContainerRegistry/registries/prancertest01",
                "result_id": "5fe0a212809c8e7657b5ccc4",
                "status": "passed",
                "test_id": "AZURE_TEST_224",
                "title": "Azure Container Registry using the deprecated not classic registry"
            },
            {
                "date": "2020-12-21 13:19:38",
                "resource_collection_name": "microsoftcontainerregistry",
                "resource_path": "/subscriptions/<subscription_id>/resourceGroups/prancer-resources-rg/providers/Microsoft.ContainerRegistry/registries/prancertest01",
                "result_id": "5fe0a0ead31abeb825f18a3f",
                "status": "passed",
                "test_id": "AZURE_TEST_224",
                "title": "Azure Container Registry using the deprecated not classic registry"
            },
            {
                "date": "2020-12-21 12:06:46",
                "resource_collection_name": "microsoftcontainerregistry",
                "resource_path": "/subscriptions/<subscription_id>/resourceGroups/prancer-resources-rg/providers/Microsoft.ContainerRegistry/registries/prancertest01",
                "result_id": "5fe08fd6e331d4dd2d3d2909",
                "status": "passed",
                "test_id": "AZURE_TEST_224",
                "title": "Azure Container Registry using the deprecated not classic registry"
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
