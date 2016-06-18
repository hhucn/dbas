"""
Utility functions for testing.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
"""
import os

from paste.deploy import appconfig


def path_to_settings(ini_file):
    """
    Find directory of ini-file relative to this directory (currently two directories up).

    :param ini_file: name of ini-file, e.g. development.ini
    :type: str
    :return: path to directory containing ini-file
    :rtype: str
    """
    dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(dir_name, ini_file)


def add_settings_to_appconfig(ini_file="development.ini"):
    """
    Configure appconfig to set correct ini-file. Defaults to development.ini for testing purposes.

    :param ini_file: name of ini-file
    :rtype: str
    :return: config with loaded ini-file
    """
    return appconfig("config:" + path_to_settings(ini_file))