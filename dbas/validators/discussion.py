"""
Discussion-related validators for statements, arguments, ...
"""
from os import environ
from typing import Callable, Set, Optional

from pyramid.request import Request

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, Argument, PremiseGroup, StatementToIssue
from dbas.handler import issue as issue_handler
from dbas.handler.language import get_language_from_cookie
from dbas.input_validator import is_integer, related_with_support, check_belonging_of_premisegroups
from dbas.lib import Relations, Attitudes, attitude_mapper, relation_mapper
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.core import has_keywords_in_json_path, has_keywords_in_path
from dbas.validators.lib import add_error, escape_if_string


def valid_issue_by_id(request):
    """
    Query issue from database and put it into the request.

    :param request:
    :return:
    """

    issue_id = issue_handler.get_issue_id(request)

    if issue_id:
        db_issue: Issue = DBDiscussionSession.query(Issue).get(issue_id)

        if db_issue and db_issue.is_disabled:
            add_error(request, 'Issue no longer available', status_code=410)
            return False
        else:
            request.validated['issue'] = db_issue
            return True

    add_error(request, 'Invalid issue')
    return False


def valid_any_issue_by_id(request):
    """
    Query issue from database and put it into the request, even if it is disabled

    :param request:
    :return:
    """

    issue_id = issue_handler.get_issue_id(request)
    if issue_id:
        db_issue: Issue = DBDiscussionSession.query(Issue).get(issue_id)
        request.validated['issue'] = db_issue
        return True

    add_error(request, 'Invalid issue {}'.format(issue_id))
    return False


def valid_issue_by_slug(request: Request) -> bool:
    """
    Query issue by slug from the path.

    :param request:
    :return:
    """
    if has_keywords_in_path(('slug', str))(request):
        db_issue: Issue = DBDiscussionSession.query(Issue).filter(
            Issue.slug == request.validated['slug']).one_or_none()

        if db_issue:
            if db_issue.is_disabled:
                add_error(request, 'Issue no longer available', location='path', status_code=410)
                return False
            else:
                request.validated['issue'] = db_issue
                return True

        add_error(request, 'Invalid slug \'{}\' for issue'.format(request.validated['slug']), location='path',
                  status_code=404)
    return False


def __check_for_empty_fields(title: str, info: str, long_info: str, request: dict) -> dict:
    """
    This method checks if there is a empty field in the data of the new issue.
    It also creates a error-message with the empty fields.

    :param title: The title of the new issue
    :param info: The info of the new issue
    :param long_info: The long info of the new issue
    :param request: The request with the data of the new issue
    :return: a dict with a boolean which tells if there is any empty field and a equivalent error-message.
    """
    _tn = Translator(get_language_from_cookie(request))
    error = _tn.get(_.newIssueErrorMsg) + ': '

    title_is_empty = title.strip() == ''
    info_is_empty = info.strip() == ''
    long_info_is_emtpy = long_info.strip() == ''

    if title_is_empty:
        error = error + _tn.get(_.newIssueTitle) + ', '
    if info_is_empty:
        error = error + _tn.get(_.newIssueInfo) + ', '
    if long_info_is_emtpy:
        error = error + _tn.get(_.newIssueLongInfo) + ', '

    return {
        "contains_empty_field": title_is_empty or info_is_empty or long_info_is_emtpy,
        "error": error[:-2]
    }


def __check_for_duplicated_field(title: str, info: str, long_info: str, request: dict) -> dict:
    """
    This method checks if there is a duplication in any field of the new issue.
    It also creates a error-message with the fields which are containing the duplication.

    :param title: The title of the new issue
    :param info: The info of the new issue
    :param long_info: The long info of the new issue
    :param request: The request with the data of the new issue
    :return: a dict with a boolean which tells if there is any duplicated field and a equivalent error-message.
    """
    _tn = Translator(get_language_from_cookie(request))
    error = _tn.get(_.duplicate) + ': '

    title_is_duplicate = DBDiscussionSession.query(Issue).filter_by(title=title).all()
    info_is_duplicate = DBDiscussionSession.query(Issue).filter_by(info=info).all()
    long_info_is_duplicate = DBDiscussionSession.query(Issue).filter_by(long_info=long_info).all()

    if title_is_duplicate:
        error = error + _tn.get(_.newIssueTitle) + ', '
    if info_is_duplicate:
        error = error + _tn.get(_.newIssueInfo) + ', '
    if long_info_is_duplicate:
        error = error + _tn.get(_.newIssueLongInfo) + ', '

    return {
        "contains_duplicated_field": title_is_duplicate or info_is_duplicate or long_info_is_duplicate,
        "error": error[:-2]
    }


