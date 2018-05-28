"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

from time import sleep

from cornice.util import json_error
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.view import view_config

import dbas.handler.history as history_handler
import dbas.handler.issue as issue_handler
import dbas.handler.news as news_handler
import dbas.strings.matcher as fuzzy_string_matcher
from dbas.auth.login import login_user, login_user_oauth, register_user_with_json_data, __refresh_headers_and_url
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement
from dbas.handler import user
from dbas.handler.arguments import set_arguments_premises, get_all_infos_about_argument, get_arguments_by_statement_uid
from dbas.handler.issue import set_discussions_properties
from dbas.handler.language import set_language, get_language_from_cookie
from dbas.handler.notification import read_notifications, delete_notifications, send_users_notification
from dbas.handler.password import request_password
from dbas.handler.references import set_reference, get_references
from dbas.handler.settings import set_settings
from dbas.handler.statements import set_correction_of_statement, set_position, set_positions_premise, \
    set_seen_statements, get_logfile_for_statements
from dbas.handler.voting import clear_vote_and_seen_values_of_user
from dbas.helper.query import set_user_language, \
    mark_statement_or_argument, get_short_url
from dbas.lib import escape_string, get_discussion_language, relation_mapper
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import valid_language, valid_lang_cookie_fallback, valid_fuzzy_search_mode
from dbas.validators.core import has_keywords, has_maybe_keywords, validate
from dbas.validators.discussion import valid_issue_by_id, valid_new_issue, valid_issue_not_readonly, valid_conclusion, \
    valid_statement, valid_argument, valid_premisegroups, valid_statement_or_argument, \
    valid_text_length_of, valid_any_issue_by_id
from dbas.validators.lib import add_error
from dbas.validators.notifications import valid_notification_title, valid_notification_text, \
    valid_notification_recipient
from dbas.validators.user import valid_user, valid_user_optional, valid_user_as_author


def __modifiy_discussion_url(prep_dict: dict) -> dict:
    """
    Adds the /discuss prefix for every url entry

    :param prep_dict:
    :return:
    """
    # modify urls for the radio buttons
    for el in prep_dict:
        if el is 'url':
            prep_dict['url'] = '/discuss' + prep_dict['url']
    return prep_dict


# fallback for an empty api route
@view_config(route_name='main_api', renderer='json')
def main_api(request):
    add_error(request, 'Route not found', 'There was no route given')
    return json_error(request)


# ajax - getting complete track of the user
@view_config(route_name='get_user_history', renderer='json')
@validate(valid_user)
def get_user_history(request):
    """
    Request the complete user track.

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    return history_handler.get_from_database(db_user, ui_locales)


# ajax - getting all text edits
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


# ajax - getting all text edits
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


# ajax - getting all votes for arguments
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
    return user.get_marked_elements_of(db_user, True, ui_locales)


# ajax - getting all votes for statements
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
    return user.get_marked_elements_of(db_user, False, ui_locales)


# ajax - getting all votes for arguments
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
    return user.get_clicked_elements_of(db_user, True, ui_locales)


# ajax - getting all votes for statements
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
    return user.get_clicked_elements_of(db_user, False, ui_locales)


# ajax - deleting complete history of the user
@view_config(route_name='delete_user_history', renderer='json')
@validate(valid_user)
def delete_user_history(request):
    """
    Request to delete the users history.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_user_history', 'main')
    db_user = request.validated['user']
    return history_handler.delete_in_database(db_user)


