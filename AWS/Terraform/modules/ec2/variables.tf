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

variable "ami_id" {
  type = string
}

variable "vpc1" {
  type = any
}

variable "vpc2" {
  type = any
}

variable "key_name" {
  type = string
}

variable "vpc1_sg_public_id" {
  type = any
}

variable "vpc1_sg_private_id" {
  type = any
}

variable "vpc2_sg_public_id" {
  type = any
}

variable "vpc2_sg_private_id" {
  type = any
}

variable "region" {
  type = string
}