"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import graphene
import json
import requests
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import get_renderer
from pyramid.security import forget
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid_mailer import get_mailer
from typing import Callable, Any
from webob_graphql import serve_graphql_request
from zope.interface.interfaces import ComponentLookupError

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
import dbas.handler.issue as issue_handler
import dbas.handler.news as news_handler
import dbas.review.helper.core as review
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.queues as review_queue_helper
import dbas.review.helper.reputation as review_reputation_helper
import dbas.review.helper.subpage as review_page_helper
import dbas.strings.matcher as fuzzy_string_matcher
from api.v2.graphql.core import Query
from dbas.auth.login import login_user, login_user_oauth, register_user_with_ajax_data, oauth_providers
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Group
from dbas.database.discussion_model import User, Issue
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.handler import user
from dbas.handler.arguments import set_arguments_premises, get_all_infos_about_argument, get_arguments_by_statement_uid
from dbas.handler.issue import get_issues_overiew, set_discussions_properties
from dbas.handler.language import set_language, set_language_for_visit, get_language_from_cookie
from dbas.handler.notification import read_notifications, delete_notifications, send_users_notification
from dbas.handler.password import request_password
from dbas.handler.references import set_reference, get_references
from dbas.handler.rss import get_list_of_all_feeds
from dbas.handler.settings import set_settings
from dbas.handler.statements import set_correction_of_statement, set_position, set_positions_premise, \
    set_seen_statements, get_logfile_for_statements
from dbas.handler.voting import clear_vote_and_seen_values_of_user
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.query import get_default_locale_name, set_user_language, \
    mark_statement_or_argument, get_short_url
from dbas.helper.validation import validate, valid_user, valid_issue, valid_conclusion, \
<<<<<<< HEAD
    has_keywords, valid_issue_not_readonly
=======
    has_keywords
>>>>>>> Refactor set_new_start_premise
from dbas.helper.views import preparation_for_view
from dbas.input_validator import is_integer
from dbas.lib import escape_string, get_discussion_language, get_changelog, is_user_author_or_admin
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import get_port

name = 'D-BAS'
version = '1.5.5'
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
    session_expired = user.update_last_action(request.authenticated_userid)
    if session_expired:
        return user_logout(request, True)


def prepare_request_dict(request, nickname, for_api=False):
    """

    :param request:
    :param nickname:
    :return:
    """

    last_topic = history_handler.get_saved_issue(nickname)

    slug = ''
    if 'slug' in request.matchdict:
        slug = request.matchdict['slug']
        if not isinstance(request.matchdict['slug'], str) and len(request.matchdict['slug']) > 0:
            slug = request.matchdict['slug'][0]

    if len(slug) == 0 and last_topic != 0:
        issue = last_topic
    elif len(slug) > 0:
        issue = issue_handler.get_id_of_slug(slug, request, True, for_api)
    else:
        issue = issue_handler.get_issue_id(request)

    ui_locales = get_language_from_cookie(request)
    if issue == -1 and for_api:
        logger('Views', 'prepare_request_dict', 'Slug error ({}) for api'.format(slug), error=True)
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.maliciousAntiSpam)}

    if len(slug) == 0:
        slug = DBDiscussionSession.query(Issue).get(issue).slug

    history = history_handler.handle_history(request, nickname, slug, issue)
    disc_ui_locales = get_discussion_language(request.matchdict, request.params, request.session, issue)
    set_language_for_visit(request)

    request_dict = {
        'nickname': nickname,
        'path': request.path,
        'app_url': request.application_url,
        'matchdict': request.matchdict,
        'params': request.params,
        'session': request.session,
        'registry': request.registry,
        'issue': issue,
        'slug': slug,
        'history': history,
        'ui_locales': ui_locales,
        'disc_ui_locales': disc_ui_locales,
        'last_topic': last_topic,
        'port': get_port(request)
    }
    return request_dict


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

    request_dict = prepare_request_dict(request, nickname)
    ui_locales = get_language_from_cookie(request)

    prepared_discussion = f(request_dict, for_api)
    if prepared_discussion:
        prepared_discussion['layout'] = base_layout()
        prepared_discussion['language'] = str(ui_locales)

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
    logger('main_page', 'def', 'request.params: {}'.format(request.params))

    set_language_for_visit(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    session_expired = 'session_expired' in request.params and request.params['session_expired'] == 'true'
    ui_locales = get_language_from_cookie(request)
    logger('main_page', 'def', 'request.params: {}'.format(request.params))
    _dh = DictionaryHelper(ui_locales, ui_locales)
    extras_dict = _dh.prepare_extras_dict_for_normal_page(request.registry, request.application_url, request.path,
                                                          request.authenticated_userid)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': name + ' ' + full_version,
        'project': project_name,
        'extras': extras_dict,
        'session_expired': session_expired,
        'news': news_handler.get_latest_news(ui_locales)
    }


