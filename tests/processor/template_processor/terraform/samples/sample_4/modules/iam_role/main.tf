resource "aws_iam_role" "iamrole" {
  name                  = var.role_name
  path                  = var.role_path
  max_session_duration  = var.max_session_duration
  description           = var.role_description

  force_detach_policies = var.force_detach_policies
  permissions_boundary  = var.role_permissions_boundary_arn

  assume_role_policy    = var.assume_role_policy

  tags = var.tags
}
