# variables.tf — declarations only (no values here)
variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "az" {
  type        = string
  description = "Availability zone for EBS volumes"
  default     = "us-east-1a"
}
variable "db_instance_type" {
  type    = string
  default = "t3.micro"
}
variable "environment" {
  type    = string
  default = "course"
}
# -- Environment IP map (keyed by workspace) --
variable "db_ip" {
  type = map(string)
  default = {
    staging    = "172.31.133.10"
    production = "172.31.133.11"
  }
}
variable "db_name" {
  type    = string
  default = "fsm_db"
}
variable "db_user" {
  type    = string
  default = "flaskapp"
}
variable "db_password" {
  type      = string
  sensitive = true
}
# -- Docker image tag (overridden in Module 5 via -var) --
variable "flask_image_tag" {
  type    = string
  default = "latest"
}