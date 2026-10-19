# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

variable "app_name" {
  description = "Name of the application in the Juju model."
  type        = string
  default     = "pollen"
  nullable    = false
}

variable "base" {
  description = "The operating system on which to deploy"
  type        = string
  default     = null
}

variable "channel" {
  description = "The channel to use when deploying a charm."
  type        = string
  default     = "latest/edge"
  nullable    = false
}

variable "config" {
  description = "Application config. Details about available options can be found at https://charmhub.io/pollen/configurations"
  type        = map(string)
  default     = {}
}

variable "constraints" {
  description = "Juju constraints to apply for this application."
  type        = string
  default     = null
}

variable "model_uuid" {
  description = "UUID of the Juju model where the application will be deployed."
  type        = string
  nullable    = false
}

variable "revision" {
  description = "Revision number of the charm"
  type        = number
  default     = null
}

variable "units" {
  description = "The number of units to deploy"
  type        = number
  default     = 1
}
