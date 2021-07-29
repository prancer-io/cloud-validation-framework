data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

module "ec2" {
  source  = "../modules/ec2"
  instance_count                       = var.instance_count
  name                                 = var.name
  ami                                  = data.aws_ami.ubuntu.id
  instance_type                        = var.instance_type
  user_data                            = var.user_data
  user_data_base64                     = var.user_data_base64
  key_name                             = var.key_name
  monitoring                           = var.monitoring
  get_password_data                    = var.get_password_data
  vpc_security_group_ids               = var.vpc_security_group_ids
  subnet_id                            = var.subnet_id
  iam_instance_profile                 = var.iam_instance_profile
  associate_public_ip_address          = var.associate_public_ip_address
  ipv6_address_count                   = var.ipv6_address_count
  ipv6_addresses                       = var.ipv6_addresses
  ebs_optimized                        = var.ebs_optimized
  root_block_device                    = var.root_block_device
  ebs_block_device                     = var.ebs_block_device
  ephemeral_block_device               = var.ephemeral_block_device
  network_interface                    = var.network_interface
  disable_api_termination              = var.disable_api_termination
  instance_initiated_shutdown_behavior = var.instance_initiated_shutdown_behavior
  placement_group                      = var.placement_group
  tenancy                              = var.tenancy
  tags                                 = var.tags
}

module "ebs_volume" {
  source = "../modules/ebs_volume"
  availability_zone = var.availability_zone
  encrypted         = var.encrypted
  size              = var.size
  tags              = var.tags
}
