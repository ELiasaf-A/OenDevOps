module "jenkins" {
  source      = "../../../modules/server"
  server_name = "jenkins prod"
  create_dns  = true

}