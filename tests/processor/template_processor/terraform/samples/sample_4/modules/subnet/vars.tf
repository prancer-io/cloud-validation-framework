variable "vpc_id" {
  description = "The VPC ID"
  type        = string
  default     = "0.0.0.0/0"
}

variable "subnet_cidr_block" {
  description = "The CIDR block for the subnet"
  type        = string
  default     = "0.0.0.0/0"
}

variable "availability_zone" {
  description = "The AZ of the subnet"
  type        = string
  default     = null
}

variable "availability_zone_id" {
  description = "The AZ ID of the subnet"
  type        = string
  default     = null
}

variable "map_public_ip_on_launch" {
  description = "Should be false if you do not want to auto-assign public IP on launch"
  type        = bool
  default     = true
}

variable "assign_ipv6_address_on_creation" {
  description = "Specify true to indicate that network interfaces created in the specified subnet should be assigned an IPv6 address"
  type        = bool
  default     = false
}

variable "ipv6_cidr_block" {
  description = "The IPv6 network range for the subnet, in CIDR notation."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}
