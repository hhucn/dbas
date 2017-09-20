from nose.tools import *
from splinter import Browser
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
_multiprocess_can_split_ = False # this could be a problem, because 

ROOT = 'http://localhost:4284'
PATH = '/ajax_switch_language?_LOCALE_='
BROWSER = 'phantomjs'

LANGUAGE = {'GERMAN': 'de', 'ENGLISH': 'en'}

TEST_STRING = {'GERMAN': 'Teil des Graduierten-Kollegs', 'ENGLISH': 'part of the graduate'}
TEST_ID = {'GERMAN': 'id="switch-lang-indicator-de"', 'ENGLISH': 'id="switch-lang-indicator-en"'}
