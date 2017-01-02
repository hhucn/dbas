import unittest

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TranslatorTest(unittest.TestCase):

    def test_get(self):
        trans_fr = Translator('fr')
        trans_de = Translator('de')
        trans_en = Translator('en')

        self.assertIn('haben eine', trans_de.get(_.forgotInputRadio))
        self.assertIn('forgot to', trans_en.get(_.forgotInputRadio))
        self.assertIn('forgot to', trans_fr.get(_.forgotInputRadio))