# ajax - deleting complete history of the user
@view_config(route_name='delete_statistics', renderer='json')
@validate(valid_user)
def delete_statistics(request):
    """
    Request to delete votes/clicks of the user.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_statistics', 'main')
    db_user = request.validated['user']
    return clear_vote_and_seen_values_of_user(db_user)


@view_config(request_method='POST', route_name='user_login', renderer='json')
@validate(has_keywords(('user', str), ('password', str), ('keep_login', bool)),
          has_maybe_keywords(('redirect_url', str, '')))
def user_login(request):
    """
    Will login the user by his nickname and password

    :param request: request of the web server
    :return: dict() with error
    """
    logger('views', 'main')
    lang = get_language_from_cookie(request)
    nickname = request.validated['user']
    password = request.validated['password']
    keep_login = request.validated['keep_login']
    redirect_url = request.validated['redirect_url']

    login_data = login_user(nickname, password, request.mailer, lang)

    if not login_data.get('error'):
        headers, url = __refresh_headers_and_url(request, login_data['user'], keep_login, redirect_url)
        sleep(0.5)
        return HTTPFound(location=url, headers=headers)

    return {'error': Translator(lang).get(_.userPasswordNotMatch)}


@view_config(route_name='user_login_oauth', renderer='json')
def user_login_oauth(request):
    """
    Will login the user via oauth

    :return: dict() with error
    """
    logger('views', 'main')

    lang = get_language_from_cookie(request)
    _tn = Translator(lang)

    # sanity check
    if request.authenticated_userid:
        return {'error': ''}

    try:
        service = request.params['service']
        url = request.params['redirect_uri']
        old_redirect = url.replace('http:', 'https:')
        # add service tag to notice the oauth provider after a redirect
        if '?service' in url:
            url = url[0:url.index('/discuss') + len('/discuss')] + url[url.index('?service'):]
        for slug in [issue.slug for issue in DBDiscussionSession.query(Issue).all()]:
            if slug in url:
                url = url[0:url.index('/discuss') + len('/discuss')]
        redirect_url = url.replace('http:', 'https:')

        val = login_user_oauth(request, service, redirect_url, old_redirect, lang)
        if val is None:
            return {'error': _tn.get(_.internalKeyError)}
        return val
    except KeyError as e:
        logger('user_login_oauth', repr(e), error=True)
        return {'error': _tn.get(_.internalKeyError)}


@view_config(route_name='user_logout', renderer='json')
def user_logout(request, redirect_to_main=False):
    """
    Will logout the user

    :param request: request of the web server
    :param redirect_to_main: Boolean
    :return: HTTPFound with forgotten headers
    """
    logger('views', 'user: {}, redirect main: {}'.format(request.authenticated_userid, redirect_to_main))
    request.session.invalidate()
    headers = forget(request)
    if redirect_to_main:
        location = request.application_url + 'discuss?session_expired=true',
    elif (request.application_url + '/discuss') in request.path_url:  # redirect to page, where you need no login
        location = request.path_url
    else:
        location = request.application_url + '/discuss'

    return HTTPFound(
        location=location,
        headers=headers
    )


@view_config(route_name='user_delete', renderer='json')
@validate(valid_user)
def user_delete(request):
    """
    Will delete the user

    :param request: request of the web server
    :param redirect_to_main: Boolean
    :return: HTTPFound with forgotten headers
    """
    logger('views', 'user_delete')
    db_user = request.validated['user']
    user.delete(db_user)
    request.session.invalidate()
    return HTTPFound(
        location=request.application_url + '/discuss',
        headers=forget(request)
    )


@view_config(route_name='user_registration', renderer='json')
@validate(valid_lang_cookie_fallback,
          has_keywords(('nickname', str), ('email', str), ('gender', str), ('password', str), ('passwordconfirm', str)),
          has_maybe_keywords(('firstname', str, ''), ('lastname', str, '')))
def user_registration(request):
    """
    Registers new user with data given in the ajax request.

    :param request: current request of the server
    :return: dict() with success and message
    """
    logger('Views', 'main: {}'.format(request.json_body))
    mailer = request.mailer
    lang = request.validated['lang']

    success, info, new_user = register_user_with_json_data(request.validated, lang, mailer)

    return {
        'success': str(success),
        'error': '',
        'info': str(info)
    }


@view_config(route_name='user_password_request', renderer='json')
@validate(valid_lang_cookie_fallback, has_keywords(('email', str)))
def user_password_request(request):
    """
    Sends an email, when the user requests his password

    :param request: current request of the server
    :return: dict() with success and message
    """
    logger('Views', 'request.params: {}'.format(request.json_body))
    _tn = Translator(request.validated['lang'])
    return request_password(request.validated['email'], request.mailer, _tn)


@view_config(route_name='set_user_setting', renderer='json')
@validate(valid_user, has_keywords(('settings_value', bool), ('service', str)))
def set_user_settings(request):
    """
    Sets a specific setting of the user.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('Views', 'request.params: {}'.format(request.json_body))
    _tn = Translator(get_language_from_cookie(request))
    db_user = request.validated['user']
    settings_value = request.validated['settings_value']
    service = request.validated['service']
    return set_settings(request.application_url, db_user, service, settings_value, _tn)


