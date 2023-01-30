# JSON to Markdown

## 1. Install required packages

- This tool requires python3, please download and install it in your machine

- Run following command in your bash shell

```bash
cd json2md

make install
```

## 2. How to run the tool?

source json2md_venv/bin/activate


export PATH_PREFIX=https://github.com/GoogleCloudPlatform/k8s-config-connector/tree/master

export REGO_PREFIX=https://github.com/prancer-io/prancer-compliance-test/tree/master/google/kcc/

python json2md.py --template template.md --input output-master-test.json --output output-master-test.md

```
usage: json2md.py [-h] [--template TEMPLATE] --input INPUT [--output OUTPUT]

optional arguments:
  -h, --help           show this help message and exit
  --template TEMPLATE  Template file
  --input INPUT        Path to json data
  --output OUTPUT      Write to markdown file

```
## 3. How to get the output-master-test.json?
```
mkdir Prancer
cd Prancer
git clone https://github.com/prancer-io/prancer-hello-world.git
cd prancer-hello-world
pip3 install prancer-basic
prancer --db NONE <collection>
```
If you want to run compliance for one (or more) of the specific mastertestIDs.
```
prancer --db NONE --mastertestid TEST_S3_14 <collection>
prancer --db NONE --mastertestid TEST_S3_14,TEST_EC2_1 <collection>
```

We use below commands for getting output of specific Resources of Azure or Aws for our Scenarios

# Azure

### AKS
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-AKS-001,PR-AZR-TRF-AKS-002,PR-AZR-TRF-AKS-003,PR-AZR-TRF-AKS-004,PR-AZR-TRF-AKS-005,PR-AZR-TRF-AKS-006,PR-AZR-TRF-AKS-007,PR-AZR-TRF-AKS-008,PR-AZR-TRF-AKS-009,PR-AZR-TRF-AKS-010 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-AKS-001,PR-AZR-ARM-AKS-002,PR-AZR-ARM-AKS-003,PR-AZR-ARM-AKS-004,PR-AZR-ARM-AKS-005,PR-AZR-ARM-AKS-006,PR-AZR-ARM-AKS-007,PR-AZR-ARM-AKS-008,PR-AZR-ARM-AKS-009,PR-AZR-ARM-AKS-010 scenario-azure-quickStart
  ```


### Application Gateway
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-AGW-001,PR-AZR-TRF-AGW-002,PR-AZR-TRF-AGW-003,PR-AZR-TRF-AGW-004,PR-AZR-TRF-AGW-005,PR-AZR-TRF-AGW-006,PR-AZR-TRF-AGW-007 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-AGW-001,PR-AZR-ARM-AGW-002,PR-AZR-ARM-AGW-003,PR-AZR-ARM-AGW-004,PR-AZR-ARM-AGW-005,PR-AZR-ARM-AGW-006,PR-AZR-ARM-AGW-007 scenario-azure-quickStart
  ```


### KeyVault
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-KV-001,PR-AZR-TRF-KV-002,PR-AZR-TRF-KV-003,PR-AZR-TRF-KV-004,PR-AZR-TRF-KV-005,PR-AZR-TRF-KV-006,PR-AZR-TRF-KV-007,PR-AZR-TRF-KV-008,PR-AZR-TRF-KV-009 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-KV-001,PR-AZR-ARM-KV-002,PR-AZR-ARM-KV-003,PR-AZR-ARM-KV-004,PR-AZR-ARM-KV-005,PR-AZR-ARM-KV-006,PR-AZR-ARM-KV-007,PR-AZR-ARM-KV-008,PR-AZR-ARM-KV-009,PR-AZR-ARM-KV-010 scenario-azure-quickStart
  ```

### PostgreSQL
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-SQL-028,PR-AZR-TRF-SQL-029,PR-AZR-TRF-SQL-062,PR-AZR-TRF-SQL-063,PR-AZR-TRF-SQL-064,PR-AZR-TRF-SQL-065,PR-AZR-TRF-SQL-066,PR-AZR-TRF-SQL-003 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-SQL-028,PR-AZR-ARM-SQL-029,PR-AZR-ARM-SQL-066 scenario-azure-quickStart
  ```


