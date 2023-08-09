#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm for Pollen on a machine."""

import logging

import ops
from charms.grafana_agent.v0.cos_agent import COSAgentProvider
from ops.model import ActiveStatus, MaintenanceStatus

from charm_state import CharmState
from pollen import PollenService

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

METRICS_PORT = 2112


class PollenOperatorCharm(ops.CharmBase):
    """Charm the Pollen service."""

    def __init__(self, *args):
        """Construct.

        Args:
            args: Arguments from the parent CharmBase constructor.
        """
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.stop, self._on_stop)
        self.framework.observe(self.on.website_relation_changed, self._on_website_relation_changed)
        self._grafana_agent = COSAgentProvider(
            self,
            metrics_endpoints=[
                {"path": "/metrics", "port": METRICS_PORT},
            ],
            metrics_rules_dir="./src/prometheus_alert_rules",
            dashboard_dirs=["./src/grafana_dashboards"],
        )
        self.pollen = PollenService()
        self._charm_state = CharmState.from_charm(self)

    def _on_website_relation_changed(self, event: ops.RelationChangedEvent):
        """Handle website-relation-changed.

        Args:
            event: Event triggering the website relation joined handler.
        """
        event.relation.data[self.unit].update(self._charm_state.website)

    def _on_install(self, event: ops.InstallEvent):
        """Handle install.

        Args:
            event: Event triggering the install handler.
        """
        self.unit.status = MaintenanceStatus("Installing dependencies")
        self.pollen.prepare(str(self.unit.name).replace("/", "-"))

    def _on_upgrade_charm(self, event: ops.UpgradeCharmEvent):
        """Handle upgrade-charm.

        Args:
            event: Event triggering the upgrade-charm handler.
        """
        self.unit.status = MaintenanceStatus("Upgrading dependencies")
        self.pollen.prepare(str(self.unit.name).replace("/", "-"))
        self.unit.status = ActiveStatus()

    def _on_start(self, event: ops.StartEvent):
        """Handle start.

        Args:
            event: Event triggering the start handler.
        """
        self.pollen.start()
        self.unit.status = ActiveStatus()

    def _on_stop(self, event: ops.StopEvent):
        """Handle stop.

        Args:
            event: Event triggering the stop handler.
        """
        self.pollen.stop()


if __name__ == "__main__":  # pragma: nocover
    ops.main(PollenOperatorCharm)
