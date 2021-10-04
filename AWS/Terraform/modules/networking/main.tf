data "aws_availability_zones" "available" {}

module "vpc1" {
  source = "terraform-aws-modules/vpc/aws"
  name                             = "${var.namespace}-VPC1"
  cidr                             = "10.0.0.0/16"
  azs                              = data.aws_availability_zones.available.names
  public_subnets                   = ["10.0.0.0/24"]
  private_subnets                  = ["10.0.100.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
}

module "vpc2" {
  source = "terraform-aws-modules/vpc/aws"
  name                             = "${var.namespace}-VPC2"
  cidr                             = "10.100.0.0/16"
  azs                              = data.aws_availability_zones.available.names
  public_subnets                   = ["10.100.0.0/24", "10.100.1.0/24"]
  private_subnets                  = ["10.100.100.0/24", "10.100.101.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
}

module "vpc1_sg_public" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "vpc1_sg_public"
  description = "vpc1_sg_public"
  vpc_id      = module.vpc1.vpc_id

  ingress_with_cidr_blocks = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow SSH"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 8
      to_port     = 0
      protocol    = "icmp"
      description = "Allow ICMP from VPC1"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 8
      to_port     = 0
      protocol    = "icmp"
      description = "Allow ICMP from VPC2"
      cidr_blocks = module.vpc2.vpc_cidr_block
    },
  ]
  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]
}

module "vpc1_sg_private" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "vpc1_sg_private"
  description = "vpc1_sg_private"
  vpc_id      = module.vpc1.vpc_id

  ingress_with_cidr_blocks = [
    {
      from_port   = 8
      to_port     = 0
      protocol    = "icmp"
      description = "Allow ICM from VPC1"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 8
      to_port     = 0
      protocol    = "icmp"
      description = "Allow ICMP from VC2"
      cidr_blocks = module.vpc2.vpc_cidr_block
    },
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow SSH from VPC1"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow SSH from VPC2"
      cidr_blocks = module.vpc2.vpc_cidr_block
    },
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      description = "Allow HTTP"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 8888
      to_port     = 8888
      protocol    = "tcp"
      description = "Allow 8888 from VPC1"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 8888
      to_port     = 8888
      protocol    = "tcp"
      description = "Allow 8888 from VPC2"
      cidr_blocks = module.vpc2.vpc_cidr_block
    },
  ]
  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]
}

module "vpc2_sg_public" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "vpc2_sg_public"
  description = "vpc2_sg_public"
  vpc_id      = module.vpc2.vpc_id

  ingress_with_cidr_blocks = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow SSH"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      description = "Allow HTTP"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 8
      to_port     = 0
      protocol    = "icmp"
      description = "Allow ICMP"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
  ]
  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]
}

module "vpc2_sg_private" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "vpc2_sg_private"
  description = "vpc2_sg_private"
  vpc_id      = module.vpc2.vpc_id

  ingress_with_cidr_blocks = [
    {
      from_port   = 8
      to_port     = 0
      protocol    = "icmp"
      description = "Allow ICMP"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow SSH"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      description = "Allow HTTP"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 8888
      to_port     = 8888
      protocol    = "tcp"
      description = "Allow 8888 from VPC1"
      cidr_blocks = module.vpc1.vpc_cidr_block
    },
    {
      from_port   = 8888
      to_port     = 8888
      protocol    = "tcp"
      description = "Allow 8888 from VPC2"
      cidr_blocks = module.vpc2.vpc_cidr_block
    },
  ]
  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_vpc_peering_connection" "peer" {
  peer_vpc_id = module.vpc2.vpc_id
  vpc_id      = module.vpc1.vpc_id
  auto_accept = true

  accepter {
    allow_remote_vpc_dns_resolution = true
  }

  requester {
    allow_remote_vpc_dns_resolution = true
  }

  tags = {
    Name = "VPC1 to VPC2 peering"
  }
}

resource "aws_route" "vpc-peering-route-VPC1-public" {
  count                     = length(module.vpc1.public_route_table_ids)
  route_table_id            = module.vpc1.public_route_table_ids[count.index]
  destination_cidr_block    = module.vpc2.vpc_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}

resource "aws_route" "vpc-peering-route-VPC1-private" {
  count                     = length(module.vpc1.private_route_table_ids)
  route_table_id            = module.vpc1.private_route_table_ids[count.index]
  destination_cidr_block    = module.vpc2.vpc_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}

resource "aws_route" "vpc-peering-route-VPC2-public" {
  count                     = length(module.vpc2.public_route_table_ids)
  route_table_id            = module.vpc2.public_route_table_ids[count.index]
  destination_cidr_block    = module.vpc1.vpc_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}

resource "aws_route" "vpc-peering-route-VPC2-private" {
  count                     = length(module.vpc2.private_route_table_ids)
  route_table_id            = module.vpc2.private_route_table_ids[count.index]
  destination_cidr_block    = module.vpc1.vpc_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}

module "vpc1-endpoints" {
  source = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"

  vpc_id             = module.vpc1.vpc_id
  security_group_ids = [module.vpc1_sg_private.security_group_id]

  endpoints = {
    s3 = {
      service         = "s3"
      service_type    = "Gateway"
      route_table_ids = flatten([module.vpc1.private_route_table_ids])
      policy          = data.aws_iam_policy_document.s3_endpoint_policy.json
      tags            = { Name = "s3-vpc1-endpoint" }
    }
  }
}

module "vpc2-endpoints" {
  source = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"

  vpc_id             = module.vpc2.vpc_id
  security_group_ids = [module.vpc2_sg_private.security_group_id]

  endpoints = {
    s3 = {
      service         = "s3"
      service_type    = "Gateway"
      route_table_ids = flatten([module.vpc2.private_route_table_ids])
      policy          = data.aws_iam_policy_document.s3_endpoint_policy.json
      tags            = { Name = "s3-vpc2-endpoint" }
    }
  }
}

data "aws_vpc_endpoint_service" "s3" {
  service = "s3"

  filter {
    name   = "service-type"
    values = ["Gateway"]
  }
}

data "aws_iam_policy_document" "s3_endpoint_policy" {
  statement {
    effect    = "Allow"
    actions   = [
      "s3:Get*",
      "s3:List*"
    ]
    resources = [
      # "arn:aws:s3:::amazonlinux.us-east-1.amazonaws.com/*",
      # "arn:aws:s3:::amazonlinux-2-repos-us-east-1/*"
      "*"
    ]

    principals {
      type        = "*"
      identifiers = ["*"]
    }
/*
    condition {
      test     = "StringNotEquals"
      variable = "aws:sourceVpce"

      values = [data.aws_vpc_endpoint_service.s3.id]
    }*/
  }
}
