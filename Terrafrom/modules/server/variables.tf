variable "server_name" {
  type = string

  default = "server name"
}

variable "instance_type" {
  default = "t2.micro"

}

variable "create_dns" {
  type    = bool
  default = true
}

