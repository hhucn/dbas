#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from .de import de_lang
from .keywords import default_lang

default = 'en'

languages = {
    'en': default_lang,
    'de': de_lang,
}


class Translator(object):
    """
    Class for translating string
    """

    def __init__(self, lang):
        """
        Initializes keywords

        :param lang: current language
        :return:
        """

        self.lang = lang if lang in languages.keys() else default

        self.lang_dict = languages[self.lang]

    def get(self, sid):
        """
        Returns an localized string

        :param sid: a key identifier from .keywords.Keywords
        :return: string
        """

        print(sid)
        try:
            return self.lang_dict[sid]
        except KeyError:
            return sid.value

    def get_lang(self):
        """
        Return ui locales code

        :return:
        """
        return self.lang
