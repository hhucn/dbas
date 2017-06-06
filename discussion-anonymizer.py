import transaction
from dbas.database import DBDiscussionSession as session
from dbas.database.discussion_model import User
from dbas.helper.tests import add_settings_to_appconfig
from dbas.helper.database import dbas_db_configuration

settings = add_settings_to_appconfig()
session.configure(bind=dbas_db_configuration('discussion', settings))

for user in session.query(User).filter(~User.nickname.in_(['anonymous'])).all():
    user.firstname = 'firstname_{}'.format(user.uid)
    user.surname = 'surname_{}'.format(user.uid)
    user.nickname = 'nickname_{}'.format(user.uid)
    user.public_nickname = 'public_nickname_{}'.format(user.uid)
    user.email = 'email_{}'.format(user.uid)
    user.password = 'password_{}'.format(user.uid)

session.flush()
transaction.commit()