def valid_new_issue(request):
    """
    Verifies given data for a new issue

    :param request:
    :return:
    """
    fn_validator = has_keywords_in_json_path(('title', str), ('info', str), ('long_info', str))
    if not fn_validator(request):
        return False

    title = escape_if_string(request.validated, 'title')
    info = escape_if_string(request.validated, 'info')
    long_info = escape_if_string(request.validated, 'long_info')

    new_issue = __check_for_empty_fields(title=title, info=info, long_info=long_info, request=request)
    if new_issue.get('contains_empty_field'):
        add_error(request, 'There is an empty field', new_issue.get('error'))
        return False
    new_issue = __check_for_duplicated_field(title=title, info=info, long_info=long_info, request=request)
    if new_issue.get('contains_duplicated_field'):
        add_error(request, 'Issue data is a duplicate', new_issue.get('error'))
        return False

    return True


def valid_issue_not_readonly(request):
    """
    Get issue from database and verify that it is not read-only.

    :param request:
    :return:
    """
    if valid_issue_by_id(request) and not request.validated.get('issue').is_read_only:
        return True
    _tn = Translator(get_language_from_cookie(request))
    uid = request.validated.get('issue').uid if request.validated.get('issue') else -1
    add_error(request, 'Issue {} is read only'.format(uid), _tn.get(_.discussionIsReadOnly))
    return False


def valid_conclusion(request):
    """
    Given a conclusion id, query the object from the database and return it in the request.

    :param request:
    :return:
    """
    conclusion_id = request.json_body.get('conclusion_id')
    issue = request.validated.get('issue')
    _tn = Translator(get_language_from_cookie(request))

    if not issue:
        find_issue_in_request = issue_handler.get_issue_id(request)
        if find_issue_in_request:
            issue = DBDiscussionSession.query(Issue).get(issue_handler.get_issue_id(request))
        else:
            add_error(request, 'Issue is missing', _tn.get(_.issueNotFound))
            return False

    if conclusion_id and isinstance(conclusion_id, int):
        db_statement2issue = DBDiscussionSession.query(StatementToIssue).filter(StatementToIssue.issue_uid == issue.uid,
                                                                                StatementToIssue.statement_uid == conclusion_id).first()
        if db_statement2issue:
            db_conclusion = DBDiscussionSession.query(Statement).filter_by(uid=conclusion_id,
                                                                           is_disabled=False).first()
            if db_conclusion:
                request.validated['conclusion'] = db_conclusion
                return True

    add_error(request, 'Conclusion id is missing', _tn.get(_.conclusionIsMissing))
    return False


def valid_position(request):
    """
    Check if given statement is a position and belongs to the queried issue.

    :param request: Request
    :return:
    """
    if not valid_issue_by_slug(request):
        return False

    if has_keywords_in_path(('position_id', int))(request):
        position_id = request.validated['position_id']
        db_position: Statement = DBDiscussionSession.query(Statement).get(position_id)
        if not db_position:
            add_error(request, 'Position with id {} not found'.format(position_id), location='path')
            return False
        if db_position.is_disabled:
            add_error(request, 'Position is disabled', location='path', status_code=410)
            return False
        if not db_position.is_position:
            add_error(request, 'Queried statement is not a valid position', location='path')
            return False

        db_statement2issues = DBDiscussionSession.query(StatementToIssue).filter(
            StatementToIssue.statement_uid == position_id,
            StatementToIssue.issue_uid == request.validated['issue'].uid).first()
        if not db_statement2issues:
            add_error(request, 'Position does not belong to the queried issue', location='path')
            return False
        request.validated['position']: Statement = db_position
        return True
    return False


def valid_reason_in_body(request):
    long_error = "JSON Body has to contain the key \'reason\'"
    reason = request.json_body.get('reason')

    if not (reason and isinstance(reason, str)):
        add_error(request, "Missing \'reason\' in body.", long_error)
        return False

    request.validated["reason-text"] = reason

    return True


def valid_new_position_in_body(request):
    long_error = "JSON Body has to look like this: {\"position\": \"my position\", \"reason\": \"My reason for the position\" "

    position = request.json_body.get('position')

    if not (position and isinstance(position, str)):
        add_error(request, "Missing \'position\' in body.", long_error)
        return False

    request.validated["position-text"] = position

    return True


