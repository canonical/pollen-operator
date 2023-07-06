# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Pollen charm business logic."""

import glob
from pathlib import Path

from charms.operator_libs_linux.v0 import apt
from charms.operator_libs_linux.v1 import systemd
from charms.operator_libs_linux.v2 import snap

from exceptions import ConfigurationWriteError, InstallError

SNAP_NAME = "gtrkiller-pollen"
RNG_FILE_VALUE = 'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'


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
                self.check_rng_file(charm_state)
                systemd.service_restart("rngd.service")
            except systemd.SystemdError as exc:
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
        # The file already has this line commented by default,
        # so we should check if it appears in the file twice (commented and actually written).
        # The file needs the commented code header so the rngd service does not fail.
        if (
            RNG_FILE_VALUE in charm_state.rng_tools_file
            and f"# {RNG_FILE_VALUE}" not in charm_state.rng_tools_file
        ):
            charm_state.rng_tools_file = ""
            return
        charm_state.rng_tools_file = RNG_FILE_VALUE
        file.write_text(RNG_FILE_VALUE, encoding="utf-8")
