resource "aws_security_group" "sgroup" {
  name                   = var.name
  description            = var.description
  vpc_id                 = var.vpc_id
  revoke_rules_on_delete = var.revoke_rules_on_delete

  dynamic "ingress" {
    for_each = var.ingress_enabled ? [1] : []

    content {
      description = var.ingress_description
      from_port   = var.ingress_from_port
      to_port     = var.ingress_to_port
      protocol    = var.ingress_protocol
      cidr_blocks = var.ingress_cidr_blocks
    }
  }

  tags = var.tags
}
