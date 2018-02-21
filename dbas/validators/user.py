# coding=utf-8
"""
When testing for valid / authenticated users, use these functions.
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Statement, Argument, TextVersion
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer
from dbas.lib import nick_of_anonymous_user
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.lib import add_error


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
        add_error(request, 'valid_user', 'Invalid user', _tn.get(_.checkNickname))
        return False


def valid_user_as_author_of_statement(request):
    """

    :param request:
    :return:
    """
    if valid_user(request):
        db_user = request.validated['user']
        uid = request.json_body.get('uid')
        db_textversion = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(
            TextVersion.uid.asc()).first() if is_integer(uid) else None
        if db_textversion and db_textversion.author_uid == db_user.uid:
            request.validated['statement'] = DBDiscussionSession.query(Statement).get(uid)
            return True
        else:
            _tn = Translator(get_language_from_cookie(request))
            add_error(request, '', _tn.get(_.userIsNotAuthorOfStatement))
    return False


def valid_user_as_author_of_argument(request):
    """

    :param request:
    :return:
    """
    if valid_user(request):
        db_user = request.validated['user']
        uid = request.json_body.get('uid')
        db_argument = DBDiscussionSession. \
            query(Argument).filter(Argument.uid == uid,
                                   Argument.author_uid == db_user.uid).first() if is_integer(uid) else None
        if db_argument:
            request.validated['argument'] = db_argument
            return True
        else:
            _tn = Translator(get_language_from_cookie(request))
            add_error(request, '', _tn.get(_.userIsNotAuthorOfArgument))
    return False


def valid_user_as_author(request):
    """

    :param request:
    :return:
    """
    _tn = Translator(get_language_from_cookie(request))
    if valid_user(request):
        db_user = request.validated['user']
        if db_user.is_admin() or db_user.is_author():
            return True
        else:
            add_error(request, 'valid_user_as_author', 'Invalid user group', _tn.get(_.justLookDontTouch))
    return False


def valid_user_as_admin(request):
    """

    :param request:
    :return:
    """
    _tn = Translator(get_language_from_cookie(request))
    if valid_user(request):
        db_user = request.validated['user']
        if db_user.is_admin():
            return True
        else:
            add_error(request, 'valid_user_as_admin', 'Invalid user group', _tn.get(_.justLookDontTouch))
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
