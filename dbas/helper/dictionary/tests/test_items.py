# coding=utf-8
import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.helper.dictionary.items import shuffle_list_by_user


class TestShuffleList(unittest.TestCase):
    def setUp(self):
        self.db_user = DBDiscussionSession.query(User).first()

    def test_empty_list(self):
        self.assertEqual(shuffle_list_by_user(self.db_user, []), [])

    def test_repeatabilty(self):
        l = list(range(100))
        l1 = shuffle_list_by_user(self.db_user, l)
        l2 = shuffle_list_by_user(self.db_user, l)

        self.assertEqual(l1, l2)

    def test_not_equal(self):
        l = list(range(100))
        l1 = shuffle_list_by_user(self.db_user, l)

        self.assertNotEqual(l, l1)
