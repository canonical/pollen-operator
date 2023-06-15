# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
# This comment will go away, it is just for testing purposes

"""Pollen charm business logic."""

import glob
import os
import shutil
import subprocess
import time

from charms.operator_libs_linux.v0 import apt
from charms.operator_libs_linux.v1 import systemd

from exceptions import ConfigurationWriteError, InstallError

POLLEN_SERVICE_NAME = "pollen.service"


class PollenService:
    """Pollen service class."""

    @classmethod
    def prepare(cls) -> None:
        """Install packages and write configuration files.

        Raises:
            InstallError: if the packages fail to install
            ConfigurationWriteError: something went wrong writing the configuration
        """
        try:
            apt.update()
            apt.add_package(["pollen", "pollinate", "ent"])
            # Apt-get makes the pollen restart error if we don't wait,
            # even if apt-get executes correctly and there are no
            # child processes left. The cause is unknown.
            time.sleep(10)
        except FileNotFoundError as exc:
            raise InstallError from exc
        if not os.path.exists("/var/log/pollen"):
            os.mkdir("/var/log/pollen")
            shutil.chown("/var/log/pollen", "syslog")
        try:
            shutil.copy("files/usr.bin.pollen", "/etc/apparmor.d/usr.bin.pollen")
            systemd.service_reload("apparmor.service")
            subprocess.run(
                [
                    "rsync",
                    "files/logrotate.conf",
                    "/etc/logrotate.d/pollen",
                ],
                check=True,
            )
            subprocess.run(
                [
                    "rsync",
                    "files/rsyslog.conf",
                    "/etc/rsyslog.d/40-pollen.conf",
                ],
                check=True,
            )
            systemd.service_restart("rsyslog.service")
        except FileNotFoundError as exc:
            raise ConfigurationWriteError from exc
        except systemd.SystemdError as exc:
            raise ConfigurationWriteError from exc
        if glob.glob("/dev/tpm*") or os.path.exists("/dev/hwrng"):
            try:
                apt.add_package("rng-tools5")
                cls.check_rng_file()
                systemd.service_restart("rngd.service")
            except FileNotFoundError as exc:
                raise ConfigurationWriteError from exc

    @classmethod
    def start(cls):
        """Start the pollen service."""
        systemd.service_start(POLLEN_SERVICE_NAME)

    @classmethod
    def stop(cls):
        """Stop the pollen service."""
        systemd.service_stop(POLLEN_SERVICE_NAME)

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
