**Tags APIs**
===

- Tags are the part of Mastertestcase and Testcase configuration files.

**Default - tags**
---
- API for get the default tags. It will return all the Provider, Compliances and Services list which are valid and supported in Testcases.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/api/default/tags -H 'authorization: Bearer <JWT Bearer Token>'
```

- **URL:** https://portal.prancer.io/api/default/tags?provider_type=iac
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "provider_type" : "iac"
}
```

- **Explanation:**

    `Optional Fields`
    - **provider_type:** Filter the tags by provider types. Valid values for provider types are `cloud` and `iac`. If the provider type not pass in request parameter then it will return all tags.

**Response:**
```
{
    "data": {
        "cloud": [
            "Azure",
            "GCP",
            "AWS",
            "Kubernetes",
            "git"
        ],
        "compliance": [
            "CIS",
            "CSA-CCM",
            "HIPAA",
            "ISO 27001",
            "PCI-DSS",
            "NIST 800",
            "HITRUST",
            "SOC 2"
        ],
        "region": {
            "AWS": [
                {
                    "displayName": "US East (Ohio)",
                    "name": "us-east-2"
                },
                {
                    "displayName": "US East (N. Virginia)",
                    "name": "us-east-1"
                },
                {
                    "displayName": "US West (N. California)",
                    "name": "us-west-1"
                },
                {
                    "displayName": "US West (Oregon)",
                    "name": "us-west-2"
                },
                {
                    "displayName": "Africa (Cape Town)",
                    "name": "af-south-1"
                },
                {
                    "displayName": "Asia Pacific (Hong Kong)",
                    "name": "ap-east-1"
                },
                {
                    "displayName": "Asia Pacific (Mumbai)",
                    "name": "ap-south-1"
                },
                {
                    "displayName": "Asia Pacific (Osaka-Local)",
                    "name": "ap-northeast-3"
                },
                {
                    "displayName": "Asia Pacific (Seoul)",
                    "name": "ap-northeast-2"
                },
                {
                    "displayName": "Asia Pacific (Singapore)",
                    "name": "ap-southeast-1"
                },
                {
                    "displayName": "Asia Pacific (Sydney)",
                    "name": "ap-southeast-2"
                },
                {
                    "displayName": "Asia Pacific (Tokyo)",
                    "name": "ap-northeast-1"
                },
                {
                    "displayName": "Canada (Central)",
                    "name": "ca-central-1"
                },
                {
                    "displayName": "China (Beijing)",
                    "name": "cn-north-1"
                },
                {
                    "displayName": "China (Ningxia)",
                    "name": "cn-northwest-1"
                },
                {
                    "displayName": "Europe (Frankfurt)",
                    "name": "eu-central-1"
                },
                {
                    "displayName": "Europe (Ireland)",
                    "name": "eu-west-1"
                },
                {
                    "displayName": "Europe (London)",
                    "name": "eu-west-2"
                },
                {
                    "displayName": "Europe (Milan)",
                    "name": "eu-south-1"
                },
                {
                    "displayName": "Europe (Paris)",
                    "name": "eu-west-3"
                },
                {
                    "displayName": "Europe (Stockholm)",
                    "name": "eu-north-1"
                },
                {
                    "displayName": "Middle East (Bahrain)",
                    "name": "me-south-1"
                },
                {
                    "displayName": "South America (São Paulo)",
                    "name": "sa-east-1"
                },
                {
                    "displayName": "AWS GovCloud (US-East)",
                    "name": "us-gov-east-1"
                },
                {
                    "displayName": "AWS GovCloud (US)",
                    "name": "us-gov-west-1"
                }
            ],
            "Azure": [
                {
                    "displayName": "East US",
                    "name": "eastus"
                },
                {
                    "displayName": "East US 2",
                    "name": "eastus2"
                },
                {
                    "displayName": "East US STG",
                    "name": "eastusstg"
                },
                {
                    "displayName": "South Central US",
                    "name": "southcentralus"
                },
                {
                    "displayName": "South Central US STG",
                    "name": "southcentralusstg"
                },
                {
                    "displayName": "West US 2",
                    "name": "westus2"
                },
                {
                    "displayName": "Australia East",
                    "name": "australiaeast"
                },
                {
                    "displayName": "Southeast Asia",
                    "name": "southeastasia"
                },
                {
                    "displayName": "North Europe",
                    "name": "northeurope"
                },
                {
                    "displayName": "UK South",
                    "name": "uksouth"
                },
                {
                    "displayName": "West Europe",
                    "name": "westeurope"
                },
                {
                    "displayName": "Central US",
                    "name": "centralus"
                },
                {
                    "displayName": "North Central US",
                    "name": "northcentralus"
                },
                {
                    "displayName": "West US",
                    "name": "westus"
                },
                {
                    "displayName": "South Africa North",
                    "name": "southafricanorth"
                },
                {
                    "displayName": "Central India",
                    "name": "centralindia"
                },
                {
                    "displayName": "East Asia",
                    "name": "eastasia"
                },
                {
                    "displayName": "Japan East",
                    "name": "japaneast"
                },
                {
                    "displayName": "Korea Central",
                    "name": "koreacentral"
                },
                {
                    "displayName": "Canada Central",
                    "name": "canadacentral"
                },
                {
                    "displayName": "France Central",
                    "name": "francecentral"
                },
                {
                    "displayName": "Germany West Central",
                    "name": "germanywestcentral"
                },
                {
                    "displayName": "Norway East",
                    "name": "norwayeast"
                },
                {
                    "displayName": "Switzerland North",
                    "name": "switzerlandnorth"
                },
                {
                    "displayName": "UAE North",
                    "name": "uaenorth"
                },
                {
                    "displayName": "Brazil South",
                    "name": "brazilsouth"
                },
                {
                    "displayName": "Central US (Stage)",
                    "name": "centralusstage"
                },
                {
                    "displayName": "East US (Stage)",
                    "name": "eastusstage"
                },
                {
                    "displayName": "East US 2 (Stage)",
                    "name": "eastus2stage"
                },
                {
                    "displayName": "North Central US (Stage)",
                    "name": "northcentralusstage"
                },
                {
                    "displayName": "South Central US (Stage)",
                    "name": "southcentralusstage"
                },
                {
                    "displayName": "West US (Stage)",
                    "name": "westusstage"
                },
                {
                    "displayName": "West US 2 (Stage)",
                    "name": "westus2stage"
                },
                {
                    "displayName": "Asia",
                    "name": "asia"
                },
                {
                    "displayName": "Asia Pacific",
                    "name": "asiapacific"
                },
                {
                    "displayName": "Australia",
                    "name": "australia"
                },
                {
                    "displayName": "Brazil",
                    "name": "brazil"
                },
                {
                    "displayName": "Canada",
                    "name": "canada"
                },
                {
                    "displayName": "Europe",
                    "name": "europe"
                },
                {
                    "displayName": "Global",
                    "name": "global"
                },
                {
                    "displayName": "India",
                    "name": "india"
                },
                {
                    "displayName": "Japan",
                    "name": "japan"
                },
                {
                    "displayName": "United Kingdom",
                    "name": "uk"
                },
                {
                    "displayName": "United States",
                    "name": "unitedstates"
                },
                {
                    "displayName": "East Asia (Stage)",
                    "name": "eastasiastage"
                },
                {
                    "displayName": "Southeast Asia (Stage)",
                    "name": "southeastasiastage"
                },
                {
                    "displayName": "Central US EUAP",
                    "name": "centraluseuap"
                },
                {
                    "displayName": "East US 2 EUAP",
                    "name": "eastus2euap"
                },
                {
                    "displayName": "West Central US",
                    "name": "westcentralus"
                },
                {
                    "displayName": "South Africa West",
                    "name": "southafricawest"
                },
                {
                    "displayName": "Australia Central",
                    "name": "australiacentral"
                },
                {
                    "displayName": "Australia Central 2",
                    "name": "australiacentral2"
                },
                {
                    "displayName": "Australia Southeast",
                    "name": "australiasoutheast"
                },
                {
                    "displayName": "Japan West",
                    "name": "japanwest"
                },
                {
                    "displayName": "Korea South",
                    "name": "koreasouth"
                },
                {
                    "displayName": "South India",
                    "name": "southindia"
                },
                {
                    "displayName": "West India",
                    "name": "westindia"
                },
                {
                    "displayName": "Canada East",
                    "name": "canadaeast"
                },
                {
                    "displayName": "France South",
                    "name": "francesouth"
                },
                {
                    "displayName": "Germany North",
                    "name": "germanynorth"
                },
                {
                    "displayName": "Norway West",
                    "name": "norwaywest"
                },
                {
                    "displayName": "Switzerland West",
                    "name": "switzerlandwest"
                },
                {
                    "displayName": "UK West",
                    "name": "ukwest"
                },
                {
                    "displayName": "UAE Central",
                    "name": "uaecentral"
                },
                {
                    "displayName": "Brazil Southeast",
                    "name": "brazilsoutheast"
                }
            ],
            "GCP": [
                {
                    "displayName": "asia-east1",
                    "name": "asia-east1"
                },
                {
                    "displayName": "asia-east2",
                    "name": "asia-east2"
                },
                {
                    "displayName": "asia-northeast1",
                    "name": "asia-northeast1"
                },
                {
                    "displayName": "asia-northeast2",
                    "name": "asia-northeast2"
                },
                {
                    "displayName": "asia-northeast3",
                    "name": "asia-northeast3"
                },
                {
                    "displayName": "asia-south1",
                    "name": "asia-south1"
                },
                {
                    "displayName": "asia-southeast1",
                    "name": "asia-southeast1"
                },
                {
                    "displayName": "asia-southeast2",
                    "name": "asia-southeast2"
                },
                {
                    "displayName": "australia-southeast1",
                    "name": "australia-southeast1"
                },
                {
                    "displayName": "europe-north1",
                    "name": "europe-north1"
                },
                {
                    "displayName": "europe-west1",
                    "name": "europe-west1"
                },
                {
                    "displayName": "europe-west2",
                    "name": "europe-west2"
                },
                {
                    "displayName": "europe-west3",
                    "name": "europe-west3"
                },
                {
                    "displayName": "europe-west4",
                    "name": "europe-west4"
                },
                {
                    "displayName": "europe-west6",
                    "name": "europe-west6"
                },
                {
                    "displayName": "northamerica-northeast1",
                    "name": "northamerica-northeast1"
                },
                {
                    "displayName": "southamerica-east1",
                    "name": "southamerica-east1"
                },
                {
                    "displayName": "us-central1",
                    "name": "us-central1"
                },
                {
                    "displayName": "us-east1",
                    "name": "us-east1"
                },
                {
                    "displayName": "us-east4",
                    "name": "us-east4"
                },
                {
                    "displayName": "us-west1",
                    "name": "us-west1"
                },
                {
                    "displayName": "us-west2",
                    "name": "us-west2"
                },
                {
                    "displayName": "us-west3",
                    "name": "us-west3"
                },
                {
                    "displayName": "us-west4",
                    "name": "us-west4"
                }
            ],
            "git": []
        },
        "service": {
            "AWS": [
                "acm",
                "apigateway",
                "cloudformation",
                "cloudfront",
                "cloudtrail",
                "config",
                "dynamodb",
                "ec2",
                "ecs",
                "efs",
                "eks",
                "elasticache",
                "elb",
                "es",
                "iam",
                "kinesis",
                "kms",
                "lambda",
                "rds",
                "redshift",
                "route53",
                "s3",
                "sns",
                "sqs",
                "ssm"
            ],
            "Azure": [
                "Compute",
                "Networking",
                "Storage",
                "Web selected",
                "Mobile",
                "Containers",
                "Databases",
                "Analytics",
                "AI & Machine Learning",
                "Internet of Things",
                "Integration",
                "Identity",
                "Security",
                "Developer Tools",
                "DevOps",
                "Management and Governance",
                "Media",
                "Migration",
                "Mixed Reality",
                "Blockchain",
                "Hybrid"
            ],
            "GCP": [
                "Compute",
                "Storage",
                "Kubernetes Engine",
                "AppEngine",
                "Migration",
                "Databases",
                "Networking",
                "Management Tools",
                "Developer Tools",
                "API management",
                "Security"
            ],
            "Kubernetes": [
                "pod",
                "serviceaccount",
                "rolebinding",
                "clusterrole",
                "podsecuritypolicy",
                "role",
                "clusterrolebinding"
            ],
            "git": [
                "arm",
                "cloudformation",
                "deploymentmanager",
                "kubernetesObjectFiles",
                "helmChart",
                "terraform",
                "kcc",
                "aso",
                "ack"
            ]
        }
    },
    "error": "",
    "message": "",
    "metadata": {},
    "status": 200
}
```