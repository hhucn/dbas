import unittest

from pyramid import testing

from dbas.review.reputation import get_reason_by_action


class LibTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_get_reputation_reason_by_wrong_action(self):
        self.assertIsNone(get_reason_by_action('foo'))

    def test_get_reputation_reason_by_action(self):
        actions = [
            'first_position',
            'first_justification',
            'first_argument_click',
            'first_confrontation',
            'first_new_argument',
            'new_statement',
            'success_flag',
            'success_edit',
            'success_duplicate',
            'bad_flag',
            'bad_edit',
            'bad_duplicate'
        ]
        for action in actions:
            self.assertIsNotNone(get_reason_by_action(action))