def valid_attitude(request):
    """
    Check if given statement is a position and belongs to the queried issue.

    :param request: Request
    :return:
    """
    attitudes = [attitude.value for attitude in Attitudes if attitude is not Attitudes.DONT_KNOW]

    if has_keywords_in_path(('attitude', str))(request):
        attitude = request.validated['attitude']
        if attitude not in attitudes:
            add_error(request,
                      'Your attitude is not correct. Received \'{}\', expected one of {}'.format(attitude, attitudes),
                      location='path')
            return False
        request.validated['attitude'] = attitude_mapper[attitude]
        return True
    return False


def valid_relation(request):
    """
    Parse relation from path.

    :param request: Request
    :return:
    """
    relation = request.matchdict.get('relation')
    if not relation:
        add_error(request, 'Relation is missing in path', location='path')
        return False

    list_of_attacks = [relation.value for relation in list(Relations)]
    if relation not in list_of_attacks:
        add_error(request,
                  'Your relation is not correct. Received \'{}\', expected one of {}'.format(relation, list_of_attacks),
                  location='path')
        return False

    request.validated['relation'] = relation_mapper[relation]
    return True


def valid_statement(location, depends_on: Set[Callable[[Request], bool]] = None) -> Callable[[Request], bool]:
    if depends_on is None:
        depends_on = set()

    def inner(request):
        if depends_on and not all([dependence(request) for dependence in depends_on if depends_on]):
            return False

        if __valid_id_from_location(request, 'statement_id', location):
            db_issue: Optional[Issue] = request.validated.get('issue')
            statement_id = request.validated['statement_id']
            db_statement: Statement = DBDiscussionSession.query(Statement).get(statement_id)
            if not db_statement:
                add_error(request, 'Statement with id {} could not be found'.format(statement_id), location='path')
                return False
            if db_statement.is_disabled:
                add_error(request, 'Statement no longer available', location='path', status_code=410)
                return False
            if db_issue and db_statement not in db_issue.statements:
                add_error(request, 'Statement does not belong to issue', location='path')
                return False

            request.validated['statement'] = db_statement

            return True
        return False

    return inner


def valid_argument(location, depends_on: Set[Callable[[Request], bool]] = None) -> Callable[[Request], bool]:
    if depends_on is None:
        depends_on = set()

    def inner(request):
        if not all([dependence(request) for dependence in depends_on if depends_on]):
            return False

        if __valid_id_from_location(request, 'argument_id', location):
            argument_id = request.validated['argument_id']
            db_entity = __validate_enabled_entity(request, request.validated.get('issue'), Argument, argument_id)
            if db_entity:
                request.validated['argument'] = db_entity
                return True
            add_error(request, 'Argument with id {} could not be found'.format(argument_id))
            return False
        return False

    return inner


def valid_reaction_arguments(request):
    if not has_keywords_in_path(('arg_id_user', int), ('arg_id_sys', int))(request):
        return False
    if not valid_issue_by_slug(request):
        return False

    arg_id_user: int = request.validated['arg_id_user']
    arg_id_sys: int = request.validated['arg_id_sys']
    issue: Issue = request.validated['issue']

    db_arg_user: Argument = __validate_enabled_entity(request, issue, Argument, arg_id_user)
    db_arg_sys: Argument = __validate_enabled_entity(request, issue, Argument, arg_id_sys)

    if not db_arg_sys or not db_arg_user:
        return False

    request.validated['arg_user'] = db_arg_user
    request.validated['arg_sys'] = db_arg_sys
    return True


def valid_support(request):
    if not valid_reaction_arguments(request):
        return False

    db_arg_user = request.validated['arg_user']
    db_arg_sys = request.validated['arg_sys']

    if db_arg_user == db_arg_sys:
        add_error(request, verbose_short="The Arguments are the same!", location='path', status_code=404)
        return False

    if not related_with_support(db_arg_user.uid, db_arg_sys.uid):
        add_error(request, "The Arguments don't share the same opinion", location='path', status_code=404)
        return False

    return True


def valid_text_length_of(keyword):
    """
    Validate the correct length of a statement's or news titles or ... input.

    :param keyword:
    :return:
    """

    def inner(request):
        min_length = int(environ.get('MIN_LENGTH_OF_STATEMENT', 10))
        text = escape_if_string(request.json_body, keyword)

        if not text or text and len(text) < min_length:
            __set_min_length_error(request, min_length)
            return False
        else:
            request.validated[keyword] = text
            return True

    return inner


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


