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

    @classmethod
    def prepare(cls, unit_name) -> None:
        """Install packages and write configuration files.

        Args:
            unit_name: ¨Pollen charm's unit name.

        Raises:
            InstallError: if the packages fail to install
            ConfigurationWriteError: something went wrong writing the configuration
        """
        try:
            apt.update()
            apt.add_package(["pollinate", "ent"])
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
        except FileNotFoundError as exc:
            raise ConfigurationWriteError from exc
        except systemd.SystemdError as exc:
            raise ConfigurationWriteError from exc
        if glob.glob("/dev/tpm*") or Path("/dev/hwrng").exists():
            try:
                apt.add_package("rng-tools5")
                cls.check_rng_file()
                systemd.service_restart("rngd.service")
            except FileNotFoundError as exc:
                raise ConfigurationWriteError from exc

    @classmethod
    def start(cls):
        """Start the pollen service."""
        cache = snap.SnapCache()
        pollen = cache[SNAP_NAME]
        pollen.start()

    @classmethod
    def stop(cls):
        """Stop the pollen service."""
        cache = snap.SnapCache()
        pollen = cache[SNAP_NAME]
        pollen.stop()

    @classmethod
    def check_rng_file(cls):
        """Check if the rng-tools-debian file needs modification."""
        file_modified = False
        with open("/etc/default/rng-tools-debian", "r", encoding="utf-8") as file:
            if file.read().count('RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"') > 1:
                file_modified = True
        if not file_modified:
            with open("/etc/default/rng-tools-debian", "a", encoding="utf-8") as file:
                file.writelines(['RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'])
