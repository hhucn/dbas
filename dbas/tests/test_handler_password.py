import unittest

from dbas.handler import password


class PasswordHandlerTests(unittest.TestCase):

    def test_get_rnd_passwd(self):
        self.assertEqual(len(password.get_rnd_passwd()), 10)

        # Test, whether 2 passwords are equal.
        is_equal = password.get_rnd_passwd() is password.get_rnd_passwd()
        self.assertFalse(is_equal)
