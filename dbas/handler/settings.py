from dbas.handler import user
import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Settings
from dbas.lib import get_profile_picture
from dbas.strings.keywords import Keywords as _


def set_settings(url, userid, service, settings_value, _tn):
    """
    Edits a user specific setting

    :param request: current request
    :param service: service, which should be modified
    :param settings_value: Boolean
    :param _tn: Translator
    :return: public_nick, public_page_url, gravatar_url, error
    """

    error = ''
    public_nick = ''
    public_page_url = ''
    gravatar_url = ''
    db_user = DBDiscussionSession.query(User).filter_by(nickname=userid).first()
    if not db_user:
        error = _tn.get(_.checkNickname)
        return public_nick, public_page_url, gravatar_url, error

    public_nick = db_user.public_nickname
    db_setting = DBDiscussionSession.query(Settings).get(db_user.uid)

    if service == 'mail':
        db_setting.set_send_mails(settings_value)

    elif service == 'notification':
        db_setting.set_send_notifications(settings_value)

    elif service == 'public_nick':
        db_setting.set_show_public_nickname(settings_value)
        if settings_value:
            db_user.set_public_nickname(db_user.nickname)
        elif db_user.nickname == db_user.public_nickname:
            user.refresh_public_nickname(db_user)
        public_nick = db_user.public_nickname
    else:
        error = _tn.get(_.keyword)

    transaction.commit()
    public_page_url = '{}/user/{}'.format(url, db_user.uid)
    gravatar_url = get_profile_picture(db_user, 80, ignore_privacy_settings=settings_value)

    return public_nick, public_page_url, gravatar_url, error
