"""
Unit tests for lib.py.
"""

import admin.lib as admin
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, APIToken
from dbas.lib import nick_of_anonymous_user
from dbas.tests.utils import TestCaseWithConfig


class AdminTest(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.new_user = {
            'firstname': 'new',
            'surname': 'one',
            'nickname': 'TheOne',
            'email': 'someNewUser@gmail.com',
            'password': 'asdfghjkl',
            'gender': 'm',
            'group': self.user_group
        }

    def test_get_overview(self):
        dict_return = admin.get_overview('some_main_page')
        for row in dict_return:
            for category in row:
                for table in category['content']:
                    self.assertIn(table['name'].lower(), admin.table_mapper)
                    self.assertEqual('some_main_page' + table['name'], table['href'])

    def test_get_table_dict(self):
        for table in admin.table_mapper:
            return_dict = admin.get_table_dict(admin.table_mapper[table]['name'], 'some_main_page')
            self.assertIn('name', return_dict)
            self.assertNotIn('password', return_dict)
            self.assertNotIn('token', return_dict)
            self.assertNotIn('token_timestamp', return_dict)

    def test_add_row(self):
        return_val = admin.add_row('User', self.new_user)
        self.assertTrue(return_val)

        db_new_user = DBDiscussionSession.query(User).filter_by(nickname=self.new_user['nickname']).all()
        self.assertEqual(len(db_new_user), 1)

    def test_update_row(self):
        keys = ['nickname']
        values = ['TheRenamedOne']
        db_old_user = DBDiscussionSession.query(User).order_by(User.uid.asc()).first()
        return_val = admin.update_row('User', [db_old_user.uid], keys, values)
        db_old_user = DBDiscussionSession.query(User).filter_by(nickname=self.new_user['nickname']).all()
        db_new_user = DBDiscussionSession.query(User).filter_by(nickname=values[0]).all()
        self.assertTrue(return_val)
        self.assertEqual(len(db_old_user), 0)
        self.assertEqual(len(db_new_user), 1)

        db_reset = admin.update_row('User', [db_new_user[0].uid], keys, [nick_of_anonymous_user])
        self.assertTrue(db_reset)

    def test_delete_row(self):
        db_new_user = DBDiscussionSession.query(User).filter(User.firstname == self.new_user['firstname'],
                                                             User.surname == self.new_user['surname']).all()
        self.assertEqual(len(db_new_user), 1)

        return_val = admin.delete_row('user', [db_new_user[0].uid])
        self.assertTrue(return_val)
        db_new_user = DBDiscussionSession.query(User).filter(User.firstname == self.new_user['firstname'],
                                                             User.surname == self.new_user['surname']).all()
        self.assertEqual(len(db_new_user), 0)


class APITokenTest(TestCaseWithConfig):
    def tearDown(self):
        DBDiscussionSession.query(APIToken).delete()
        super().tearDown()

    def test_generate_check(self):
        token = admin.generate_application_token("test")
        self.assertTrue(admin.check_api_token(token))

    def test_fail_check(self):
        token = "hglug8o7aug458oghag8o7h5o87gao87ha47z"  # contains non hex symbols
        self.assertFalse(admin.check_api_token(token))
