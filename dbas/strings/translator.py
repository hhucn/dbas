#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Translator module for german and english version
"""

from .de import de_lang
from .en import en_lang
from .keywords import Keywords

languages = {
    'de': de_lang,
    'en': en_lang,
}


def get_translation(sid: Keywords, lang: str = 'en') -> str:
    """
    Returns an localized string

    :param lang: a local code e.g. 'en'
    :param sid: a key identifier from .keywords.Keywords or the name of a key (for backwards compatibility reasons)
    :return: string
    """
    if isinstance(sid, Keywords):
        if lang in languages:
            return languages[lang][sid]
        else:
            return languages['en'][sid]
    else:
        return get_translation(Keywords.get_key_by_string(sid), lang)


class Translator(object):
    """
    Class for translating string
    """

    def __init__(self, lang: str):
        """
        Initializes keywords

        :param lang: current language
        :return:
        """

        self.lang = lang

    def get(self, sid: Keywords) -> str:
        """
        Returns an localized string

        :param sid: a key identifier from .keywords.Keywords
        :return: string
        """
        return get_translation(sid, self.lang)

    def get_lang(self) -> str:
        """
        Return ui locales code

        :return:
        """
        return self.lang
