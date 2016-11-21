import unittest

from dbas.lib import is_user_author

from sqlalchemy import engine_from_config

from dbas import user_management
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.helper.tests import add_settings_to_appconfig

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class UserManagementTest(unittest.TestCase):

    def test_update_last_action(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=str('Tobias')).first()
        last_action_old = db_user.last_action
        user_management.update_last_action('Tobias')
        last_action_new = db_user.last_action
        self.assertNotEqual(last_action_old, last_action_new)

    def test_refresh_public_nickname(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=str('Tobias')).first()
        old_public_nickname = db_user.public_nickname
        new_public_nickname = user_management.refresh_public_nickname(db_user)
        self.assertNotEqual(old_public_nickname, new_public_nickname)

    def test_is_user_in_group(self):
        self.assertTrue(user_management.is_user_in_group('Tobias', 'admins'))
        self.assertFalse(user_management.is_user_in_group('WeGi', 'admins'))
        self.assertFalse(user_management.is_user_in_group('Torben', 'admins'))

        self.assertFalse(user_management.is_user_in_group('Tobias', 'authors'))
        self.assertTrue(user_management.is_user_in_group('WeGi', 'authors'))
        self.assertFalse(user_management.is_user_in_group('Torben', 'authors'))

        self.assertFalse(user_management.is_user_in_group('Tobias', 'users'))
        self.assertFalse(user_management.is_user_in_group('WeGi', 'users'))
        self.assertTrue(user_management.is_user_in_group('Torben', 'users'))

    def test_is_user_admin(self):
        self.assertTrue(user_management.is_user_admin('Tobias'))
        self.assertFalse(user_management.is_user_admin('WeGi'))
        self.assertFalse(user_management.is_user_admin('Torben'))

    def test_is_user_author(self):
        self.assertTrue(is_user_author('Tobias'))
        self.assertTrue(is_user_author('WeGi'))
        self.assertFalse(is_user_author('Torben'))
