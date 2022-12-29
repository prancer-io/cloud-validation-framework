**Drift detection APIs**
===

**Drift detection - Check Drift**
---
- API for running the drift detection on a cloud collection.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/drift_detection/find_drift/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{"cloud_container": "aws_cloud"}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/find_drift/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "cloud_container": "aws_cloud"
}
```

- **Explanation:**

    `Required Fields`

    - **cloud_container:** Name of the cloud container for which you want to run the drift detection.


**Response:**
```
{
    "data": {},
    "error": "",
    "error_list": [],
    "message": "Drift detection started running successfully.",
    "metadata": {},
    "status": 200
}
```


**Drift detection - Output list**
---
- API for drift detection output list.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/drift_detection/report/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{
"container": "aws_cloud_1", "status": "drifted", "count": 10 "index": 0}'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/report/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "container": "aws_cloud_1",
    "status": "drifted",
    "count": 10,
    "index": 0
}
```

- **Explanation:**

    `Required Fields`

    - **container:** Name of the cloud container for which you want drift detection output list.

    `Optional Fields`

    - **status:** : Status of the output you want. Valid values are `drifted` and `undrifted`.

 **NOTE:**

- `index` and `count` parameters are useful for pagination. If no index pass then it will return all the records.
    
**Response:**
```
{
    "data": {
        "drift_results": [
            {
                "_id": "63806b3a73577a9f3ed00a8e",
                "container": "aws_cloud_1",
                "json": {
                    "cloud_type": "aws",
                    "collection": "drift_outputs",
                    "container": "aws_cloud_1",
                    "nos_of_drifted_resources": "1",
                    "nos_of_total_resources": "12",
                    "nos_of_tracked_resources": "1",
                    "results": [
                        {
                            "cloud_snapshot_data": {
                                "paths": "arn:aws:iam:aws-global::arnarn",
                                "session_id": "session_1669340617681",
                                "snapshot_collection": "aws_iam",
                                "snapshot_id": "TEST_IAM_050"
                            },
                            "drifted_attributes": [
                                {
                                    "cloud_attribute": "User.UserName",
                                    "cloud_attribute_value": "test",
                                    "cloudformation_attribute": "Properties.UserName",
                                    "cloudformation_attribute_value": "testuser"
                                }
                            ],
                            "iac_snapshot_data": {
                                "paths": [
                                    "/iam/iam.yaml"
                                ],
                                "session_id": "session_1669340640559",
                                "snapshot_collection": "cloudformation",
                                "snapshot_id": "CFR_TEMPLATE_SNAPSHOTbZdbl1"
                            },
                            "resource_type": "AWS::IAM::User",
                            "result": "drifted",
                            "result_id": "awscloud1_1669360442",
                            "tags": {
                                "prancer_unique_id": "c3b370c9-a596-416b-bf2c-265a6bd1c056",
                                "resource_type": "aws::iam::user"
                            }
                        }
                    ],
                    "timestamp": 1669360442651
                },
                "timestamp": 1669360442651,
                "type": "drift_output"
            }
        ],
        "metadata": {
            "count": 1,
            "current_page": 1,
            "next_index": -1,
            "total": 1
        }
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Drift detection - Output detail**
---
- API for drift detection output detail.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/drift_detection/report/detail/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{"drift_output_id": "63aad93b76780fb0b1913033","drift_result_id": "awsdrifttf_TEST_IAM_050_1672141115","container": "aws_drift_tf"}
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/report/detail/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "drift_output_id": "63aad93b76780fb0b1913033",
    "drift_result_id": "awsdrifttf_TEST_IAM_050_1672141115",
    "container": "aws_drift_tf"
}
```

- **Explanation:**

    `Required Fields`

    - **container:** Name of the cloud container for which you want drift detection output detail.
    - **drift_output_id:** Output id of the drift detection output record.
    - **drift_result_id:** Result id of the drift detection output result.

    
