output "bastion_public_ip" {
  value = aws_instance.ec2_bastion.public_ip
}

output "host1_private_ip" {
  value = aws_instance.ec2_host1.private_ip
}

output "host2_private_ip" {
  value = aws_instance.ec2_host2.private_ip
}

output "host1_id" {
  value = aws_instance.ec2_host1.id
}

output "host2_id" {
  value = aws_instance.ec2_host2.id
}

output "ec2_profile" {
  value = aws_iam_instance_profile.ec2_profile.arn
}