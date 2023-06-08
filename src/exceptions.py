# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Exceptions used by the Pollen charm."""


class ConfigurationWriteError(Exception):
    """Exception raised when the configuration writing process goes wrong."""


class InstallError(Exception):
    """Exception raised when package installation fails."""
