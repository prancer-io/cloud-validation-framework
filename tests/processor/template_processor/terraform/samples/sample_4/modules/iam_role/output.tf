output "arn" {
  description = "ARN of IAM role"
  value       = aws_iam_role.iamrole.arn
}

output "name" {
  description = "Name of IAM role"
  value       = aws_iam_role.iamrole.name
}

output "path" {
  description = "Path of IAM role"
  value       = aws_iam_role.iamrole.path
}
