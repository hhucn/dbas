"""
Unit tests for lib.py

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import unittest

from admin.lib import get_overview, update_row, delete_row, add_row, table_mapper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))

new_user = {
    'firstname': 'new',
    'surname': 'one',
    'nickname': 'TheOne',
    'email': 'someNewUser@gmail.com',
    'password': 'asdfghjkl',
    'gender': 'm',
    'group_uid': '3',
}


class AdminTest(unittest.TestCase):

    def test_get_overview(self):
        dict_return = get_overview('some_main_page')
        for row in dict_return:
            for category in row:
                for table in category['content']:
                    self.assertTrue(table['name'].lower() in table_mapper)
                    self.assertTrue(table['count'] >= 0)
                    self.assertTrue('some_main_page' + table['name'] == table['href'])

    #def test_get_table_dict(self):
    #    for table in table_mapper:
    #        return_dict = get_table_dict(table_mapper[table]['name'])
    #        self.assertTrue('is_existing' in return_dict)
    #        self.assertTrue('name' in return_dict)
    #        self.assertFalse('password' in return_dict)
    #        self.assertFalse('token' in return_dict)
    #        self.assertFalse('token_timestamp' in return_dict)

    def test_add_row(self):
        translator = Translator('en')

        return_val = add_row('User', new_user, 'Tobia', translator)
        self.assertEqual(return_val, translator.get(_.noRights))

        return_val = add_row('Userr', new_user, 'Tobias', translator)
        self.assertEqual(return_val, translator.get(_.internalKeyError))

        return_val = add_row('User', new_user, 'Tobias', translator)
        self.assertEqual(len(return_val), 0)

        db_new_user = DBDiscussionSession.query(User).filter_by(nickname=new_user['nickname']).all()
        self.assertEqual(len(db_new_user), 1)

    def test_update_row(self):
        translator = Translator('en')
        uids = [0]
        keys = ['nickname']
        values = ['TheRenamedOne']

        return_val = update_row('User', uids, keys, values, 'Tobia', translator)
        self.assertTrue(return_val == translator.get(_.noRights))

        return_val = update_row('Userr', uids, keys, values, 'Tobias', translator)
        self.assertTrue(return_val == translator.get(_.internalKeyError))

        db_old_user = DBDiscussionSession.query(User).order_by(User.uid.asc()).first()
        return_val = update_row('User', [db_old_user.uid], keys, values, 'Tobias', translator)
        db_old_user = DBDiscussionSession.query(User).filter_by(nickname=new_user['nickname']).all()
        db_new_user = DBDiscussionSession.query(User).filter_by(nickname=values[0]).all()
        self.assertTrue(len(return_val) == 0)
        self.assertTrue(len(db_old_user) == 0)
        self.assertTrue(len(db_new_user) == 1)

    def test_delete_row(self):
        translator = Translator('en')

        return_val = delete_row('User', [0], 'Tobia', translator)
        self.assertTrue(return_val == translator.get(_.noRights))

        return_val = delete_row('Userr', [0], 'Tobias', translator)
        self.assertTrue(return_val == translator.get(_.internalKeyError))

        db_new_user = DBDiscussionSession.query(User).filter(User.firstname == new_user['firstname'],
                                                             User.surname == new_user['surname']).all()
        self.assertTrue(len(db_new_user) == 1)

        return_val = delete_row('user', [db_new_user[0].uid], 'Tobias', translator)
        self.assertTrue(len(return_val) == 0)
        db_new_user = DBDiscussionSession.query(User).filter(User.firstname == new_user['firstname'],
                                                             User.surname == new_user['surname']).all()
        self.assertTrue(len(db_new_user) == 0)
