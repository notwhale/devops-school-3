module "alb" {
  source  = "terraform-aws-modules/alb/aws"

  name = "${var.namespace}-ALB"

  load_balancer_type = "application"

  vpc_id             = var.vpc
  subnets            = var.subnets
  security_groups    = [var.security_groups]

  target_groups = [
    {
      name             = "${var.namespace}-TG"
      backend_protocol = "HTTP"
      backend_port     = 8888
      target_type      = "instance"
      targets = [
        {
        #   target_id = data.aws_instance.host1.id
          target_id = var.host1_id
        },
        {
        #   target_id = data.aws_instance.host2.id
          target_id = var.host2_id
        }
      ]
    }
  ]

  http_tcp_listeners = [
    {
      port               = 80
      protocol           = "HTTP"
      target_group_index = 0
    }
  ]

  tags = {
    Name = "${var.namespace}-TG"
  }
}