import unittest

from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class TranslatorTest(unittest.TestCase):

    def test_get(self):
        trans_fr = Translator('fr')
        trans_de = Translator('de')
        trans_en = Translator('en')

        self.assertIn('haben eine', trans_de.get(_.forgotInputRadio))
        self.assertIn('forgot to', trans_en.get(_.forgotInputRadio))
        self.assertIn('forgot to', trans_fr.get(_.forgotInputRadio))
