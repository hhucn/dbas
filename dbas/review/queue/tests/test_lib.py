import unittest

from pyramid import testing

from dbas.review.reputation import get_reason_by_action, ReputationReasons


class LibTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def test_get_reputation_reason_by_action(self):
        for action in ReputationReasons.list():
            db_reason = get_reason_by_action(action)
            self.assertIsNotNone(db_reason)
            self.assertTrue(db_reason.points != 0)
