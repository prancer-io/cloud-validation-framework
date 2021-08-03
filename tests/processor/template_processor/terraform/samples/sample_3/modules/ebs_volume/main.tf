resource "aws_ebs_volume" "volume" {
  availability_zone = var.availability_zone
  encrypted         = var.encrypted
  size              = var.size
  tags              = var.tags

  lifecycle {
    prevent_destroy = false
  }
}
