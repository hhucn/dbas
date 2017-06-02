"""
Collection of all view registrations of the core component of D-BAS.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import json
import subprocess
from typing import Callable, Any

import requests
import transaction
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.security import forget
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyshorteners.shorteners import Shortener, Shorteners
from requests.exceptions import ReadTimeout
from sqlalchemy import and_

import dbas.discussion.core as discussion
import dbas.discussion.additives as add
import dbas.handler.news as news_handler
import dbas.helper.history as history_helper
import dbas.helper.issue as issue_helper
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.queues as review_queue_helper
import dbas.review.helper.reputation as review_reputation_helper
import dbas.review.helper.subpage as review_page_helper
import dbas.strings.matcher as fuzzy_string_matcher
from dbas import user_management as user_manager
from dbas.auth.login import login_user, register_with_ajax_data
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Group, Issue, Message
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.handler.opinion import get_infos_about_argument, get_user_with_same_opinion_for_argument, \
    get_user_with_same_opinion_for_statements, get_user_with_opinions_for_attitude, \
    get_user_with_same_opinion_for_premisegroups, get_user_and_opinions_for_argument
from dbas.handler.password import request_password
from dbas.handler.rss import get_list_of_all_feeds
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.language import set_language, get_language_from_cookie, set_language_for_first_visit
from dbas.helper.notification import count_of_new_notifications, get_box_for
from dbas.helper.query import get_logfile_for_statements, insert_as_statements, \
    process_input_of_premises_for_arguments_and_receive_url, process_input_of_start_premises_and_receive_url, \
    process_seen_statements, mark_or_unmark_statement_or_argument, get_text_for_justification_or_reaction_bubble
from dbas.helper.references import get_references_for_argument, get_references_for_statements, set_reference
from dbas.helper.settings import set_settings
from dbas.helper.views import preparation_for_view, try_to_contact
from dbas.helper.voting import clear_vote_and_seen_values_of_user
from dbas.input_validator import is_integer
from dbas.lib import escape_string, get_discussion_language, get_changelog, is_user_author_or_admin, \
    get_all_arguments_with_text_and_url_by_statement_id, get_slug_by_statement_uid
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for, rep_reason_first_position, \
    rep_reason_first_justification, rep_reason_first_new_argument, rep_reason_new_statement
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager
from websocket.lib import send_request_for_info_popup_to_socketio

name = 'D-BAS'
version = '1.4.1'
full_version = version
project_name = name + ' ' + full_version


def base_layout():
    return get_renderer('templates/basetemplate.pt').implementation()


def check_authentication(request):
    """
    The entry routine performed by a bulk of functions.
    Checks whether the user is authenticated and if not logs user out.

    This function is not pure!
    :param request: current request of the server
    :return: HTTP response or None if no change in session
    """
    session_expired = user_manager.update_last_action(request.authenticated_userid)
    if session_expired:
        return user_logout(request, True)


def api_notfound(request):
    body = {
        'requested_path': request.path,
        'message': "Not Found",
    }
    response = Response(json.dumps(body).encode("utf-8"))
    response.status_int = 404
    response.content_type = 'application/json'
    return response


def __call_from_discussion_step(request, f: Callable[[Any, Any, Any], Any], for_api=False, api_data=None):
    """
    Checks for an expired session, the authentication and calls f with for_api, api_data and the users nickname.
    On error an HTTPNotFound-Error is raised, otherwise the discussion dict is returned.

    :param request: A pyramid request
    :param f: A function with three arguments
    :param for_api: boolean if requests came via the API
    :param api_data: dict if requests came via the API
    :return: prepared collection for the discussion
    """
    nickname, session_expired = preparation_for_view(for_api, api_data, request)
    if session_expired:
        return user_logout(request, True)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    prepared_discussion = f(request, nickname, for_api)
    if prepared_discussion:
        prepared_discussion['layout'] = base_layout()
        prepared_discussion['language'] = str(get_language_from_cookie(request))

    return prepared_discussion


# main page
@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
@forbidden_view_config(renderer='templates/index.pt')
def main_page(request):
    """
    View configuration for the main page

    :param request: current request of the server
    :return: HTTP 200 with several information
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_page', 'def', 'request.params: {}'.format(request.params))

    set_language_for_first_visit(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    session_expired = True if 'session_expired' in request.params and request.params['session_expired'] == 'true' else False
    ui_locales      = get_language_from_cookie(request)
    logger('main_page', 'def', 'request.params: {}'.format(request.params))
    _dh             = DictionaryHelper(ui_locales, ui_locales)
    extras_dict     = _dh.prepare_extras_dict_for_normal_page(request)
    _dh.add_language_options_for_extra_dict(extras_dict)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': name + ' ' + full_version,
        'project': project_name,
        'extras': extras_dict,
        'session_expired': session_expired
    }


# contact page
@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody', require_csrf=False)
def main_contact(request):
    """
    View configuration for the contact view.

    :param request: current request of the server
    :return: dictionary with title and project username as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_contact', 'def', 'request.params: {}, request.matchdict: {}'.format(request.params, request.matchdict))
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    contact_error, send_message, message = False, False, ''
    ui_locales = get_language_from_cookie(request)

    username  = escape_string(request.params['name']) if 'name' in request.params else ''
    email     = escape_string(request.params['mail']) if 'mail' in request.params else ''
    content   = escape_string(request.params['content']) if 'content' in request.params else ''
    recaptcha = request.params['g-recaptcha-response'] if 'g-recaptcha-response' in request.params else ''

    # check for user data
    if len(name) == 0 or len(email) == 0:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=str(request.authenticated_userid)).first()
        username = '{} {}'.format(db_user.firstname, db_user.surname) if db_user else ''
        email = db_user.email if db_user else ''

    if 'form.contact.submitted' in request.params:
        contact_error, message, send_message = try_to_contact(request, username, email, content, ui_locales, recaptcha)

    bug_view = False
    if 'reason' in request.matchdict and len(request.matchdict['reason']) > 0:
        if request.matchdict['reason'].lower() == '&bug=true':
            bug_view = True
        else:
            logger('main_contact', 'def', 'wrong reason: {}'.format(request.matchdict['reason']), error=True)
            raise HTTPNotFound()

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)
    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)
    placeholder = {
        'name': _t.get(_.exampleName),
        'mail': _t.get(_.exampleMail),
        'message': _t.get(_.exampleMessageBug if bug_view else _.exampleMessage)
    }

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _t.get(_.reportIssue if bug_view else _.contact),
        'project': project_name,
        'extras': extras_dict,
        'was_message_send': send_message,
        'contact_error': contact_error,
        'message': message,
        'name': username,
        'mail': email,
        'content': content,
        'spamanswer': '',
        'placeholder': placeholder,
        'bug_view': bug_view
    }


# settings page, when logged in
@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
def main_settings(request):
    """
    View configuration for the personal settings view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_settings', 'def', 'request.params: {}'.format(request.params))
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    ui_locales  = get_language_from_cookie(request)
    old_pw      = ''
    new_pw      = ''
    confirm_pw  = ''
    message     = ''
    success     = False
    error       = False
    db_user     = DBDiscussionSession.query(User).filter_by(nickname=str(request.authenticated_userid)).join(Group).first()
    _uh         = user_manager
    _t          = Translator(ui_locales)

    if not db_user:
        raise HTTPNotFound()

    if db_user and 'form.passwordchange.submitted' in request.params:
        old_pw = escape_string(request.params['passwordold'])
        new_pw = escape_string(request.params['password'])
        confirm_pw = escape_string(request.params['passwordconfirm'])

        message, success = _uh.change_password(db_user, old_pw, new_pw, confirm_pw, ui_locales)
        error = not success

    _dh = DictionaryHelper(ui_locales)
    extras_dict = _dh.prepare_extras_dict_for_normal_page(request)
    settings_dict = _dh.prepare_settings_dict(success, old_pw, new_pw, confirm_pw, error, message, db_user, request.application_url)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _t.get(_.settings),
        'project': project_name,
        'extras': extras_dict,
        'settings': settings_dict
    }