**Response:**
```
{
    "data": {
        "cloud_snapshot": {
            "ResponseMetadata": {
                "HTTPHeaders": {
                    "content-length": "686",
                    "content-type": "text/xml",
                    "date": "Tue, 27 Dec 2022 09:43:25 GMT",
                    "x-amzn-requestid": "8cdc318d-c156-427c-b9ce-cad7898fbdb3"
                },
                "HTTPStatusCode": 200,
                "RequestId": "8cdc318d-c156-427c-b9ce-cad7898fbdb3",
                "RetryAttempts": 0
            },
            "User": {
                "Arn": "arn:aws:iam::155603667260:user/ajeyk",
                "CreateDate": "Fri, 17 Jun 2022 08:56:17 GMT",
                "PasswordLastUsed": "Wed, 16 Nov 2022 10:08:45 GMT",
                "Path": "/",
                "Tags": [
                    {
                        "Key": "prancer_unique_id",
                        "Value": "c3b370c9-a596-416b-bf2c-265a6bd1c056"
                    }
                ],
                "UserId": "AIDASIOVTRE6FVNW5G6TU",
                "UserName": "ajeyk"
            }
        },
        "container": "aws_drift_tf",
        "drift_result": {
            "cloud_snapshot_data": {
                "paths": "arn:aws:iam::155603667260:user/ajeyk",
                "session_id": "session_1672114403721",
                "snapshot_collection": "aws_iam",
                "snapshot_id": "TEST_IAM_050"
            },
            "drifted_attributes": [
                {
                    "cloud_attribute": "User.UserName",
                    "cloud_attribute_value": "ajeyk",
                    "iac_attribute": "properties.name",
                    "iac_attribute_value": "testuser"
                }
            ],
            "iac_snapshot_data": {
                "paths": [
                    "/aws/iam/main.tf"
                ],
                "session_id": "session_1672114397231",
                "snapshot_collection": "terraformtemplate",
                "snapshot_id": "TRF_TEMPLATE_SNAPSHOTZjVey1"
            },
            "resource_type": "aws_iam_user",
            "result": "drifted",
            "result_id": "awsdrifttf_TEST_IAM_050_1672141115",
            "tags": {
                "prancer_unique_id": "c3b370c9-a596-416b-bf2c-265a6bd1c056",
                "resource_type": "aws_iam_user"
            },
            "undrifted_attributes": [
                {
                    "cloud_attribute": "User.Path",
                    "cloud_attribute_value": "/",
                    "iac_attribute": "properties.path",
                    "iac_attribute_value": "/"
                }
            ]
        },
        "iac_snapshot": {
            "resources": [
                {
                    "name": "test_role",
                    "properties": {
                        "assume_role_policy": {
                            "Statement": [
                                {
                                    "Action": "sts:AssumeRole",
                                    "Effect": "Allow",
                                    "Principal": {
                                        "Service": "ec2.amazonaws.com"
                                    },
                                    "Sid": ""
                                }
                            ],
                            "Version": "2012-10-17"
                        },
                        "compiletime_identity": "aws_iam_role.test_role",
                        "name": "test_role",
                        "tags": {
                            "tag-key": "tag-value"
                        }
                    },
                    "type": "aws_iam_role"
                },
                {
                    "name": "policy",
                    "properties": {
                        "compiletime_identity": "aws_iam_policy.policy",
                        "description": "My test policy",
                        "name": "test_policy",
                        "path": "/",
                        "policy": "jsonencode({'Version': '2012-10-17', 'Statement': [{'Action': ['ec2:Describe*'], 'Effect': 'Allow', 'Resource': '*']})}"
                    },
                    "type": "aws_iam_policy"
                },
                {
                    "name": "policy_one",
                    "properties": {
                        "compiletime_identity": "aws_iam_policy.policy_one",
                        "name": "policy-618033",
                        "policy": "jsonencode({'Version': '2012-10-17', 'Statement': [{'Action': ['ec2:Describe*'], 'Effect': 'Allow', 'Resource': '*']})}"
                    },
                    "type": "aws_iam_policy"
                },
                {
                    "name": "policy_two",
                    "properties": {
                        "compiletime_identity": "aws_iam_policy.policy_two",
                        "name": "policy-381966",
                        "policy": "jsonencode({'Version': '2012-10-17', 'Statement': [{'Action': ['s3:ListAllMyBuckets', 's3:ListBucket', 's3:HeadBucket'], 'Effect': 'Allow', 'Resource': '*']})}"
                    },
                    "type": "aws_iam_policy"
                },
                {
                    "name": "Test",
                    "properties": {
                        "compiletime_identity": "aws_iam_user.Test",
                        "name": "testuser",
                        "path": "/",
                        "tags": {
                            "prancer_unique_id": "c3b370c9-a596-416b-bf2c-265a6bd1c056",
                            "resource_type": "aws_iam_user"
                        }
                    },
                    "type": "aws_iam_user"
                }
            ]
        },
        "timestamp": 1672141115547
    },
    "error": "",
    "error_list": [],
    "message": "",
    "metadata": {},
    "status": 200
}
```


**Drift detection - Get tag**
---
- API for getting the prancer_unique_id tags.

**CURL Sample**
```
curl -X GET https://portal.prancer.io/prancer-customer1/api/drift_detection/get_tag -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/get_tag/
- **Method:** GET
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```

**Response:**
```
{
    "data": {
        "prancer_unique_id": "1e08eaab-666d-4d4c-bf3b-88ffcd3e8af5"
    },
    "error": "",
    "error_list": [],
    "message": "Tag received successfully.",
    "metadata": {},
    "status": 200
}
```