# settings page, when logged in
@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
def main_settings(request):
    """
    View configuration for the personal settings view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_settings', 'def', 'request.params: {}'.format(request.params))
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    ui_locales = get_language_from_cookie(request)
    old_pw, new_pw, confirm_pw, message = '', '', '', ''
    success, error = False, False
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(request.authenticated_userid)).join(Group).first()
    _uh = user
    _t = Translator(ui_locales)

    if not db_user:
        raise HTTPNotFound()

    if db_user and 'form.passwordchange.submitted' in request.params:
        old_pw = escape_string(request.params['passwordold'])
        new_pw = escape_string(request.params['password'])
        confirm_pw = escape_string(request.params['passwordconfirm'])

        message, success = _uh.change_password(db_user, old_pw, new_pw, confirm_pw, ui_locales)
        error = not success

    _dh = DictionaryHelper(ui_locales)
    extras_dict = _dh.prepare_extras_dict_for_normal_page(request.registry, request.application_url, request.path,
                                                          request.authenticated_userid)
    settings_dict = _dh.prepare_settings_dict(success, old_pw, new_pw, confirm_pw, error, message, db_user,
                                              request.application_url, extras_dict['use_with_ldap'])

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
    logger('main_notifications', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid,
                                                                                   append_notifications=True)

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
    logger('main_news', 'def', 'main')
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    ui_locales = get_language_from_cookie(request)
    is_author = is_user_author_or_admin(request.authenticated_userid)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

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
    match_dict = request.matchdict
    params = request.params
    logger('main_user', 'def', 'request.matchdict: {}'.format(match_dict))
    logger('main_user', 'def', 'request.params: {}'.format(params))

    uid = match_dict.get('uid', 0)
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
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

    user_dict = user.get_information_of(current_user, ui_locales)

    db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    logger('X', 'X', request.authenticated_userid)
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
    logger('main_imprint', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    _tn = Translator(ui_locales)

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

    # add version of pyramid
    import pkg_resources
    extras_dict.update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

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
    logger('main_faq', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'FAQ',
        'project': project_name,
        'extras': extras_dict
    }


# fieldtest
@view_config(route_name='main_experiment', renderer='templates/fieldtest.pt', permission='everybody')
def main_experiment(request):
    """
    View configuration for fieldtest.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_experiment', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': Translator(ui_locales).get(_.fieldtest),
        'project': project_name,
        'extras': extras_dict
    }


# my discussions
@view_config(route_name='main_mydiscussions', renderer='templates/discussions.pt', permission='use')
def main_mydiscussions(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_mydiscussions', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)
    issue_dict = get_issues_overiew(request.authenticated_userid, request.application_url)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': Translator(ui_locales).get(_.myDiscussions),
        'project': project_name,
        'extras': extras_dict,
        'issues': issue_dict
    }