@view_config(route_name='set_user_language', renderer='json')
@validate(valid_user, valid_lang_cookie_fallback)
def set_user_lang(request):
    """
    Specify new UI language for user.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'request.params: {}'.format(request.json_body))
    return set_user_language(request.validated['user'], request.validated.get('lang'))


@view_config(route_name='set_discussion_properties', renderer='json')
@validate(valid_user, valid_any_issue_by_id, has_keywords(('property', bool), ('value', str)))
def set_discussion_properties(request):
    """
    Set availability, read-only, ... flags in the admin panel.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'request.params: {}'.format(request.json_body))
    _tn = Translator(get_language_from_cookie(request))

    prop = request.validated['property']
    db_user = request.validated['user']
    issue = request.validated['issue']
    value = request.validated['value']
    return set_discussions_properties(db_user, issue, prop, value, _tn)


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################

@view_config(route_name='set_new_start_argument', renderer='json')
@validate(valid_user, valid_issue_not_readonly, has_keywords(('position', str), ('reason', str)))
def set_new_start_argument(request):
    """
    Inserts a new argument as starting point into the database

    :param request: request of the web server
    :return: a status code, if everything was successful
    """
    logger('views', 'request.params: {}'.format(request.json_body))
    reason = request.validated['reason']

    # set the new position
    logger('views', 'set conclusion/position')
    prepared_dict_pos = set_position(request.validated['user'], request.validated['issue'],
                                     request.validated['position'])

    if len(prepared_dict_pos['error']) is 0:
        logger('views', 'set premise/reason')
        prepared_dict_pos = set_positions_premise(request.validated['issue'],
                                                  request.validated['user'],
                                                  DBDiscussionSession.query(Statement).get(
                                                      prepared_dict_pos['statement_uids'][0]),
                                                  [[reason]],
                                                  True,
                                                  request.cookies.get('_HISTORY_'),
                                                  request.mailer)
    __modifiy_discussion_url(prepared_dict_pos)

    return prepared_dict_pos


@view_config(route_name='set_new_start_premise', renderer='json')
@validate(valid_user, valid_issue_not_readonly, valid_conclusion, valid_premisegroups,
          has_keywords(('supportive', bool)))
def set_new_start_premise(request):
    """
    Sets new premise for the start

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    prepared_dict = set_positions_premise(request.validated['issue'],
                                          request.validated['user'],
                                          request.validated['conclusion'],
                                          request.validated['premisegroups'],
                                          request.validated['supportive'],
                                          request.cookies.get('_HISTORY_'),
                                          request.mailer)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_new_premises_for_argument', renderer='json')
@validate(valid_user, valid_premisegroups, valid_argument(location='json_body', depends_on={valid_issue_not_readonly}),
          has_keywords(('attack_type', str)))
def set_new_premises_for_argument(request):
    """
    Sets a new premise for an argument

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    prepared_dict = set_arguments_premises(request.validated['issue'],
                                           request.validated['user'],
                                           request.validated['argument'],
                                           request.validated['premisegroups'],
                                           relation_mapper[request.validated['attack_type']],
                                           request.cookies['_HISTORY_'] if '_HISTORY_' in request.cookies else None,
                                           request.mailer)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_correction_of_statement', renderer='json')
@validate(valid_user, has_keywords(('elements', list)))
def set_correction_of_some_statements(request):
    """
    Sets a new textvalue for a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    ui_locales = get_language_from_cookie(request)
    elements = request.validated['elements']
    db_user = request.validated['user']
    _tn = Translator(ui_locales)
    return set_correction_of_statement(elements, db_user, _tn)


@view_config(route_name='notifications_read', renderer='json')
@validate(valid_user, has_keywords(('ids', list)))
def set_notifications_read(request):
    """
    Set a notification as read

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main {}'.format(request.json_body))
    return read_notifications(request.validated['ids'], request.validated['user'])


@view_config(route_name='notifications_delete', renderer='json')
@validate(valid_user, has_keywords(('ids', list)))
def set_notifications_delete(request):
    """
    Request the removal of a notification

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main {}'.format(request.json_body))
    ui_locales = get_language_from_cookie(request)
    return delete_notifications(request.validated['ids'], request.validated['user'], ui_locales,
                                request.application_url)


@view_config(route_name='send_notification', renderer='json')
@validate(valid_user, valid_notification_title, valid_notification_text, valid_notification_recipient)
def send_some_notification(request):
    """
    Set a new message into the inbox of an recipient, and the outbox of the sender.

    :param request: current request of the server
    :return: dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    ui_locales = get_language_from_cookie(request)
    author = request.validated['user']
    recipient = request.validated['recipient']
    title = request.validated['title']
    text = request.validated['text']
    return send_users_notification(author, recipient, title, text, ui_locales)


