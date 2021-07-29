role_name                     = "prancer-iam-role"
role_path                     = "/"
max_session_duration          = 3600
role_description              = ""
force_detach_policies         = false
role_permissions_boundary_arn = ""
assume_role_policy            = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

cidr_block                      = "10.10.0.0/16"
instance_tenancy                = "default"
enable_dns_hostnames            = false
enable_dns_support              = true
enable_classiclink              = null
enable_classiclink_dns_support  = null
enable_ipv6                     = false

subnet_cidr_block               = "10.10.1.0/24"
availability_zone               = null
availability_zone_id            = null
map_public_ip_on_launch         = false
assign_ipv6_address_on_creation = false
ipv6_cidr_block                 = null

sgroup_name                     = "prancer-security-group"
sgroup_description              = "Prancer Security Group"
revoke_rules_on_delete          = false

description                    = ""
environment                    = {
  variables = {
    API_KEY = "3c3ac97c6fa1850d366b70fbcd49a3db"
  }
}
kms_key_arn                    = null
filename                       = "function.py.zip"
function_name                  = "prancer-lambda-fn"
handler                        = "prancer-lambda-handler"
memory_size                    = 128
publish                        = false
reserved_concurrent_executions = -1
runtime                        = "python3.7"
s3_bucket                      = ""
s3_key                         = ""
s3_object_version              = ""
timeout                        = 5
tracing_mode                   = "PassThrough"

tags = {
  environment = "Production"
  project = "Prancer"
}
