"""
When testing for valid / authenticated users, use these functions.
"""
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Statement, Argument, TextVersion
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.core import has_keywords_in_json_path
from dbas.validators.lib import add_error


def valid_user(request, **kwargs):
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
        add_error(request, 'Invalid user', _tn.get(_.checkNickname))
        return False


def valid_user_optional(request, **kwargs):
    """
    If user is provided, query her, else return the anonymous user.

    :param request:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).one_or_none()

    if not db_user:
        db_user = DBDiscussionSession.query(User).get(1)

    request.validated['user'] = db_user
    return True


def valid_user_as_author_of_statement(request):
    """

    :param request:
    :return:
    """
    if not has_keywords_in_json_path(('statement_id', int))(request):
        return False

    statement_id = request.validated['statement_id']

    if valid_user(request):
        db_user = request.validated['user']
        db_textversion = DBDiscussionSession.query(TextVersion) \
            .filter_by(statement_uid=statement_id) \
            .order_by(TextVersion.uid.asc()).first()
        if db_textversion and db_textversion.author_uid == db_user.uid:
            request.validated['statement'] = DBDiscussionSession.query(Statement).get(statement_id)
            return True
        else:
            _tn = Translator(get_language_from_cookie(request))
            add_error(request, _tn.get(_.userIsNotAuthorOfStatement))
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
            add_error(request, _tn.get(_.userIsNotAuthorOfArgument))
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
            add_error(request, 'Invalid user group', _tn.get(_.justLookDontTouch))
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
            add_error(request, 'Invalid user group', _tn.get(_.justLookDontTouch))
    return False
