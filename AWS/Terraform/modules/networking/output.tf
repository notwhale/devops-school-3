output "vpc1" {
  value = module.vpc1
}

output "vpc2" {
  value = module.vpc2
}

output "vpc1_sg_public_id" {
  value = module.vpc1_sg_public.security_group_id
}

output "vpc1_sg_private_id" {
  value = module.vpc1_sg_private.security_group_id
}

output "vpc2_sg_public_id" {
  value = module.vpc2_sg_public.security_group_id
}

output "vpc2_sg_private_id" {
  value = module.vpc2_sg_private.security_group_id
}