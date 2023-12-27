variable "project_id" {
  type        = string
  description = "ID of the google project"
}

variable "region" {
  type        = string
  description = "Region google project"
}

variable "resource_prefix" {
  type        = string
  description = "Prefix to add to each ressource of this project"
}

variable "environment" {
  type        = string
  description = "name of the current environment"
  default = "prod"
}