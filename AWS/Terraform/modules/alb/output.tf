output "alb" {
  value = module.alb
}

output "lb_dns_name" {
  description = "The DNS name of the load balancer."
  value       = module.alb.lb_dns_name
}

output "target_group_arns" {
  description = "Target group arns"
  value       = module.alb.target_group_arns
}