# message page, when logged in
@view_config(route_name='main_notification', renderer='templates/notifications.pt', permission='use')
def main_notifications(request):
    """
    View configuration for the notification view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_notifications', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request, append_notifications=True)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Messages',
        'project': project_name,
        'extras': extras_dict
    }


# news page for everybody
@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
def main_news(request):
    """
    View configuration for the news.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_news', 'def', 'main')
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    ui_locales = get_language_from_cookie(request)
    is_author = is_user_author_or_admin(request.authenticated_userid)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'News',
        'project': project_name,
        'extras': extras_dict,
        'is_author': is_author,
        'news': news_handler.get_news(ui_locales)
    }


# public users page for everybody
@view_config(route_name='main_user', renderer='templates/user.pt', permission='everybody')
def main_user(request):
    """
    View configuration for the public user page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    match_dict = request.matchdict
    params = request.params
    logger('main_user', 'def', 'request.matchdict: {}'.format(match_dict))
    logger('main_user', 'def', 'request.params: {}'.format(params))

    uid = match_dict['uid'] if 'uid' in match_dict else 0
    logger('main_user', 'def', 'uid: {}'.format(uid))

    if not is_integer(uid):
        raise HTTPNotFound

    current_user = DBDiscussionSession.query(User).get(uid)
    if current_user is None or current_user.nickname == nick_of_anonymous_user:
        logger('main_user', 'def', 'no user: {}'.format(uid), error=True)
        raise HTTPNotFound()

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    ui_locales = get_language_from_cookie(request)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    user_dict = user_manager.get_information_of(current_user, ui_locales)

    db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    can_send_notification = False
    if db_user_of_request:
        can_send_notification = current_user.uid != db_user_of_request.uid

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': user_dict['public_nick'],
        'project': project_name,
        'extras': extras_dict,
        'user': user_dict,
        'can_send_notification': can_send_notification
    }


# imprint
@view_config(route_name='main_imprint', renderer='templates/imprint.pt', permission='everybody')
def main_imprint(request):
    """
    View configuration for the imprint.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_imprint', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    _tn = Translator(ui_locales)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    # add version of pyramid
    import pkg_resources
    extras_dict.update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

    try:  # try to get current commit hash
        extras_dict.update({'dbas_build': subprocess.check_output(['git', 'describe'])})
    except FileNotFoundError:  # fallback
        extras_dict.update({'dbas_build': full_version})

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.imprint),
        'project': project_name,
        'extras': extras_dict,
        'imprint': get_changelog(5)
    }


# faq
@view_config(route_name='main_faq', renderer='templates/faq.pt', permission='everybody')
def main_faq(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_faq', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'FAQ',
        'project': project_name,
        'extras': extras_dict
    }


# docs
@view_config(route_name='main_docs', renderer='templates/docs.pt', permission='everybody')
def main_docs(request):
    """
    View configuration for the documentation.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_docs', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.docs),
        'project': project_name,
        'extras': extras_dict
    }


# imprint
@view_config(route_name='main_publications', renderer='templates/publications.pt', permission='everybody')
def main_publications(request):
    """
    View configuration for the publications list.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_publications', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.publications),
        'project': project_name,
        'extras': extras_dict
    }


# imprint
@view_config(route_name='main_rss', renderer='templates/rss.pt', permission='everybody')
def main_rss(request):
    """
    View configuration for the RSS feed.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_rss', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)
    rss = get_list_of_all_feeds(ui_locales)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'RSS',
        'project': project_name,
        'extras': extras_dict,
        'rss': rss
    }


# 404 page
@notfound_view_config(renderer='templates/404.pt')
def notfound(request):
    """
    View configuration for the 404 page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    if request.path.startswith('/api'):
        return api_notfound(request)

    user_manager.update_last_action(request.authenticated_userid)
    logger('notfound', 'def', 'main in {}'.format(request.method) + '-request' +
           ', path: ' + request.path +
           ', view name: ' + request.view_name +
           ', params: {}'.format(request.params))
    path = request.path
    if path.startswith('/404/'):
        path = path[4:]

    param_error = 'param_error' in request.params and request.params['param_error'] == 'true'
    revoked_content = 'revoked_content' in request.params and request.params['revoked_content'] == 'true'

    request.response.status = 404
    ui_locales = get_language_from_cookie(request)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'Error',
        'project': project_name,
        'page_notfound_viewname': path,
        'extras': extras_dict,
        'param_error': param_error,
        'revoked_content': revoked_content
    }

# ####################################
# DISCUSSION                         #
# ####################################


