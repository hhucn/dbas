import unittest

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config
from dbas.strings.translator import translator
from dbas.strings.en import EnglischDict
from dbas.strings.de import GermanDict

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class TranslatorTest(unittest.TestCase):

    def test_get(self):
        trans_fr = translator('fr')
        trans_de = translator('de')
        trans_en = translator('en')

        en_dict = EnglischDict().set_up(trans_en)
        de_dict = GermanDict().set_up(trans_de)

        self.assertTrue('unknown' in trans_fr.get(trans_fr.accepting))
        self.assertTrue('unknown' in trans_fr.get('some_weird_text'))
        self.assertTrue('unbekannt' in trans_de.get('some_weird_text'))
        self.assertTrue('unknown' in trans_en.get('some_weird_text'))

        for value in de_dict:
            if value in ['signs']:
                continue
            val = trans_de.get(value)
            self.assertFalse(val.startswith('unbekannt'))

        for value in en_dict:
            if value in ['signs']:
                continue
            val = trans_en.get(value)
            self.assertFalse(val.startswith('unknown'))
