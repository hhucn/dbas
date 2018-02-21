"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import json
from time import sleep

import requests
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.security import forget
from pyramid.view import view_config

import dbas.handler.history as history_handler
import dbas.handler.issue as issue_handler
import dbas.handler.news as news_handler
import dbas.review.helper.flags as review_flag_helper
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.main as review_main_helper
import dbas.review.helper.queues as review_queue_helper
import dbas.strings.matcher as fuzzy_string_matcher
from dbas.auth.login import login_user, login_user_oauth, register_user_with_json_data, __refresh_headers_and_url
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.database.discussion_model import Statement, ReviewEdit, ReviewMerge, ReviewSplit, ReviewOptimization, \
    ReviewDuplicate, ReviewDelete
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
from dbas.helper.query import get_default_locale_name, set_user_language, \
    mark_statement_or_argument, get_short_url, revoke_author_of_argument_content, revoke_author_of_statement_content
from dbas.lib import escape_string, get_discussion_language
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import valid_language, valid_lang_cookie_fallback
from dbas.validators.core import has_keywords, has_maybe_keywords, validate
from dbas.validators.database import valid_database_model
from dbas.validators.discussion import valid_issue, valid_new_issue, valid_issue_not_readonly, valid_conclusion, \
    valid_statement, valid_argument, valid_premisegroup, valid_premisegroups, valid_statement_or_argument, \
    valid_text_values
from dbas.validators.notifications import valid_notification_title, valid_notification_text, \
    valid_notification_recipient
from dbas.validators.reviews import valid_review_reason, valid_not_executed_review, valid_uid_as_row_in_review_queue
from dbas.validators.user import valid_user, invalid_user, valid_user_as_author, \
    valid_user_as_author_of_statement, valid_user_as_author_of_argument
from websocket.lib import get_port, send_request_for_recent_reviewer_socketio


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
    return history_handler.get_history_from_database(db_user, ui_locales)


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
    return user.get_marked_elements_of_user(db_user, True, ui_locales)


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
    return user.get_marked_elements_of_user(db_user, False, ui_locales)


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
    return user.get_clicked_element_of_user(db_user, True, ui_locales)


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
    return user.get_clicked_element_of_user(db_user, False, ui_locales)


# ajax - deleting complete history of the user
@view_config(route_name='delete_user_history', renderer='json')
@validate(valid_user)
def delete_user_history(request):
    """
    Request to delete the users history.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_user_history', 'def', 'main')
    db_user = request.validated['user']
    return history_handler.delete_history_in_database(db_user)


# ajax - deleting complete history of the user
@view_config(route_name='delete_statistics', renderer='json')
@validate(valid_user)
def delete_statistics(request):
    """
    Request to delete votes/clicks of the user.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_statistics', 'def', 'main')
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
    logger('views', 'user_login', 'main: {}'.format(request.json_body))
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
    logger('views', 'user_login_oauth', 'main: {}'.format(request.params))

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
        logger('user_login_oauth', 'error', repr(e), error=True)
        return {'error': _tn.get(_.internalKeyError)}


@view_config(route_name='user_logout', renderer='json')
def user_logout(request, redirect_to_main=False):
    """
    Will logout the user

    :param request: request of the web server
    :param redirect_to_main: Boolean
    :return: HTTPFound with forgotten headers
    """
    logger('views', 'user_logout', 'user: {}, redirect main: {}'.format(request.authenticated_userid, redirect_to_main))
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
    logger('Views', 'user_registration', 'main: {}'.format(request.json_body))
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
    logger('Views',
           'user_password_request',
           'request.params: {}'.format(request.json_body))
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
    logger('Views', 'set_user_settings', 'request.params: {}'.format(request.json_body))
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
    logger('views', 'set_user_lang', 'request.params: {}'.format(request.json_body))
    return set_user_language(request.validated['user'], request.validated.get('lang'))


