# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Pollen charm business logic."""

import glob
from pathlib import Path
import os

from charms.operator_libs_linux.v0 import apt
from charms.operator_libs_linux.v1 import systemd
from charms.operator_libs_linux.v2 import snap

from exceptions import ConfigurationWriteError, InstallError

SNAP_NAME = "gtrkiller-pollen"


class PollenService:
    """Pollen service class."""

    def prepare(self, unit_name, charm_state) -> None:
        """Install packages and write configuration files.

        Args:
            unit_name: ¨Pollen charm's unit name.
            charm_state: Pollen charm's CharmState instance.

        Raises:
            InstallError: if the snap fails to install
            ConfigurationWriteError: something went wrong writing the configuration
        """
        try:
            snap.add(SNAP_NAME, channel="candidate")
        except snap.SnapError as exc:
            raise InstallError from exc
        try:
            logrotate_src = Path(
                f"/var/lib/juju/agents/unit-{unit_name}/charm/files/logrotate.conf"
            )
            logrotate_dest = Path("/etc/logrotate.d/pollen")
            logrotate_dest.write_bytes(logrotate_src.read_bytes())
            rsyslog_src = Path(f"/var/lib/juju/agents/unit-{unit_name}/charm/files/rsyslog.conf")
            rsyslog_dest = Path("/etc/rsyslog.d/40-pollen.conf")
            rsyslog_dest.write_bytes(rsyslog_src.read_bytes())
            systemd.service_restart("rsyslog.service")
        except (FileNotFoundError, systemd.SystemdError) as exc:
            raise ConfigurationWriteError from exc
        # Check for the existence of the /dev/tpm* pattern on the
        # folders or if the rng_available file has something else than the
        # standard non-hardware rng generator.
        if (
            glob.glob("/dev/tpm*")
            or Path("/sys/class/misc/hw_random/rng_available").read_text(encoding="utf-8")
            != "tpm-rng-0"
        ):
            try:
                apt.update()
                apt.add_package("rng-tools5")
                charm_state.check_rng_file()
                systemd.service_restart("rngd.service")
            except (systemd.SystemdError) as exc:
                raise ConfigurationWriteError from exc

    def start(self):
        """Start the pollen service."""
        cache = snap.SnapCache()
        pollen = cache[SNAP_NAME]
        pollen.start()

    def stop(self):
        """Stop the pollen service."""
        cache = snap.SnapCache()
        pollen = cache[SNAP_NAME]
        pollen.stop()