def valid_premisegroup_in_path(request):
    """
    Sets the premisegroup id from the path into the json_body and executes valid_premisegroup

    :param request:
    :return:
    """
    pgroup_uid = request.matchdict.get('id', [None])[0]
    db_pgroup = None
    if is_integer(pgroup_uid):
        db_pgroup = DBDiscussionSession.query(PremiseGroup).get(pgroup_uid)

    if db_pgroup:
        request.validated['pgroup_uid'] = db_pgroup
        return True
    else:
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'PGroup uid is missing in path', _tn.get(_.internalError))
        return False


def valid_premisegroups(request):
    """
    Validates the correct build of premisegroups

    :param request:
    :return:
    """
    premisegroups = request.json_body.get('premisegroups')
    if not premisegroups \
            or not isinstance(premisegroups, list) \
            or not all([isinstance(l, list) for l in premisegroups]):
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'Invalid conclusion id', _tn.get(_.requestFailed))
        return False

    min_length = int(environ.get('MIN_LENGTH_OF_STATEMENT', 10))
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


def valid_list_of_premisegroups_in_path(request):
    """
    Fetches the list of premisegroups and checks their validity

    :param request:
    :return:
    """
    pgroup_uids = request.matchdict.get('pgroup_ids')

    if not pgroup_uids or not valid_issue_by_slug(request):
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'PGroup uids are missing in path', _tn.get(_.internalError))
        return False

    for pgroup in pgroup_uids:
        if not is_integer(pgroup):
            _tn = Translator(get_language_from_cookie(request))
            add_error(request, 'One uid of the pgroups in path is malicious', _tn.get(_.internalError))
            return False

    if not check_belonging_of_premisegroups(request.validated['issue'].uid, pgroup_uids):
        _tn = Translator(get_language_from_cookie(request))
        add_error(request, 'One uid of the pgroups does not belong to the issue', _tn.get(_.internalError))
        return False

    for pgroup in pgroup_uids:
        if not DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=pgroup).first():
            _tn = Translator(get_language_from_cookie(request))
            add_error(request, 'One uid of the pgroups argument is not supportive', _tn.get(_.internalError))
            return False

    request.validated['pgroup_uids'] = [int(uid) for uid in pgroup_uids]
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
    min_length = int(environ.get('MIN_LENGTH_OF_STATEMENT', 10))
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


def valid_reason_and_position_not_equal(request) -> bool:
    """
    Check if provided position and reason have the same content.

    :param request:
    :return:
    """
    if not valid_new_position_in_body(request) or not valid_reason_in_body(request) or not valid_issue_by_slug(request):
        return False

    position: str = request.validated.get('position-text').strip().lower()
    reason: str = request.validated.get('reason-text').strip().lower()
    issue: Issue = request.validated.get('issue')

    _tn = Translator(issue.lang)

    if position == reason:
        add_error(request, _tn.get(_.premiseAndConclusionAreEqual))
        return False

    return True


# -----------------------------------------------------------------------------
# Helper functions

def __validate_enabled_entity(request: Request, db_issue: Optional[Issue], entity, entity_id):
    """
    Get entity-id from path and query it in the database. Check if it belongs to the queried issue and if it is disabled.

    :param request:
    :param db_issue:
    :param entity:
    :param entity_id:
    :return:
    """
    db_entity: entity = DBDiscussionSession.query(entity).get(entity_id)
    if not db_entity:
        add_error(request, 'Entity with id {} could not be found'.format(entity_id), location='path')
        return None
    if db_entity.is_disabled:
        add_error(request, '{} no longer available'.format(db_entity.__class__.__name__), location='path',
                  status_code=410)
        return None
    if db_issue and not db_entity.issue_uid == db_issue.uid:
        add_error(request, '{} does not belong to issue'.format(db_entity.__class__.__name__), location='path')
        return None
    return db_entity


def __valid_id_from_location(request, entity_name, location='path') -> int:
    """
    Find id in specified location.

    :param request:
    :param entity_name:
    :param location:
    :return:
    """
    if location == 'path':
        success = has_keywords_in_path((entity_name, int))(request)
        return success
    elif location == 'json_body':
        if entity_name in request.json_body:
            value = request.json_body.get(entity_name)
            try:
                request.validated[entity_name] = int(value)
                return True
            except ValueError:
                add_error(request, '\'{}\' is not int parsable!'.format(value))
                return False
        else:
            add_error(request, '{} is missing in json_body'.format(entity_name))
            return False
    else:
        raise KeyError("location has to be one of: ('path', 'json_body')")


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
