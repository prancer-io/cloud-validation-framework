module "iam_role" {
  source                        = "../modules/iam_role"
  role_name                     = var.role_name
  role_path                     = var.role_path
  max_session_duration          = var.max_session_duration
  role_description              = var.role_description
  force_detach_policies         = var.force_detach_policies
  role_permissions_boundary_arn = var.role_permissions_boundary_arn
  assume_role_policy            = var.assume_role_policy
  tags                          = var.tags
}

module "vpc" {
  source  = "../modules/vpc"
  cidr_block                       = var.cidr_block
  instance_tenancy                 = var.instance_tenancy
  enable_dns_hostnames             = var.enable_dns_hostnames
  enable_dns_support               = var.enable_dns_support
  enable_classiclink               = var.enable_classiclink
  enable_classiclink_dns_support   = var.enable_classiclink_dns_support
  enable_ipv6                      = var.enable_ipv6
  tags                             = var.tags
}

module "subnet" {
  source  = "../modules/subnet"
  vpc_id                          = module.vpc.vpc_id
  subnet_cidr_block               = var.subnet_cidr_block
  availability_zone               = var.availability_zone
  availability_zone_id            = var.availability_zone_id
  map_public_ip_on_launch         = var.map_public_ip_on_launch
  assign_ipv6_address_on_creation = var.assign_ipv6_address_on_creation
  ipv6_cidr_block                 = var.ipv6_cidr_block
  tags                            = var.tags
}

module "security_group" {
  source                 = "../modules/security_group"
  name                   = var.sgroup_name
  description            = var.sgroup_description
  vpc_id                 = module.vpc.vpc_id
  revoke_rules_on_delete = var.revoke_rules_on_delete
  tags                   = var.tags
}

resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole" {
    role       = module.iam_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

module "lambda" {
  source                         = "git::https://github.com/prancer-io/prancer-terramerra.git//aws/modules/lambda"
  description                    = var.description
  environment                    = var.environment
  kms_key_arn                    = var.kms_key_arn
  filename                       = var.filename
  function_name                  = var.function_name
  handler                        = var.handler
  memory_size                    = var.memory_size
  publish                        = var.publish
  reserved_concurrent_executions = var.reserved_concurrent_executions
  iam_role                       = module.iam_role.arn
  runtime                        = var.runtime
  s3_bucket                      = var.s3_bucket
  s3_key                         = var.s3_key
  s3_object_version              = var.s3_object_version
  source_code_hash               = filebase64sha256(var.filename)
  timeout                        = var.timeout
  tags                           = var.tags
  vpc_config = {
    subnet_ids         = [module.subnet.id]
    security_group_ids = [module.security_group.id]
  }
  tracing_mode                   = var.tracing_mode
}
