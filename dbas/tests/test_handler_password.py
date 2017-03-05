import unittest

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.handler import password
from sqlalchemy import engine_from_config


class PasswordHandlerTests(unittest.TestCase):

    def test_get_rnd_passwd(self):
        self.assertEqual(len(password.get_rnd_passwd()), 10)

        # Test, whether 2 passwords are equal.
        is_equal = password.get_rnd_passwd() is password.get_rnd_passwd()
        self.assertFalse(is_equal)