### SQL Servers
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-SQL-047,PR-AZR-TRF-SQL-048,PR-AZR-TRF-SQL-068,PR-AZR-TRF-SQL-069,PR-AZR-TRF-SQL-031,PR-AZR-TRF-SQL-046 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-SQL-048,PR-AZR-ARM-SQL-050,PR-AZR-ARM-SQL-069,PR-AZR-ARM-SQL-047,PR-AZR-ARM-SQL-049,PR-AZR-ARM-SQL-030,PR-AZR-ARM-SQL-031,PR-AZR-ARM-SQL-032,PR-AZR-ARM-SQL-033,PR-AZR-ARM-SQL-034,PR-AZR-ARM-SQL-035,PR-AZR-ARM-SQL-036,PR-AZR-ARM-SQL-037,PR-AZR-ARM-SQL-038,PR-AZR-ARM-SQL-039,PR-AZR-ARM-SQL-040 scenario-azure-quickStart
  ```
  

### Storage Account
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-STR-003,PR-AZR-TRF-STR-004,PR-AZR-TRF-STR-005,PR-AZR-TRF-STR-008,PR-AZR-TRF-STR-009,PR-AZR-TRF-STR-010,PR-AZR-TRF-STR-011,PR-AZR-TRF-STR-012,PR-AZR-TRF-STR-014,PR-AZR-TRF-STR-017,PR-AZR-TRF-STR-018,PR-AZR-TRF-STR-019,PR-AZR-TRF-STR-020,PR-AZR-TRF-STR-023,PR-AZR-TRF-STR-024 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-STR-001,PR-AZR-ARM-STR-002,PR-AZR-ARM-STR-003,PR-AZR-ARM-STR-004,PR-AZR-ARM-STR-005,PR-AZR-ARM-STR-006,PR-AZR-ARM-STR-007,PR-AZR-ARM-STR-008,PR-AZR-ARM-STR-009,PR-AZR-ARM-STR-010,PR-AZR-ARM-STR-011,PR-AZR-ARM-STR-018,PR-AZR-ARM-STR-019,PR-AZR-ARM-STR-020,PR-AZR-ARM-STR-021,PR-AZR-ARM-STR-022,PR-AZR-ARM-STR-023,PR-AZR-ARM-STR-024 scenario-azure-quickStart
  ```
  
### VM
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AZR-TRF-VM-001,PR-AZR-TRF-VM-002,PR-AZR-TRF-VM-003,PR-AZR-TRF-VM-004,PR-AZR-TRF-VM-005,PR-AZR-TRF-VM-006,PR-AZR-TRF-VM-007 scenario-azure-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AZR-ARM-VM-001,PR-AZR-ARM-VM-002,PR-AZR-ARM-VM-003 scenario-azure-quickStart
  ```
  


# AWS

### Security
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AWS-TRF-ACM-001,PR-AWS-TRF-ACM-002,PR-AWS-TRF-ACM-003,PR-AWS-TRF-CT-001,PR-AWS-TRF-CT-002,PR-AWS-TRF-CT-003,PR-AWS-TRF-CT-004,PR-AWS-TRF-IAM-001,PR-AWS-TRF-IAM-002,PR-AWS-TRF-IAM-003,PR-AWS-TRF-IAM-004,PR-AWS-TRF-IAM-005,PR-AWS-TRF-IAM-006,PR-AWS-TRF-IAM-007,PR-AWS-TRF-IAM-008,PR-AWS-TRF-KMS-001,PR-AWS-TRF-KMS-002,PR-AWS-TRF-KMS-003 scenario-aws-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AWS-CFR-ACM-001,PR-AWS-CFR-ACM-002,PR-AWS-CFR-ACM-003,PR-AWS-CFR-CT-001,PR-AWS-CFR-CT-002,PR-AWS-CFR-CT-003,PR-AWS-CFR-CT-004,PR-AWS-CFR-IAM-001,PR-AWS-CFR-IAM-002,PR-AWS-CFR-IAM-003,PR-AWS-CFR-IAM-004,PR-AWS-CFR-IAM-005,PR-AWS-CFR-IAM-006,PR-AWS-CFR-IAM-007,PR-AWS-CFR-IAM-008,PR-AWS-CFR-KMS-001,PR-AWS-CFR-KMS-002,PR-AWS-CFR-KMS-003 scenario-aws-Labs

  ```
  