# docs
@view_config(route_name='main_docs', renderer='templates/docs.pt', permission='everybody')
def main_docs(request):
    """
    View configuration for the documentation.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_docs', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': _tn.get(_.docs),
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
    logger('main_rss', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)
    rss = get_list_of_all_feeds(ui_locales)

    return {
        'layout': base_layout(),
        'language': str(ui_locales),
        'title': 'RSS',
        'project': project_name,
        'extras': extras_dict,
        'rss': rss
    }


# graphiql
@view_config(route_name='main_graphiql', permission='everybody', require_csrf=False)
def main_graphiql(request):
    """
    View configuration for GraphiQL.

    :param request: current request of the server
    :return: graphql
    """
    logger('main_graphiql', 'def', 'main')
    schema = graphene.Schema(query=Query)
    context = {'session': DBDiscussionSession}
    return serve_graphql_request(request, schema, batch_enabled=True, context_value=context)


# 404 page
@notfound_view_config(renderer='templates/404.pt')
def notfound(request):
    """
    View configuration for the 404 page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    if request.path.startswith('/api'):
        return HTTPNotFound({
            'path': request.path,
            'message': 'Not Found'
        })

    user.update_last_action(request.authenticated_userid)
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

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

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

    # redirect to oauth url after login and redirecting
    if request.authenticated_userid and 'service' in request.params and request.params['service'] in oauth_providers:
        url = request.session['oauth_redirect_url']
        return HTTPFound(location=url)

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
    match_dict = request.matchdict
    params = request.params
    logger('views', 'discussion.finish', 'request.matchdict: {}'.format(match_dict))
    logger('views', 'discussion.finish', 'request.params: {}'.format(params))

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    request_dict = {
        'registry': request.registry,
        'app_url': request.application_url,
        'nickname': request.authenticated_userid,
        'path': request.path,
        'ui_locales': get_language_from_cookie(request)
    }

    prepared_discussion = discussion.finish(request_dict)
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
    logger('main_review', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    nickname = request.authenticated_userid
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    issue = issue_handler.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request.matchdict, request.params, request.session, issue)

    issue_dict = issue_handler.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, False,
                                                     request.authenticated_userid)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

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
    logger('review_content', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    subpage_name = request.matchdict['queue']
    nickname = request.authenticated_userid
    session = request.session
    application_url = request.application_url
    subpage_dict = review_page_helper.get_subpage_elements_for(nickname, session, application_url, subpage_name, _tn)
    request.session.update(subpage_dict['session'])
    if not subpage_dict['elements'] and not subpage_dict['has_access'] and not subpage_dict['no_arguments_to_review']:
        logger('review_content', 'def', 'subpage error', error=True)
        raise HTTPNotFound()

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

    title = _tn.get(_.review)
    if subpage_name in review_queue_helper.title_mapping:
        title = review_queue_helper.title_mapping[subpage_name]

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
    logger('review_history', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    request_authenticated_userid = request.authenticated_userid
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    history = review_history_helper.get_review_history(request.application_url, request_authenticated_userid, _tn)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)
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
    logger('ongoing_history', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    history = review_history_helper.get_ongoing_reviews(request.application_url, request.authenticated_userid, _tn)
    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

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
    logger('review_reputation', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    unauthenticated = check_authentication(request)
    if unauthenticated:
        return unauthenticated

    extras_dict = DictionaryHelper(ui_locales).prepare_extras_dict_for_normal_page(request.registry,
                                                                                   request.application_url,
                                                                                   request.path,
                                                                                   request.authenticated_userid)

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
    user.update_last_action(userid)
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
    ui_locales = get_language_from_cookie(request)
    return history_handler.get_history_from_database(request.authenticated_userid, ui_locales)


# ajax - getting all text edits
@view_config(route_name='ajax_get_all_posted_statements', renderer='json')
def get_all_posted_statements(request):
    """
    Request for all statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    return_array, _ = user.get_textversions(request.authenticated_userid, ui_locales)
    return return_array


# ajax - getting all text edits
@view_config(route_name='ajax_get_all_edits', renderer='json')
def get_all_edits_of_user(request):
    """
    Request for all edits of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    _, return_array = user.get_textversions(request.authenticated_userid, ui_locales)
    return return_array


# ajax - getting all votes for arguments
@view_config(route_name='ajax_get_all_marked_arguments', renderer='json')
def get_all_marked_arguments(request):
    """
    Request for all marked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    return user.get_marked_elements_of_user(request.authenticated_userid, True, ui_locales)


# ajax - getting all votes for statements
@view_config(route_name='ajax_get_all_marked_statements', renderer='json')
def get_all_marked_statements(request):
    """
    Request for all marked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    return user.get_marked_elements_of_user(request.authenticated_userid, False, ui_locales)


# ajax - getting all votes for arguments
@view_config(route_name='ajax_get_all_argument_clicks', renderer='json')
def get_all_argument_clicks(request):
    """
    Request for all clicked arguments of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    return user.get_arg_clicks_of_user(request.authenticated_userid, ui_locales)


# ajax - getting all votes for statements
@view_config(route_name='ajax_get_all_statement_clicks', renderer='json')
def get_all_statement_clicks(request):
    """
    Request for all clicked statements of the user

    :param request: current request of the server
    :return: json-dict()
    """
    ui_locales = get_language_from_cookie(request)
    return user.get_stmt_clicks_of_user(request.authenticated_userid, ui_locales)


# ajax - deleting complete history of the user
@view_config(route_name='ajax_delete_user_history', renderer='json')
def delete_user_history(request):
    """
    Request to delete the users history.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_user_history', 'def', 'main')
    user.update_last_action(request.authenticated_userid)
    return {'removed_data': str(history_handler.delete_history_in_database(request.authenticated_userid)).lower()}


# ajax - deleting complete history of the user
@view_config(route_name='ajax_delete_statistics', renderer='json')
def delete_statistics(request):
    """
    Request to delete votes/clicks of the user.

    :param request: request of the web server
    :return: json-dict()
    """
    logger('delete_statistics', 'def', 'main')
    user.update_last_action(request.authenticated_userid)
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
    logger('views', 'user_login', 'request.params: {} (api: {})'.format(request.params, str(for_api)))

    lang = get_language_from_cookie(request)

    try:
        return login_user(request, nickname, password, for_api, keep_login, lang)
    except KeyError as e:
        logger('user_login', 'error', repr(e), error=True)
        _tn = Translator(lang)
        return {'error': _tn.get(_.internalKeyError)}


# ajax - user login via oauth
@view_config(route_name='ajax_user_login_oauth', renderer='json')
def user_login_oauth(request):
    """
    Will login the user via oauth

    :return: dict() with error
    """
    logger('views', 'user_login_oauth', 'request.params: {}'.format(request.params))

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


# ajax - user logout
@view_config(route_name='ajax_user_logout', renderer='json')
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


# ajax - registration of users
@view_config(route_name='ajax_user_registration', renderer='json')
def user_registration(request):
    """
    Registers new user with data given in the ajax requesst

    :param request: current request of the server
    :return: dict() with success and message
    """
    logger('Views', 'user_registration', 'request.params: {}'.format(request.params))

    # default values
    success = ''
    error = ''
    info = ''

    try:
        params = request.params
        ui_locales = params['lang'] if 'lang' in params else get_language_from_cookie(request)
        mailer = get_mailer(request)
        success, info, new_user = register_user_with_ajax_data(params, ui_locales, mailer)

    except KeyError as e:
        logger('Views', 'user_registration', repr(e), error=True)
        ui_locales = request.params.get('lang', get_language_from_cookie(request))
        _t = Translator(ui_locales)
        error = _t.get(_.internalKeyError)

    return {
        'success': str(success),
        'error': str(error),
        'info': str(info)
    }


# ajax - password requests
@view_config(route_name='ajax_user_password_request', renderer='json')
def user_password_request(request):
    """
    Sends an email, when the user requests his password

    :param request: current request of the server
    :return: dict() with success and message
    """
    logger('Views', 'user_password_request', 'request.params: {}'.format(request.params))

    success = ''
    info = ''
    ui_locales = request.params['lang'] if 'lang' in request.params else get_language_from_cookie(request)
    _t = Translator(ui_locales)

    try:
        success, error, info = request_password(request)

    except KeyError as e:
        logger('iew', 'user_password_request', repr(e), error=True)
        error = _t.get(_.internalKeyError)

    return_dict = {
        'success': str(success),
        'error': str(error),
        'info': str(info)
    }

    return return_dict


# ajax - set boolean for receiving information
@view_config(route_name='ajax_set_user_setting', renderer='json')
def set_user_settings(request):
    """
    Sets a specific setting of the user

    :param request: current request of the server
    :return: json-dict()
    """
    logger('Views', 'set_user_settings', 'request.params: {}'.format(request.params))
    _tn = Translator(get_language_from_cookie(request))

    settings_value = request.params.get('settings_value') == 'True'
    service = request.params.get('service')
    return_dict = set_settings(request.application_url, request.authenticated_userid, service, settings_value, _tn)
    return return_dict


# ajax - set boolean for receiving information
@view_config(route_name='ajax_set_user_language', renderer='json')
def set_user_lang(request):
    """
    Will logout the user

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_user_lang', 'request.params: {}'.format(request.params))

    try:
        ui_locales = request.params.get('ui_locales', None)
        prepared_dict = set_user_language(request.authenticated_userid, ui_locales)
    except KeyError as e:
        logger('views', 'set_user_lang', repr(e), error=True)
        _tn = Translator(get_language_from_cookie(request))
        prepared_dict = {
            'error': _tn.get(_.internalKeyError),
            'ui_locales': '',
            'current_lang': ''
        }
    return prepared_dict


# ajax - sending notification
@view_config(route_name='ajax_send_notification', renderer='json')
def send_some_notification(request):
    """
    Set a new message into the inbox of an recipient, and the outbox of the sender.

    :param request: current request of the server
    :return: dict()
    """
    logger('views', 'send_some_notification', 'request.params: {}'.format(request.params))

    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        recipient = str(request.params['recipient']).replace('%20', ' ')
        title = request.params['title']
        text = request.params['text']
    except KeyError as e:
        logger('views', 'send_some_notification', repr(e), error=True)
        prepared_dict = {'error': _tn.get(_.internalKeyError), 'timestamp': '', 'uid': '', 'recipient_avatar': ''}
        return prepared_dict

    prepared_dict = send_users_notification(get_port(request), recipient, title, text, request.authenticated_userid,
                                            ui_locales)

    return prepared_dict


# ajax - set boolean for receiving information
@view_config(route_name='ajax_set_discussion_properties', renderer='json')
def set_discussion_properties(request):
    """
    Sets the discussions availability

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_discussion_properties', 'request.params: {}'.format(request.params))
    _tn = Translator(get_language_from_cookie(request))

    try:
        checked = request.params['checked'] == 'True'
        uid = request.params['uid']
        key = request.params['key']
        prepared_dict = set_discussions_properties(request.authenticated_userid, uid, checked, key, _tn)
    except KeyError as e:
        logger('views', 'set_discussion_properties', repr(e), error=True)
        prepared_dict = {
            'error': _tn.get(_.internalKeyError)
        }
    return prepared_dict


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################

@validate(valid_user, valid_issue)
@view_config(route_name='ajax_set_new_start_argument', renderer='json')
@validate(valid_user, valid_issue_not_readonly, has_keywords('position', 'reason'))
def set_new_start_argument(request):
    """
    Inserts a new argument as starting point into the database

    :param request: request of the web server
    :return: a status code, if everything was successful
    """
    logger('views', 'set_new_start_argument', 'request.params: {}'.format(request.params))

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
    }

    try:
        data['mailer'] = get_mailer(request)
    except ComponentLookupError as e:
        logger('views', 'set_new_start_argument', repr(e), error=True)

    # set the new position
    logger('views', 'set_new_start_argument', 'set conclusion/position')
    prepared_dict_pos = set_position(False, data)
    if len(prepared_dict_pos['error']) is 0:
        logger('views', 'set_new_start_argument', 'set premise/reason')
        # set the premise
        data['premisegroup'] = [reason]
        data['conclusion_id'] = prepared_dict_pos['statement_uids'][0]
        prepared_dict_reas = set_positions_premise(False, data)
        return prepared_dict_reas

    return prepared_dict_pos


# ajax - send new start premise
@view_config(route_name='ajax_set_new_start_premise', renderer='json')
@validate(valid_user, valid_issue, valid_conclusion,
          has_keywords('premisegroup', 'supportive'))
def set_new_start_premise(request):
    """
    Sets new premise for the start

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'set_new_start_premise', 'request.params: {}'.format(request.params))
    data = {
        'user': request.validated['user'],
        'application_url': request.application_url,
        'issue': request.validated['issue'],
        'premisegroup': request.validated['premisegroup'],
        'conclusion': request.validated['conclusion'],
        'supportive': request.validated['supportive'],
        'port': get_port(request),
        'history': request.cookies.get('_HISTORY_'),
        'default_locale_name': get_default_locale_name(request.registry)
    }

    # TODO Is this a configuration or a runtime error? -> Fix it everywhere! Don't catch errors!
    try:
        data['mailer'] = get_mailer(request)
    except ComponentLookupError as e:
        logger('views', 'set_new_start_premise', repr(e), error=True)

    prepared_dict = set_positions_premise(False, data)
    return prepared_dict


# ajax - send new premises
@view_config(route_name='ajax_set_new_premises_for_argument', renderer='json')
def set_new_premises_for_argument(request):
    """
    Sets a new premise for an argument

    :param request: request of the web server
    :return: json-dict()
    """
    logger('views', 'set_new_premises_for_argument', 'request.params: {}'.format(request.params))
    lang = get_discussion_language(request.matchdict, request.params, request.session)
    _tn = Translator(lang)
    data = {}
    try:
        data['nickname'] = request.authenticated_userid
        data['statement'] = json.loads(request.params['premisegroups'])
        data['issue_id'] = issue_handler.get_issue_id(request)
        data['issue'] = DBDiscussionSession.query(Issue).get(data['issue_id'])
        data['arg_uid'] = request.params['arg_uid']
        data['attack_type'] = request.params['attack_type']
        data['port'] = get_port(request)
        data['history'] = request.cookies['_HISTORY_'] if '_HISTORY_' in request.cookies else None
        data['discussion_lang'] = get_discussion_language(request.matchdict, request.params, request.session)
        data['default_locale_name'] = get_default_locale_name(request.registry)
        data['application_url'] = request.application_url
        try:
            data['mailer'] = get_mailer(request)
        except ComponentLookupError as e:
            logger('views', 'set_new_premises_for_argument', repr(e), error=True)
    except KeyError as e:
        logger('views', 'set_new_premises_for_argument', repr(e), error=True)
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    prepared_dict = set_arguments_premises(False, data)
    return prepared_dict


# ajax - set new textvalue for a statement
@view_config(route_name='ajax_set_correction_of_statement', renderer='json')
def set_correction_of_some_statements(request):
    """
    Sets a new textvalue for a statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_correction_of_some_statements', 'request.params: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        elements = json.loads(request.params['elements'])
    except KeyError as e:
        logger('views', 'set_correction_of_some_statements', repr(e), error=True)
        return {'error': _tn.get(_.internalError), 'info': ''}

    prepared_dict = set_correction_of_statement(elements, request.authenticated_userid, ui_locales)
    return prepared_dict


# ajax - set notifications as read
@view_config(route_name='ajax_notifications_read', renderer='json')
def set_notifications_read(request):
    """
    Set a notification as read

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_notifications_read', 'main {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)

    try:
        uids_list = json.loads(request.params['ids'])
    except KeyError as e:
        logger('views', 'set_notifications_read', repr(e), error=True)
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError), 'success': ''}

    prepared_dict = read_notifications(uids_list, request.authenticated_userid, ui_locales)
    return prepared_dict


# ajax - deletes notifications
@view_config(route_name='ajax_notifications_delete', renderer='json')
def set_notifications_delete(request):
    """
    Request the removal of a notification

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_notifications_delete', 'main {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)

    try:
        uids_list = json.loads(request.params['ids'])
    except KeyError as e:
        logger('views', 'set_notifications_delete', repr(e), error=True)
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError), 'success': ''}

    prepared_dict = delete_notifications(uids_list, request.authenticated_userid, ui_locales, request.application_url)
    return prepared_dict


