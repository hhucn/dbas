import unittest

from sqlalchemy import engine_from_config

from dbas import password_handler, DBDiscussionSession
from dbas.helper.tests_helper import add_settings_to_appconfig

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class PasswordHandlerTests(unittest.TestCase):

    def test_get_rnd_passwd(self):
        self.assertEqual(len(password_handler.get_rnd_passwd()), 12);

