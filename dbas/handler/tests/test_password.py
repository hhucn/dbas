import unittest

from dbas.handler import password
from cryptacular.bcrypt import BCRYPTPasswordManager


class PasswordHandlerTests(unittest.TestCase):

    def test_get_rnd_passwd(self):
        self.assertEqual(len(password.get_rnd_passwd()), 10)
        self.assertEqual(len(password.get_rnd_passwd(8)), 8)

        # Test, whether 2 passwords are equal.
        self.assertNotEqual(password.get_rnd_passwd(), password.get_rnd_passwd())

    def test_get_hashed_password(self):
        clear_text = 'hello'
        hashed_pwd = '$2a$10$TxlwjqsDC3qJl3U0nxTcLe8wvAkrcVid5GvoQFy6BObfNCUwRH5H6'
        self.assertEqual(hashed_pwd, BCRYPTPasswordManager().encode(clear_text))
