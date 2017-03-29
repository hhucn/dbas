from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.helper.database import dbas_db_configuration


def setup_package():
    settings = add_settings_to_appconfig()
    DBDiscussionSession.configure(bind=dbas_db_configuration(settings, 'sqlalchemy.discussion.'))
    DBNewsSession.configure(bind=dbas_db_configuration(settings, 'sqlalchemy.news.'))


def teardown_package():
    pass