# ajax - set new issue
@view_config(route_name='ajax_set_new_issue', renderer='json')
def set_new_issue(request):
    """

    :param request: current request of the server
    :return:
    """
    logger('views', 'set_new_issue', 'main {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)

    try:
        info = escape_string(request.params['info'])
        long_info = escape_string(request.params['long_info'])
        title = escape_string(request.params['title'])
        lang = escape_string(request.params['lang'])
        is_public = request.params['is_public'] == 'True'
        is_read_only = request.params['is_read_only'] == 'True'
    except KeyError as e:
        _tn = Translator(ui_locales)
        logger('views', 'set_new_issue', repr(e), error=True)
        return {'error': _tn.get(_.notInsertedErrorBecauseInternal)}

    prepared_dict = issue_handler.set_issue(request.authenticated_userid, info, long_info, title, lang, is_public,
                                            is_read_only, request.application_url, ui_locales)
    return prepared_dict


# ajax - set seen premisegroup
@view_config(route_name='ajax_set_seen_statements', renderer='json')
def set_statements_as_seen(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'set_statements_as_seen', 'main {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        uids = json.loads(request.params['uids'])
    except KeyError as e:
        logger('views', 'set_statements_as_seen', repr(e), error=True)
        return {'error': _tn.get(_.internalKeyError)}

    prepared_dict = set_seen_statements(uids, request.path, request.authenticated_userid, ui_locales)
    return prepared_dict


# ajax - set users opinion
@view_config(route_name='ajax_mark_statement_or_argument', renderer='json')
def mark_or_unmark_statement_or_argument(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'mark_or_unmark_statement_or_argument', 'main {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)

    try:
        uid = request.params['uid']
        step = request.params['step']
        is_argument = str(request.params['is_argument']).lower() == 'true'
        is_supportive = str(request.params['is_supportive']).lower() == 'true'
        should_mark = str(request.params['should_mark']).lower() == 'true'
        history = request.params.get('history', '')
    except KeyError as e:
        logger('views', 'mark_or_unmark_statement_or_argument', repr(e), error=True)
        _t = Translator(ui_locales)
        return {'succes': '', 'text': '', 'error': _t.get(_.internalKeyError)}

    prepared_dict = mark_statement_or_argument(uid, step, is_argument, is_supportive, should_mark, history, ui_locales,
                                               request.authenticated_userid)
    return prepared_dict


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
    logger('views', 'get_logfile_for_statements', 'request.params: {}'.format(request.params))

    try:
        uids = json.loads(request.params['uids'])
        issue = request.params['issue']
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session, issue)
        prepared_dict = get_logfile_for_statements(uids, ui_locales, request.application_url)
        prepared_dict['error'] = ''
    except KeyError as e:
        logger('views', 'get_logfile_for_statements', repr(e), error=True)
        _tn = Translator(get_discussion_language(request.matchdict, request.params, request.session))
        prepared_dict = {'error': _tn.get(_.noCorrections)}

    return prepared_dict


# ajax - for shorten url
@view_config(route_name='ajax_get_shortened_url', renderer='json')
def get_shortened_url(request):
    """
    Shortens url with the help of a python lib

    :param request: current request of the server
    :return: dictionary with shortend url
    """
    logger('views', 'get_shortened_url', 'main')
    try:
        url = request.params['url']
        prepared_dict = get_short_url(url, request.unauthenticated_userid, get_discussion_language(request.matchdict,
                                                                                                   request.params,
                                                                                                   request.session))
    except KeyError as e:
        logger('views', 'get_shortened_url', repr(e), error=True)
        _tn = Translator(get_discussion_language(request.matchdict, request.params, request.session))
        return {'error': _tn.get(_.internalKeyError)}

    return prepared_dict


# ajax - for getting all news
@view_config(route_name='ajax_get_news', renderer='json')
def get_news(request):
    """
    ajax interface for getting news

    :param request: current request of the server
    :return: json-set with all news
    """
    logger('views', 'get_news', 'main')
    return news_handler.get_news(get_language_from_cookie(request))


# ajax - for getting argument infos
@view_config(route_name='ajax_get_infos_about_argument', renderer='json')
def get_infos_about_argument(request):
    """
    ajax interface for getting a dump

    :param request: current request of the server
    :return: json-set with everything
    """
    logger('views', 'get_infos_about_argument', 'request.params: {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)

    try:
        uid = request.params['uid']
    except KeyError as e:
        logger('views', 'get_infos_about_argument', repr(e), error=True)
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError)}

    prepared_dict = get_all_infos_about_argument(uid, request.application_url, request.authenticated_userid, ui_locales)
    return prepared_dict


# ajax - for getting all users with the same opinion
@view_config(route_name='ajax_get_user_with_same_opinion', renderer='json')
def get_users_with_opinion(request):
    """
    ajax interface for getting a dump

    :params reqeust: current request of the web  server
    :return: json-set with everything
    """
    logger('views', 'get_users_with_opinion', 'main: {}'.format(request.params))

    try:
        params = request.params
        ui_locales = params['lang'] if 'lang' in params else 'en'
        uids = params['uids']
        is_arg = params.get('is_argument') == 'true'
        is_att = params.get('is_attitude') == 'true'
        is_rea = params.get('is_reaction') == 'true'
        is_pos = params.get('is_position') == 'true'
    except KeyError as e:
        logger('views', 'get_users_with_opinion', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError)}

    path = request.path
    application_url = request.application_url
    nickname = request.authenticated_userid
    prepared_dict = user.get_users_with_same_opinion(uids, application_url, path, nickname, is_arg, is_att, is_rea,
                                                     is_pos, ui_locales)
    return prepared_dict


