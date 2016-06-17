"""
Utility functions for testing.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
"""
import os

from paste.deploy import appconfig


def path_to_settings(ini_file):
    dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(dir_name, ini_file)


def add_settings_to_appconfig(ini_file="development.ini"):
    return appconfig("config:" + path_to_settings(ini_file))