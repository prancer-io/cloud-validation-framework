variable "vpc_id" {
  description = "ID of the VPC where to create security group"
  type        = string
}

variable "name" {
  description = "Name of security group"
  type        = string
}

variable "description" {
  description = "Description of security group"
  type        = string
  default     = "Security Group managed by Terraform"
}

variable "revoke_rules_on_delete" {
  description = "Instruct Terraform to revoke all of the Security Groups attached ingress and egress rules before deleting the rule itself. Enable for EMR."
  type        = bool
  default     = false
}

variable "ingress_enabled" {
  type    = bool
  default = false
}

variable "ingress_description" {
  default = ""
}

variable "ingress_from_port" {
  default = ""
}

variable "ingress_to_port" {
  default = ""
}

variable "ingress_protocol" {
  default = ""
}

variable "ingress_cidr_blocks" {
  type = list(string)
  default = []
}

variable "tags" {
  description = "A mapping of tags to assign to security group"
  type        = map(string)
  default     = {}
}