# content page
@view_config(route_name='discussion_init', renderer='templates/content.pt', permission='everybody')
def discussion_init(request, for_api=False, api_data=None):
    """
    View configuration for the initial discussion.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data: Dictionary, containing data of a user who logged in via API
    :return: dictionary
    """
    logger('Views', 'discussion_init', 'request.matchdict: {}'.format(request.matchdict))
    logger('Views', 'discussion_init', 'request.params: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.init, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# attitude page
@view_config(route_name='discussion_attitude', renderer='templates/content.pt', permission='everybody')
def discussion_attitude(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where we will ask the user for her attitude towards a statement.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    # '/discuss/{slug}/attitude/{statement_id}'
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('Views', 'discussion_attitude', 'request.matchdict: {}'.format(request.matchdict))
    logger('Views', 'discussion_attitude', 'request.params: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.attitude, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# justify page
@view_config(route_name='discussion_justify', renderer='templates/content.pt', permission='everybody')
def discussion_justify(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    # '/discuss/{slug}/justify/{statement_or_arg_id}/{mode}*relation'
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'discussion_justify', 'request.matchdict: {}'.format(request.matchdict))
    logger('views', 'discussion_justify', 'request.params: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.justify, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# reaction page
@view_config(route_name='discussion_reaction', renderer='templates/content.pt', permission='everybody')
def discussion_reaction(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where we will ask the user for her reaction (support, undercut, rebut)...

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    # '/discuss/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys'
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'discussion_reaction', 'request.matchdict: {}'.format(request.matchdict))
    logger('views', 'discussion_reaction', 'request.params: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.reaction, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# support page
@view_config(route_name='discussion_support', renderer='templates/content.pt', permission='everybody')
def discussion_support(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where we will present another supportive argument.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    # '/discuss/{slug}/jump/{arg_id}'
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'discussion_support', 'request.matchdict: {}'.format(request.matchdict))
    logger('views', 'discussion_support', 'request.params: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.support, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# finish page
@view_config(route_name='discussion_finish', renderer='templates/finish.pt', permission='everybody')
def discussion_finish(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    match_dict = request.matchdict
    params = request.params
    logger('views', 'discussion.finish', 'request.matchdict: {}'.format(match_dict))
    logger('views', 'discussion.finish', 'request.params: {}'.format(params))

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    prepared_discussion = discussion.finish(request)
    prepared_discussion['layout'] = base_layout()
    prepared_discussion['language'] = str(get_language_from_cookie(request))
    prepared_discussion['show_summary'] = len(prepared_discussion['summary']) != 0
    return prepared_discussion


# choosing page
@view_config(route_name='discussion_choose', renderer='templates/content.pt', permission='everybody')
def discussion_choose(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where the user has to choose between given statements.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    # '/discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids'
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    match_dict = request.matchdict
    params = request.params
    logger('discussion_choose', 'def', 'request.matchdict: {}'.format(match_dict))
    logger('discussion_choose', 'def', 'request.params: {}'.format(params))

    prepared_discussion = __call_from_discussion_step(request, discussion.choose, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# jump page
@view_config(route_name='discussion_jump', renderer='templates/content.pt', permission='everybody')
def discussion_jump(request, for_api=False, api_data=None):
    """
    View configuration for the jump view.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    # '/discuss/{slug}/jump/{arg_id}'
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'discussion_jump', 'request.matchdict: {}'.format(request.matchdict))
    logger('views', 'discussion_jump', 'request.params: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.jump, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# ####################################
# REVIEW                             #
# ####################################

# index page for reviews
@view_config(route_name='review_index', renderer='templates/review.pt', permission='use')
def main_review(request):
    """
    View configuration for the review index.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('main_review', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    nickname = request.authenticated_userid
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    issue = issue_helper.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, False)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    review_dict = review_queue_helper.get_review_queues_as_lists(request.application_url, _tn, nickname)
    count, all_rights = review_reputation_helper.get_reputation_of(nickname)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.review),
        'project': project_name,
        'extras': extras_dict,
        'review': review_dict,
        'privilege_list': review_reputation_helper.get_privilege_list(_tn),
        'reputation_list': review_reputation_helper.get_reputation_list(_tn),
        'issues': issue_dict,
        'reputation': {'count': count,
                       'has_all_rights': all_rights}
    }


# content page for reviews
@view_config(route_name='review_content', renderer='templates/review-content.pt', permission='use')
def review_content(request):
    """
    View configuration for the review content.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('review_content', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    request_authenticated_userid = request.authenticated_userid
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    subpage_name = request.matchdict['queue']
    subpage_dict = review_page_helper.get_subpage_elements_for(request, subpage_name,
                                                               request_authenticated_userid, _tn)
    if not subpage_dict['elements'] and not subpage_dict['has_access'] and not subpage_dict['no_arguments_to_review']:
        logger('review_content', 'def', 'subpage error', error=True)
        raise HTTPNotFound()

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    title = _tn.get(_.review)
    if subpage_name == 'deletes':
        title = _tn.get(_.queueDelete)
    if subpage_name == 'optimizations':
        title = _tn.get(_.queueOptimization)
    if subpage_name == 'edits':
        title = _tn.get(_.queueEdit)
    if subpage_name == 'duplicates':
        title = _tn.get(_.queueDuplicates)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': title,
        'project': project_name,
        'extras': extras_dict,
        'subpage': subpage_dict,
        'lock_time': review_queue_helper.max_lock_time_in_sec
    }


# history page for reviews
@view_config(route_name='review_history', renderer='templates/review-history.pt', permission='use')
def review_history(request):
    """
    View configuration for the review history.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('review_history', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    request_authenticated_userid = request.authenticated_userid
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    history = review_history_helper.get_review_history(request.application_url, request_authenticated_userid, _tn)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)
    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.review_history),
        'project': project_name,
        'extras': extras_dict,
        'history': history
    }


# history page for reviews
@view_config(route_name='review_ongoing', renderer='templates/review-history.pt', permission='use')
def ongoing_history(request):
    """
    View configuration for the current reviews.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('ongoing_history', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    history = review_history_helper.get_ongoing_reviews(request.application_url, request.authenticated_userid, _tn)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.review_ongoing),
        'project': project_name,
        'extras': extras_dict,
        'history': history
    }


# reputation_borders page for reviews
@view_config(route_name='review_reputation', renderer='templates/review-reputation.pt', permission='use')
def review_reputation(request):
    """
    View configuration for the review reputation_borders.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('review_reputation', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request)

    reputation_dict = review_history_helper.get_reputation_history_of(request.authenticated_userid, _tn)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.reputation),
        'project': project_name,
        'extras': extras_dict,
        'reputation': reputation_dict
    }


# #####################################
# ADDITIONAL AJAX STUFF # USER THINGS #
# #####################################


def call_from_request(request, f: Callable[[Any, Any], Any]):
    """
    Calls f with the authenticated_userid and ui_locales from request.

    :param request: A pyramid request
    :param f: A function with two arguments
    :return: Return value of f
    """
    logger(f.__name__, 'def', 'main')
    userid = request.authenticated_userid
    user_manager.update_last_action(userid)
    ui_locales = get_language_from_cookie(request)

    return f(userid, ui_locales)


# ajax - getting complete track of the user
@view_config(route_name='ajax_get_user_history', renderer='json')
def get_user_history(request):
    """
    Request the complete user track.

    :param request: current request of the server
    :return: json-dict()
    """
    return call_from_request(request, history_helper.get_history_from_database)


# ajax - getting all text edits
@view_config(route_name='ajax_get_all_posted_statements', renderer='json')
def get_all_posted_statements(request):
    """
    Request for all statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    return_array, _ = call_from_request(request, user_manager.get_textversions_of_user)
    return return_array


# ajax - getting all text edits
@view_config(route_name='ajax_get_all_edits', renderer='json')
def get_all_edits_of_user(request):
    """
    Request for all edits of the user

    :param request: current request of the server
    :return: json-dict()
    """
    _, return_array = call_from_request(request, user_manager.get_textversions_of_user)
    return return_array


# ajax - getting all votes for arguments
@view_config(route_name='ajax_get_all_marked_arguments', renderer='json')
def get_all_marked_arguments(request):
    """
    Request for all marked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    return call_from_request(request, user_manager.get_marked_elements_of_user)


# ajax - getting all votes for statements
@view_config(route_name='ajax_get_all_marked_statements', renderer='json')
def get_all_marked_statements(request):
    """
    Request for all marked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    return call_from_request(request, user_manager.get_arg_clicks_of_user)


# ajax - getting all votes for arguments
@view_config(route_name='ajax_get_all_argument_clicks', renderer='json')
def get_all_argument_clicks(request):
    """
    Request for all clicked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    return call_from_request(request, user_manager.get_arg_clicks_of_user)


# ajax - getting all votes for statements
@view_config(route_name='ajax_get_all_statement_clicks', renderer='json')
def get_all_statement_clicks(request):
    """
    Request for all clicked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    return call_from_request(request, user_manager.get_stmt_clicks_of_user)


# ajax - deleting complete history of the user
@view_config(route_name='ajax_delete_user_history', renderer='json')
def delete_user_history(request):
    """
    Request to delete the users history.

    :param request: request of the web server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('delete_user_history', 'def', 'main')
    user_manager.update_last_action(request.authenticated_userid)
    return {'removed_data': str(history_helper.delete_history_in_database(request.authenticated_userid)).lower()}


# ajax - deleting complete history of the user
@view_config(route_name='ajax_delete_statistics', renderer='json')
def delete_statistics(request):
    """
    Request to delete votes/clicks of the user.

    :param request: request of the web server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('delete_statistics', 'def', 'main')
    user_manager.update_last_action(request.authenticated_userid)
    return {'removed_data': str(clear_vote_and_seen_values_of_user(request.authenticated_userid)).lower()}


# ajax - user login
@view_config(route_name='ajax_user_login', renderer='json')
def user_login(request, nickname=None, password=None, for_api=False, keep_login=False):
    """
    Will login the user by his nickname and password

    :param request: request of the web server
    :param nickname: Manually provide nickname (e.g. from API)
    :param password: Manually provide password (e.g. from API)
    :param for_api: Manually provide boolean (e.g. from API)
    :param keep_login: Manually provide boolean (e.g. from API)
    :return: dict() with error
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('user_login', 'def', 'request.params: {} (api: {})'.format(request.params, str(for_api)))

    lang = get_language_from_cookie(request)
    _tn = Translator(lang)

    try:
        return login_user(request, nickname, password, for_api, keep_login, _tn)
    except KeyError as e:
        logger('user_login', 'error', repr(e))
        return {'error': _tn.get(_.internalKeyError)}


# ajax - user logout
@view_config(route_name='ajax_user_logout', renderer='json')
def user_logout(request, redirect_to_main=False):
    """
    Will logout the user

    :param request: request of the web server
    :param redirect_to_main: Boolean
    :return: HTTPFound with forgotten headers
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('user_logout', 'def', 'user: {}, redirect_to_main: {}'.format(request.authenticated_userid, redirect_to_main))
    request.session.invalidate()
    headers = forget(request)
    if redirect_to_main:
        return HTTPFound(
            location=request.application_url + '?session_expired=true',
            headers=headers,
        )
    else:
        request.response.headerlist.extend(headers)
        return request.response


# ajax - registration of users
@view_config(route_name='ajax_user_registration', renderer='json')
def user_registration(request):
    """
    Registers new user with data given in the ajax requesst

    :param request: current request of the server
    :return: dict() with success and message
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('user_registration', 'def', 'request.params: {}'.format(request.params))

    # default values
    success = ''
    error = ''
    info = ''

    ui_locales = request.params['lang'] if 'lang' in request.params else get_language_from_cookie(request)
    _t = Translator(ui_locales)

    try:
        success, info = register_with_ajax_data(request, ui_locales)

    except KeyError as e:
        logger('user_registration', 'error', repr(e))
        error = _t.get(_.internalKeyError)

    return {'success': str(success),
            'error': str(error),
            'info': str(info)}


# ajax - password requests
@view_config(route_name='ajax_user_password_request', renderer='json')
def user_password_request(request):
    """
    Sends an email, when the user requests his password

    :param request: current request of the server
    :return: dict() with success and message
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('user_password_request', 'def', 'request.params: {}'.format(request.params))

    success = ''
    info = ''
    return_dict = dict()
    ui_locales = request.params['lang'] if 'lang' in request.params else get_language_from_cookie(request)
    _t = Translator(ui_locales)

    try:
        success, error, info = request_password(request, ui_locales)

    except KeyError as e:
        logger('user_password_request', 'error', repr(e))
        error = _t.get(_.internalKeyError)

    return_dict['success'] = str(success)
    return_dict['error']   = str(error)
    return_dict['info']    = str(info)

    logger('user_password_request', 'success', str(success))
    logger('user_password_request', 'error', str(error))
    logger('user_password_request', 'info', str(info))

    return return_dict


# ajax - set boolean for receiving information
@view_config(route_name='ajax_set_user_setting', renderer='json')
def set_user_settings(request):
    """
    Sets a specific setting of the user

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('set_user_settings', 'def', 'request.params: {}'.format(request.params))
    _tn = Translator(get_language_from_cookie(request))

    try:
        settings_value = request.params['settings_value'] == 'True'
        service = request.params['service']
        public_nick, public_page_url, gravatar_url, error = set_settings(request.application_url, request.authenticated_userid, service, settings_value, _tn)
    except KeyError as e:
        error = _tn.get(_.internalKeyError)
        public_nick = ''
        public_page_url = ''
        gravatar_url = ''
        logger('set_user_settings', 'error', repr(e))

    return_dict = {'error': error, 'public_nick': public_nick, 'public_page_url': public_page_url, 'gravatar_url': gravatar_url}
    return return_dict


# ajax - set boolean for receiving information
@view_config(route_name='ajax_set_user_language', renderer='json')
def set_user_language(request):
    """
    Will logout the user

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'set_user_language', 'request.params: {}'.format(request.params))

    try:
        ui_locales = request.params['ui_locales'] if 'ui_locales' in request.params else None
        prepared_dict = add.set_user_language(request.authenticated_userid, ui_locales)
    except KeyError as e:
        logger('views', 'set_user_settings', repr(e), error=True)
        _tn = Translator(get_language_from_cookie(request))
        prepared_dict = {}
        prepared_dict['error'] = _tn.get(_.internalKeyError)
        prepared_dict['ui_locales'] = ''
        prepared_dict['current_lang'] = ''
    return prepared_dict


# ajax - sending notification
@view_config(route_name='ajax_send_notification', renderer='json')
def send_some_notification(request):
    """
    Set a new message into the inbox of an recipient, and the outbox of the sender.

    :param request: current request of the server
    :return: dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('send_some_notification', 'def', 'request.params: {}'.format(request.params))

    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        prepared_dict = add.send_some_notification(request)

    except (KeyError, AttributeError):
        prepared_dict = {}
        prepared_dict['error'] = _tn.get(_.internalKeyError)
        prepared_dict['timestamp'] = ''
        prepared_dict['uid'] = ''
        prepared_dict['recipient_avatar'] = ''

    return prepared_dict


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################


# ajax - send new start statement
@view_config(route_name='ajax_set_new_start_statement', renderer='json')
def set_new_start_statement(request, for_api=False, api_data=None):
    """
    Inserts a new statement into the database, which should be available at the beginning

    :param request: request of the web server
    :param for_api: boolean
    :param api_data: api_data
    :return: a status code, if everything was successful
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'set_new_start_statement', 'request.params: {}'.format(request.params))

    discussion_lang = get_discussion_language(request)
    _tn = Translator(discussion_lang)
    return_dict = dict()
    return_dict['error'] = ''
    return_dict['statement_uids'] = []
    try:
        if for_api and api_data:
            nickname  = api_data["nickname"]
            statement = api_data["statement"]
            issue     = api_data["issue_id"]
            slug      = api_data["slug"]
        else:
            nickname    = request.authenticated_userid
            statement   = request.params['statement']
            issue       = issue_helper.get_issue_id(request)
            slug        = DBDiscussionSession.query(Issue).get(issue).get_slug()

        # escaping will be done in QueryHelper().set_statement(...)
        user_manager.update_last_action(nickname)
        new_statement = insert_as_statements(request, statement, nickname, issue, discussion_lang, is_start=True)

        if new_statement == -1:
            a = _tn.get(_.notInsertedErrorBecauseEmpty)
            b = _tn.get(_.minLength)
            c = _tn.get(_.eachStatement)
            error = '{} ({}: {} {})'.format(a, b, str(10), c)
            return_dict['error'] = error
        elif new_statement == -2:
            return_dict['error'] = _tn.get(_.noRights)
        else:
            url = UrlManager(request.application_url, slug, for_api).get_url_for_statement_attitude(False, new_statement[0].uid)
            return_dict['url'] = url
            return_dict['statement_uids'].append(new_statement[0].uid)

            # add reputation
            add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_position)
            if not add_rep:
                add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
                # send message if the user is now able to review
            if broke_limit:
                # ui_locales = get_language_from_cookie(request)
                # _t = Translator(ui_locales)
                # send_request_for_info_popup_to_socketio(nickname, _t.get(_.youAreAbleToReviewNow), request.application_url + '/review')
                url += '#access-review'
                return_dict['url'] = url

    except KeyError as e:
        logger('set_new_start_statement', 'error', repr(e))
        return_dict['error'] = _tn.get(_.notInsertedErrorBecauseInternal)

    return return_dict


# ajax - send new start premise
@view_config(route_name='ajax_set_new_start_premise', renderer='json')
def set_new_start_premise(request, for_api=False, api_data=None):
    """
    Sets new premise for the start

    :param request: request of the web server
    :param for_api: boolean
    :param api_data:
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('set_new_start_premise', 'def', 'request.params: {}'.format(request.params))

    return_dict = dict()
    lang = get_discussion_language(request)
    _tn = Translator(lang)
    try:
        if for_api and api_data:
            nickname      = api_data['nickname']
            premisegroups = api_data['statement']
            issue         = api_data['issue_id']
            conclusion_id = api_data['conclusion_id']
            supportive    = api_data['supportive']
        else:
            nickname        = request.authenticated_userid
            issue           = issue_helper.get_issue_id(request)
            premisegroups   = json.loads(request.params['premisegroups'])
            conclusion_id   = request.params['conclusion_id']
            supportive      = True if request.params['supportive'].lower() == 'true' else False

        # escaping will be done in QueryHelper().set_statement(...)
        user_manager.update_last_action(nickname)

        url, statement_uids, error = process_input_of_start_premises_and_receive_url(request, premisegroups,
                                                                                     conclusion_id, supportive, issue,
                                                                                     nickname, for_api,
                                                                                     request.application_url, lang)

        return_dict['error'] = error
        return_dict['statement_uids'] = statement_uids

        # add reputation
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_justification)
        if not add_rep:
            add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
            # send message if the user is now able to review
        if broke_limit:
            ui_locales = get_language_from_cookie(request)
            _t = Translator(ui_locales)
            send_request_for_info_popup_to_socketio(request, _t.get(_.youAreAbleToReviewNow),  request.application_url + '/review')
            return_dict['url'] = str(url) + str('#access-review')

        if url == -1:
            return return_dict

        return_dict['url'] = url
    except KeyError as e:
        logger('set_new_start_premise', 'error', repr(e))
        return_dict['error'] = _tn.get(_.notInsertedErrorBecauseInternal)

    return return_dict


# ajax - send new premises
@view_config(route_name='ajax_set_new_premises_for_argument', renderer='json')
def set_new_premises_for_argument(request, for_api=False, api_data=None):
    """
    Sets a new premise for an argument

    :param request: request of the web server
    :param api_data:
    :param for_api: boolean
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('set_new_premises_for_argument', 'def', 'request.params: {}'.format(request.params))

    return_dict = dict()
    lang = get_language_from_cookie(request)
    _tn = Translator(lang)

    try:
        if for_api and api_data:
            nickname      = api_data['nickname']
            premisegroups = api_data['statement']
            issue         = api_data['issue_id']
            arg_uid       = api_data['arg_uid']
            attack_type   = api_data['attack_type']
        else:
            nickname = request.authenticated_userid
            premisegroups = json.loads(request.params['premisegroups'])
            issue = issue_helper.get_issue_id(request)
            arg_uid = request.params['arg_uid']
            attack_type = request.params['attack_type']

        # escaping will be done in QueryHelper().set_statement(...)
        discussion_lang = get_discussion_language(request)
        url, statement_uids, error = process_input_of_premises_for_arguments_and_receive_url(request,
                                                                                             arg_uid, attack_type,
                                                                                             premisegroups, issue,
                                                                                             nickname, for_api,
                                                                                             request.application_url,
                                                                                             discussion_lang)
        user_manager.update_last_action(nickname)

        return_dict['error'] = error
        return_dict['statement_uids'] = statement_uids

        # add reputation
        add_rep, broke_limit = add_reputation_for(nickname, rep_reason_first_new_argument)
        if not add_rep:
            add_rep, broke_limit = add_reputation_for(nickname, rep_reason_new_statement)
            # send message if the user is now able to review
        if broke_limit:
            # ui_locales = get_language_from_cookie(request)
            # _t = Translator(ui_locales)
            # send_request_for_info_popup_to_socketio(nickname, _t.get(_.youAreAbleToReviewNow), request.application_url + '/review')
            url += '#access-review'
            return_dict['url'] = url

        if url == -1:
            return return_dict

        return_dict['url'] = url

    except KeyError as e:
        logger('set_new_premises_for_argument', 'error', repr(e))
        return_dict['error'] = _tn.get(_.notInsertedErrorBecauseInternal)

    logger('set_new_premises_for_argument', 'def', 'returning {}'.format(return_dict))
    return return_dict


# ajax - set new textvalue for a statement
@view_config(route_name='ajax_set_correction_of_statement', renderer='json')
def set_correction_of_statement(request):
    """
    Sets a new textvalue for a statement

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('set_correction_of_statement', 'def', 'request.params: {}'.format(request.params))
    nickname = request.authenticated_userid
    user_manager.update_last_action(nickname)

    _tn = Translator(get_language_from_cookie(request))

    return_dict = dict()
    try:
        elements = json.loads(request.params['elements'])
        msg, error = review_queue_helper.add_proposals_for_statement_corrections(elements, nickname, _tn)
        return_dict['error'] = msg if error else ''
        return_dict['info'] = msg if len(msg) > 0 else ''
    except KeyError as e:
        return_dict['error'] = _tn.get(_.internalError)
        return_dict['info'] = ''
        logger('set_correction_of_statement', 'error', repr(e))

    return return_dict


# ajax - set notification as read
@view_config(route_name='ajax_notification_read', renderer='json')
def set_notification_read(request):
    """
    Set a notification as read

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    request_authenticated_userid = request.authenticated_userid
    user_manager.update_last_action(request_authenticated_userid)

    logger('set_notification_read', 'def', 'main {}'.format(request.params))
    return_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)

    try:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=request_authenticated_userid).first()
        if db_user:
            DBDiscussionSession.query(Message).filter(and_(Message.uid == request.params['id'],
                                                           Message.to_author_uid == db_user.uid,
                                                           Message.is_inbox == True)).first().set_read(True)
            transaction.commit()
            return_dict['unread_messages'] = count_of_new_notifications(request_authenticated_userid)
            return_dict['error'] = ''
        else:
            return_dict['error'] = _t.get(_.noRights)
    except KeyError as e:
        logger('set_message_read', 'error', repr(e))
        return_dict['error'] = _t.get(_.internalKeyError)

    return return_dict


# ajax - deletes a notification
@view_config(route_name='ajax_notification_delete', renderer='json')
def set_notification_delete(request):
    """
    Request the removal of a notification

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    request_authenticated_userid = request.authenticated_userid
    user_manager.update_last_action(request_authenticated_userid)

    logger('set_notification_delete', 'def', 'main {}'.format(request.params))
    return_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)

    try:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=request_authenticated_userid).first()
        if db_user:
            # inbox
            DBDiscussionSession.query(Message).filter(and_(Message.uid == request.params['id'],
                                                           Message.to_author_uid == db_user.uid,
                                                           Message.is_inbox == True)).delete()
            # send
            DBDiscussionSession.query(Message).filter(and_(Message.uid == request.params['id'],
                                                           Message.from_author_uid == db_user.uid,
                                                           Message.is_inbox == False)).delete()
            transaction.commit()
            return_dict['unread_messages'] = count_of_new_notifications(request_authenticated_userid)
            return_dict['total_in_messages'] = str(len(get_box_for(request_authenticated_userid, ui_locales, request.application_url, True)))
            return_dict['total_out_messages'] = str(len(get_box_for(request_authenticated_userid, ui_locales, request.application_url, False)))
            return_dict['error'] = ''
            return_dict['success'] = _t.get(_.messageDeleted)
        else:
            return_dict['error'] = _t.get(_.noRights)
            return_dict['success'] = ''
    except KeyError as e:
        logger('set_message_read', 'error', repr(e))
        return_dict['error'] = _t.get(_.internalKeyError)
        return_dict['success'] = ''

    return return_dict


