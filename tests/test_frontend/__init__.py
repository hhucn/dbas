from nose.tools import *
from splinter import Browser
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
_multiprocess_can_split_ = True  # if the pipeline crashes please disable the multiprocess

ROOT = 'http://localhost:4284'
BROWSER = 'phantomjs'

'''

.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
'''

PATH = '/switch_language?_LOCALE_='

LANGUAGE = {
    'GERMAN': 'de',
    'ENGLISH': 'en'
}  # to check if the cookies had changed

TEST_STRING = {
    'GERMAN': 'Teil des Graduierten-Kollegs',
    'ENGLISH': 'part of the graduate'
}  # to check if the content of the source_page(html) had changed (ugly)

# english page has a german flag and vice versa
TEST_IMG = {
    'GERMAN': 'flag-us-gb',
    'ENGLISH': 'flag-de'
}  # to check if the flag in the source_page(html) had changed

TIME_TO_PREPARE = 1  # used in setup() of test_LanguageSwitch.py to make sure everything had loaded (important but ugly)
