
# Best Practices For Creating Rego Rules

## 1. Policy Code

The policy code of a rule should follow this pattern.

- `PR-<CLOUD TYPE>-<TEMPLATE TYPE>-<RESOURCE TYPE>-<UNIQUE ID>`

Example

- `PR-AWS-CFR-S3-001`

## 2. Initialize default evalution variable

- `default s3_accesslog = null`

## 3. Write the rule to verify the your resources configuration

There are 2 situation exist when you check configuration of a resource

### **a. Attribute is not exist**

The attribute which you want to check in your configuration is not exist in your file.

```
aws_attribute_absence["s3_accesslog"] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    not resource.Properties.LoggingConfiguration.DestinationBucketName
}
```

### **b. Policy issue exist in configuration**

```
aws_issue["s3_accesslog"] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    count(resource.Properties.LoggingConfiguration.DestinationBucketName) == 0
}
```

## 4. Send failed resource path in issue metadata

`source_path contains same logic of the issue with extra field on metadata, which sends path of failed resource.`

```
source_path[{"s3_accesslog": metadata}] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    not resource.Properties.LoggingConfiguration.DestinationBucketName
    metadata := {
        "resource_path": [["Resources", i, "Properties", "LoggingConfiguration", "DestinationBucketName"]],
    }
}
```


## 5. Update the evalution variable value to `true` or `false`

```
s3_accesslog {
    lower(input.Resources[i].Type) == "aws::s3::bucket"
    not aws_issue["s3_accesslog"]
    not aws_attribute_absence["s3_accesslog"]
}

s3_accesslog = false {
    aws_issue["s3_accesslog"]
}
```

## 6. Set the proper error message

```
s3_accesslog_err = "AWS Access logging not enabled on S3 buckets" {
    aws_issue["s3_accesslog"]
} else = "S3 Bucket attribute DestinationBucketName/LogFilePrefix missing in the resource" {
    aws_attribute_absence["s3_accesslog"]
}
```

## 7. Define the Metadata

```
s3_accesslog_metadata := {
    "Policy Code": "PR-AWS-CFR-S3-001",
    "Type": "IaC",
    "Product": "AWS",
    "Language": "AWS Cloud formation",
    "Policy Title": "AWS Access logging not enabled on S3 buckets",
    "Policy Description": "Checks for S3 buckets without access logging turned on. Access logging allows customers to view complete audit trail on sensitive workloads such as S3 buckets",
    "Resource Type": "",
    "Policy Help URL": "",
    "Resource Help URL": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html"
}
```

- `Policy Code:` which should be the same as defined at the starting of the test and must be unique across all rules in the project
- `Type:` type of policy, available values are: IAC and Cloud
- `Product:` type of the cloud for example 'AWS'
- `Language`: related to the product, for example for product 'AWS' Languange will be 'AWS Cloud Formation'
- `Title`: Title of the policy
- `Description`: Description of the policy
- `Policy Help URL`: more information about the rule
- `Resource Help URL`: more information about the resource

## Complate Example

```
package rule
default metadata = {}

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html

#
# PR-AWS-CFR-S3-001
#

default s3_accesslog = null

aws_attribute_absence["s3_accesslog"] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    not resource.Properties.LoggingConfiguration.DestinationBucketName
}

source_path[{"s3_accesslog": metadata}] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    not resource.Properties.LoggingConfiguration.DestinationBucketName
    metadata := {
        "resource_path": [["Resources", i, "Properties", "LoggingConfiguration", "DestinationBucketName"]],
    }
}

aws_attribute_absence["s3_accesslog"] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    not resource.Properties.LoggingConfiguration.LogFilePrefix
}

source_path[{"s3_accesslog": metadata}] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    not resource.Properties.LoggingConfiguration.LogFilePrefix
    metadata := {
        "resource_path": [["Resources", i, "Properties", "LoggingConfiguration", "LogFilePrefix"]],
    }
}

aws_issue["s3_accesslog"] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    count(resource.Properties.LoggingConfiguration.DestinationBucketName) == 0
}

source_path[{"s3_accesslog": metadata}] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    count(resource.Properties.LoggingConfiguration.DestinationBucketName) == 0
    metadata := {
        "resource_path": [["Resources", i, "Properties", "LoggingConfiguration", "DestinationBucketName"]],
    }
}

aws_issue["s3_accesslog"] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    count(resource.Properties.LoggingConfiguration.LogFilePrefix) == 0
}

source_path[{"s3_accesslog": metadata}] {
    resource := input.Resources[i]
    lower(resource.Type) == "aws::s3::bucket"
    count(resource.Properties.LoggingConfiguration.LogFilePrefix) == 0
    metadata := {
        "resource_path": [["Resources", i, "Properties", "LoggingConfiguration", "LogFilePrefix"]],
    }
}

s3_accesslog {
    lower(input.Resources[i].Type) == "aws::s3::bucket"
    not aws_issue["s3_accesslog"]
    not aws_attribute_absence["s3_accesslog"]
}

s3_accesslog = false {
    aws_issue["s3_accesslog"]
}

s3_accesslog = false {
    aws_attribute_absence["s3_accesslog"]
}

s3_accesslog_err = "AWS Access logging not enabled on S3 buckets" {
    aws_issue["s3_accesslog"]
} else = "S3 Bucket attribute DestinationBucketName/LogFilePrefix missing in the resource" {
    aws_attribute_absence["s3_accesslog"]
}

s3_accesslog_metadata := {
    "Policy Code": "PR-AWS-CFR-S3-001",
    "Type": "IaC",
    "Product": "AWS",
    "Language": "AWS Cloud formation",
    "Policy Title": "AWS Access logging not enabled on S3 buckets",
    "Policy Description": "Checks for S3 buckets without access logging turned on. Access logging allows customers to view complete audit trail on sensitive workloads such as S3 buckets",
    "Resource Type": "",
    "Policy Help URL": "",
    "Resource Help URL": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html"
}
```
