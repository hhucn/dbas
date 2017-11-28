"""
Unit tests for lib.py

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import unittest

import admin.lib as admin
from dbas.database import DBDiscussionSession, get_dbas_db_configuration
from dbas.database.discussion_model import User, APIToken
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.database.initializedb import nick_of_anonymous_user

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))

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
        dict_return = admin.get_overview('some_main_page')
        for row in dict_return:
            for category in row:
                for table in category['content']:
                    self.assertIn(table['name'].lower(), admin.table_mapper)
                    self.assertEqual('some_main_page' + table['name'], table['href'])

    def test_get_table_dict(self):
        for table in admin.table_mapper:
            return_dict = admin.get_table_dict(admin.table_mapper[table]['name'], 'some_main_page')
            self.assertIn('is_existing', return_dict)
            self.assertIn('name', return_dict)
            self.assertNotIn('password', return_dict)
            self.assertNotIn('token', return_dict)
            self.assertNotIn('token_timestamp', return_dict)

    def test_add_row(self):
        translator = Translator('en')

        return_val = admin.add_row('User', new_user, 'Tobia', translator)
        self.assertEqual(return_val, translator.get(_.noRights))

        return_val = admin.add_row('Userr', new_user, 'Tobias', translator)
        self.assertEqual(return_val, translator.get(_.internalKeyError))

        return_val = admin.add_row('User', new_user, 'Tobias', translator)
        self.assertEqual(len(return_val), 0)

        db_new_user = DBDiscussionSession.query(User).filter_by(nickname=new_user['nickname']).all()
        self.assertEqual(len(db_new_user), 1)

    def test_update_row(self):
        translator = Translator('en')
        uids = [0]
        keys = ['nickname']
        values = ['TheRenamedOne']

        return_val = admin.update_row('User', uids, keys, values, 'Tobia', translator)
        self.assertEqual(return_val, translator.get(_.noRights))

        return_val = admin.update_row('Userr', uids, keys, values, 'Tobias', translator)
        self.assertEqual(return_val, translator.get(_.internalKeyError))

        db_old_user = DBDiscussionSession.query(User).order_by(User.uid.asc()).first()
        return_val = admin.update_row('User', [db_old_user.uid], keys, values, 'Tobias', translator)
        db_old_user = DBDiscussionSession.query(User).filter_by(nickname=new_user['nickname']).all()
        db_new_user = DBDiscussionSession.query(User).filter_by(nickname=values[0]).all()
        self.assertEqual(len(return_val), 0)
        self.assertEqual(len(db_old_user), 0)
        self.assertEqual(len(db_new_user), 1)

        db_reset = admin.update_row('User', [db_new_user[0].uid], keys, [nick_of_anonymous_user], 'Tobias', translator)
        self.assertEqual(len(db_reset), 0)

    def test_delete_row(self):
        translator = Translator('en')

        return_val = admin.delete_row('User', [0], 'Tobia', translator)
        self.assertEqual(return_val, translator.get(_.noRights))

        return_val = admin.delete_row('Userr', [0], 'Tobias', translator)
        self.assertEqual(return_val, translator.get(_.internalKeyError))

        db_new_user = DBDiscussionSession.query(User).filter(User.firstname == new_user['firstname'],
                                                             User.surname == new_user['surname']).all()
        self.assertEqual(len(db_new_user), 1)

        return_val = admin.delete_row('user', [db_new_user[0].uid], 'Tobias', translator)
        self.assertEqual(len(return_val), 0)
        db_new_user = DBDiscussionSession.query(User).filter(User.firstname == new_user['firstname'],
                                                             User.surname == new_user['surname']).all()
        self.assertEqual(len(db_new_user), 0)


class APITokenTest(unittest.TestCase):
    def tearDown(self):
        DBDiscussionSession.query(APIToken).delete()

    def test_generate_check(self):
        token = admin.generate_application_token("test")
        self.assertTrue(admin.check_token(token))

    def test_fail_check(self):
        token = "hglug8o7aug458oghag8o7h5o87gao87ha47z"  # contains non hex symbols
        self.assertFalse(admin.check_token(token))