**Drift detection - Resource map manage**
---
- To add or create resource mapping data into the database  

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/drift_detection/get_resource_map -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/drift_detection/get_resource_map/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
    "reset": "true"
}
```

- **Explanation:**

    `Required Fields`

    - **NONE:**

    `Optional Fields`

    - **reset:** : Valid values are `true` and `false`. Default value is `false`.
        - `true:` To Update resource mapping data.
        - `false:` To Create resource mapping data.
    


**Response:**
```
{
    "data": {
        "AWS": [
            {
                "cloud": {
                    "attribute": "Reservations.0.Instances.0.EbsOptimized.enabled",
                    "resource_type": "",
                    "tag_location": "Reservations.0.Instances.0.Tags"
                },
                "cloudformation": {
                    "attribute": "Properties.EbsOptimized",
                    "resource_type": "aws::ec2::instance",
                    "tag_location": "Properties.Tags"
                }
            },
            {
                "cloud_tag_location": "Reservations.0.Instances.0.Tags",
                "cloudformation_resource_type": "aws::ec2::instance",
                "cloudformation_tag_location": "Properties.Tags",
                "map_attributes": [
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.EbsOptimized",
                        "cloudformation_attribute": "Properties.EbsOptimized",
                        "cloudformation_value_map": {
                            "default": "false",
                            "required": "false"
                        },
                        "terraform_attribute": "ebs_optimized",
                        "terraform_value_map": {
                            "allowed_values": {
                                "false": "disabled",
                                "true": "enabled"
                            },
                            "default": "false",
                            "required": "false"
                        }
                    },
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.InstanceType",
                        "cloudformation_attribute": "Properties.InstanceType",
                        "terraform_attribute": "instance_type"
                    },
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.Monitoring.State",
                        "cloudformation_attribute": "Properties.Monitoring",
                        "cloudformation_value_map": {
                            "allowed_values": {
                                "false": "disabled",
                                "true": "enabled"
                            },
                            "default": "false",
                            "required": "false"
                        },
                        "terraform_attribute": "monitoring",
                        "terraform_value_map": {
                            "allowed_values": {
                                "false": "disabled",
                                "true": "enabled"
                            },
                            "default": "false",
                            "required": "false"
                        }
                    },
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.Placement.AvailabilityZone",
                        "cloudformation_attribute": "Properties.AvailabilityZone",
                        "cloudformation_value_map": {
                            "required": "false"
                        },
                        "terraform_attribute": "availability_zone",
                        "terraform_value_map": {
                            "required": "false"
                        }
                    },
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.Placement.HostId",
                        "cloudformation_attribute": "Properties.HostId",
                        "cloudformation_value_map": {
                            "required": "false"
                        },
                        "terraform_attribute": "host_id",
                        "terraform_value_map": {
                            "required": "false"
                        }
                    },
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.Placement.HostResourceGroupArn",
                        "cloudformation_attribute": "Properties.HostResourceGroupArn",
                        "cloudformation_value_map": {
                            "required": "false"
                        }
                    },
                    {
                        "cloud_attribute": "Reservations.0.Instances.0.Placement.Affinity",
                        "cloudformation_attribute": "Properties.Affinity",
                        "cloudformation_value_map": {
                            "required": "false"
                        }
                    }
                ],
                "terraform_resource_type": "aws_instance",
                "terraform_tag_location": "tags"
            },
            {
                "cloud_tag_location": "User.Tags",
                "cloudformation_resource_type": "aws::iam::user",
                "cloudformation_tag_location": "Properties.Tags",
                "map_attributes": [
                    {
                        "cloud_attribute": "User.Path",
                        "cloudformation_attribute": "Properties.Path",
                        "cloudformation_value_map": {
                            "allowed_values": {
                                "/": "/"
                            },
                            "default": "/",
                            "required": "false"
                        },
                        "terraform_attribute": "path",
                        "terraform_value_map": {
                            "allowed_values": {
                                "/": "/"
                            },
                            "default": "/",
                            "required": "false"
                        }
                    },
                    {
                        "cloud_attribute": "User.UserName",
                        "cloudformation_attribute": "Properties.UserName",
                        "cloudformation_value_map": {
                            "required": "false"
                        },
                        "terraform_attribute": "name",
                        "terraform_value_map": {
                            "required": "true"
                        }
                    }
                ],
                "terraform_resource_type": "aws_iam_user",
                "terraform_tag_location": "tags"
            }
        ]
    },
    "error": "",
    "error_list": [],
    "message": "Resource Map found",
    "metadata": {},
    "status": 200
}
```
