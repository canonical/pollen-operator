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
import os
from subprocess import STDOUT, check_call

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
        #self.framework.observe(self.on.start, self._on_start)
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

    def _on_website_relation_joined(self, event: ops.PebbleReadyEvent):
        """Handle website-relation-joined.

        Args:
            event: Event triggering the website relation joined handler.
        """
        hostname = self.model.get_binding("website").network.bind_address
        self.website = CharmState.website(hostname)
    
    def _on_install(self, event: ops.PebbleReadyEvent):
        """Handle install.

        Args:
            event: Event triggering the install handler.
        """
        self.unit.status = MaintenanceStatus("Installing dependencies")
        pollen.prepare_pollen()
    
    def _on_start(self, event: ops.PebbleReadyEvent):
        """Handle start.

        Args:
            event: Event triggering the start handler.
        """
        check_call(['systemctl', 'restart', 'pollen.service'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT, shell=True)
        self.unit.status = ActiveStatus("Ready")

    def _on_stop(self, event: ops.PebbleReadyEvent):
        """Handle stop.

        Args:
            event: Event triggering the stop handler.
        """
        check_call(['systemctl', 'stop', 'pollen.service'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT, shell=True)

if __name__ == "__main__":  # pragma: nocover
    ops.main(PollenOperatorCharm)
