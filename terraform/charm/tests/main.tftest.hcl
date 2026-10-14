# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

variables {
  app_name    = "pollen"
  base        = "ubuntu@22.04"
  channel     = "latest/edge"
  config      = {}
  constraints = "arch=amd64"
  model_uuid  = "00000000-0000-0000-0000-000000000001"
  revision    = 10
  units       = 2
}

mock_provider "juju" {
  mock_resource "juju_application" {
    override_during = plan
    defaults = {
      id         = "pollen"
      model_type = "lxd"
    }
  }
}

run "deploys_application" {
  command = plan

  assert {
    condition     = output.application.name == "pollen" && output.application.model_uuid == "00000000-0000-0000-0000-000000000001" && output.application.charm[0].name == "pollen" && output.application.charm[0].channel == "latest/edge" && output.application.charm[0].base == "ubuntu@22.04" && output.application.charm[0].revision == 10
    error_message = "application identity did not match the expected deployment"
  }

  assert {
    condition     = output.application.constraints == "arch=amd64"
    error_message = "application constraints did not match expected"
  }

  assert {
    condition     = output.application.units == 2
    error_message = "application units did not match expected"
  }

  assert {
    condition = output.provides == {
      cos_agent = {
        kind     = "endpoint"
        name     = "pollen"
        endpoint = "cos-agent"
      }
      website = {
        kind     = "endpoint"
        name     = "pollen"
        endpoint = "website"
      }
    }
    error_message = "provided relation outputs did not match expected structure"
  }

  assert {
    condition = output.requires == {
      haproxy_route = {
        kind     = "endpoint"
        name     = "pollen"
        endpoint = "haproxy_route"
      }
    }
    error_message = "required relation outputs did not match expected structure"
  }
}
