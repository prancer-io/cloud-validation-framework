instance_count                       = 1
name                                 = "ec2"
instance_type                        = "t3.micro"
user_data                            = null
user_data_base64                     = null
key_name                             = ""
monitoring                           = false
get_password_data                    = false
vpc_security_group_ids               = null
iam_instance_profile                 = null
subnet_id                            = ""
associate_public_ip_address          = null
ipv6_address_count                   = null
ipv6_addresses                       = null
ebs_optimized                        = false
root_block_device                    = []
ebs_block_device                     = []
ephemeral_block_device               = []
network_interface                    = []
disable_api_termination              = false
instance_initiated_shutdown_behavior = "stop"
placement_group                      = null
tenancy                              = null

availability_zone                    = "us-east-2a"
encrypted                            = false
size                                 = 5

tags = {
  Name = "prancer-ec2"
  Environment = "Production"
  Project = "Prancer"
}
