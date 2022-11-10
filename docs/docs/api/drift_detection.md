**Drift detection APIs**
===

**Drift detection - Check Drift**
---
- API for running the drift detection on a cloud collection.

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/drift_detection/find_drift/ -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{"cloud_container": "aws_jaimin"}'
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