### Networking
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AWS-TRF-AG-001,PR-AWS-TRF-AG-002,PR-AWS-TRF-AG-003,PR-AWS-TRF-AG-004,PR-AWS-TRF-AG-005,PR-AWS-TRF-AG-006,PR-AWS-TRF-AG-007,PR-AWS-TRF-CF-001,PR-AWS-TRF-CF-002,PR-AWS-TRF-CF-003,PR-AWS-TRF-CF-004,PR-AWS-TRF-CF-005,PR-AWS-TRF-CF-006,PR-AWS-TRF-CF-007,PR-AWS-TRF-CF-008,PR-AWS-TRF-CF-009,PR-AWS-TRF-CF-010,PR-AWS-TRF-SG-001,PR-AWS-TRF-SG-002,PR-AWS-TRF-SG-003,PR-AWS-TRF-SG-004,PR-AWS-TRF-SG-005,PR-AWS-TRF-SG-006,PR-AWS-TRF-SG-007,PR-AWS-TRF-SG-008,PR-AWS-TRF-SG-009,PR-AWS-TRF-SG-010,PR-AWS-TRF-SG-011,PR-AWS-TRF-SG-012,PR-AWS-TRF-SG-013,PR-AWS-TRF-SG-014,PR-AWS-TRF-SG-015,PR-AWS-TRF-SG-016,PR-AWS-TRF-SG-017,PR-AWS-TRF-SG-018,PR-AWS-TRF-SG-019,PR-AWS-TRF-SG-020,PR-AWS-TRF-SG-021,PR-AWS-TRF-SG-022,PR-AWS-TRF-SG-023,PR-AWS-TRF-SG-024,PR-AWS-TRF-SG-025,PR-AWS-TRF-SG-026,PR-AWS-TRF-SG-027,PR-AWS-TRF-SG-028,PR-AWS-TRF-SG-029,PR-AWS-TRF-SG-030,PR-AWS-TRF-SG-031,PR-AWS-TRF-SG-032,PR-AWS-TRF-VPC-001,PR-AWS-TRF-VPC-002,PR-AWS-TRF-VPC-003 scenario-aws-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AWS-CFR-AG-001,PR-AWS-CFR-AG-002,PR-AWS-CFR-AG-003,PR-AWS-CFR-AG-004,PR-AWS-CFR-AG-005,PR-AWS-CFR-AG-006,PR-AWS-CFR-AG-007,PR-AWS-CFR-CF-001,PR-AWS-CFR-CF-002,PR-AWS-CFR-CF-003,PR-AWS-CFR-CF-004,PR-AWS-CFR-CF-005,PR-AWS-CFR-CF-006,PR-AWS-CFR-CF-007,PR-AWS-CFR-CF-008,PR-AWS-CFR-CF-009,PR-AWS-CFR-SG-001,PR-AWS-CFR-SG-002,PR-AWS-CFR-SG-003,PR-AWS-CFR-SG-004,PR-AWS-CFR-SG-005,PR-AWS-CFR-SG-006,PR-AWS-CFR-SG-007,PR-AWS-CFR-SG-008,PR-AWS-CFR-SG-009,PR-AWS-CFR-SG-010,PR-AWS-CFR-SG-011,PR-AWS-CFR-SG-012,PR-AWS-CFR-SG-013,PR-AWS-CFR-SG-014,PR-AWS-CFR-SG-015,PR-AWS-CFR-SG-016,PR-AWS-CFR-SG-017,PR-AWS-CFR-SG-018,PR-AWS-CFR-SG-019,PR-AWS-CFR-SG-020,PR-AWS-CFR-SG-021,PR-AWS-CFR-SG-022,PR-AWS-CFR-SG-023,PR-AWS-CFR-SG-024,PR-AWS-CFR-SG-025,PR-AWS-CFR-SG-026,PR-AWS-CFR-SG-027,PR-AWS-CFR-SG-028,PR-AWS-CFR-SG-029,PR-AWS-CFR-SG-030,PR-AWS-CFR-SG-031,PR-AWS-CFR-SG-032,PR-AWS-CFR-SG-033,PR-AWS-CFR-VPC-001,PR-AWS-CFR-VPC-002,PR-AWS-CFR-VPC-003 scenario-aws-Labs
  ```
  


### Management
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AWS-TRF-CB-001,PR-AWS-TRF-CB-002,PR-AWS-TRF-CD-001,PR-AWS-TRF-CP-001,PR-AWS-TRF-SNS-001,PR-AWS-TRF-SNS-002,PR-AWS-TRF-SNS-003,PR-AWS-TRF-SNS-004,PR-AWS-TRF-SQS-001,PR-AWS-TRF-SQS-002,PR-AWS-TRF-SQS-003,PR-AWS-TRF-SQS-004,PR-AWS-TRF-SQS-005 scenario-aws-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AWS-CFR-CB-001,PR-AWS-CFR-CB-002,PR-AWS-CFR-CP-001,PR-AWS-CFR-CD-001,PR-AWS-CFR-SNS-001,PR-AWS-CFR-SNS-002,PR-AWS-CFR-SNS-003,PR-AWS-CFR-SNS-004,PR-AWS-CFR-SQS-001,PR-AWS-CFR-SQS-002,PR-AWS-CFR-SQS-003,PR-AWS-CFR-SQS-004,PR-AWS-CFR-SQS-005 scenario-aws-Labs
  ```


