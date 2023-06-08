# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration test module."""

import json

import pytest
from ops.model import ActiveStatus, Application

ANY_APP_NAME = "any-app"


@pytest.mark.asyncio
@pytest.mark.abort_on_fail
async def test_active(app: Application):
    """
    arrange: given charm has been built, deployed and related to a dependent application
    act: when the status is checked
    assert: then the workload status is active.
    """
    assert app.units[0].workload_status == ActiveStatus.name


@pytest.mark.asyncio
async def test_website_relation(app: Application, run_action):
    """
    arrange: given charm has been built and deployed,
    act: update the additional-hostnames option in the nginx-route relation using any-charm.
    assert: HTTP request with the additional-hostnames value as the host header should be
        forwarded to the application correctly. And the additional-hostnames should exist
        in the nginx-route relation data.
    """
    action_result = await run_action(ANY_APP_NAME, "get-relation-data")
    relation_data = json.loads(action_result["relation-data"])[0]
    assert "hostname" and "port" in relation_data["application_data"]["pollen"]
