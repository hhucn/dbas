from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.helper.database import dbas_db_configuration


def setup_package():
    settings = add_settings_to_appconfig()
    DBDiscussionSession.configure(bind=dbas_db_configuration('discussion', settings))
    DBNewsSession.configure(bind=dbas_db_configuration('news', settings))


def teardown_package():
    pass
