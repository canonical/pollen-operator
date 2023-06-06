#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

https://discourse.charmhub.io/t/4208
"""

import logging

import ops
from charms.grafana_agent.v0.cos_agent import COSAgentProvider
from ops.model import ActiveStatus, MaintenanceStatus

import pollen
from charm_state import CharmState

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

class PollenOperatorCharm(ops.CharmBase):
    """Charm the service."""

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
        self.framework.observe(self.on.website_relation_joined, self._on_website_relation_joined)
        self._grafana_agent = COSAgentProvider(
            self,
            metrics_endpoints=[
                {"path": "/metrics", "port": 443},
            ],
            metrics_rules_dir="./src/prometheus_alert_rules",
            logs_rules_dir="./src/loki_alert_rules",
            dashboard_dirs=["./src/grafana_dashboards"],
            log_slots=["pollen:logs"],
        )

    def _on_website_relation_joined(self, event: ops.RelationJoinedEvent):
        """Handle website-relation-joined.

        Args:
            event: Event triggering the website relation joined handler.
        """
        hostname = self.model.get_binding("website").network.bind_address
        self.website = CharmState.website(hostname)
    
    def _on_install(self, event: ops.InstallEvent):
        """Handle install.

        Args:
            event: Event triggering the install handler.
        """
        self.unit.status = MaintenanceStatus("Installing dependencies")
        pollen.prepare_pollen()
    
    def _on_upgrade_charm(self, event: ops.UpgradeCharmEvent):
        """Handle upgrade-charm.

        Args:
            event: Event triggering the upgrade-charm handler.
        """
        self.unit.status = MaintenanceStatus("Upgrading dependencies")
        pollen.prepare_pollen()
        self.unit.status = ActiveStatus("Ready")
    
    def _on_start(self, event: ops.StartEvent):
        """Handle start.

        Args:
            event: Event triggering the start handler.
        """
        pollen.start_pollen()
        self.unit.status = ActiveStatus("Ready")

    def _on_stop(self, event: ops.StopEvent):
        """Handle stop.

        Args:
            event: Event triggering the stop handler.
        """
        pollen.stop_pollen()

if __name__ == "__main__":  # pragma: nocover
    ops.main(PollenOperatorCharm)
