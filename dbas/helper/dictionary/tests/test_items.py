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
        list0 = list(range(100))
        list1 = shuffle_list_by_user(self.db_user, list0)
        list2 = shuffle_list_by_user(self.db_user, list0)

        self.assertEqual(list1, list2)

    def test_not_equal(self):
        list0 = list(range(100))
        list1 = shuffle_list_by_user(self.db_user, list0)

        self.assertNotEqual(list0, list1)
