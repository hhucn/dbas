"""
Validate notification-related content.
"""
from os import environ

from dbas.handler.language import get_language_from_cookie
from dbas.lib import get_user_by_private_or_public_nickname, nick_of_anonymous_user
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.lib import add_error, escape_if_string
from dbas.validators.user import valid_user


def __validate_notification_msg(request, key):
    """
    Lookup key in request.json_body and validate it against the necessary length for a message.

    :param request:
    :param key:
    :return:
    """
    notification_text = escape_if_string(request.json_body, key)
    min_length = int(environ.get('MIN_LENGTH_OF_STATEMENT', 10))

    if notification_text and isinstance(notification_text, str) and len(notification_text) >= min_length:
        request.validated[key] = notification_text
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        error_msg = '{} ({}: {})'.format(_tn.get(_.empty_notification_input), _tn.get(_.minLength), min_length)
        add_error(request, 'Notification {} too short or invalid'.format(key), error_msg)
        return False


def valid_notification_title(request):
    """
    Validate length of notification-title.

    :param request:
    :return:
    """
    return __validate_notification_msg(request, 'title')


def valid_notification_text(request):
    """
    Validate length of notification-text.

    :param request:
    :return:
    """
    return __validate_notification_msg(request, 'text')


def valid_notification_recipient(request):
    """
    Recipients must exist, author and recipient must be different users.

    :param request:
    :return:
    """
    _tn = Translator(get_language_from_cookie(request))
    if not valid_user(request):
        add_error(request, 'Not logged in', _tn.get(_.notLoggedIn))
        return False

    db_author = request.validated["user"]
    recipient_nickname = str(request.json_body.get('recipient')).replace('%20', ' ')
    db_recipient = get_user_by_private_or_public_nickname(recipient_nickname)

    if not db_recipient or recipient_nickname == 'admin' or recipient_nickname == nick_of_anonymous_user:
        add_error(request, 'Recipient not found', _tn.get(_.recipientNotFound))
        return False
    elif db_author and db_author.uid == db_recipient.uid:
        add_error(request, 'Author and Recipient are the same user', _tn.get(_.senderReceiverSame))
        return False
    else:
        request.validated["recipient"] = db_recipient
        return True
