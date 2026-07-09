# outputs.tf - values printed after terraform apply
# These are also readable by other Terraform configs

# -- ECR repository URL (needed in Module 5 for docker push) --
output "ecr_repository_url" {
  description = "Push Docker images here in Module 5"
  value       = aws_ecr_repository.flask_app.repository_url
}

# -- MySQL private IPs (useful for debugging SSH tunnels) --
output "db_private_ip" {
  description = "MySQL IP for current workspace"
  value       = aws_instance.mysql_db.private_ip
}

# production output handled by Jenkins in Module 6

# -- ECS service names (useful for aws ecs describe-services) --
output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}
