# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import os
import shutil
from subprocess import STDOUT, check_call

from exceptions import ConfigurationWriteError, InstallError


def prepare_pollen() -> None:
    """Install packages and write configuration files

    Raises:
        InstallError: if the packages fail to install
        ConfigurationWriteError: something went wrong writing the configuration
    """
    try:
        check_call(['apt-get', 'install', '-y', 'pollen', 'pollinate', 'ent', 'rng-tools'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT)
    except:
        raise InstallError
    if not os.path.exists("/var/log/pollen"):
        os.mkdir("/var/log/pollen")
        shutil.chown("/var/log/pollen", "syslog")
    try:
        check_call(['rsync', 'files/logrotate.conf', '/etc/logrotate.d/pollen'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT)
        check_call(['rsync', 'files/rsyslog.conf', '/etc/rsyslog.d/40-pollen.conf'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT)
        check_call(['systemctl', 'restart', 'rsyslog.service'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT, shell=True)
        check_call(['echo', 'RNGDOPTIONS="--fill-watermark=90% --no-tpm=0"', '>>', '/etc/default/rng-tools'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT, shell=True)
        check_call(['systemctl', 'restart', 'rng-tools-debian.service'],
            stdout=open(os.devnull,'wb'), stderr=STDOUT, shell=True)
    except:
        raise ConfigurationWriteError

