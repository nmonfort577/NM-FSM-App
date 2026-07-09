# ecs.tf
resource "aws_ecs_cluster" "main" {
  name = "cis4641-cluster"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}
resource "aws_ecs_service" "app" {
  name            = "flask-${terraform.workspace}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [aws_subnet.private.id]
    security_groups  = [aws_security_group.fargate.id]
    assign_public_ip = true
  }
}
resource "aws_ecs_task_definition" "app" {
  family                   = "flask-${terraform.workspace}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = data.aws_iam_role.lab.arn
  container_definitions = jsonencode([{
    name         = "flask-app"
    image        = "${aws_ecr_repository.flask_app.repository_url}:latest"
    portMappings = [{ containerPort = 5000, protocol = "tcp" }]
    environment = [
      { name = "DATABASE_URL"
      value = "mysql+pymysql://${var.db_user}:${var.db_password}@${var.db_ip[terraform.workspace]}/${var.db_name}" }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/flask-${terraform.workspace}"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}
resource "aws_ecr_repository" "flask_app" {
  name                 = "nm-fsm-app"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # allows destroy even with images
  tags                 = { Name = "nm-fsm-app" }
}
