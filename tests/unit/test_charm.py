# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest import mock

import ops
import ops.testing
from charms.operator_libs_linux.v1 import systemd

import exceptions
from charm import HTTP_PORT, PollenOperatorCharm
from charm_state import CharmState
from pollen import PollenService


class TestCharm(unittest.TestCase):
    """Test class for unit testing."""

    @mock.patch("ops.model.Model.get_binding")
    def setUp(self, network_mock):
        """Initialize the class.

        Args:
            network_mock: Network bind address mock.
        """
        network_mock.return_value.network.bind_address = "10.10.10.10"
        self.harness = ops.testing.Harness(PollenOperatorCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @mock.patch("charms.operator_libs_linux.v1.systemd.service_start")
    def test_pollen_start(self, start_mock):
        PollenService.start()
        start_mock.assert_called_with("pollen.service")

    @mock.patch("charms.operator_libs_linux.v1.systemd.service_stop")
    def test_pollen_stop(self, start_mock):
        PollenService.stop()
        start_mock.assert_called_with("pollen.service")

    @mock.patch("glob.glob")
    @mock.patch("builtins.open")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_reload")
    @mock.patch("subprocess.run")
    @mock.patch("shutil.chown")
    @mock.patch("shutil.copy")
    @mock.patch("os.path.exists")
    @mock.patch("os.mkdir")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_extra_modules(
        self,
        apt_update_mock,
        apt_install_mock,
        os_mkdir_mock,
        os_path_mock,
        shutil_copy_mock,
        shutil_chown_mock,
        run_mock,
        service_reload_mock,
        service_restart_mock,
        open_mock,
        glob_mock,
    ):
        glob_mock.return_value = None
        os_path_mock.side_effect = [False, True]
        PollenService.prepare()
        os_mkdir_mock.assert_called_once()
        apt_update_mock.assert_called_once()
        apt_install_mock.has_calls(["pollen", "pollinate", "ent"], "rng-tools-5")
        service_reload_mock.assert_called_once_with("apparmor.service")
        service_restart_mock.has_calls("rsyslog.service", "rngd.service")

    @mock.patch("glob.glob")
    @mock.patch("builtins.open")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_reload")
    @mock.patch("subprocess.run")
    @mock.patch("shutil.chown")
    @mock.patch("shutil.copy")
    @mock.patch("os.path.exists")
    @mock.patch("os.mkdir")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_extra_modules_error(
        self,
        apt_update_mock,
        apt_install_mock,
        os_mkdir_mock,
        os_path_mock,
        shutil_copy_mock,
        shutil_chown_mock,
        run_mock,
        service_reload_mock,
        service_restart_mock,
        open_mock,
        glob_mock,
    ):
        glob_mock.return_value = None
        os_path_mock.side_effect = [False, True]
        apt_install_mock.side_effect = [None, FileNotFoundError]
        with self.assertRaises(exceptions.ConfigurationWriteError):
            PollenService.prepare()

    @mock.patch("glob.glob")
    @mock.patch("builtins.open")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_reload")
    @mock.patch("subprocess.run")
    @mock.patch("shutil.chown")
    @mock.patch("shutil.copy")
    @mock.patch("os.path.exists")
    @mock.patch("os.mkdir")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare(
        self,
        apt_update_mock,
        apt_install_mock,
        os_mkdir_mock,
        os_path_mock,
        shutil_copy_mock,
        shutil_chown_mock,
        run_mock,
        service_reload_mock,
        service_restart_mock,
        open_mock,
        glob_mock,
    ):
        glob_mock.return_value = None
        os_path_mock.side_effect = [True, False]
        PollenService.prepare()
        os_mkdir_mock.assert_not_called()
        apt_update_mock.assert_called_once()
        apt_install_mock.assert_called_once_with(["pollen", "pollinate", "ent"])
        service_reload_mock.assert_called_once_with("apparmor.service")
        service_restart_mock.assert_called_once_with("rsyslog.service")

    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_install_error(
        self,
        apt_update_mock,
        apt_install_mock,
    ):
        apt_install_mock.side_effect = FileNotFoundError
        with self.assertRaises(exceptions.InstallError):
            PollenService.prepare()

    @mock.patch("charms.operator_libs_linux.v1.systemd.service_reload")
    @mock.patch("shutil.chown")
    @mock.patch("shutil.copy")
    @mock.patch("os.path.exists")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_configuration_error(
        self,
        apt_update_mock,
        apt_install_mock,
        os_path_mock,
        shutil_copy_mock,
        shutil_chown_mock,
        service_reload_mock,
    ):
        service_reload_mock.side_effect = FileNotFoundError
        with self.assertRaises(exceptions.ConfigurationWriteError):
            PollenService.prepare()
        service_reload_mock.side_effect = systemd.SystemdError
        with self.assertRaises(exceptions.ConfigurationWriteError):
            PollenService.prepare()

    def test_charm_state_website_property(self):
        charm_state = CharmState("hostname")
        self.assertEqual(charm_state.website, {"hostname": "hostname", "port": HTTP_PORT})
