terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
  # No profile/credentials block needed -
  # EC2 Instance Role supplies auth automatically

  default_tags {
    tags = {
      Course      = "CIS-4641"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}