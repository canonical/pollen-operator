# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Fixtures for Pollen charm tests."""


def pytest_addoption(parser):
    """Parse additional pytest options.

    Args:
        parser: Pytest parser.
    """
    raise NotImplementedError
    parser.addoption("--charm-file", action="store")
