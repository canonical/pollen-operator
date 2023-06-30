# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Pollen charm business logic."""

import glob
import subprocess
from pathlib import Path

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
            InstallError: if the packages fail to install
            ConfigurationWriteError: something went wrong writing the configuration
        """
        try:
            apt.update()
            snap.add(SNAP_NAME, channel="candidate")
        except FileNotFoundError as exc:
            raise InstallError from exc
        try:
            subprocess.run(
                [
                    "rsync",
                    f"/var/lib/juju/agents/unit-{unit_name}/charm/files/logrotate.conf",
                    "/etc/logrotate.d/pollen",
                ],
                check=True,
            )
            subprocess.run(
                [
                    "rsync",
                    f"/var/lib/juju/agents/unit-{unit_name}/charm/files/rsyslog.conf",
                    "/etc/rsyslog.d/40-pollen.conf",
                ],
                check=True,
            )
            systemd.service_restart("rsyslog.service")
        except (FileNotFoundError, systemd.SystemdError) as exc:
            raise ConfigurationWriteError from exc
        if (
            glob.glob("/dev/tpm*")
            or Path("/sys/class/misc/hw_random/rng_available").read_text(encoding="utf-8")
            != "tpm-rng-0"
        ):
            try:
                apt.add_package("rng-tools5")
                self.check_rng_file(charm_state)
                systemd.service_restart("rngd.service")
            except FileNotFoundError as exc:
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

    def check_rng_file(self, charm_state):
        """Check if the rng-tools-debian file needs modification.

        Args:
            charm_state: Pollen charm's CharmState instance.
        """
        file = Path("/etc/default/rng-tools-debian")
        charm_state.rng_tools_file = (
            None
            if 2
            > file.read_text(encoding="utf-8").count(
                'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
            )
            else 'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
        )
        if not charm_state.rng_tools_file:
            charm_state.rng_tools_file = 'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
            file.write_text(f"\n{charm_state.rng_tools_file}", encoding="utf-8")
