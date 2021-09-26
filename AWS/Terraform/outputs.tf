output "add_ssh_key" {
  description = "add ssh key"
  value       = "ssh-add -k ${module.ssh-key.key_name}.pem"
}

output "bastion_connection" {
  description = "Bastion host"
  value       = "ssh ec2-user@${module.ec2.bastion_public_ip}"
}

output "host1_connection" {
  description = "Private host1"
  value       = "ssh -AJ ec2-user@${module.ec2.bastion_public_ip} ec2-user@${module.ec2.host1_private_ip}"
}

output "host2_connection" {
  description = "Private host2"
  value       = "ssh -AJ ec2-user@${module.ec2.bastion_public_ip} ec2-user@${module.ec2.host2_private_ip}"
}

output "load_balancer_dns" {
  description = "Application load balancer link"
  value = "http://${module.alb.lb_dns_name}"
}
