# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest import mock

import ops
import ops.testing
from charms.operator_libs_linux.v1 import systemd
from charms.operator_libs_linux.v2 import snap

import exceptions
from charm import PollenOperatorCharm
from charm_state import HTTP_PORT, CharmState
from pollen import RNG_FILE_VALUE, PollenService


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
        self.pollen = PollenService()

    @mock.patch("charms.operator_libs_linux.v2.snap.Snap.set")
    @mock.patch("charms.operator_libs_linux.v2.snap.Snap.start")
    def test_pollen_start(self, start_mock, set_mock):
        self.pollen.start()
        set_mock.assert_called_once()
        start_mock.assert_called_once()

    @mock.patch("charms.operator_libs_linux.v2.snap.Snap.stop")
    def test_pollen_stop(self, stop_mock):
        self.pollen.stop()
        stop_mock.assert_called_once()

    @mock.patch("glob.glob")
    @mock.patch("pathlib.Path.write_text")
    @mock.patch("pathlib.Path.read_text")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("pathlib.Path.read_bytes")
    @mock.patch("pathlib.Path.write_bytes")
    @mock.patch("pathlib.Path.exists")
    @mock.patch("charms.operator_libs_linux.v2.snap.add")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_extra_modules(
        self,
        apt_update_mock,
        apt_install_mock,
        snap_mock,
        exists_path_mock,
        write_bytes_mock,
        read_bytes_mock,
        service_restart_mock,
        read_mock,
        write_mock,
        glob_mock,
    ):
        glob_mock.return_value = None
        read_mock.return_value = f"# {RNG_FILE_VALUE}"
        exists_path_mock.return_value = True
        self.pollen.prepare("pollen-0")
        apt_update_mock.assert_called_once()
        write_mock.assert_called_once()
        apt_install_mock.assert_called_once_with("rng-tools5")
        service_restart_mock.has_calls("rsyslog.service", "rngd.service")

    @mock.patch("glob.glob")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("charms.operator_libs_linux.v2.snap.add")
    @mock.patch("pathlib.Path.read_bytes")
    @mock.patch("pathlib.Path.write_bytes")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_extra_modules_error(
        self,
        apt_update_mock,
        apt_install_mock,
        write_bytes_error,
        read_bytes_mock,
        snap_mock,
        service_restart_mock,
        glob_mock,
    ):
        glob_mock.return_value = None
        apt_install_mock.side_effect = [systemd.SystemdError]
        with self.assertRaises(exceptions.ConfigurationWriteError):
            self.pollen.prepare("pollen-0")

    @mock.patch("glob.glob")
    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("charms.operator_libs_linux.v2.snap.add")
    @mock.patch("pathlib.Path.read_bytes")
    @mock.patch("pathlib.Path.write_bytes")
    @mock.patch("pathlib.Path.exists")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    @mock.patch("pathlib.Path.read_text")
    def test_pollen_prepare(
        self,
        read_text_mock,
        apt_update_mock,
        path_mock,
        write_bytes_mock,
        read_bytes_mock,
        snap_mock,
        service_restart_mock,
        glob_mock,
    ):
        read_text_mock.return_value = "tpm-rng-0"
        glob_mock.return_value = None
        path_mock.return_value = False
        self.pollen.prepare("pollen-0")
        service_restart_mock.assert_called_once_with("rsyslog.service")

    @mock.patch("charms.operator_libs_linux.v2.snap.add")
    def test_pollen_prepare_install_error(
        self,
        snap_mock,
    ):
        snap_mock.side_effect = snap.SnapError
        with self.assertRaises(exceptions.InstallError):
            self.pollen.prepare("pollen-0")

    @mock.patch("charms.operator_libs_linux.v1.systemd.service_restart")
    @mock.patch("charms.operator_libs_linux.v2.snap.add")
    @mock.patch("pathlib.Path.read_bytes")
    @mock.patch("pathlib.Path.write_bytes")
    @mock.patch("charms.operator_libs_linux.v0.apt.add_package")
    @mock.patch("charms.operator_libs_linux.v0.apt.update")
    def test_pollen_prepare_configuration_error(
        self,
        apt_update_mock,
        apt_install_mock,
        write_bytes_mock,
        read_bytes_mock,
        snap_mock,
        service_restart_mock,
    ):
        service_restart_mock.side_effect = FileNotFoundError
        with self.assertRaises(exceptions.ConfigurationWriteError):
            self.pollen.prepare("pollen-0")
        service_restart_mock.side_effect = systemd.SystemdError
        with self.assertRaises(exceptions.ConfigurationWriteError):
            self.pollen.prepare("pollen-0")

    def test_charm_state_website_property(self):
        charm_state = CharmState("hostname")
        self.assertEqual(charm_state.website, {"hostname": "hostname", "port": str(HTTP_PORT)})
