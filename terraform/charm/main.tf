# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

resource "juju_application" "pollen" {
  name       = var.app_name
  model_uuid = var.model_uuid

  charm {
    name     = "pollen"
    channel  = var.channel
    revision = var.revision
    base     = var.base
  }

  config      = var.config
  constraints = var.constraints
  units       = var.units
}