# ajax - set new issue
@view_config(route_name='ajax_set_new_issue', renderer='json')
def set_new_issue(request):
    """

    :param request: current request of the server
    :return:
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    request_authenticated_userid = request.authenticated_userid
    user_manager.update_last_action(request_authenticated_userid)

    logger('set_new_issue', 'def', 'main {}'.format(request.params))
    return_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)
    was_set = False

    try:
        info = escape_string(request.params['info'])
        long_info = escape_string(request.params['long_info'])
        title = escape_string(request.params['title'])
        lang = escape_string(request.params['lang'])
        was_set, error = issue_helper.set_issue(info, long_info, title, lang, request_authenticated_userid, ui_locales)
        if was_set:
            db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
                                                                    Issue.info == info)).first()
            return_dict['issue'] = issue_helper.get_issue_dict_for(db_issue, request.application_url, False, 0, ui_locales)
    except KeyError as e:
        logger('set_new_issue', 'error', repr(e))
        error = _tn.get(_.notInsertedErrorBecauseInternal)

    return_dict['error'] = '' if was_set else error
    return return_dict


# ajax - set seen premisegroup
@view_config(route_name='ajax_set_seen_statements', renderer='json')
def set_seen_statements(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('set_seen_statements', 'def', 'main {}'.format(request.params))
    return_dict = dict()
    ui_locales = get_language_from_cookie(request)
    _t = Translator(ui_locales)

    try:
        uids = json.loads(request.params['uids'])
        # are the statements connected to an argument?
        additional_argument = None
        if 'justify' in request.path:
            url = request.path[request.path.index('justify/') + len('justify/'):]
            additional_argument = int(url[:url.index('/')])

        error = process_seen_statements(uids, request.authenticated_userid, _t, additional_argument=additional_argument)
        return_dict['error'] = error
    except KeyError as e:
        logger('set_seen_statements', 'error', repr(e))
        return_dict['error'] = _t.get(_.internalKeyError)

    return return_dict


# ajax - set users opinion
@view_config(route_name='ajax_mark_statement_or_argument', renderer='json')
def mark_statement_or_argument(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('mark_statement_or_argument', 'def', 'main {}'.format(request.params))
    return_dict = dict()
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)

    try:
        uid = request.params['uid']
        step = request.params['step']
        is_argument = str(request.params['is_argument']).lower() == 'true'
        is_supportive = str(request.params['is_supportive']).lower() == 'true'
        should_mark = str(request.params['should_mark']).lower() == 'true'
        history = request.params['history'] if 'history' in request.params else ''

        success, error = mark_or_unmark_statement_or_argument(uid, is_argument, should_mark, request.authenticated_userid, _t)
        return_dict['success'] = success
        return_dict['error'] = error
        return_dict['text'] = get_text_for_justification_or_reaction_bubble(uid, is_argument, is_supportive, request.authenticated_userid, step, history, _t)
    except KeyError as e:
        logger('set_seen_statements', 'error', repr(e))
        return_dict['error'] = _t.get(_.internalKeyError)

    return return_dict

# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################


# ajax - getting changelog of a statement
@view_config(route_name='ajax_get_logfile_for_statements', renderer='json')
def get_logfile_for_some_statements(request):
    """
    Returns the changelog of a statement

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_logfile_for_statements', 'def', 'request.params: {}'.format(request.params))
    user_manager.update_last_action(request.authenticated_userid)

    return_dict = {'info': ''}
    ui_locales = get_language_from_cookie(request)

    try:
        uids = json.loads(request.params['uids'])
        issue = request.params['issue']
        ui_locales = get_discussion_language(request, issue)
        return_dict = get_logfile_for_statements(uids, ui_locales, request.application_url)
        return_dict['error'] = ''
    except KeyError as e:
        logger('get_logfile_for_premisegroup', 'error', repr(e))
        _tn = Translator(ui_locales)
        return_dict['error'] = _tn.get(_.noCorrections)

    return return_dict


