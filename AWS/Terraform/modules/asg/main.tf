module "asg" {
  source  = "terraform-aws-modules/autoscaling/aws"

  name                      = "${var.namespace}-ASG"
  lc_use_name_prefix        = false
  lt_use_name_prefix        = false
  min_size                  = 0
  desired_capacity          = 0
  max_size                  = 0
  wait_for_capacity_timeout = 0
  health_check_type         = "EC2"
  health_check_grace_period = 30
  default_cooldown          = 30
  vpc_zone_identifier       = var.subnets
  security_groups           = [var.security_groups]
  target_group_arns         = var.target_group_arns
  lt_name                   = "${var.namespace}-LT"
  description               = "${var.namespace}-LT"
  update_default_version    = true
  enable_monitoring         = true
  use_lt                    = true
  create_lt                 = true
  image_id                  = var.ami_id
  instance_type             = "t2.micro"
  key_name                  = var.key_name
  iam_instance_profile_arn  = var.ec2_profile
  user_data_base64          = base64encode("${file("${path.module}/../scripts/nginx.sh")}")
  tag_specifications        = [
    {
      resource_type = "instance"
      tags          = {
        "Name"        = "${var.namespace}-EC2-ASG"
        "owner"       = "${var.owner}"
        "project"     = "${var.project}"
        "environment" = "${var.environment}"
        }
    },
    {
      resource_type = "volume"
      tags          = {
        "Name"        = "${var.namespace}-VOL-ASG"
        "owner"       = "${var.owner}"
        "project"     = "${var.project}"
        "environment" = "${var.environment}"
        }
    },
  ]
}

resource "aws_autoscaling_policy" "asg_policy" {
  name                   = "${var.namespace}-ASG-Policy"
  policy_type            = "TargetTrackingScaling"
  autoscaling_group_name = module.asg.autoscaling_group_name

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 50.0
  }
}