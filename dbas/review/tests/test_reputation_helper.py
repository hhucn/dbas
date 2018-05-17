import unittest

import dbas.review.reputation as ReviewReputationHelper
from dbas.strings.translator import Translator


class TestReviewReputationHelper(unittest.TestCase):

    def test_get_reputation_list(self):
        some_list = ReviewReputationHelper.get_reputation_list(Translator('en'))
        self.assertTrue('gains' in some_list)
        self.assertTrue('looses' in some_list)

    def test_get_privilege_list(self):
        some_list = ReviewReputationHelper.get_privilege_list(Translator('en'))
        for element in some_list:
            self.assertTrue('points' in element)
            self.assertTrue('icon' in element)
            self.assertTrue('text' in element)

    def test_get_reputation_of(self):
        count, has_all_rights = ReviewReputationHelper.get_reputation_of('Tobias')
        self.assertTrue(count > 20)
        self.assertTrue(has_all_rights)

        count, has_all_rights = ReviewReputationHelper.get_reputation_of('Tobiass')
        self.assertTrue(count == 0)
        self.assertFalse(has_all_rights)
