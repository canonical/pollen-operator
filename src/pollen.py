# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import os
import shutil
from glob import glob
from subprocess import STDOUT, check_call

from charms.operator_libs_linux.v0 import apt
from charms.operator_libs_linux.v1 import systemd

from exceptions import ConfigurationWriteError, InstallError


def prepare_pollen() -> None:
    """Install packages and write configuration files

    Raises:
        InstallError: if the packages fail to install
        ConfigurationWriteError: something went wrong writing the configuration
    """
    try:
        apt.update()
        apt.add_package(["pollen", "pollinate", "ent"])
    except:
        raise InstallError
    if not os.path.exists("/var/log/pollen"):
        os.mkdir("/var/log/pollen")
        shutil.chown("/var/log/pollen", "syslog")
    try:
        os.chmod('/etc/apparmor.d/usr.bin.pollen', 0o666)
        shutil.copy("files/usr.bin.pollen", "/etc/apparmor.d/usr.bin.pollen")
        systemd.service_reload('apparmor.service')
        check_call(['rsync', 'files/logrotate.conf', '/etc/logrotate.d/pollen'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT)
        check_call(['rsync', 'files/rsyslog.conf', '/etc/rsyslog.d/40-pollen.conf'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT)
        systemd.service_restart('rsyslog.service')
    except:
        raise ConfigurationWriteError
    if glob("/dev/tpm*") or os.path.exists("/dev/hwrng"):
        try:
            apt.add_package("rng-tools5")
            os.chmod('/etc/default/rng-tools-debian', 0o666)
            with open('/etc/default/rng-tools-debian', 'a') as file:
                file.writelines([
                    'HRNGDEVICE=/dev/urandom'
                    'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
                ])
            check_call(['/etc/init.d/rng-tools-debian', 'restart'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
            systemd.service_restart('rngd.service')
        except:
            raise ConfigurationWriteError


def start_pollen():
        """Start the pollen service."""
        systemd.service_restart('pollen.service')


def stop_pollen():
        """Stop the pollen service."""
        systemd.service_stop('pollen.service')
