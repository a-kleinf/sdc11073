import logging
from unittest import TestCase
from unittest import mock

from sdc11073.mdib import clientmdib


class TestClientMidb(TestCase):
    def setUp(self) -> None:
        sdc_client = mock.MagicMock()
        sdc_client.all_subscribed = True
        self.mdib = clientmdib.ClientMdibContainer(sdcClient=sdc_client)
        self.mdib.mdibVersion = 10

        self.logger_prefix = "mock_logger"
        self.mdib._logger = mock.MagicMock()

    def _assert_logs_not_called(self):
        self.mdib._logger.log.assert_not_called()
        self.mdib._logger.error.assert_not_called()
        self.mdib._logger.warning.assert_not_called()

    # test MDIB version smaller 0
    # check raise ValueError is raised
    def test_negative_mdib_version_raises(self):
        with self.assertRaises(ValueError):
            self.mdib._canAcceptMdibVersion(self.logger_prefix, -1)

    # test MDIB version is 0
    # check raise ValueError is raised
    def test_zero_mdib_version_raises(self):
        with self.assertRaises(ValueError):
            self.mdib._canAcceptMdibVersion(self.logger_prefix, 0)

    # test mdib_version < self.mdibVersion
    # a) if self._synchronizedReports is set -> check raise ValueError is raised
    def test_older_mdib_version_synchronized_raises(self):
        self.mdib._synchronizedReports.set()
        with self.assertRaises(ValueError):
            self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion - 1)

    # b) if self._synchronizedReports is not set -> return False and log debug was called
    def test_older_mdib_version_not_synchronized_returns_false(self):
        self.assertFalse(self.mdib._synchronizedReports.is_set())

        result = self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion - 1)

        self.assertFalse(result)
        self.mdib._logger.debug.assert_called_once()
        self.assertFalse(self.mdib._synchronizedReports.is_set())

    # test mdib_version == self.mdibVersion
    # a) if self._synchronizedReports is set -> check raise ValueError is raised
    def test_equal_mdib_version_synchronized_raises(self):
        self.mdib._synchronizedReports.set()
        with self.assertRaises(ValueError):
            self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion)

    # b) if self._synchronizedReports is not set -> return False and self._synchronizedReports is then set
    def test_equal_mdib_version_not_synchronized_sets_synchronized(self):
        self.assertFalse(self.mdib._synchronizedReports.is_set())

        result = self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion)

        self.assertFalse(result)
        self.assertTrue(self.mdib._synchronizedReports.is_set())
        self._assert_logs_not_called()

    # test (mdib_version - self.mdibVersion) > 1
    # a) if self._sdcClient.all_subscribed is not set -> returns True and self._synchronizedReports is
    #    then set and error was logged
    def test_gap_mdib_version_not_all_subscribed_returns_true(self):
        self.mdib._sdcClient.all_subscribed = False
        self.assertFalse(self.mdib._synchronizedReports.is_set())

        result = self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion + 2)

        self.assertTrue(result)
        self.assertTrue(self.mdib._synchronizedReports.is_set())
        self.mdib._logger.error.assert_called_once()

    # b) self._sdcClient.all_subscribed is set -> check raise ValueError is raised
    def test_gap_mdib_version_all_subscribed_raises(self):
        self.mdib._sdcClient.all_subscribed = True
        with self.assertRaises(ValueError):
            self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion + 2)
        # error is logged before the exception is raised
        self.mdib._logger.error.assert_called_once()

    # test (mdib_version - self.mdibVersion) == 1
    # results in self._synchronizedReports is set, no error is logged, true is returned
    def test_next_mdib_version_returns_true(self):
        self.assertFalse(self.mdib._synchronizedReports.is_set())

        result = self.mdib._canAcceptMdibVersion(self.logger_prefix, self.mdib.mdibVersion + 1)

        self.assertTrue(result)
        self.assertTrue(self.mdib._synchronizedReports.is_set())
        self._assert_logs_not_called()
