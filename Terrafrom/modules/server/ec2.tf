resource "aws_instance" "web" {
  ami           = "ami-namber"
  instance_type = var.instance_type
  tags          = {
    Name = var.server_name
  }
}
