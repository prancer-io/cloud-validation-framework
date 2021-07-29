output "id" {
  description = "List of IDs of private subnets"
  value       = aws_subnet.subnet.id
}

output "arn" {
  description = "List of ARNs of private subnets"
  value       = aws_subnet.subnet.arn
}

output "cidr_block" {
  description = "List of cidr_blocks of private subnets"
  value       = aws_subnet.subnet.cidr_block
}

output "ipv6_cidr_block" {
  description = "List of IPv6 cidr_blocks of private subnets in an IPv6 enabled VPC"
  value       = aws_subnet.subnet.ipv6_cidr_block
}