# ajax - set new issue
@view_config(route_name='set_new_issue', renderer='json')
@validate(valid_user, valid_language, valid_new_issue, has_keywords(('is_public', bool), ('is_read_only', bool)))
def set_new_issue(request):
    """

    :param request: current request of the server
    :return:
    """
    logger('views', 'main {}'.format(request.json_body))
    info = escape_string(request.validated['info'])
    long_info = escape_string(request.validated['long_info'])
    title = escape_string(request.validated['title'])
    lang = request.validated['lang']
    is_public = request.validated['is_public']
    is_read_only = request.validated['is_read_only']

    return issue_handler.set_issue(request.validated['user'], info, long_info, title, lang, is_public, is_read_only)


# ajax - set seen premisegroup
@view_config(route_name='set_seen_statements', renderer='json')
@validate(valid_user, has_keywords(('uids', list)))
def set_statements_as_seen(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'main {}'.format(request.json_body))
    uids = request.validated['uids']
    return set_seen_statements(uids, request.path, request.validated['user'])


# ajax - set users opinion
@view_config(route_name='mark_statement_or_argument', renderer='json')
@validate(valid_user, valid_statement_or_argument, has_keywords(('step', str), ('is_supportive', bool),
                                                                ('should_mark', bool)))
def mark_or_unmark_statement_or_argument(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'main {}'.format(request.json_body))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    arg_or_stmt = request.validated['arg_or_stmt']
    step = request.validated['step']
    is_supportive = request.validated['is_supportive']
    should_mark = request.validated['should_mark']
    history = request.json_body.get('history', '')
    db_user = request.validated['user']
    return mark_statement_or_argument(arg_or_stmt, step, is_supportive, should_mark, history, ui_locales, db_user)


# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################


# ajax - getting changelog of a statement
@view_config(route_name='get_logfile_for_statements', renderer='json')
@validate(valid_issue_by_id, has_keywords(('uids', list)))
def get_logfile_for_some_statements(request):
    """
    Returns the changelog of a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    uids = request.validated['uids']
    db_issue = request.validated['issue']
    return get_logfile_for_statements(uids, db_issue.lang, request.application_url)


# ajax - for shorten url
@view_config(route_name='get_shortened_url', renderer='json')
@validate(has_keywords(('url', str)))
def get_shortened_url(request):
    """
    Shortens url with the help of a python lib

    :param request: current request of the server
    :return: dictionary with shortend url
    """
    logger('views', 'main')
    return get_short_url(request.validated['url'])


# ajax - for getting all news
@view_config(route_name='get_news', renderer='json')
def get_news(request):
    """
    ajax interface for getting news

    :param request: current request of the server
    :return: json-set with all news
    """
    logger('views', 'main')
    return news_handler.get_news(get_language_from_cookie(request))


# ajax - for getting argument infos
@view_config(route_name='get_infos_about_argument', renderer='json')
@validate(valid_issue_by_id, valid_language, valid_argument(location='json_body'), valid_user_optional)
def get_infos_about_argument(request):
    """
    ajax interface for getting a dump

    :param request: current request of the server
    :return: json-set with everything
    """
    logger('views', 'main: {}'.format(request.json_body))
    lang = request.validated['lang']
    db_user = request.validated['user']
    db_argument = request.validated['argument']
    return get_all_infos_about_argument(db_argument, request.application_url, db_user, lang)


# ajax - for getting all users with the same opinion
@view_config(route_name='get_user_with_same_opinion', renderer='json')
@validate(valid_language, valid_user_optional,
          has_keywords(('uids', list), ('is_argument', bool), ('is_attitude', bool), ('is_reaction', bool),
                       ('is_position', bool)))
def get_users_with_opinion(request):
    """
    ajax interface for getting a dump

    :params reqeust: current request of the web  server
    :return: json-set with everything
    """
    logger('views', 'main: {}'.format(request.json_body))
    db_lang = request.validated['lang']
    uids = request.json_body.get('uids')
    is_arg = request.validated['is_argument']
    is_att = request.validated['is_attitude']
    is_rea = request.validated['is_reaction']
    is_pos = request.validated['is_position']
    db_user = request.validated['user']
    return user.get_users_with_same_opinion(uids, request.application_url, request.path, db_user, is_arg, is_att,
                                            is_rea, is_pos, db_lang)


# ajax - for getting all users with the same opinion
@view_config(route_name='get_public_user_data', renderer='json')
@validate(has_keywords(('nickname', str)))
def get_public_user_data(request):
    """
    Returns dictionary with public user data

    :param request: request of the web server
    :return:
    """
    logger('views', 'main: {}'.format(request.json_body))
    return user.get_public_data(request.validated['nickname'], get_language_from_cookie(request))


@view_config(route_name='get_arguments_by_statement_uid', renderer='json')
@validate(valid_any_issue_by_id, valid_statement(location='json_body'))
def get_arguments_by_statement_id(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    db_statement = request.validated['statement']
    db_issue = request.validated['issue']
    return get_arguments_by_statement_uid(db_statement, db_issue)


@view_config(route_name='get_references', renderer='json')
@validate(has_keywords(('uids', list), ('is_argument', bool)))
def get_reference(request):
    """
    Returns all references for an argument or statement


    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    uids = request.validated['uids']
    is_argument = request.validated['is_argument']
    return get_references(uids, is_argument, request.application_url)


