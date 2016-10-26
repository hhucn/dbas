#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from .de import GermanDict
from .en import EnglischDict
from .keywords import Keywords


class Translator(object):
    """
    Class for translating string
    """

    def __getattr__(self, item):
        return item

    def __init__(self, lang):
        """
        Initializes keywords

        :param lang: current language
        :return:
        """
        self.lang = lang

        self.lang_dict = {
            'en': EnglischDict().set_up(self),
            'de': GermanDict().set_up(self)
        }

    def get(self, sid):
        """
        Returns an localized string

        :param sid: string identifier
        :return: string
        """

        if self.lang not in self.lang_dict.keys():
            return 'unknown language: ' + self.lang

        else:
            if isinstance(sid, Keywords):
                sid = sid.name
            return self.lang_dict[self.lang][sid]

    def get_lang(self):
        """
        Return ui locales code

        :return:
        """
        return self.lang