# ajax - for shorten url
@view_config(route_name='ajax_get_shortened_url', renderer='json')
def get_shortened_url(request):
    """
    Shortens url with the help of a python lib

    :param request: current request of the server
    :return: dictionary with shortend url
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    user_manager.update_last_action(request.authenticated_userid)

    logger('get_shortened_url', 'def', 'main')

    return_dict = dict()

    try:
        url = request.params['url']
        service = Shorteners.TINYURL
        service_url = 'http://tinyurl.com/'
        shortener = Shortener(service)

        short_url = format(shortener.short(url))
        return_dict['url'] = short_url
        return_dict['service'] = service
        return_dict['service_url'] = service_url

        return_dict['error'] = ''
    except KeyError as e:
        logger('get_shortened_url', 'error', repr(e))
        _tn = Translator(get_discussion_language(request))
        return_dict['error'] = _tn.get(_.internalKeyError)
    except ReadTimeout as e:
        logger('get_shortened_url', 'read timeout error', repr(e))
        _tn = Translator(get_discussion_language(request))
        return_dict['error'] = _tn.get(_.serviceNotAvailable)

    return return_dict


# ajax - for getting all news
@view_config(route_name='ajax_get_news', renderer='json')
def get_news(request):
    """
    ajax interface for getting news

    :param request: current request of the server
    :return: json-set with all news
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_news', 'def', 'main')
    return news_handler.get_news(get_language_from_cookie(request))


