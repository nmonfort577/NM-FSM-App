# mysql-ami.pkr.hcl - Putting It All Together

packer {
  required_plugins {
    amazon  = { source = "github.com/hashicorp/amazon", version = "~> 1" }
    ansible = { source = "github.com/hashicorp/ansible", version = "~> 1" }
  }
}

locals {
  timestamp = formatdate("YYYYMMDDhhmmss", timestamp())
  ami_name  = "mysql-golden-${local.timestamp}"
}

source "amazon-ebs" "mysql" {
  region = "us-east-1"
  source_ami_filter {
    filters     = { name = "al2023-ami-2023.*-x86_64", root-device-type = "ebs", virtualization-type = "hvm" }
    most_recent = true
    owners      = ["amazon"]
  }
  instance_type               = "t3.micro"
  ssh_username                = "ec2-user"
  communicator                = "ssh"
  ssh_interface               = "private_ip"
  iam_instance_profile        = "LabInstanceProfile"
  security_group_id           = "sg-03639ecb8a67176d0"
  subnet_id                   = "subnet-0f8d022ffb51970a0"
  ami_name                    = local.ami_name
  associate_public_ip_address = true
  tags                        = { Name = local.ami_name, BuiltBy = "packer", Module = "mysql" }
}

build {
  sources = ["source.amazon-ebs.mysql"]
  provisioner "shell" {
    inline = ["sudo dnf update -y", "sudo dnf install -y python3"]
  }
  provisioner "ansible" {
    playbook_file    = "./site.yml"
    user             = "ec2-user"
    use_proxy        = false
    ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
    groups           = ["dbservers"]
  }
  post-processor "manifest" {
    output     = "ami-manifest.json"
    strip_path = true
  }
}

