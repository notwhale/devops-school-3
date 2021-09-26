module "networking" {
  source    = "./modules/networking"
  namespace = var.namespace
  region    = var.region
}

module "ssh-key" {
  source    = "./modules/ssh-key"
  namespace = var.namespace
}

module "ami" {
  source = "./modules/ami"
}
module "ec2" {
  source             = "./modules/ec2"
  namespace          = var.namespace
  owner              = var.owner
  project            = var.project
  environment        = var.environment
  ami_id             = module.ami.ami_id
  vpc1               = module.networking.vpc1
  vpc2               = module.networking.vpc2
  vpc1_sg_public_id  = module.networking.vpc1_sg_public_id
  vpc1_sg_private_id = module.networking.vpc1_sg_private_id
  vpc2_sg_public_id  = module.networking.vpc2_sg_public_id
  vpc2_sg_private_id = module.networking.vpc2_sg_private_id
  key_name           = module.ssh-key.key_name
  region             = var.region
}

module "alb" {
  source            = "./modules/alb"
  namespace         = var.namespace
  vpc               = module.networking.vpc2.vpc_id
  subnets           = module.networking.vpc2.public_subnets
  security_groups   = module.networking.vpc2_sg_public_id
  host1_id          = module.ec2.host1_id
  host2_id          = module.ec2.host2_id
}

module "asg" {
  source            = "./modules/asg"
  namespace         = var.namespace
  owner             = var.owner
  project           = var.project
  environment       = var.environment
  ami_id            = module.ami.ami_id
  key_name          = module.ssh-key.key_name
  subnets           = module.networking.vpc2.public_subnets
  security_groups   = module.networking.vpc2_sg_private_id
  target_group_arns = module.alb.target_group_arns
  ec2_profile       = module.ec2.ec2_profile
}