# ajax - for getting argument infos
@view_config(route_name='ajax_get_infos_about_argument', renderer='json')
def get_all_infos_about_argument(request):
    """
    ajax interface for getting a dump

    :param request: current request of the server
    :return: json-set with everything
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_all_infos_about_argument', 'def', 'request.params: {}'.format(request.params))
    ui_locales = get_discussion_language(request)
    _t = Translator(ui_locales)
    return_dict = dict()

    try:
        uid = request.params['uid']
        if not is_integer(uid):
            return_dict['error'] = _t.get(_.internalError)
        else:
            return_dict = get_infos_about_argument(uid, request.application_url, request.authenticated_userid, _t)
            return_dict['error'] = ''
    except KeyError as e:
        logger('get_infos_about_argument', 'error', repr(e))
        return_dict['error'] = _t.get(_.internalKeyError)

    return return_dict


# ajax - for getting all users with the same opinion
@view_config(route_name='ajax_get_user_with_same_opinion', renderer='json')
def get_users_with_same_opinion(request):
    """
    ajax interface for getting a dump

    :params reqeust: current request of the web  server
    :return: json-set with everything
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_users_with_same_opinion', 'def', 'main: {}'.format(request.params))
    nickname = request.authenticated_userid
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        params = request.params
        ui_locales = params['lang'] if 'lang' in params else 'en'
        uids = params['uids']
        is_arg = params['is_argument'] == 'true' if 'is_argument' in params else False
        is_att = params['is_attitude'] == 'true' if 'is_attitude' in params else False
        is_rea = params['is_reaction'] == 'true' if 'is_reaction' in params else False
        is_pos = params['is_position'] == 'true' if 'is_position' in params else False

        if is_arg:
            if is_rea:
                uids = json.loads(uids)
                return_dict = get_user_and_opinions_for_argument(uids, nickname, ui_locales, request.application_url, request.path)
            else:
                return_dict = get_user_with_same_opinion_for_argument(uids, nickname, ui_locales, request.application_url)
        elif is_pos:
            uids = json.loads(uids)
            uids = uids if isinstance(uids, list) else [uids]
            return_dict = get_user_with_same_opinion_for_statements(uids, True, nickname, ui_locales, request.application_url)
        else:
            if is_att:
                return_dict = get_user_with_opinions_for_attitude(uids, nickname, ui_locales, request.application_url)
            else:
                uids = json.loads(uids)
                uids = uids if isinstance(uids, list) else [uids]
                return_dict = get_user_with_same_opinion_for_premisegroups(uids, nickname, ui_locales, request.application_url)
        return_dict['info'] = _tn.get(_.otherParticipantsDontHaveOpinionForThisStatement) if len(uids) == 0 else ''
        return_dict['error'] = ''
    except KeyError as e:
        logger('get_users_with_same_opinion', 'error', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return return_dict


# ajax - for getting all users with the same opinion
@view_config(route_name='ajax_get_public_user_data', renderer='json')
def get_public_user_data(request):
    """
    Returns dictionary with public user data

    :param request: request of the web server
    :return:
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_public_user_data', 'def', 'main: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        nickname = request.params['nickname']
        return_dict = user_manager.get_public_information_data(nickname, ui_locales)
        return_dict['error'] = '' if len(return_dict) != 0 else _tn.get(_.internalKeyError)

    except KeyError as e:
        logger('get_public_user_data', 'error', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return return_dict


@view_config(route_name='ajax_get_arguments_by_statement_uid', renderer='json')
def get_arguments_by_statement_uid(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_arguments_by_statement_uid', 'def', 'main: {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    return_dict = dict()
    try:
        uid = request.matchdict['uid']
        if not is_integer(uid):
            return_dict['error'] = _tn.get(_.internalKeyError)
        else:
            slug = get_slug_by_statement_uid(uid)
            _um = UrlManager(request.application_url, slug)
            return_dict['arguments'] = get_all_arguments_with_text_and_url_by_statement_id(uid, _um, True, is_jump=True)
            return_dict['error'] = ''

    except KeyError as e:
        logger('get_arguments_by_statement_uid', 'error', repr(e))
        return_dict['error'] = _tn.get(_.internalKeyError)

    return return_dict


@view_config(route_name='ajax_get_references', renderer='json')
def get_references(request):
    """
    Returns all references for an argument or statement


    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('get_references', 'def', 'main: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)
    data = ''
    text = ''

    try:
        # uid is an integer if it is an argument and a list otherwise
        uid = json.loads(request.params['uid'])
        is_argument = str(request.params['is_argument']) == 'true'
        are_all_integer = all(is_integer(tmp) for tmp in uid) if isinstance(uid, list) else is_integer(uid)

        error = ''
        if are_all_integer:
            if is_argument:
                data, text = get_references_for_argument(uid, request.application_url)
            else:
                data, text = get_references_for_statements(uid, request.application_url)
        else:
            logger('get_references', 'def', 'uid is not an integer')
            data = ''
            text = ''
            error = _tn.get(_.internalKeyError)

    except KeyError as e:
        logger('get_references', 'error', repr(e))
        error = _tn.get(_.internalKeyError)

    return_dict = {'error': error,
                   'data': data,
                   'text': text}

    return return_dict


@view_config(route_name='ajax_set_references', renderer='json')
def set_references(request):
    """
    Sets a reference for a statement or an arguments

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('set_references', 'def', 'main: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        nickname    = request.authenticated_userid
        issue_uid   = issue_helper.get_issue_id(request)

        uid         = request.params['uid']
        reference   = escape_string(json.loads(request.params['reference']))
        source      = escape_string(json.loads(request.params['ref_source']))
        success     = set_reference(reference, source, nickname, uid, issue_uid)
        return_dict = {'error': '' if success else _tn.get(_.internalKeyError)}

    except KeyError as e:
        logger('set_references', 'error', repr(e))
        return_dict = {'error': _tn.get(_.internalKeyError)}

    return return_dict


# ########################################
# ADDTIONAL AJAX STUFF # ADDITION THINGS #
# ########################################


# ajax - for language switch
@view_config(route_name='ajax_switch_language', renderer='json')
def switch_language(request):
    """
    Switches the language

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    user_manager.update_last_action(request.authenticated_userid)
    logger('switch_language', 'def', 'request.params: {}'.format(request.params))

    return_dict = set_language(request)

    return return_dict


# ajax - for sending news
@view_config(route_name='ajax_send_news', renderer='json')
def send_news(request):
    """
    ajax interface for settings news

    :param request: current request of the server
    :return: json-set with new news
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'send_news', 'request.params: {}'.format(request.params))
    _tn = Translator(get_language_from_cookie(request))

    try:
        return_dict, success = news_handler.set_news(request)
        return_dict['error'] = '' if success else _tn.get(_.noRights)
    except KeyError as e:
        return_dict = dict()
        logger('views', 'send_news', repr(e), error=True)
        return_dict['error'] = _tn.get(_.internalKeyError)

    return return_dict


# ajax - for fuzzy search
@view_config(route_name='ajax_fuzzy_search', renderer='json')
def fuzzy_search(request, for_api=False, api_data=None):
    """
    ajax interface for fuzzy string search

    :param request: request of the web server
    :param for_api: boolean
    :param api_data: data
    :return: json-set with all matched strings
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('fuzzy_search', 'def', 'for_api: {}, request.params: {}'.format(for_api, request.params))

    _tn = Translator(get_language_from_cookie(request))
    request_authenticated_userid = request.authenticated_userid

    try:
        mode = str(api_data['mode']) if for_api else str(request.params['type'])
        value = api_data['value'] if for_api else request.params['value']
        issue = api_data['issue'] if for_api else issue_helper.get_issue_id(request)
        extra = request.params['extra'] if 'extra' in request.params else None

        return_dict = fuzzy_string_matcher.get_prediction(request, _tn, for_api, api_data, request_authenticated_userid, value, mode, issue, extra)

    except KeyError as e:
        return_dict = {'error': _tn.get(_.internalKeyError)}
        logger('fuzzy_search', 'error', repr(e))

    return return_dict


# ajax - for additional service
@view_config(route_name='ajax_additional_service', renderer='json')
def additional_service(request):
    """
    Easteregg O:-)

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'additional_service', 'request.params: {}'.format(request.params))

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


# ajax - for flagging arguments
@view_config(route_name='ajax_flag_argument_or_statement', renderer='json')
def flag_argument_or_statement(request):
    """
    Flags an argument or statement for a specific reason

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'flag_argument_or_statement', 'request.params: {}'.format(request.params))
    ui_locales = get_discussion_language(request)

    try:
        uid = request.params['uid']
        reason = request.params['reason']
        extra_uid = request.params['extra_uid'] if 'extra_uid' in request.params else None
        is_argument = True if request.params['is_argument'] == 'true' else False
        nickname = request.authenticated_userid

        prepared_dict = add.flag_argument_or_statement(uid, reason, extra_uid, is_argument, nickname, ui_locales)
    except KeyError as e:
        _t = Translator(ui_locales)
        logger('views', 'flag_argument_or_statement', repr(e), error=True)
        prepared_dict = {'error': _t.get(_.internalKeyError), 'info': '', 'success': ''}

    return json.dumps(prepared_dict)


# ajax - for feedback on flagged arguments
@view_config(route_name='ajax_review_delete_argument', renderer='json')
def review_delete_argument(request):
    """
    Values for the review for an argument, which should be deleted

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'review_delete_argument', 'main: {}'.format(request.params))

    try:
        prepared_dict = add.review_delete_argument(request)
    except KeyError as e:
        logger('views', 'review_delete_argument', repr(e), error=True)
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for feedback on flagged arguments
@view_config(route_name='ajax_review_edit_argument', renderer='json')
def review_edit_argument(request):
    """
    Values for the review for an argument, which should be edited

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('view', 'review_edit_argument', 'main: {} - {}'.format(request.params, request.authenticated_userid))

    try:
        prepared_dict = add.review_edit_argument(request)
    except KeyError as e:
        logger('view', 'review_edit_argument', repr(e), error=True)
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for feedback on duplicated statements
@view_config(route_name='ajax_review_duplicate_statement', renderer='json')
def review_duplicate_statement(request):
    """
    Values for the review for an argument, which is maybe a duplicate

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('view', 'review_duplicate_statement', 'main: {} - {}'.format(request.params, request.authenticated_userid))
    try:
        prepared_dict = add.review_duplicate_statement(request)
    except KeyError as e:
        logger('view', 'review_duplicate_statement', repr(e), error=True)
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for feedback on optimization arguments
@view_config(route_name='ajax_review_optimization_argument', renderer='json')
def review_optimization_argument(request):
    """
    Values for the review for an argument, which should be optimized

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'review_optimization_argument', 'main: {}'.format(request.params))

    try:
        prepared_dict = add.review_optimization_argument(request)
    except KeyError as e:
        logger('view', 'review_optimization_argument', repr(e), error=True)
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for undoing reviews
@view_config(route_name='ajax_undo_review', renderer='json')
def undo_review(request):
    """
    Trys to undo a done review process

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'undo_review', 'main: {}'.format(request.params))

    try:
        prepared_dict = add.undo_review(request)
    except KeyError as e:
        logger('views', 'undo_review', repr(e), error=True)
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for canceling reviews
@view_config(route_name='ajax_cancel_review', renderer='json')
def cancel_review(request):
    """
    Trys to cancel an ongoing review

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'cancel_review', 'main: {}'.format(request.params))

    try:
        prepared_dict = add.cancel_review(request)
    except KeyError as e:
        logger('views', 'cancel_review', repr(e), error=True)
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for undoing reviews
@view_config(route_name='ajax_review_lock', renderer='json', require_csrf=False)
def review_lock(request):
    """
    Locks a review so that the user can do an edit

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'review_lock', 'main: {}'.format(request.params))

    try:
        prepared_dict = add.review_lock(request)

    except KeyError as e:
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        logger('views', 'review_lock', repr(e), error=True)
        prepared_dict = {'info': '', 'error': _t.get(_.internalKeyError), 'success': '', 'is_locked': False}

    return json.dumps(prepared_dict)


# ajax - for revoking content
@view_config(route_name='ajax_revoke_content', renderer='json', require_csrf=False)
def revoke_some_content(request):
    """
    Revokes the given user as author from a statement or an argument

    :param request: current request of the server
    :return: json-dict()
    """
    #  logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('views', 'revoke_some_content', 'main: {}'.format(request.params))

    try:
        prepared_dict = add.review_lock(request)

    except KeyError as e:
        ui_locales = get_discussion_language(request)
        _t = Translator(ui_locales)
        logger('views', 'revoke_some_content', repr(e), error=True)
        prepared_dict = {'success': False, 'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)
