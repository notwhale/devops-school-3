variable "namespace" {
  type = string
}

variable "owner" {
  type = string
}

variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "key_name" {
  type = string
}

variable "subnets" {
  type = any
}

variable "security_groups" {
  type = any
}

variable "target_group_arns" {
  type = any
}

variable "ec2_profile" {
  type = any
}

variable "ami_id" {
  type = string
}