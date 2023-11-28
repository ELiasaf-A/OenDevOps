module "record" {
  count       = 10
  source      = "../dns"
  record_ip   = aws_instance.web.private_ip
  record_name = format("jenkins-%02d", count.index + 1)

}



