variable "instance_count" {}
variable "name" {}
variable "instance_type" {}
variable "user_data" {}
variable "user_data_base64" {}
variable "key_name" {}
variable "monitoring" {}
variable "get_password_data" {}
variable "vpc_security_group_ids" {}
variable "subnet_id" {}
variable "iam_instance_profile" {}
variable "associate_public_ip_address" {}
variable "ipv6_address_count" {}
variable "ipv6_addresses" {}
variable "ebs_optimized" {}
variable "root_block_device" {}
variable "ebs_block_device" {}
variable "ephemeral_block_device" {}
variable "network_interface" {}
variable "disable_api_termination" {}
variable "instance_initiated_shutdown_behavior" {}
variable "placement_group" {}
variable "tenancy" {}

variable "availability_zone" {}
variable "encrypted" {}
variable "size" {}

variable "tags" {
  type = map
}
