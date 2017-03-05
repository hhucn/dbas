from sqlalchemy import engine_from_config

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.helper.tests import add_settings_to_appconfig


def setup_package():
    settings = add_settings_to_appconfig()
    DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))
    DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


def teardown_package():
    pass
