"""
Testing the tests_helper!
"""

from dbas.helper.test import add_settings_to_appconfig


def test_settings_to_appconfig():
    config_default = str(add_settings_to_appconfig())
    config_docker = str(add_settings_to_appconfig("production.ini"))
    assert "production.ini" not in config_default
    assert "development.ini" in config_default
    assert "production.ini" in config_docker
    assert "development.ini" not in config_docker
