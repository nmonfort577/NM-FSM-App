# networking.tf — private subnet, routing, security groups

# -- 1. Private subnet (Terraform owns this) ------------------
resource "aws_subnet" "private" {
  vpc_id            = data.aws_vpc.main.id
  cidr_block        = "172.31.133.0/24"
  availability_zone = var.az
  tags              = { Name = "AWS-VPCB-PRIVATE" }
}

# -- 2. Route table — directs private traffic via Control Node -
resource "aws_route_table" "private" {
  vpc_id = data.aws_vpc.main.id
  route {
    cidr_block           = "0.0.0.0/0"
    network_interface_id = data.aws_network_interface.nat.id
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# -- 3. Security group — MySQL (port 3306) ---------------------
resource "aws_security_group" "mysql" {
  name   = "mysql-sg"
  vpc_id = data.aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.fargate.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# -- 4. Security group — ECS Fargate (HTTP 5000) ---------------
resource "aws_security_group" "fargate" {
  name   = "fargate-sg"
  vpc_id = data.aws_vpc.main.id
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}