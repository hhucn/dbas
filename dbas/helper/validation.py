# coding=utf-8
from cornice import Errors
from cornice.util import json_error

import dbas.handler.issue as issue_handler
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Issue, Statement, Language, Argument, ReviewDeleteReason, PremiseGroup
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer
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


def __set_min_length_error(request, min_length):
    """
    Add an error to the request due to too short statements text.

    :param request:
    :param min_length: minimum length of the statement
    :return:
    """
    _tn = Translator(get_language_from_cookie(request))
    a = _tn.get(_.notInsertedErrorBecauseEmpty)
    b = _tn.get(_.minLength)
    c = _tn.get(_.eachStatement)
    error_msg = '{} ({}: {} {})'.format(a, b, min_length, c)
    __add_error(request, '__set_min_length_error', 'Text too short', error_msg)


# #############################################################################
# Validators for discussion-content

def valid_user(request):
    """
    Given a nickname of a user authenticated, return the object from the database.

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


def invalid_user(request):
    """
    Given a nickname of a (un)-authenticated user, return the object from the database.

    :param request:
    :return:
    """
    if request.authenticated_userid:
        return valid_user(request)
    else:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
        request.validated['user'] = db_user
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
        return False


def valid_new_issue(request):
    """
    Verifies given data for a new issue

    :param request:
    :return:
    """

    fn_validator = has_keywords(('title', str), ('info', str), ('long_info', str))
    if not fn_validator(request):
        return False

    db_dup1 = DBDiscussionSession.query(Issue).filter_by(title=request.validated['title']).all()
    db_dup2 = DBDiscussionSession.query(Issue).filter_by(info=request.validated['info']).all()
    db_dup3 = DBDiscussionSession.query(Issue).filter_by(long_info=request.validated['long_info']).all()
    if db_dup1 or db_dup2 or db_dup3:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_new_issue', 'Issue data is a duplicate', _tn.get(_.duplicate))
        return False
    return True


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
        db_conclusion = DBDiscussionSession.query(Statement).filter_by(uid=conclusion_id,
                                                                       issue_uid=issue_id,
                                                                       is_disabled=False).first()
        request.validated['conclusion'] = db_conclusion
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_conclusion', 'Conclusion id is missing', _tn.get(_.wrongConclusion))


def valid_statement(request):
    """
    Given an uid, query the statement object from the database and return it in the request.

    :param request:
    :return:
    """
    statement_id = request.json_body.get('uid')
    db_statement = DBDiscussionSession.query(Statement).filter(Statement.uid == statement_id,
                                                               Statement.is_disabled == False).first() if is_integer(
        statement_id) else None

    if db_statement:
        request.validated['statement'] = db_statement
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_statement', 'Statement uid is missing', _tn.get(_.wrongStatement))


def valid_argument(request):
    """
    Given an uid, query the argument object from the database and return it in the request.

    :param request:
    :return:
    """
    argument_id = request.json_body.get('uid')
    db_argument = DBDiscussionSession.query(Argument).filter(Argument.uid == argument_id,
                                                             Argument.is_disabled == False).first() if is_integer(
        argument_id) else None

    if db_argument:
        request.validated['argument'] = db_argument
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_argument', 'Argument uid is missing', _tn.get(_.wrongArgument))


def valid_statement_text(request):
    """
    Validate the correct length of a statement's input.

    :param request:
    :return:
    """
    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    text = request.json_body.get('statement', '')

    if len(text) < min_length:
        __set_min_length_error(request, min_length)
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
# UI-related

def valid_language(request):
    """
    Given a nickname of a user, return the object from the database.

    :param request:
    :return:
    """
    lang = request.json_body.get('lang')
    _tn = Translator(get_language_from_cookie(request))
    if not lang:
        __add_error(request, 'valid_language', 'Invalid language', _tn.get(_.checkLanguage))
        return

    db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=lang).first()
    if db_lang:
        request.validated['lang'] = db_lang
        return True
    else:
        __add_error(request, 'valid_language', 'Invalid language {}'.format(lang), _tn.get(_.checkLanguage))
        return False


def valid_ui_locales(request):
    """
    Get provided language from form, else interpret it from the request.

    :param request:
    :return:
    """
    lang = request.json_body.get('ui_locales')
    if not lang:
        lang = get_language_from_cookie(request)
    request.validated['ui_locales'] = lang


# #############################################################################
# General validation

def valid_review_reason(request):
    """
    Given an reason, validates the correctness for our review system.

    :param request:
    :return:
    """
    reason = request.json_body.get('reason')
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).first()

    if db_reason or reason in ['optimization', 'duplicate']:
        request.validated['reason'] = reason
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_review_reason', 'Invalid reason', _tn.get(_.internalError))


def valid_text_values(request):
    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    tvalues = request.json_body.get('text_values')
    if not tvalues:
        __set_min_length_error(request, min_length)

    error = False
    for text in tvalues:
        if len(text) < min_length:
            __set_min_length_error(request, min_length)
            error = True

    if not error:
        request.validated['text_values'] = tvalues


def valid_premisegroup(request):
    """
    Validates the uid of a premisegroup

    :param request:
    :return:
    """
    pgroup_uid = request.json_body.get('uid')
    db_pgroup = DBDiscussionSession.query(PremiseGroup).get(pgroup_uid) if is_integer(pgroup_uid) else None

    if db_pgroup:
        request.validated['pgroup'] = db_pgroup
    else:
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_premisegroup', 'PGroup uid is missing', _tn.get(_.internalError))


def valid_premisegroups(request):
    """
    Validates the correct build of premisegroups

    :param request:
    :return:
    """
    premisegroups = request.json_body.get('premisegroups')
    if not premisegroups or not isinstance(premisegroups, list) or not all(
            [isinstance(l, list) for l in premisegroups]):
        _tn = Translator(get_language_from_cookie(request))
        __add_error(request, 'valid_premisegroups', 'Invalid conclusion id', _tn.get(_.requestFailed))
        return

    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    for premisegroup in premisegroups:
        for premise in premisegroup:
            if len(premise) < min_length:
                __set_min_length_error(request, min_length)
    request.validated['premisegroups'] = premisegroups


def has_keywords(*keywords):
    """
    Verify that specified keywords exist in the request.json_body.

    :param keywords: tuple of keys and their expected types in request.json_body
    :return:
    """

    def valid_keywords(request):
        error_occured = False
        for (keyword, ktype) in keywords:
            value = request.json_body.get(keyword)
            if value is not None and isinstance(value, ktype):
                request.validated[keyword] = value
            elif value is None:
                __add_error(request, 'has_keywords', 'Parameter {} missing'.format(keyword),
                            '{} is missing'.format(keyword))
                error_occured = True
            else:
                __add_error(request, 'has_keywords', 'Parameter {} has wrong type'.format(keyword),
                            '{} is {}, expected {}'.format(keyword, type(keyword), ktype))
                error_occured = True
        return not error_occured

    return valid_keywords


def has_maybe_keywords(*keywords):
    """
    Check if parameter exists. If not, provide fallback value.

    :param keywords: 3-tuple of keys, their expected types in request.json_body and a default value
    :return:
    """

    def valid_keywords(request):
        error_occured = False
        for (keyword, ktype, kdefault) in keywords:
            value = request.json_body.get(keyword)
            if value is not None and isinstance(value, ktype):
                request.validated[keyword] = value
            elif value is None:
                request.validated[keyword] = kdefault
            else:
                __add_error(request, 'has_keywords', 'Parameter {} has wrong type'.format(keyword),
                            '{} is {}, expected {}'.format(keyword, type(keyword), ktype))
                error_occured = True
        return not error_occured

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