@view_config(route_name='set_discussion_properties', renderer='json')
@validate(valid_user, valid_issue, has_keywords(('property', bool), ('value', str)))
def set_discussion_properties(request):
    """
    Set availability, read-only, ... flags in the admin panel.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_discussion_properties', 'request.params: {}'.format(request.json_body))
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
    logger('views', 'set_new_start_argument', 'request.params: {}'.format(request.json_body))
    reason = request.validated['reason']
    data = {
        'user': request.validated['user'],
        'issue': request.validated['issue'],
        'statement_text': request.validated['position'],
        'default_locale_name': get_default_locale_name(request.registry),
        'application_url': request.application_url,
        'supportive': True,
        'port': get_port(request),
        'history': request.cookies.get('_HISTORY_'),
        'mailer': request.mailer
    }

    # set the new position
    logger('views', 'set_new_start_argument', 'set conclusion/position')
    prepared_dict_pos = set_position(request.validated['user'], request.validated['issue'],
                                     request.validated['position'])
    if len(prepared_dict_pos['error']) is 0:
        logger('views', 'set_new_start_argument', 'set premise/reason')
        data['premisegroups'] = [[reason]]
        data['conclusion'] = DBDiscussionSession.query(Statement).get(prepared_dict_pos['statement_uids'][0])
        prepared_dict_pos = set_positions_premise(data)
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
    logger('views', 'set_new_start_premise', 'main: {}'.format(request.json_body))
    data = {
        'user': request.validated['user'],
        'application_url': request.application_url,
        'issue': request.validated['issue'],
        'premisegroups': request.validated['premisegroups'],
        'conclusion': request.validated['conclusion'],
        'supportive': request.validated['supportive'],
        'port': get_port(request),
        'history': request.cookies.get('_HISTORY_'),
        'default_locale_name': get_default_locale_name(request.registry),
        'mailer': request.mailer
    }
    prepared_dict = set_positions_premise(data)
    __modifiy_discussion_url(prepared_dict)
    return prepared_dict


@view_config(route_name='set_new_premises_for_argument', renderer='json')
@validate(valid_user, valid_issue_not_readonly, valid_premisegroups,
          has_keywords(('arg_uid', int), ('attack_type', str)))
def set_new_premises_for_argument(request):
    """
    Sets a new premise for an argument

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'set_new_premises_for_argument', 'main: {}'.format(request.json_body))
    data = {
        'user': request.validated['user'],
        'issue': request.validated['issue'],
        'premisegroups': request.validated['premisegroups'],
        'arg_uid': request.validated['arg_uid'],
        'attack_type': request.validated['attack_type'],
        'port': get_port(request),
        'history': request.cookies['_HISTORY_'] if '_HISTORY_' in request.cookies else None,
        'default_locale_name': get_default_locale_name(request.registry),
        'mailer': request.mailer
    }
    prepared_dict = set_arguments_premises(data)
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
    logger('views', 'set_correction_of_some_statements', 'main: {}'.format(request.json_body))
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
    logger('views', 'set_notifications_read', 'main {}'.format(request.json_body))
    return read_notifications(request.validated['ids'], request.validated['user'])


