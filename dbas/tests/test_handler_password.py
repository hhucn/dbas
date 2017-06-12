import unittest

from dbas.handler import password


class PasswordHandlerTests(unittest.TestCase):

    def test_get_rnd_passwd(self):
        self.assertEqual(len(password.get_rnd_passwd()), 10)

        # Test, whether 2 passwords are equal.
        self.assertNotEqual(password.get_rnd_passwd(), password.get_rnd_passwd())
