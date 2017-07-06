from dbas.database import DBDiscussionSession as session, get_dbas_db_configuration
from dbas.database.discussion_model import User
from dbas.helper.tests import add_settings_to_appconfig

settings = add_settings_to_appconfig()
session.configure(bind=get_dbas_db_configuration('discussion', settings))

title = {
    'm': 'Herr',
    'f': 'Frau',
    'n': 'Frau/Herr'
}
for user in session.query(User).filter(~User.nickname.in_(['anonymous', 'admin', 'Tobias', 'Christian'])).all():
    print('{} {} - {}'.format(title[user.gender], user.surname, user.email))
