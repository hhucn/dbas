import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.handler import user
from dbas.strings import keywords as _
from dbas.strings.translator import Translator


class UserManagementTest(unittest.TestCase):

    def test_update_last_action(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=str('Tobias')).first()
        last_action_old = db_user.last_action
        user.update_last_action('Tobias')
        last_action_new = db_user.last_action
        self.assertNotEqual(last_action_old, last_action_new)

    def test_refresh_public_nickname(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=str('Tobias')).first()
        old_public_nickname = db_user.public_nickname
        new_public_nickname = user.refresh_public_nickname(db_user)
        self.assertNotEqual(old_public_nickname, new_public_nickname)

    def test_is_user_in_group(self):
        self.assertTrue(user.is_in_group('Tobias', 'admins'))
        self.assertFalse(user.is_in_group('Torben', 'admins'))

        self.assertFalse(user.is_in_group('Tobias', 'authors'))
        self.assertFalse(user.is_in_group('Torben', 'authors'))

        self.assertFalse(user.is_in_group('Tobias', 'users'))
        self.assertTrue(user.is_in_group('Torben', 'users'))

    def test_is_user_admin(self):
        self.assertTrue(user.is_admin('Tobias'))
        self.assertFalse(user.is_admin('Torben'))

    def test_is_user_author(self):
        db_user1 = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user2 = DBDiscussionSession.query(User).filter_by(nickname='Torben').first()
        self.assertTrue(db_user1.is_admin() or db_user1.is_author())
        self.assertFalse(db_user2.is_admin() or db_user2.is_author())

    def change_password(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=str('Tobias')).first()
        _t = Translator('en')

        msg1, success1 = user.change_password(db_user, None, 'tobiass', 'tobias', 'en')  # not old pw
        msg2, success2 = user.change_password(db_user, 'tobias', None, 'tobias', 'en')  # not new pw
        msg3, success3 = user.change_password(db_user, 'tobias', 'tobiass', None, 'en')  # not confirm_pw
        msg4, success4 = user.change_password(db_user, 'tobias', 'tobias1', 'tobias2', 'en')  # not new == confirm
        msg5, success5 = user.change_password(db_user, 'tobias', 'tobias', 'tobias', 'en')  # old == new
        msg6, success6 = user.change_password(db_user, 'tobiaS', 'tobiass', 'tobias', 'en')  # old wrong
        msg7, success7 = user.change_password(db_user, 'tobias', '123456', '123456', 'en')
        msg8, success8 = user.change_password(db_user, '123456', 'tobias', 'tobias', 'en')

        self.assertFalse(success1)
        self.assertFalse(success2)
        self.assertFalse(success3)
        self.assertFalse(success4)
        self.assertFalse(success5)
        self.assertFalse(success6)
        self.assertTrue(success7)
        self.assertTrue(success8)

        self.assertEquals(msg1, _t.get(_.oldPwdEmpty))
        self.assertEquals(msg2, _t.get(_.newPwdEmtpy))
        self.assertEquals(msg3, _t.get(_.confPwdEmpty))
        self.assertEquals(msg4, _t.get(_.newPwdNotEqual))
        self.assertEquals(msg5, _t.get(_.pwdsSame))
        self.assertEquals(msg6, _t.get(_.oldPwdWrong))
        self.assertEquals(msg7, _t.get(_.pwdChanged))
        self.assertEquals(msg8, _t.get(_.pwdChanged))
