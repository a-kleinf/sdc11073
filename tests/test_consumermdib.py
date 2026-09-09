"""Tests for consumer mdib handling."""

import unittest
import unittest.mock

from sdc11073 import definitions_sdc
from sdc11073.mdib import ConsumerMdib


class TestHasNewStateUsableStateVersion(unittest.TestCase):
    REPORT_NAME = 'SomeReport'

    def setUp(self) -> None:
        sdc_client = unittest.mock.MagicMock()
        sdc_client.sdc_definitions = definitions_sdc.SdcV1Definitions
        sdc_client.log_prefix = ''
        self.mdib = ConsumerMdib(sdc_client)
        self.mdib._logger = unittest.mock.MagicMock()

    @staticmethod
    def _mk_state(state_version: int) -> unittest.mock.MagicMock:
        state = unittest.mock.MagicMock()
        state.StateVersion = state_version
        state.DescriptorHandle = 'my_handle'
        return state

    def _has_new_state_usable_state_version(self, old_version: int, new_version: int) -> bool:
        return self.mdib._has_new_state_usable_state_version(
            self._mk_state(old_version),
            self._mk_state(new_version),
            self.REPORT_NAME,
        )

    def test_incremented_state_version_returns_true(self):
        self.assertTrue(self._has_new_state_usable_state_version(41, 42))

    def test_missed_state_versions_raises(self):
        with self.assertRaises(ValueError) as ctx:
            self._has_new_state_usable_state_version(41, 44)
        msg = str(ctx.exception)
        self.assertIn(self.REPORT_NAME, msg)
        self.assertIn('missed 2 states', msg)
        self.assertIn('my_handle', msg)
        self.assertIn('(41->44)', msg)

    def test_decremented_state_version_raises(self):
        with self.assertRaises(ValueError) as ctx:
            self._has_new_state_usable_state_version(42, 41)
        msg = str(ctx.exception)
        self.assertIn(self.REPORT_NAME, msg)
        self.assertIn('received older state', msg)
        self.assertIn('my_handle', msg)
        self.assertIn('(42->41)', msg)

    def test_repeated_state_version_raises(self):
        with self.assertRaises(ValueError) as ctx:
            self._has_new_state_usable_state_version(42, 42)
        msg = str(ctx.exception)
        self.assertIn(self.REPORT_NAME, msg)
        self.assertIn('received older state', msg)
        self.assertIn('my_handle', msg)
        self.assertIn('(42->42)', msg)