# ajax - for getting all users with the same opinion
@view_config(route_name='ajax_get_public_user_data', renderer='json')
def get_public_user_data(request):
    """
    Returns dictionary with public user data

    :param request: request of the web server
    :return:
    """
    logger('views', 'get_public_user_data', 'main: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        nickname = request.params['nickname']
    except KeyError as e:
        logger('views', 'get_public_user_data', repr(e), error=True)
        return {'error': _tn.get(_.internalKeyError)}

    prepared_dict = user.get_public_data(nickname, ui_locales)
    prepared_dict['error'] = '' if len(prepared_dict) != 0 else _tn.get(_.internalKeyError)

    return prepared_dict


@view_config(route_name='ajax_get_arguments_by_statement_uid', renderer='json')
def get_arguments_by_statement_id(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'get_arguments_by_statement_id', 'main: {}'.format(request.matchdict))

    ui_locales = get_language_from_cookie(request)
    try:
        uid = request.matchdict['uid']

    except KeyError as e:
        logger('views', 'get_arguments_by_statement_uid', repr(e), error=True)
        _tn = Translator(ui_locales)
        return {'error': _tn.get(_.internalKeyError)}

    prepared_dict = get_arguments_by_statement_uid(uid, request.application_url, ui_locales)
    return prepared_dict


@view_config(route_name='ajax_get_references', renderer='json')
def get_reference(request):
    """
    Returns all references for an argument or statement


    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'get_reference', 'main: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    try:
        # uid is an integer if it is an argument and a list otherwise
        uids = json.loads(request.params['uid'])
        is_argument = str(request.params['is_argument']) == 'true'
        are_all_integer = all(is_integer(tmp) for tmp in uids) if isinstance(uids, list) else is_integer(uids)

        if not are_all_integer:
            logger('views', 'get_reference', 'uid is not an integer', error=True)
            return {'data': '', 'text': '', 'error': _tn.get(_.internalKeyError)}

    except KeyError as e:
        logger('views', 'get_reference', repr(e), error=True)
        return {'data': '', 'text': '', 'error': _tn.get(_.internalKeyError)}

    prepared_dict = get_references(uids, is_argument, request.application_url)
    return prepared_dict


@view_config(route_name='ajax_set_references', renderer='json')
def set_references(request):
    """
    Sets a reference for a statement or an arguments

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_references', 'main: {}'.format(request.params))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)
    issue_uid = issue_handler.get_issue_id(request)

    try:
        uid = request.params['uid']
        reference = escape_string(json.loads(request.params['reference']))
        source = escape_string(json.loads(request.params['ref_source']))
    except KeyError as e:
        logger('views', 'set_references', repr(e), error=True)
        prepared_dict = {'error': _tn.get(_.internalKeyError)}
        return prepared_dict

    success = set_reference(reference, source, request.authenticated_userid, uid, issue_uid)
    prepared_dict = {'error': '' if success else _tn.get(_.internalKeyError)}

    return prepared_dict


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
    user.update_last_action(request.authenticated_userid)
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
    logger('views', 'fuzzy_search', 'for_api: {}, request.params: {}'.format(for_api, request.params))

    _tn = Translator(get_language_from_cookie(request))
    request_authenticated_userid = request.authenticated_userid

    try:
        mode = str(api_data['mode']) if for_api else str(request.params['type'])
        value = api_data['value'] if for_api else request.params['value']
        issue = api_data['issue'] if for_api else issue_handler.get_issue_id(request)
        extra = request.params.get('extra')
    except KeyError as e:
        logger('views', 'fuzzy_search', repr(e), error=True)
        return {'error': _tn.get(_.internalKeyError)}

    issue_uid = issue_handler.get_issue_id(request)
    return_dict = fuzzy_string_matcher.get_prediction(_tn, for_api, api_data, request_authenticated_userid, issue_uid,
                                                      request.application_url, value, mode, issue, extra)

    return return_dict


# ajax - for additional service
@view_config(route_name='ajax_additional_service', renderer='json')
def additional_service(request):
    """
    Easteregg O:-)

    :param request: current request of the server
    :return: json-dict()
    """
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
    logger('views', 'flag_argument_or_statement', 'request.params: {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)

    try:
        uid = request.params['uid']
        reason = request.params['reason']
        extra_uid = request.params['extra_uid'] if 'extra_uid' in request.params else None
        is_argument = True if request.params['is_argument'] == 'true' else False
        nickname = request.authenticated_userid

        prepared_dict = review.flag(uid, reason, extra_uid, is_argument, nickname, ui_locales)
    except KeyError as e:
        _t = Translator(ui_locales)
        logger('views', 'flag_argument_or_statement', repr(e), error=True)
        prepared_dict = {'error': _t.get(_.internalKeyError), 'info': '', 'success': ''}

    return json.dumps(prepared_dict)


# #######################################
# ADDITIONAL AJAX STUFF # REVIEW THINGS #
# #######################################


# ajax - for flagging arguments
@view_config(route_name='ajax_split_or_merge_statement', renderer='json')
def split_or_merge_statement(request):
    """
    Flags a statement for a specific reason

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'split_or_merge_statement', 'request.params: {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)

    try:
        nickname = request.authenticated_userid
        pgroup_uid = request.params['pgroup_uid']
        key = request.params['key']
        tvalues = json.loads(request.params['text_values'])
        prepared_dict = review.merge_or_split_statement(key, pgroup_uid, tvalues, nickname, ui_locales)

    except KeyError as e:
        _t = Translator(ui_locales)
        logger('views', 'split_or_merge_statement', repr(e), error=True)
        prepared_dict = {'error': _t.get(_.internalKeyError), 'info': '', 'success': ''}

    return json.dumps(prepared_dict)


# #######################################
# ADDITIONAL AJAX STUFF # REVIEW THINGS #
# #######################################


# ajax - for flagging arguments
@view_config(route_name='ajax_split_or_merge_premisegroup', renderer='json')
def split_or_merge_premisegroup(request):
    """
    Flags a premisegroup for a specific reason

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'split_or_merge_premisegroup', 'request.params: {}'.format(request.params))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)

    try:
        pgroup_uid = request.params['pgroup_uid']
        key = request.params['key']
        nickname = request.authenticated_userid

        prepared_dict = review.merge_or_split_premisegroup(key, pgroup_uid, nickname, ui_locales)

    except KeyError as e:
        _t = Translator(ui_locales)
        logger('views', 'split_or_merge_premisegroup', repr(e), error=True)
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
    logger('views', 'review_delete_argument', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.delete_argument(request)
    except KeyError as e:
        logger('views', 'review_delete_argument', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
    logger('Views', 'review_edit_argument', 'main: {} - {}'.format(request.params, request.authenticated_userid))

    try:
        prepared_dict = review.edit_argument(request)
    except KeyError as e:
        logger('Views', 'review_edit_argument', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
    logger('Views', 'review_duplicate_statement', 'main: {} - {}'.format(request.params, request.authenticated_userid))
    try:
        prepared_dict = review.duplicate_statement(request)
    except KeyError as e:
        logger('Views', 'review_duplicate_statement', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
    logger('views', 'review_optimization_argument', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.optimization_argument(request)
    except KeyError as e:
        logger('Views', 'review_optimization_argument', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for feedback on a splitted premisegroup
@view_config(route_name='ajax_review_splitted_premisegroup', renderer='json')
def review_splitted_premisegroup(request):
    """
    Values for the review for a premisegroup, which should be splitted

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_splitted_premisegroup', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.split_premisegroup(request)
    except KeyError as e:
        logger('Views', 'review_splitted_premisegroup', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
        _t = Translator(ui_locales)
        prepared_dict = {'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)


# ajax - for feedback on a merged premisegroup
@view_config(route_name='ajax_review_merged_premisegroup', renderer='json')
def review_merged_premisegroup(request):
    """
    Values for the review for a statement, which should be merged

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'review_merged_premisegroup', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.merge_premisegroup(request)
    except KeyError as e:
        logger('Views', 'review_merged_premisegroup', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
    logger('views', 'undo_review', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.undo(request)
    except KeyError as e:
        logger('views', 'undo_review', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
        _t = Translator(ui_locales)
        prepared_dict = {
            'error': _t.get(_.internalKeyError),
            'info': '',
            'success': ''
        }

    return json.dumps(prepared_dict)


# ajax - for canceling reviews
@view_config(route_name='ajax_cancel_review', renderer='json')
def cancel_review(request):
    """
    Trys to cancel an ongoing review

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'cancel_review', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.cancel(request)
    except KeyError as e:
        logger('views', 'cancel_review', repr(e), error=True)
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
    logger('views', 'review_lock', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.lock(request)

    except KeyError as e:
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
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
    logger('views', 'revoke_some_content', 'main: {}'.format(request.params))

    try:
        prepared_dict = review.revoke(request)

    except KeyError as e:
        ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
        _t = Translator(ui_locales)
        logger('views', 'revoke_some_content', repr(e), error=True)
        prepared_dict = {'success': False, 'error': _t.get(_.internalKeyError)}

    return json.dumps(prepared_dict)
