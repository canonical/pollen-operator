# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import os
import shutil
import time
from glob import glob
from subprocess import run

from charms.operator_libs_linux.v0 import apt
from charms.operator_libs_linux.v1 import systemd

from exceptions import ConfigurationWriteError, InstallError


def prepare() -> None:
    """Install packages and write configuration files

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
    except:
        raise InstallError
    if not os.path.exists("/var/log/pollen"):
        os.mkdir("/var/log/pollen")
        shutil.chown("/var/log/pollen", "syslog")
    try:
        os.chmod('/etc/apparmor.d/usr.bin.pollen', 0o666)
        shutil.copy("files/usr.bin.pollen", "/etc/apparmor.d/usr.bin.pollen")
        systemd.service_restart('apparmor.service')
        run(['rsync', 'files/logrotate.conf', '/etc/logrotate.d/pollen'])
        run(['rsync', 'files/rsyslog.conf', '/etc/rsyslog.d/40-pollen.conf'])
        systemd.service_restart('rsyslog.service')
    except:
        raise ConfigurationWriteError
    if glob("/dev/tpm*") or os.path.exists("/dev/hwrng"):
        try:
            apt.add_package("rng-tools5")
            os.chmod('/etc/default/rng-tools-debian', 0o666)
            with open('/etc/default/rng-tools-debian', 'a') as file:
                file.writelines([
                    'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
                ])
            run(['/etc/init.d/rng-tools-debian', 'restart'])
            systemd.service_restart('rngd.service')
        except:
            raise ConfigurationWriteError


def start():
    """Start the pollen service."""
    systemd.service_restart('pollen.service')


def stop():
    """Stop the pollen service."""
    systemd.service_stop('pollen.service')
