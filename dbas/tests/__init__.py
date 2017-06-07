from dbas.database import DBDiscussionSession, DBNewsSession, get_dbas_db_configuration
from dbas.helper.tests import add_settings_to_appconfig


def setup_package():
    settings = add_settings_to_appconfig()
    DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))
    DBNewsSession.configure(bind=get_dbas_db_configuration('news', settings))


def teardown_package():
    pass
