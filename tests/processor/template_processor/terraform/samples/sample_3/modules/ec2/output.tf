output "id" {
  description = "List of IDs of instances"
  value       = aws_instance.ec2.*.id
}

output "arn" {
  description = "List of ARNs of instances"
  value       = aws_instance.ec2.*.arn
}

output "availability_zone" {
  description = "List of availability zones of instances"
  value       = aws_instance.ec2.*.availability_zone
}

output "public_ip" {
  description = "List of public IP addresses assigned to the instances, if applicable"
  value       = aws_instance.ec2.*.public_ip
}

output "private_dns" {
  description = "List of private DNS names assigned to the instances. Can only be used inside the Amazon EC2, and only available if you've enabled DNS hostnames for your VPC"
  value       = aws_instance.ec2.*.private_dns
}

output "private_ip" {
  description = "List of private IP addresses assigned to the instances"
  value       = aws_instance.ec2.*.private_ip
}

output "security_groups" {
  description = "List of associated security groups of instances"
  value       = aws_instance.ec2.*.security_groups
}
