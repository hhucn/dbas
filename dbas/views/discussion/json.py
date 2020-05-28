import logging
from typing import List

from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Issue, User
from dbas.handler import history as history_handler, user
from dbas.handler.arguments import set_arguments_premises, get_all_infos_about_argument, get_arguments_by_statement
from dbas.handler.history import SessionHistory
from dbas.handler.issue import set_discussions_properties, get_issue_dict_for
from dbas.handler.language import get_language_from_cookie
from dbas.handler.statements import set_position, set_positions_premise, set_correction_of_statement, \
    set_seen_statements, get_logfile_for_statements
from dbas.handler.voting import clear_vote_and_seen_values_of_user
from dbas.helper.query import mark_statement_or_argument
from dbas.lib import relation_mapper, escape_string, get_discussion_language
from dbas.strings.translator import Translator
from dbas.validators.common import valid_language
from dbas.validators.core import validate, has_keywords_in_json_path
from dbas.validators.discussion import valid_any_issue_by_id, valid_issue_not_readonly, valid_conclusion, \
    valid_premisegroups, valid_argument, valid_new_issue, valid_statement_or_argument, valid_issue_by_id, \
    valid_statement
from dbas.validators.user import valid_user, valid_user_optional
from dbas.views.json import __modifiy_discussion_url

LOG = logging.getLogger(__name__)


@view_config(route_name='get_user_history', renderer='json')
@validate(valid_user)
def get_user_history(request):
    """
    Request the complete user track.

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales: str = get_language_from_cookie(request)
    user: User = request.validated['user']
    return history_handler.get_from_database(user, ui_locales)


@view_config(route_name='get_all_posted_statements', renderer='json')
@validate(valid_user)
def get_all_posted_statements(request):
    """
    Request for all statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_textversions(db_user, ui_locales).get('statements', [])


@view_config(route_name='get_all_edits', renderer='json')
@validate(valid_user)
def get_all_edits_of_user(request):
    """
    Request for all edits of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_textversions(db_user, ui_locales).get('edits', [])


@view_config(route_name='get_all_marked_arguments', renderer='json')
@validate(valid_user)
def get_all_marked_arguments(request):
    """
    Request for all marked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_marked_arguments(db_user, ui_locales)


@view_config(route_name='get_all_marked_statements', renderer='json')
@validate(valid_user)
def get_all_marked_statements(request):
    """
    Request for all marked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_marked_statements(db_user, ui_locales)


@view_config(route_name='get_all_argument_clicks', renderer='json')
@validate(valid_user)
def get_all_argument_clicks(request):
    """
    Request for all clicked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_clicked_arguments(db_user, ui_locales)


@view_config(route_name='get_all_statement_clicks', renderer='json')
@validate(valid_user)
def get_all_statement_clicks(request):
    """
    Request for all clicked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return user.get_clicked_statements(db_user, ui_locales)


@view_config(route_name='delete_user_history', renderer='json')
@validate(valid_user)
def delete_user_history(request):
    """
    Request to delete the users history.

    :param request: request of the web server
    :return: json-dict()
    """
    LOG.debug("Delete user history")
    db_user = request.validated['user']
    return history_handler.delete_in_database(db_user)


@view_config(route_name='delete_statistics', renderer='json')
@validate(valid_user)
def delete_statistics(request):
    """
    Request to delete votes/clicks of the user.

    :param request: request of the web server
    :return: json-dict()
    """
    LOG.debug("Delete votes and clicks of a user")
    db_user = request.validated['user']
    return clear_vote_and_seen_values_of_user(db_user)


@view_config(route_name='set_discussion_properties', renderer='json')
@validate(valid_user, valid_any_issue_by_id, has_keywords_in_json_path(('property', bool), ('value', str)))
def set_discussion_properties(request):
    """
    Set availability, read-only, ... flags in the admin panel.

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Request.params: %s", request.json_body)
    _tn = Translator(get_language_from_cookie(request))

    prop = request.validated['property']
    db_user = request.validated['user']
    issue = request.validated['issue']
    value = request.validated['value']
    return set_discussions_properties(db_user, issue, prop, value, _tn)


@view_config(route_name='set_new_start_argument', renderer='json')
@validate(valid_user, valid_issue_not_readonly,
          has_keywords_in_json_path(('position', str), ('reason', str), ('feature_data', dict)))
def set_new_start_argument(request: Request):
    """
    Inserts a new argument as starting point into the database

    :param request: request of the web server
    :return: a status code, if everything was successful
    """
    LOG.debug("Insert a new argument as starting point: %s", request.json_body)
    reason = request.validated['reason']

    # set the new position
    LOG.debug("Set conclusion/position")
    prepared_dict_pos = set_position(request.validated['user'], request.validated['issue'],
                                     request.validated['position'], request.validated['feature_data'])

    reponse: Response = request.response
    if not prepared_dict_pos['errors']:
        LOG.debug("Set premise/reason")
        session_history = SessionHistory(request.cookies.get('_HISTORY_'))
        prepared_dict_pos = set_positions_premise(request.validated['issue'],
                                                  request.validated['user'],
                                                  DBDiscussionSession.query(Statement).get(
                                                      prepared_dict_pos['statement_uids'][0]),
                                                  [[reason]],
                                                  True,
                                                  session_history,
                                                  request.mailer)
    else:
        reponse.status_code = 400

    __modifiy_discussion_url(prepared_dict_pos)

    reponse.json_body = prepared_dict_pos
    return reponse


