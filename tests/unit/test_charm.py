# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest

import ops
import ops.testing

from charm import EntropyOperatorCharm


class TestCharm(unittest.TestCase):
    """Test class for unit testing."""

    def setUp(self):
        """Initialize the class."""
        self.harness = ops.testing.Harness(EntropyOperatorCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
