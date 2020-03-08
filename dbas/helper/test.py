"""
Utility functions for testing.
"""
import os

from nose.tools import assert_in
from paste.deploy import appconfig

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import SeenStatement, ClickedStatement, SeenArgument, ClickedArgument, User, \
    ReputationHistory


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
    Configure app config to set correct ini-file. Defaults to development.ini for testing purposes.
    If D-BAS runs inside a docker container and no ini-file is provided, then load the docker.ini.

    :param ini_file: name of ini-file
    :return: config with loaded ini-file
    :rtype: dict
    """
    if os.path.isfile("/.dockerenv") and not ini_file:
        return appconfig("config:" + path_to_settings("docker.ini"))
    return appconfig("config:" + path_to_settings(ini_file))


def verify_dictionary_of_view(some_dict):
    """
    Check for keys in the dict

    :param some_dict: dict()
    :return: None
    :rtype: None
    """
    assert_in('ui_locales', some_dict['extras'])
    assert_in('title', some_dict)
    assert_in('extras', some_dict)


def refresh_user(nickname):
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_user.update_last_login()
    db_user.update_last_action()
    DBDiscussionSession.add(db_user)
    return db_user


def clear_seen_by_of(nickname):
    """
    Clears every "SeenBy" rows of the user

    :param nickname: User.nickname
    :return: None
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    DBDiscussionSession.query(SeenStatement).filter_by(user_uid=db_user.uid).delete()
    DBDiscussionSession.query(SeenArgument).filter_by(user_uid=db_user.uid).delete()


def clear_clicks_of(nickname):
    """
    Clears ever clicked elements of the user

    :param nickname: User.nickname
    :return: None
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=db_user.uid).delete()
    DBDiscussionSession.query(ClickedArgument).filter_by(author_uid=db_user.uid).delete()


def clear_reputation_of_user(db_user: User) -> None:
    """
    Delete reputation of db_user in the database.

    :param db_user:
    :return:
    """
    DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).delete()
