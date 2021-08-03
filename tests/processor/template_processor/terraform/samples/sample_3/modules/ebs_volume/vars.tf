variable "availability_zone" {
  description = "Availability zone for volume (NOTE: EC2 instance mounting volume must reside in the same AS as the volume created here"
}

variable "encrypted" {
  description = "Encryption"
  default     = true
}

variable "size" {
  description = "The size of the drive in GiBs"
  type        = number
}

variable "tags" {
  description = "Mapping of tags to assign to resources"
  type        = map(string)
}