### Data Store
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AWS-TRF-RDS-001,PR-AWS-TRF-RDS-002,PR-AWS-TRF-RDS-003,PR-AWS-TRF-RDS-004,PR-AWS-TRF-RDS-005,PR-AWS-TRF-RDS-006,PR-AWS-TRF-RDS-007,PR-AWS-TRF-RDS-008,PR-AWS-TRF-RDS-009,PR-AWS-TRF-RDS-010,PR-AWS-TRF-RDS-011,PR-AWS-TRF-RDS-012,PR-AWS-TRF-RDS-013,PR-AWS-TRF-RDS-016,PR-AWS-TRF-RDS-017,PR-AWS-TRF-RDS-018,PR-AWS-TRF-RDS-019,PR-AWS-TRF-ECR-001,PR-AWS-TRF-ECR-002,PR-AWS-TRF-ECR-003,PR-AWS-TRF-ECR-004,PR-AWS-TRF-RSH-001,PR-AWS-TRF-RSH-002,PR-AWS-TRF-RSH-003,PR-AWS-TRF-RSH-004,PR-AWS-TRF-RSH-005,PR-AWS-TRF-RSH-006,PR-AWS-TRF-RSH-007,PR-AWS-TRF-S3-001,PR-AWS-TRF-S3-002,PR-AWS-TRF-S3-003,PR-AWS-TRF-S3-004,PR-AWS-TRF-S3-005,PR-AWS-TRF-S3-006,PR-AWS-TRF-S3-007,PR-AWS-TRF-S3-008,PR-AWS-TRF-S3-009,PR-AWS-TRF-S3-010,PR-AWS-TRF-S3-011,PR-AWS-TRF-S3-012,PR-AWS-TRF-S3-013,PR-AWS-TRF-S3-014,PR-AWS-TRF-S3-015,PR-AWS-TRF-S3-016,PR-AWS-TRF-S3-017,PR-AWS-TRF-S3-018,PR-AWS-TRF-S3-019,PR-AWS-TRF-S3-020,PR-AWS-TRF-S3-021 scenario-aws-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AWS-CFR-RDS-001,PR-AWS-CFR-RDS-002,PR-AWS-CFR-RDS-003,PR-AWS-CFR-RDS-004,PR-AWS-CFR-RDS-005,PR-AWS-CFR-RDS-006,PR-AWS-CFR-RDS-007,PR-AWS-CFR-RDS-008,PR-AWS-CFR-RDS-009,PR-AWS-CFR-RDS-010,PR-AWS-CFR-RDS-011,PR-AWS-CFR-RDS-012,PR-AWS-CFR-RDS-013,PR-AWS-CFR-RDS-016,PR-AWS-CFR-RDS-017,PR-AWS-CFR-RDS-018,PR-AWS-CFR-RDS-019,PR-AWS-CFR-ECR-001,PR-AWS-CFR-ECR-002,PR-AWS-CFR-ECR-003,PR-AWS-CFR-ECR-004,PR-AWS-CFR-RSH-001,PR-AWS-CFR-RSH-002,PR-AWS-CFR-RSH-003,PR-AWS-CFR-RSH-004,PR-AWS-CFR-RSH-005,PR-AWS-CFR-RSH-006,PR-AWS-CFR-RSH-007,PR-AWS-CFR-S3-001,PR-AWS-CFR-S3-002,PR-AWS-CFR-S3-003,PR-AWS-CFR-S3-004,PR-AWS-CFR-S3-005,PR-AWS-CFR-S3-006,PR-AWS-CFR-S3-007,PR-AWS-CFR-S3-008,PR-AWS-CFR-S3-009,PR-AWS-CFR-S3-010,PR-AWS-CFR-S3-011,PR-AWS-CFR-S3-012,PR-AWS-CFR-S3-013,PR-AWS-CFR-S3-014,PR-AWS-CFR-S3-015,PR-AWS-CFR-S3-016,PR-AWS-CFR-S3-017,PR-AWS-CFR-S3-018,PR-AWS-CFR-S3-019,PR-AWS-CFR-S3-020,PR-AWS-CFR-S3-021 scenario-aws-Labs
  ```

### Compute
- Terraform
  ```
  prancer --db NONE --mastertestid PR-AWS-TRF-ECS-001,PR-AWS-TRF-ECS-002,PR-AWS-TRF-ECS-003,PR-AWS-TRF-ECS-004,PR-AWS-TRF-ECS-005,PR-AWS-TRF-ECS-006,PR-AWS-TRF-ECS-007,PR-AWS-TRF-ECS-008,PR-AWS-TRF-ECS-009,PR-AWS-TRF-ECS-010,PR-AWS-TRF-ECS-011,PR-AWS-TRF-ECS-012,PR-AWS-TRF-ECS-013,PR-AWS-TRF-ECS-014,PR-AWS-TRF-EC2-001,PR-AWS-TRF-EC2-002,PR-AWS-TRF-EC2-003,PR-AWS-TRF-EC2-004,PR-AWS-TRF-EC2-005,PR-AWS-TRF-LMD-001,PR-AWS-TRF-LMD-002,PR-AWS-TRF-LMD-003,PR-AWS-TRF-LMD-004,PR-AWS-TRF-LMD-005 scenario-aws-terraform-hashicorp
  ```
- IaC
  ```
  prancer --db NONE --mastertestid PR-AWS-CFR-ECS-001,PR-AWS-CFR-ECS-002,PR-AWS-CFR-ECS-003,PR-AWS-CFR-ECS-004,PR-AWS-CFR-ECS-005,PR-AWS-CFR-ECS-006,PR-AWS-CFR-ECS-007,PR-AWS-CFR-ECS-008,PR-AWS-CFR-ECS-009,PR-AWS-CFR-ECS-010,PR-AWS-CFR-ECS-011,PR-AWS-CFR-ECS-012,PR-AWS-CFR-ECS-013,PR-AWS-CFR-ECS-014,PR-AWS-CFR-EC2-001,PR-AWS-CFR-EC2-002,PR-AWS-CFR-EC2-003,PR-AWS-CFR-EC2-004,PR-AWS-CFR-EC2-005,PR-AWS-CFR-LMD-001,PR-AWS-CFR-LMD-002,PR-AWS-CFR-LMD-003,PR-AWS-CFR-LMD-004,PR-AWS-CFR-LMD-005 scenario-aws-Labs
  ```


put details of output of each test case to output-master-test.json as input

## 4. Update template.md, export PATH_PREFIX and REGO_PREFIX

We should update REGO_PREFIX and PATH_PREFIX and also template.md according to below

# Azure
- Terraform
  ```
  export PATH_PREFIX=https://github.com/hashicorp/terraform-provider-azurerm/tree/main
  export REGO_PREFIX=https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/terraform/
  ```
  and for template.md
  ```
  Source Repository: https://github.com/hashicorp/terraform-provider-azurerm
  Compliance Database: https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/terraform
  ```
- IaC
  ```
  export PATH_PREFIX=https://github.com/Azure/azure-quickstart-templates/tree/master
  export REGO_PREFIX=https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/
  ```
  and for template.md
  ```
  Source Repository: https://github.com/Azure/azure-quickstart-templates
  Compliance Database: https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac
  ```

# Aws
- Terraform
  ```
  export PATH_PREFIX=https://github.com/hashicorp/terraform-provider-aws/tree/main
  export REGO_PREFIX=https://github.com/prancer-io/prancer-compliance-test/tree/master/aws/terraform/
  ```
  and for template.md
  ```
  Source Repository: https://github.com/hashicorp/terraform-provider-aws
  Compliance Database: https://github.com/prancer-io/prancer-compliance-test/tree/master/aws/terraform
  ```
- IaC
  ```
  export PATH_PREFIX=https://github.com/awslabs/aws-cloudformation-templates/tree/master
  export REGO_PREFIX=https://github.com/prancer-io/prancer-compliance-test/tree/master/aws/iac/
  ```
  and for template.md
  ```
  Source Repository: https://github.com/awslabs/aws-cloudformation-templates
  Compliance Database: https://github.com/prancer-io/prancer-compliance-test/tree/master/aws/iac
  ```

Now you may Run below command
```
python json2md.py --template template.md --input output-master-test.json --output output-master-test.md
```