@view_config(route_name='notifications_delete', renderer='json')
@validate(valid_user, has_keywords(('ids', list)))
def set_notifications_delete(request):
    """
    Request the removal of a notification

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_notifications_delete', 'main {}'.format(request.json_body))
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
    logger('views', 'send_some_notification', 'main: {}'.format(request.json_body))
    ui_locales = get_language_from_cookie(request)
    author = request.validated['user']
    recipient = request.validated['recipient']
    title = request.validated['title']
    text = request.validated['text']
    return send_users_notification(author, recipient, title, text, get_port(request), ui_locales)


# ajax - set new issue
@view_config(route_name='set_new_issue', renderer='json')
@validate(valid_user, valid_language, valid_new_issue, has_keywords(('is_public', bool), ('is_read_only', bool)))
def set_new_issue(request):
    """

    :param request: current request of the server
    :return:
    """
    logger('views', 'set_new_issue', 'main {}'.format(request.json_body))
    info = escape_string(request.validated['info'])
    long_info = escape_string(request.validated['long_info'])
    title = escape_string(request.validated['title'])
    lang = request.validated['lang']
    is_public = request.validated['is_public']
    is_read_only = request.validated['is_read_only']

    return issue_handler.set_issue(request.validated['user'], info, long_info, title, lang, is_public, is_read_only,
                                   request.application_url)


# ajax - set seen premisegroup
@view_config(route_name='set_seen_statements', renderer='json')
@validate(valid_user, has_keywords(('uids', list)))
def set_statements_as_seen(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'set_statements_as_seen', 'main {}'.format(request.json_body))
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
    logger('views', 'mark_or_unmark_statement_or_argument', 'main {}'.format(request.json_body))
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
@validate(valid_issue, has_keywords(('uids', list)))
def get_logfile_for_some_statements(request):
    """
    Returns the changelog of a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'get_logfile_for_statements', 'main: {}'.format(request.json_body))
    uids = request.validated['uids']
    db_issue = request.validated['issue']
    return get_logfile_for_statements(uids, db_issue.lang, request.application_url)


# ajax - for shorten url
@view_config(route_name='get_shortened_url', renderer='json')
@validate(valid_issue, has_keywords(('url', str)))
def get_shortened_url(request):
    """
    Shortens url with the help of a python lib

    :param request: current request of the server
    :return: dictionary with shortend url
    """
    logger('views', 'get_shortened_url', 'main')
    db_issue = request.validated['issue']
    return get_short_url(request.validated['url'], db_issue.lang)


# ajax - for getting all news
@view_config(route_name='get_news', renderer='json')
def get_news(request):
    """
    ajax interface for getting news

    :param request: current request of the server
    :return: json-set with all news
    """
    logger('views', 'get_news', 'main')
    return news_handler.get_news(get_language_from_cookie(request))


# ajax - for getting argument infos
@view_config(route_name='get_infos_about_argument', renderer='json')
@validate(valid_issue, valid_language, valid_argument, invalid_user)
def get_infos_about_argument(request):
    """
    ajax interface for getting a dump

    :param request: current request of the server
    :return: json-set with everything
    """
    logger('views', 'get_infos_about_argument', 'main: {}'.format(request.json_body))
    lang = request.validated['lang']
    db_user = request.validated['user']
    db_argument = request.validated['argument']
    return get_all_infos_about_argument(db_argument, request.application_url, db_user, lang)


# ajax - for getting all users with the same opinion
@view_config(route_name='get_user_with_same_opinion', renderer='json')
@validate(valid_language, invalid_user,
          has_keywords(('is_argument', bool), ('is_attitude', bool), ('is_reaction', bool), ('is_position', bool)))
def get_users_with_opinion(request):
    """
    ajax interface for getting a dump

    :params reqeust: current request of the web  server
    :return: json-set with everything
    """
    logger('views', 'get_users_with_opinion', 'main: {}'.format(request.json_body))
    db_lang = request.validated['lang']
    uids = request.json_body.get('uid')
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
    logger('views', 'get_public_user_data', 'main: {}'.format(request.json_body))
    return user.get_public_data(request.validated['nickname'], get_language_from_cookie(request))


@view_config(route_name='get_arguments_by_statement_uid', renderer='json')
@validate(valid_statement)
def get_arguments_by_statement_id(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'get_arguments_by_statement_id', 'main: {}'.format(request.json_body))
    return get_arguments_by_statement_uid(request.validated['statement'], request.application_url)


@view_config(route_name='get_references', renderer='json')
@validate(has_keywords(('uids', list), ('is_argument', bool)))
def get_reference(request):
    """
    Returns all references for an argument or statement


    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'get_reference', 'main: {}'.format(request.json_body))
    uids = request.validated['uids']
    is_argument = request.validated['is_argument']
    return get_references(uids, is_argument, request.application_url)


@view_config(route_name='set_references', renderer='json')
@validate(valid_user, valid_statement, has_keywords(('reference', str), ('ref_source', str)))
def set_references(request):
    """
    Sets a reference for a statement or an arguments

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_references', 'main: {}'.format(request.json_body))
    db_statement = request.validated['statement']
    reference = escape_string(request.validated['reference'])
    source = escape_string(request.validated['ref_source'])
    db_user = request.validated['user']
    return set_reference(reference, source, db_user, db_statement, db_statement.issue_uid)


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
    logger('switch_language', 'def', 'main: {}'.format(request.json_body))
    return set_language(request, request.validated['lang'])


