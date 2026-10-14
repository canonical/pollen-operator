# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

run "setup_tests" {
  module {
    source = "./tests/setup"
  }
}

run "basic_deploy" {
  variables {
    model_uuid = run.setup_tests.model_uuid
    base       = "ubuntu@22.04"
    channel    = "latest/edge"
    # renovate: depName="pollen"
    revision = 64
  }

  assert {
    condition     = output.application.name == "pollen"
    error_message = "pollen application name did not match expected"
  }

  assert {
    condition     = output.provides.value.endpoint == "cos-agent"
    error_message = "pollen module should provide 'provides.value' output"
  }

  assert {
    condition     = output.provides.website.endpoint == "website"
    error_message = "pollen module should provide 'provides.website' output"
  }

  assert {
    condition     = output.requires.value.endpoint == "haproxy_route"
    error_message = "pollen module should provide 'requires.value' output"
  }
}
