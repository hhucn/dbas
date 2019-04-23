from dbas.handler import user
from dbas.strings import keywords as _
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class UserManagementTest(TestCaseWithConfig):

    def test_refresh_public_nickname(self):
        old_public_nickname = self.user_tobi.public_nickname
        new_public_nickname = user.refresh_public_nickname(self.user_tobi)
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
        self.assertTrue(self.user_tobi.is_admin() or self.user_tobi.is_author())
        self.assertFalse(self.user_anonymous.is_admin() or self.user_anonymous.is_author())

    def change_password(self):
        _t = Translator('en')

        msg1, success1 = user.change_password(self.user_tobi, None, 'tobiass', 'tobias', 'en')  # not old pw
        msg2, success2 = user.change_password(self.user_tobi, 'tobias', None, 'tobias', 'en')  # not new pw
        msg3, success3 = user.change_password(self.user_tobi, 'tobias', 'tobiass', None, 'en')  # not confirm_pw
        msg4, success4 = user.change_password(self.user_tobi, 'tobias', 'tobias1', 'tobias2',
                                              'en')  # not new == confirm
        msg5, success5 = user.change_password(self.user_tobi, 'tobias', 'tobias', 'tobias', 'en')  # old == new
        msg6, success6 = user.change_password(self.user_tobi, 'tobiaS', 'tobiass', 'tobias', 'en')  # old wrong
        msg7, success7 = user.change_password(self.user_tobi, 'tobias', '123456', '123456', 'en')
        msg8, success8 = user.change_password(self.user_tobi, '123456', 'tobias', 'tobias', 'en')

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
