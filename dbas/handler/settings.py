from dbas.handler import user
import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Settings, User
from dbas.lib import get_public_profile_picture
from dbas.strings.keywords import Keywords as _


def set_settings(url, nickname, service, settings_value, _tn):
    """
    Edits a user specific setting

    :param url: current url of request
    :param nickname: instance of user
    :param service: service, which should be modified
    :param settings_value: Boolean
    :param _tn: Translator
    :return: public_nick, public_page_url, gravatar_url, error
    """

    error = ''
    public_nick = ''
    public_page_url = ''
    gravatar_url = ''

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        error = _tn.get(_.checkNickname)
        return {
            'error': error,
            'public_nick': public_nick,
            'public_page_url': public_page_url,
            'gravatar_url': gravatar_url
        }

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
    gravatar_url = get_public_profile_picture(db_user, 80)

    return {
        'error': error,
        'public_nick': public_nick,
        'public_page_url': public_page_url,
        'gravatar_url': gravatar_url
    }
