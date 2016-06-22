"""
Testing the tests_helper!

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
"""

from dbas.helper.tests_helper import add_settings_to_appconfig


def test_settings_to_appconfig():
    config_default = str(add_settings_to_appconfig())
    config_docker = str(add_settings_to_appconfig("docker.ini"))
    assert "docker.ini" not in config_default
    assert "development.ini" in config_default
    assert "docker.ini" in config_docker
    assert "development.ini" not in config_docker