@view_config(route_name='set_new_start_premise', renderer='json')
@validate(valid_user, valid_issue_not_readonly, valid_conclusion, valid_premisegroups,
          has_keywords_in_json_path(('supportive', bool)))
def set_new_start_premise(request):
    """
    Sets new premise for the start

    :param request: request of the web server
    :return: json-dict()
    """
    LOG.debug("Set new premise for start: %s", request.json_body)
    session_history = SessionHistory(request.cookies.get('_HISTORY_'))
    prepared_dict = set_positions_premise(request.validated['issue'],
                                          request.validated['user'],
                                          request.validated['conclusion'],
                                          request.validated['premisegroups'],
                                          request.validated['supportive'],
                                          session_history,
                                          request.mailer)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_new_premises_for_argument', renderer='json')
@validate(valid_user, valid_premisegroups, valid_argument(location='json_body', depends_on={valid_issue_not_readonly}),
          has_keywords_in_json_path(('attack_type', str)))
def set_new_premises_for_argument(request):
    """
    Sets a new premise for an argument

    :param request: request of the web server
    :return: json-dict()
    """
    LOG.debug("Set new premise for an argument. %s", request.json_body)
    session_history = SessionHistory(request.cookies.get('_HISTORY_'))
    prepared_dict = set_arguments_premises(request.validated['issue'],
                                           request.validated['user'],
                                           request.validated['argument'],
                                           request.validated['premisegroups'],
                                           relation_mapper[request.validated['attack_type']],
                                           session_history,
                                           request.mailer)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_correction_of_statement', renderer='json')
@validate(valid_user, has_keywords_in_json_path(('elements', list)))
def set_correction_of_some_statements(request):
    """
    Sets a new textvalue for a statement

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Set textvalue for a statement: %s", request.json_body)
    ui_locales = get_language_from_cookie(request)
    corrections = request.validated['elements']
    db_user = request.validated['user']
    _tn = Translator(ui_locales)
    return set_correction_of_statement(corrections, db_user, _tn)


def create_issue_after_validation(request: Request):
    LOG.debug("Set a new issue: %s", request.json_body)

    db_issue = Issue(title=escape_string(request.validated['title']),
                     info=escape_string(request.validated['info']),
                     long_info=escape_string(request.validated['long_info']),
                     author=request.validated['user'],
                     is_read_only=request.validated['is_read_only'],
                     is_private=not request.validated['is_public'],
                     language=request.validated['lang'])
    DBDiscussionSession.add(db_issue)
    return {'issue': get_issue_dict_for(db_issue, 0, request.validated['lang'].ui_locales)}


@view_config(route_name='set_new_issue', renderer='json')
@validate(valid_user, valid_language, valid_new_issue,
          has_keywords_in_json_path(('is_public', bool), ('is_read_only', bool)))
def set_new_issue(request):
    """

    :param request: current request of the server
    :return:
    """
    return create_issue_after_validation(request)


@view_config(route_name='set_seen_statements', renderer='json')
@validate(valid_user, has_keywords_in_json_path(('uids', list)))
def set_statements_as_seen(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    LOG.debug("Set statement as seen. %s", request.json_body)
    statements: List[Statement] = [DBDiscussionSession.query(Statement).get(uid) for uid in request.validated['uids']]
    return set_seen_statements(statements, request.path, request.validated['user'])


@view_config(route_name='mark_statement_or_argument', renderer='json')
@validate(valid_user, valid_statement_or_argument, has_keywords_in_json_path(('step', str), ('is_supportive', bool),
                                                                             ('should_mark', bool)))
def mark_or_unmark_statement_or_argument(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    LOG.debug("Set statement as seen. %s", request.json_body)
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    arg_or_stmt = request.validated['arg_or_stmt']
    step = request.validated['step']
    is_supportive = request.validated['is_supportive']
    should_mark = request.validated['should_mark']
    history = request.json_body.get('history', '')
    db_user = request.validated['user']
    return mark_statement_or_argument(arg_or_stmt, step, is_supportive, should_mark, history, ui_locales, db_user)


@view_config(route_name='get_logfile_for_statements', renderer='json')
@validate(valid_issue_by_id, has_keywords_in_json_path(('uids', list)))
def get_logfile_for_some_statements(request):
    """
    Returns the changelog of a statement

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Return the changelog of a statement. %s", request.json_body)
    uids = request.validated['uids']
    db_issue = request.validated['issue']
    return get_logfile_for_statements(uids, db_issue.lang, request.application_url)


@view_config(route_name='get_infos_about_argument', renderer='json')
@validate(valid_issue_by_id, valid_language, valid_argument(location='json_body'), valid_user_optional)
def get_infos_about_argument(request):
    """
    ajax interface for getting a dump

    :param request: current request of the server
    :return: json-set with everything
    """
    LOG.debug("Get infos about an argument via AJAX. %s", request.json_body)
    lang = request.validated['lang']
    db_user = request.validated['user']
    db_argument = request.validated['argument']
    return get_all_infos_about_argument(db_argument, request.application_url, db_user, lang)


@view_config(route_name='get_arguments_by_statement_uid', renderer='json')
@validate(valid_any_issue_by_id, valid_statement(location='path'))
def get_arguments_by_statement_id(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    LOG.debug("Return all arguments which use the given statement. %s", request.json_body)
    db_statement = request.validated['statement']
    db_issue = request.validated['issue']
    argument_list = get_arguments_by_statement(db_statement, db_issue)
    for el in argument_list.get('arguments', []):
        el['url'] = '/discuss' + el['url']
    return argument_list
