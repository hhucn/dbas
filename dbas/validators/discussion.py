"""
Discussion-related validators for statements, arguments, ...
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, Argument, PremiseGroup
from dbas.handler import issue as issue_handler
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.core import has_keywords
from dbas.validators.lib import add_error, escape_if_string


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
        add_error(request, 'Invalid issue')
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
    title = escape_if_string(request.validated, 'title')
    info = escape_if_string(request.validated, 'info')
    long_info = escape_if_string(request.validated, 'long_info')
    db_dup1 = DBDiscussionSession.query(Issue).filter_by(title=title).all()
    db_dup2 = DBDiscussionSession.query(Issue).filter_by(info=info).all()
    db_dup3 = DBDiscussionSession.query(Issue).filter_by(long_info=long_info).all()
    if db_dup1 or db_dup2 or db_dup3:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Issue data is a duplicate', _tn.get(_.duplicate))
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
    add_error(request, 'Issue is read only', _tn.get(_.discussionIsReadOnly))
    return False


def valid_conclusion(request):
    """
    Given a conclusion id, query the object from the database and return it in the request.

    :param request:
    :return:
    """
    conclusion_id = request.json_body.get('conclusion_id')
    issue = request.validated.get('issue')
    if not issue:
        issue = DBDiscussionSession.query(Issue).get(issue_handler.get_issue_id(request))

    if conclusion_id and isinstance(conclusion_id, int):
        db_conclusion = DBDiscussionSession.query(Statement).filter_by(uid=conclusion_id,
                                                                       issue_uid=issue.uid,
                                                                       is_disabled=False).first()
        if db_conclusion:
            request.validated['conclusion'] = db_conclusion
            return True
        else:
            _tn = Translator(get_language_from_cookie(request))
            add_error(request, 'Conclusion is missing', _tn.get(_.conclusionIsMissing))
            return False
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Conclusion id is missing', _tn.get(_.conclusionIsMissing))
        return False


def valid_statement(request):
    """
    Given an uid, query the statement object from the database and return it in the request.

    :param request:
    :return:
    """
    statement_id = request.json_body.get('uid')
    db_statement = None
    if is_integer(statement_id):
        db_statement = DBDiscussionSession.query(Statement).filter(Statement.uid == statement_id,
                                                                   Statement.is_disabled == False).first()

    if db_statement:
        request.validated['statement'] = db_statement
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Statement uid is missing', _tn.get(_.wrongStatement))
        return False


def valid_argument(request):
    """
    Given an uid, query the argument object from the database and return it in the request.

    :param request:
    :return:
    """
    argument_id = request.json_body.get('uid')
    db_argument = None
    if is_integer(argument_id):
        db_argument = DBDiscussionSession.query(Argument).filter(Argument.uid == argument_id,
                                                                 Argument.is_disabled == False).first()

    if db_argument:
        request.validated['argument'] = db_argument
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Argument uid is missing', _tn.get(_.wrongArgument))
        return False


def valid_statement_text(request):
    """
    Validate the correct length of a statement's input.

    :param request:
    :return:
    """
    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    text = escape_if_string(request.json_body, 'statement')

    if not text or text and len(text) < min_length:
        __set_min_length_error(request, min_length)
        return False
    else:
        request.validated['statement'] = text
        return True


def valid_premisegroup(request):
    """
    Validates the uid of a premisegroup

    :param request:
    :return:
    """
    pgroup_uid = request.json_body.get('uid')
    db_pgroup = None
    if is_integer(pgroup_uid):
        db_pgroup = DBDiscussionSession.query(PremiseGroup).get(pgroup_uid)

    if db_pgroup:
        request.validated['pgroup'] = db_pgroup
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'PGroup uid is missing', _tn.get(_.internalError))
        return False


def valid_premisegroups(request):
    """
    Validates the correct build of premisegroups

    :param request:
    :return:
    """
    premisegroups = request.json_body.get('premisegroups')
    if not premisegroups \
            or not isinstance(premisegroups, list)\
            or not all([isinstance(l, list) for l in premisegroups]):
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid conclusion id', _tn.get(_.requestFailed))
        return False

    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    for premisegroup in premisegroups:
        for premise in premisegroup:
            if isinstance(premise, str):
                if len(premise) < min_length:
                    __set_min_length_error(request, min_length)
                    return False
            else:
                add_error(request, 'At least one premise isn\'t a string!')
                return False

    request.validated['premisegroups'] = premisegroups
    return True


def valid_statement_or_argument(request):
    is_argument = request.json_body.get('is_argument')
    t = Argument if is_argument else Statement
    uid = request.json_body.get('uid')
    if uid:
        db_arg_or_stmt = DBDiscussionSession.query(t).get(uid)
    else:
        add_error(request, 'Missing uid for ' + t.__name__)
        return False

    if db_arg_or_stmt:
        request.validated['arg_or_stmt'] = db_arg_or_stmt
        return True
    else:
        add_error(request, t.__name__ + ' is invalid')
        return False


def valid_text_values(request):
    min_length = request.registry.settings.get('settings:discussion:statement_min_length', 10)
    tvalues = escape_if_string(request.json_body, 'text_values')
    if not tvalues:
        __set_min_length_error(request, min_length)
        return False

    error = False
    for text in tvalues:
        if len(text) < min_length:
            __set_min_length_error(request, min_length)
            error = True

    if not error:
        request.validated['text_values'] = tvalues
        return True
    return False


# -----------------------------------------------------------------------------
# Helper functions

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
    add_error(request, 'Text too short', error_msg)