# ajax - for sending news
@view_config(route_name='send_news', renderer='json')
@validate(valid_user, has_keywords(('title', str), ('text', str)))
def send_news(request):
    """
    ajax interface for settings news

    :param request: current request of the server
    :return: json-set with new news
    """
    logger('views', 'send_news', 'main: {}'.format(request.json_body))
    title = escape_string(request.validated['title'])
    text = escape_string(request.validated['text'])
    db_user = request.validated['user']
    return news_handler.set_news(title, text, db_user, request.registry.settings['pyramid.default_locale_name'],
                                 request.application_url)


# ajax - for fuzzy search
@view_config(route_name='fuzzy_search', renderer='json')
@validate(valid_issue, invalid_user, has_keywords(('type', int), ('value', str), ('statement_uid', int)))
def fuzzy_search(request):
    """
    ajax interface for fuzzy string search

    :param request: request of the web server
    :return: json-set with all matched strings
    """
    logger('views', 'fuzzy_search', 'main: {}'.format(request.json_body))

    _tn = Translator(get_language_from_cookie(request))
    mode = request.validated['type']
    value = request.validated['value']
    db_issue = request.validated['issue']
    statement_uid = request.validated['statement_uid']
    db_user = request.validated['user']
    return fuzzy_string_matcher.get_prediction(_tn, db_user, db_issue, request.application_url, value, mode,
                                               statement_uid)


# ajax - for additional service
@view_config(route_name='additional_service', renderer='json')
def additional_service(request):
    """
    Easteregg O:-)

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'additional_service', 'main: {}'.format(request.params))

    try:
        rtype = request.params['type']
        if rtype == "chuck":
            data = requests.get('http://api.icndb.com/jokes/random')
        else:
            data = requests.get('http://api.yomomma.info/')

        for a in data.json():
            logger('views', 'additional_service', str(a) + ': {}'.format(data.json()[a]))

    except KeyError as e:
        logger('views', 'additional_service', repr(e), error=True)
        return json.dumps(dict())

    return data.json()


# #######################################
# ADDITIONAL AJAX STUFF # REVIEW THINGS #
# #######################################


@view_config(route_name='flag_argument_or_statement', renderer='json')
@validate(valid_user, valid_review_reason, has_keywords(('uid', int), ('is_argument', bool)),
          has_maybe_keywords(('extra_uid', int, None)))
def flag_argument_or_statement(request):
    """
    Flags an argument or statement for a specific reason

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'flag_argument_or_statement', 'main: {}'.format(request.json_body))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    uid = request.validated['uid']
    reason = request.validated['reason']
    extra_uid = request.validated['extra_uid']
    is_argument = request.validated['is_argument']
    db_user = request.validated['user']
    return review_flag_helper.flag_element(uid, reason, db_user, is_argument, ui_locales, extra_uid)


@view_config(route_name='split_or_merge_statement', renderer='json')
@validate(valid_user, valid_premisegroup, valid_text_values, has_keywords(('key', str)))
def split_or_merge_statement(request):
    """
    Flags a statement for a specific reason

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'split_or_merge_statement', 'main: {}'.format(request.json_body))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _tn = Translator(ui_locales)
    db_user = request.validated['user']
    pgroup = request.validated['pgroup']
    key = request.validated['key']
    tvalues = request.validated['text_values']

    if key not in ['merge', 'split']:
        raise HTTPBadRequest()
    return review_flag_helper.flag_statement_for_merge_or_split(key, pgroup, tvalues, db_user, _tn)


@view_config(route_name='split_or_merge_premisegroup', renderer='json')
@validate(valid_user, valid_premisegroup, has_keywords(('key', str)))
def split_or_merge_premisegroup(request):
    """
    Flags a premisegroup for a specific reason

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'split_or_merge_premisegroup', 'main: {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _tn = Translator(ui_locales)
    db_user = request.validated['user']
    pgroup = request.validated['pgroup']
    key = request.validated['key']

    if key not in ['merge', 'split']:
        raise HTTPBadRequest()
    return review_flag_helper.flag_pgroup_for_merge_or_split(key, pgroup, db_user, _tn)


