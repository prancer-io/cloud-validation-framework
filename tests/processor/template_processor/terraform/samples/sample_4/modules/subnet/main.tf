resource "aws_subnet" "subnet" {
  vpc_id                          = var.vpc_id
  cidr_block                      = var.subnet_cidr_block
  availability_zone               = var.availability_zone
  availability_zone_id            = var.availability_zone_id
  map_public_ip_on_launch         = var.map_public_ip_on_launch
  assign_ipv6_address_on_creation = var.assign_ipv6_address_on_creation
  ipv6_cidr_block                 = var.ipv6_cidr_block
  tags                            = var.tags
}