@view_config(route_name='set_references', renderer='json')
@validate(valid_user, valid_any_issue_by_id, valid_statement('json_body'),
          has_keywords(('reference', str), ('ref_source', str)))
def set_references(request):
    """
    Sets a reference for a statement or an arguments

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'main: {}'.format(request.json_body))
    db_statement = request.validated['statement']
    reference = escape_string(request.validated['reference'])
    source = escape_string(request.validated['ref_source'])
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    # db_statement2issue = DBDiscussionSession.query(StatementToIssue)
    return set_reference(reference, source, db_user, db_statement, db_issue.uid)


# ########################################
# ADDTIONAL AJAX STUFF # ADDITION THINGS #
# ########################################


# ajax - for language switch
@view_config(route_name='switch_language', renderer='json')
@validate(valid_language)
def switch_language(request):
    """
    Switches the language

    :param request: current request of the server
    :return: json-dict()
    """
    logger('switch_language', 'main: {}'.format(request.json_body))
    return set_language(request, request.validated['lang'])


# ajax - for sending news
@view_config(route_name='send_news', renderer='json')
@validate(valid_user_as_author, valid_text_length_of('title'), valid_text_length_of('text'))
def send_news(request):
    """
    ajax interface for settings news

    :param request: current request of the server
    :return: json-set with new news
    """
    logger('views', 'main: {}'.format(request.json_body))
    title = escape_string(request.validated['title'])
    text = escape_string(request.validated['text'])
    db_user = request.validated['user']
    return news_handler.set_news(title, text, db_user, request.registry.settings['pyramid.default_locale_name'],
                                 request.application_url)


# ajax - for fuzzy search
@view_config(route_name='fuzzy_search', renderer='json')
@validate(valid_issue_by_id, valid_user_optional, valid_fuzzy_search_mode,
          has_keywords(('value', str), ('statement_uid', int)))
def fuzzy_search(request):
    """
    ajax interface for fuzzy string search

    :param request: request of the web server
    :return: json-set with all matched strings
    """
    logger('views', 'main: {}'.format(request.json_body))

    mode = request.validated['type']
    value = request.validated['value']
    db_issue = request.validated['issue']
    statement_uid = request.validated['statement_uid']
    db_user = request.validated['user']
    prepared_dict = fuzzy_string_matcher.get_prediction(db_user, db_issue, value, mode, statement_uid)
    for part_dict in prepared_dict['values']:
        __modifiy_discussion_url(part_dict)
    return prepared_dict


# ajax - for fuzzy search of nickname
@view_config(route_name='fuzzy_nickname_search', renderer='json')
@validate(valid_user_optional, has_keywords(('value', str)))
def fuzzy_nickname_search(request):
    """
    ajax interface for fuzzy string search

    :param request: request of the web server
    :return: json-set with all matched strings
    """
    logger('views', 'main: {}'.format(request.json_body))
    return fuzzy_string_matcher.get_nicknames(request.validated['user'], request.validated['value'])