@view_config(route_name='review_delete_argument', renderer='json')
@validate(valid_user, valid_not_executed_review('review_uid', ReviewDelete), has_keywords(('should_delete', bool)))
def review_delete_argument(request):
    """
    Values for the review for an argument, which should be deleted

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_delete_argument', 'main: {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    db_review = request.validated['db_review']
    db_user = request.validated['user']
    should_delete = request.validated['should_delete']
    main_page = request.application_url
    port = get_port(request)
    _t = Translator(ui_locales)

    review_main_helper.add_review_opinion_for_delete(db_user, main_page, port, db_review, should_delete, _t)
    send_request_for_recent_reviewer_socketio(db_user.nickname, main_page, port, 'deletes')
    return True


@view_config(route_name='review_edit_argument', renderer='json')
@validate(valid_user, valid_not_executed_review('review_uid', ReviewEdit), has_keywords(('is_edit_okay', bool)))
def review_edit_argument(request):
    """
    Values for the review for an argument, which should be edited

    :param request: current request of the server
    :return: json-dict()
    """
    logger('Views', 'review_edit_argument', 'main: {} - {}'.format(request.json_body, request.authenticated_userid))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    db_review = request.validated['db_review']
    db_user = request.validated['user']
    is_edit_okay = request.validated['is_edit_okay']
    main_page = request.application_url
    port = get_port(request)

    _t = Translator(ui_locales)
    review_main_helper.add_review_opinion_for_edit(db_user, main_page, port, db_review, is_edit_okay, _t)
    send_request_for_recent_reviewer_socketio(db_user.nickname, main_page, port, 'edits')
    return True


@view_config(route_name='review_duplicate_statement', renderer='json')
@validate(valid_user, valid_not_executed_review('review_uid', ReviewDuplicate), has_keywords(('is_duplicate', bool)))
def review_duplicate_statement(request):
    """
    Values for the review for an argument, which is maybe a duplicate

    :param request: current request of the server
    :return: json-dict()
    """
    logger('Views', 'review_duplicate_statement',
           'main: {} - {}'.format(request.json_body, request.authenticated_userid))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    db_review = request.validated['db_review']
    db_user = request.validated['user']
    is_duplicate = request.validated['is_duplicate']
    main_page = request.application_url
    port = get_port(request)

    _t = Translator(ui_locales)
    review_main_helper.add_review_opinion_for_duplicate(db_user, main_page, port, db_review, is_duplicate, _t)
    send_request_for_recent_reviewer_socketio(db_user.nickname, main_page, port, 'duplicates')
    return True


@view_config(route_name='review_optimization_argument', renderer='json')
@validate(valid_user, valid_not_executed_review('review_uid', ReviewOptimization),
          has_keywords(('should_optimized', bool), ('new_data', list)))
def review_optimization_argument(request):
    """
    Values for the review for an argument, which should be optimized

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_optimization_argument',
           'main: {} - {}'.format(request.json_body, request.authenticated_userid))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    db_review = request.validated['db_review']
    db_user = request.validated['user']
    should_optimized = request.validated['should_optimized']
    new_data = request.validated['new_data']
    main_page = request.application_url
    port = get_port(request)

    _t = Translator(ui_locales)
    review_main_helper.add_review_opinion_for_optimization(db_user, main_page, port, db_review, should_optimized,
                                                           new_data, _t)
    send_request_for_recent_reviewer_socketio(db_user.nickname, main_page, port, 'optimizations')
    return True


