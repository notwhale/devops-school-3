variable "namespace" {
  description = "Namespace"
  default     = "tf"
  type        = string
}

variable "owner" {
  description = "Owner"
  default       = "User"
  type        = string
}

variable "project" {
  description = "Project"
  default     = "Terraform"
  type        = string
}

variable "environment" {
  description = "Environment"
  default     = "Prod"
  type        = string
}

variable "region" {
  description = "AWS region"
  default     = "us-east-1"
  type        = string
}
variable "profile" {
    description = "AWS CLI profile"
    default     = "default"
    type        = string
}