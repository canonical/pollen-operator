# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

output "application" {
  description = "The deployed application object."
  value       = juju_application.pollen
}

output "provides" {
  description = "Map of the provided integration endpoints."
  value = {
    cos_agent = {
      kind     = "endpoint"
      name     = juju_application.pollen.name
      endpoint = "cos-agent"
    }
    website = {
      kind     = "endpoint"
      name     = juju_application.pollen.name
      endpoint = "website"
    }
  }
}

output "requires" {
  description = "Map of the required integration endpoints."
  value = {
    haproxy_route = {
      kind     = "endpoint"
      name     = juju_application.pollen.name
      endpoint = "haproxy_route"
    }
  }
}
