# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""General configuration module for integration tests."""
import json
from pathlib import Path
from typing import Any, Awaitable, Callable

import pytest_asyncio
import yaml
from ops.model import ActiveStatus
from pytest import fixture
from pytest_operator.plugin import OpsTest


@fixture(scope="module")
def metadata():
    """Provide charm metadata."""
    yield yaml.safe_load(Path("./metadata.yaml").read_text())


@fixture(scope="module")
def app_name(metadata):
    """Provide app name from the metadata."""
    yield metadata["name"]


@fixture(scope="module")
def run_action(ops_test: OpsTest) -> Callable[[str, str], Awaitable[Any]]:
    """Create a async function to run action and return results."""

    async def _run_action(application_name: str, action_name: str, **params):
        """Run a specified action.

        Args:
            application_name: Name the application is deployed with.
            action_name: Name of the action to be executed.
            params: Dictionary with action parameters.

        Returns:
            The results of the executed action
        """
        application = ops_test.model.applications[application_name]
        action = await application.units[0].run_action(action_name, **params)
        await action.wait()
        return action.results

    return _run_action


@pytest_asyncio.fixture(scope="module")
async def app(
    ops_test: OpsTest,
    app_name: str,
    run_action,
):
    """Pollen charm used for integration testing.

    Deploy any-charm charm, builds the charm and deploys it for testing purposes.
    """
    any_app_name = "any-app"
    any_charm_script = Path("tests/integration/any_charm.py").read_text()

    any_charm_src_overwrite = {
        "any_charm.py": any_charm_script,
    }

    await ops_test.model.deploy(
        "any-charm",
        application_name=any_app_name,
        channel="beta",
        config={"src-overwrite": json.dumps(any_charm_src_overwrite)},
    )
    await ops_test.model.wait_for_idle(status="active")

    app_charm = await ops_test.build_charm(".")
    application = await ops_test.model.deploy(
        app_charm,
        application_name=app_name,
        series="jammy",
    )
    await ops_test.model.add_relation(f"{any_app_name}:require-http", f"{app_name}:website")
    apps = [app_name, any_app_name]
    await ops_test.model.wait_for_idle(apps=apps, status=ActiveStatus.name, timeout=60 * 5)
    assert ops_test.model.applications[app_name].units[0].workload_status == ActiveStatus.name
    assert ops_test.model.applications[any_app_name].units[0].workload_status == ActiveStatus.name

    yield application
