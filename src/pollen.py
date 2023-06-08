# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Pollen charm business logic."""

import os
import shutil
import time
from glob import glob
from subprocess import run

from charms.operator_libs_linux.v0 import apt
from charms.operator_libs_linux.v1 import systemd

from exceptions import ConfigurationWriteError, InstallError


def prepare() -> None:
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
    except Exception as exc:
        raise InstallError from exc
    if not os.path.exists("/var/log/pollen"):
        os.mkdir("/var/log/pollen")
        shutil.chown("/var/log/pollen", "syslog")
    try:
        shutil.copy("files/usr.bin.pollen", "/etc/apparmor.d/usr.bin.pollen")
        systemd.service_restart("apparmor.service")
        run(["rsync", "files/logrotate.conf", "/etc/logrotate.d/pollen"], check=True)
        run(["rsync", "files/rsyslog.conf", "/etc/rsyslog.d/40-pollen.conf"], check=True)
        systemd.service_restart("rsyslog.service")
    except Exception as exc:
        raise ConfigurationWriteError from exc
    if glob("/dev/tpm*") or os.path.exists("/dev/hwrng"):
        try:
            apt.add_package("rng-tools5")
            with open("/etc/default/rng-tools-debian", "a", encoding="utf-8") as file:
                file.writelines(['RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'])
            run(["/etc/init.d/rng-tools-debian", "restart"], check=True)
            systemd.service_restart("rngd.service")
        except Exception as exc:
            raise ConfigurationWriteError from exc


def start():
    """Start the pollen service."""
    systemd.service_restart("pollen.service")


def stop():
    """Stop the pollen service."""
    systemd.service_stop("pollen.service")
