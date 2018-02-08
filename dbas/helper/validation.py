# coding=utf-8
from cornice import Errors
from cornice.util import json_error

import dbas.handler.issue as issue_handler
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Issue, Statement
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.handler.language import get_language_from_cookie
from dbas.lib import get_user_by_private_or_public_nickname
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


# #############################################################################
# Helper-functions

def __add_error(request, log_key, verbose_short, verbose_long=None):
    """
    Log and add errors to request. Supports different verbose-messages.

    :param request:
    :param log_key: category in log-description, e.g. the caller function
    :param verbose_short: short description of error
    :param verbose_long: long, verbose description of error
    :return:
    """
    logger('validation', log_key, verbose_short, error=True)
    request.errors.add('body', verbose_short, verbose_long)
    request.errors.status = 400


# #############################################################################
# Validators for discussion-content

def valid_user(request):
    """
    Given a nickname of a user, return the object from the database.

    :param request:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).one_or_none()

    if db_user:
        request.validated['user'] = db_user
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_user', 'Invalid user', _tn.get(_.checkNickname))
        return False


def valid_issue(request):
    """
    Query issue from database and put it into the request.

    :param request:
    :return:
    """
    db_issue = DBDiscussionSession.query(Issue).get(issue_handler.get_issue_id(request))

    if db_issue:
        request.validated['issue'] = db_issue
        return True
    else:
        __add_error(request, 'valid_issue', 'Invalid issue')


def valid_issue_not_readonly(request):
    """
    Get issue from database and verify that it is not read-only.

    :param request:
    :return:
    """
    if valid_issue(request) and not request.validated.get('issue').is_read_only:
        return True
    _tn = Translator(get_language_from_cookie(request))
    __add_error(request, 'valid_issue_not_readonly', 'Issue is read only', _tn.get(_.discussionIsReadOnly))
    return False


def valid_conclusion(request):
    """
    Given a conclusion id, query the object from the database and return it in the request.

    :param request:
    :return:
    """
    conclusion_id = request.json_body.get('conclusion_id')
    issue_id = request.validated['issue'].uid if 'issue' in request.validated else issue_handler.get_issue_id(request)

    if conclusion_id:
        db_conclusion = DBDiscussionSession.query(Statement).filter_by(uid=conclusion_id, issue_uid=issue_id).first()
        request.validated['conclusion'] = db_conclusion
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_conclusion', 'Conclusion id is missing', _tn.get(_.wrongConclusion))


def valid_statement_text(request):
    """
    Validate the correct length of a statement's input.

    :param request:
    :return:
    """
    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    text = request.json_body.get('statement', '')

    if len(text) < min_length:
        _tn = Translator(get_language_from_cookie(request))
        a = _tn.get(_.notInsertedErrorBecauseEmpty)
        b = _tn.get(_.minLength)
        c = _tn.get(_.eachStatement)
        error_msg = '{} ({}: {} {})'.format(a, b, min_length, c)
        __add_error(request, 'valid_statement_text', 'Text too short', error_msg)
    else:
        request.validated['statement'] = text


# #############################################################################
# Validators for notifications

def __validate_notification_msg(request, key):
    """
    Lookup key in request.json_body and validate it against the necessary length for a message.

    :param request:
    :param key:
    :return:
    """
    notification_text = request.json_body.get(key, '')
    min_length = request.registry.settings.get('settings:discussion:notification_min_length', 5)

    if isinstance(notification_text, str) and len(notification_text) >= min_length:
        request.validated[key] = notification_text
    else:
        _tn = Translator(get_language_from_cookie(request))
        error_msg = '{} ({}: {})'.format(_tn.get(_.empty_notification_input), _tn.get(_.minLength), min_length)
        __add_error(request, 'valid_notification_content', 'Notification {} too short or invalid'.format(key),
                    error_msg)


def valid_notification_title(request):
    """
    Validate length of notification-title.

    :param request:
    :return:
    """
    __validate_notification_msg(request, 'title')


def valid_notification_text(request):
    """
    Validate length of notification-text.

    :param request:
    :return:
    """
    __validate_notification_msg(request, 'text')


def valid_notification_recipient(request):
    """
    Recipients must exist, author and recipient must be different users.

    :param request:
    :return:
    """
    _tn = Translator(get_language_from_cookie(request))
    if not valid_user(request):
        __add_error(request, 'valid_notification_recipient', 'Not logged in', _tn.get(_.notLoggedIn))
        return False

    db_author = request.validated["user"]
    recipient_nickname = str(request.json_body.get('recipient')).replace('%20', ' ')
    db_recipient = get_user_by_private_or_public_nickname(recipient_nickname)

    if not db_recipient or recipient_nickname == 'admin' or recipient_nickname == nick_of_anonymous_user:
        __add_error(request, 'valid_notification_recipient', 'Recipient not found', _tn.get(_.notLoggedIn))
        return False
    elif db_author and db_author.uid == db_recipient.uid:
        __add_error(request, 'valid_notification_recipient', 'Author and Recipient are the same user',
                    _tn.get(_.senderReceiverSame))
        return False
    else:
        request.validated["recipient"] = db_recipient
        return True


# #############################################################################
# General validation

def has_keywords(*keywords):
    """
    Verify that specified keywords exist in the request.json_body.

    :param keywords: keys in request.json_body
    :return:
    """

    def valid_keywords(request):
        for keyword in keywords:
            value = request.json_body.get(keyword)
            if value is not None:
                request.validated[keyword] = value
            else:
                logger('validation', 'valid_keywords', 'keyword: {} is not there'.format(keyword), error=True)
                request.errors.add('body', '{} is missing'.format(keyword))
                request.errors.status = 400

    return valid_keywords


class validate(object):
    """
        Applies all validators to this function.
        If one of the validators adds an error, the function will not be called.
        In this situation a response is given with a json body, containing all errors from all validators.

        Decorate a function like this

        .. code-block:: python
        @validate(validators=(check_for_user, check_for_issue, )
        def my_view(request)
    """

    def __init__(self, *validators):
        self.validators = validators

    def __call__(self, func):
        def inner(request):
            if not hasattr(request, 'validated'):
                setattr(request, 'validated', {})
            if not hasattr(request, 'errors'):
                setattr(request, 'errors', Errors())
            if not hasattr(request, 'info'):
                setattr(request, 'info', {})

            for validator in self.validators:
                validator(request=request)

            if len(request.errors) > 0:
                return json_error(request)

            return func(request)

        return inner
