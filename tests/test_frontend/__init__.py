import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
_multiprocess_can_split_ = True
ROOT = 'http://localhost:4284'
BROWSER = 'phantomjs'
