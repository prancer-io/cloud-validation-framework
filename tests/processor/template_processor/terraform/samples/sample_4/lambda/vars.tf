variable "role_name" {}
variable "role_path" {}
variable "max_session_duration" {}
variable "role_description" {}
variable "force_detach_policies" {}
variable "role_permissions_boundary_arn" {}
variable "assume_role_policy" {}

variable "cidr_block" {}
variable "instance_tenancy" {}
variable "enable_dns_hostnames" {}
variable "enable_dns_support" {}
variable "enable_classiclink" {}
variable "enable_classiclink_dns_support" {}
variable "enable_ipv6" {}

variable "subnet_cidr_block" {}
variable "availability_zone" {}
variable "availability_zone_id" {}
variable "map_public_ip_on_launch" {}
variable "assign_ipv6_address_on_creation" {}
variable "ipv6_cidr_block" {}

variable "sgroup_name" {}
variable "sgroup_description" {}
variable "revoke_rules_on_delete" {}

variable "description" {}
variable "environment" {}
variable "kms_key_arn" {}
variable "filename" {}
variable "function_name" {}
variable "handler" {}
variable "memory_size" {}
variable "publish" {}
variable "reserved_concurrent_executions" {}
variable "runtime" {}
variable "s3_bucket" {}
variable "s3_key" {}
variable "s3_object_version" {}
variable "timeout" {}

variable "tags" {
  type = map
}
variable "tracing_mode" {}