@view_config(route_name='review_splitted_premisegroup', renderer='json')
@validate(valid_user, valid_not_executed_review('review_uid', ReviewSplit), has_keywords(('should_split', bool)))
def review_splitted_premisegroup(request):
    """
    Values for the review for a premisegroup, which should be splitted

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_splitted_premisegroup',
           'main: {} - {}'.format(request.json_body, request.authenticated_userid))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    db_review = request.validated['db_review']
    db_user = request.validated['user']
    should_split = request.validated['should_split']
    main_page = request.application_url
    port = get_port(request)
    _t = Translator(ui_locales)

    review_main_helper.add_review_opinion_for_split(db_user, main_page, port, db_review, should_split, _t)
    send_request_for_recent_reviewer_socketio(db_user.nickname, main_page, port, 'splits')
    return True


@view_config(route_name='review_merged_premisegroup', renderer='json')
@validate(valid_user, valid_not_executed_review('review_uid', ReviewMerge), has_keywords(('should_merge', bool)))
def review_merged_premisegroup(request):
    """
    Values for the review for a statement, which should be merged

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_merged_premisegroup',
           'main: {} - {}'.format(request.json_body, request.authenticated_userid))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    db_review = request.validated['db_review']
    db_user = request.validated['user']
    should_merge = request.validated['should_merge']
    main_page = request.application_url
    port = get_port(request)
    _t = Translator(ui_locales)

    review_main_helper.add_review_opinion_for_merge(db_user, main_page, port, db_review, should_merge, _t)
    send_request_for_recent_reviewer_socketio(db_user.nickname, main_page, port, 'merges')
    return True


@view_config(route_name='undo_review', renderer='json')
@validate(valid_user_as_author, valid_uid_as_row_in_review_queue, has_keywords(('queue', str)))
def undo_review(request):
    """
    Trys to undo a done review process

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'undo_review', 'main: {}'.format(request.json_body))
    db_user = request.validated['user']
    queue = request.validated['queue']
    db_review = request.validated['review']
    return review_history_helper.revoke_old_decision(queue, db_review, db_user)


@view_config(route_name='cancel_review', renderer='json')
@validate(valid_user_as_author, valid_uid_as_row_in_review_queue, has_keywords(('queue', str)))
def cancel_review(request):
    """
    Trys to cancel an ongoing review

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'cancel_review', 'main: {}'.format(request.json_body))
    db_user = request.validated['user']
    queue = request.validated['queue']
    db_review = request.validated['review']
    return review_history_helper.cancel_ongoing_decision(queue, db_review, db_user)


@view_config(route_name='review_lock', renderer='json', require_csrf=False)
@validate(valid_user, valid_database_model('review_uid', ReviewOptimization), has_keywords(('lock', bool)))
def review_lock(request):
    """
    Locks an optimization review so that the user can do an edit

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_lock', 'main: {}'.format(request.json_body))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    _tn = Translator(ui_locales)
    lock = request.validated['lock']
    db_review = request.validated['db_model']
    db_user = request.validated['user']

    if lock:
        return review_queue_helper.lock_optimization_review(db_user, db_review, _tn)
    else:
        return review_queue_helper.unlock_optimization_review(db_review, _tn)


@view_config(route_name='revoke_statement_content', renderer='json', require_csrf=False)
@validate(valid_user_as_author_of_statement, valid_statement)
def revoke_statement_content(request):
    """
    Revokes the given user as author from a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'revoke_statement_content', 'main: {}'.format(request.json_body))
    db_user = request.validated['user']
    statement = request.validated['statement']
    return revoke_author_of_statement_content(statement, db_user)


@view_config(route_name='revoke_argument_content', renderer='json', require_csrf=False)
@validate(valid_user_as_author_of_argument, valid_argument)
def revoke_argument_content(request):
    db_user = request.validated['user']
    argument = request.validated['argument']
    return revoke_author_of_argument_content(argument, db_user)
