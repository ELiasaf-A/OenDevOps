resource "aws_route53_record" "b" {
  name    = var.record_name
  records = [var.record_ip]
  type    = "A"
  zone_id = "AA"

}

variable "record_name" {}
variable "record_ip" {}


