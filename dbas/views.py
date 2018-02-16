"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import json
from time import sleep
from typing import Callable, Any

import graphene
import pkg_resources
import requests
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.renderers import get_renderer
from pyramid.security import forget
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from webob_graphql import serve_graphql_request

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
import dbas.handler.issue as issue_handler
import dbas.handler.news as news_handler
import dbas.review.helper.flags as review_flag_helper
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.main as review_main_helper
import dbas.review.helper.queues as review_queue_helper
import dbas.review.helper.reputation as review_reputation_helper
import dbas.review.helper.subpage as review_page_helper
import dbas.strings.matcher as fuzzy_string_matcher
from api.v2.graphql.core import Query
from dbas.auth.login import login_user, login_user_oauth, register_user_with_ajax_data, oauth_providers, \
    __refresh_headers_and_url
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, ReviewEdit, ReviewMerge, ReviewSplit, ReviewOptimization, \
    ReviewDuplicate, ReviewDelete
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
from dbas.helper.decoration import prep_extras_dict
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.query import get_default_locale_name, set_user_language, \
    mark_statement_or_argument, get_short_url, revoke_author_of_argument_content, revoke_author_of_statement_content
from dbas.helper.validation import validate, valid_user, valid_issue, valid_conclusion, has_keywords, \
    valid_issue_not_readonly, valid_notification_text, valid_notification_title, valid_notification_recipient, \
    valid_premisegroups, valid_language, valid_new_issue, invalid_user, valid_argument, valid_statement, \
    valid_not_executed_review, valid_database_model, valid_user_as_author, valid_uid_as_row_in_review_queue, \
    valid_user_as_author_of_statement, valid_user_as_author_of_argument, valid_review_reason, \
    valid_premisegroup, valid_text_values, has_maybe_keywords, check_authentication, valid_lang_cookie_fallback
from dbas.helper.views import preparation_for_view
from dbas.input_validator import is_integer
from dbas.lib import escape_string, get_discussion_language, get_changelog
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import get_port, send_request_for_recent_reviewer_socketio

name = 'D-BAS'
version = '1.5.5'
full_version = version
project_name = name + ' ' + full_version


def base_layout():
    return get_renderer('templates/basetemplate.pt').implementation()


def prepare_request_dict(request, nickname, for_api=False):
    """

    :param request:
    :param nickname:
    :param for_api:
    :return:
    """

    last_topic = history_handler.get_saved_issue(nickname)

    slug = None
    if 'slug' in request.matchdict:
        slug = request.matchdict['slug']
        if not isinstance(request.matchdict['slug'], str) and len(request.matchdict['slug']) > 0:
            slug = request.matchdict['slug'][0]

    if not slug and last_topic != 0:
        issue = last_topic
    elif slug and not for_api:
        issue = issue_handler.get_id_of_slug(slug, request, True)
    else:
        issue = issue_handler.get_issue_id(request)

    ui_locales = get_language_from_cookie(request)
    if not issue:
        if for_api:
            logger('Views', 'prepare_request_dict', 'Slug error ({}) for api'.format(slug), error=True)
            _tn = Translator(ui_locales)
            return {'error': _tn.get(_.issueNotFound)}
        else:
            raise HTTPNotFound()

    if not slug:
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

    request_dict = prepare_request_dict(request, nickname)
    prepared_discussion = f(request_dict, for_api)
    if prepared_discussion:
        prepared_discussion['layout'] = base_layout()

    return prepared_discussion


def __main_dict(request, title):
    return {
        'layout': base_layout(),
        'title': title,
        'project': project_name,
        'extras': request.decorated['extras'],
    }


# main page
@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
@forbidden_view_config(renderer='templates/index.pt')
@validate(check_authentication, prep_extras_dict)
def main_page(request):
    """
    View configuration for the main page

    :param request: current request of the server
    :return: HTTP 200 with several information
    """
    logger('main_page', 'def', 'main: {}'.format(request.params))
    set_language_for_visit(request)
    session_expired = 'session_expired' in request.params and request.params['session_expired'] == 'true'
    ui_locales = get_language_from_cookie(request)

    prep_dict = __main_dict(request, name + ' ' + full_version)
    prep_dict.update({
        'session_expired': session_expired,
        'news': news_handler.get_latest_news(ui_locales)
    })
    return prep_dict


# settings page, when logged in
@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
@validate(valid_user, check_authentication, prep_extras_dict)
def main_settings(request):
    """
    View configuration for the personal settings view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_settings', 'def', 'main: {}'.format(request.params))

    ui_locales = get_language_from_cookie(request)
    old_pw, new_pw, confirm_pw, message = '', '', '', ''
    success, error = False, False
    db_user = request.validated['user']

    if 'form.passwordchange.submitted' in request.params:
        old_pw = escape_string(request.params['passwordold'])
        new_pw = escape_string(request.params['password'])
        confirm_pw = escape_string(request.params['passwordconfirm'])

        message, success = user.change_password(db_user, old_pw, new_pw, confirm_pw, ui_locales)
        error = not success

    settings_dict = DictionaryHelper(ui_locales).prepare_settings_dict(success, old_pw, new_pw, confirm_pw, error,
                                                                       message, db_user, request.application_url,
                                                                       request.decorated['extras']['use_with_ldap'])

    prep_dict = __main_dict(request, Translator(ui_locales).get(_.settings))
    prep_dict.update({
        'settings': settings_dict
    })
    return prep_dict


# message page, when logged in
@view_config(route_name='main_notification', renderer='templates/notifications.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def main_notifications(request):
    """
    View configuration for the notification view. Only logged in user can reach this page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_notifications', 'def', 'main')
    return __main_dict(request, 'Message')


# news page for everybody
@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
@validate(invalid_user, check_authentication, prep_extras_dict)
def main_news(request):
    """
    View configuration for the news.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_news', 'def', 'main')

    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    is_author = db_user.is_admin() or db_user.is_author()

    prep_dict = __main_dict(request, 'News')
    prep_dict.update({
        'is_author': is_author,
        'news': news_handler.get_news(ui_locales)
    })
    return prep_dict


# public users page for everybody
@view_config(route_name='main_user', renderer='templates/user.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_user(request):
    """
    View configuration for the public user page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    match_dict = request.matchdict
    params = request.params
    logger('main_user', 'def', 'request.matchdict: {}'.format(match_dict))
    logger('main_user', 'def', 'main: {}'.format(params))

    uid = match_dict.get('uid', 0)
    logger('main_user', 'def', 'uid: {}'.format(uid))

    if not is_integer(uid):
        raise HTTPNotFound

    current_user = DBDiscussionSession.query(User).get(uid)
    if current_user is None or current_user.nickname == nick_of_anonymous_user:
        logger('main_user', 'def', 'no user: {}'.format(uid), error=True)
        raise HTTPNotFound()

    ui_locales = get_language_from_cookie(request)
    user_dict = user.get_information_of(current_user, ui_locales)

    db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    can_send_notification = False
    if db_user_of_request:
        can_send_notification = current_user.uid != db_user_of_request.uid

    prep_dict = __main_dict(request, user_dict['public_nick'])
    prep_dict.update({
        'user': user_dict,
        'can_send_notification': can_send_notification
    })
    return prep_dict


# imprint
@view_config(route_name='main_imprint', renderer='templates/imprint.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_imprint(request):
    """
    View configuration for the imprint.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_imprint', 'def', 'main')
    # add version of pyramid
    request.decorated['extras'].update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

    prep_dict = __main_dict(request, Translator(get_language_from_cookie(request)).get(_.imprint))
    prep_dict.update({'imprint': get_changelog(5)})
    return prep_dict


# faq
@view_config(route_name='main_faq', renderer='templates/faq.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_faq(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_faq', 'def', 'main')

    return __main_dict(request, 'FAQ')


# fieldtest
@view_config(route_name='main_experiment', renderer='templates/fieldtest.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_experiment(request):
    """
    View configuration for fieldtest.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_experiment', 'def', 'main')
    ui_locales = get_language_from_cookie(request)

    return __main_dict(request, Translator(ui_locales).get(_.fieldtest))


# my discussions
@view_config(route_name='main_mydiscussions', renderer='templates/discussions.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def main_mydiscussions(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_mydiscussions', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    issue_dict = get_issues_overiew(request.authenticated_userid, request.application_url)

    prep_dict = __main_dict(request, Translator(ui_locales).get(_.myDiscussions))
    prep_dict.update({
        'issues': issue_dict
    })
    return prep_dict


# docs
@view_config(route_name='main_docs', renderer='templates/docs.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_docs(request):
    """
    View configuration for the documentation.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_docs', 'def', 'main')
    return __main_dict(request, Translator(get_language_from_cookie(request)).get(_.docs))


# imprint
@view_config(route_name='main_rss', renderer='templates/rss.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_rss(request):
    """
    View configuration for the RSS feed.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_rss', 'def', 'main')
    ui_locales = get_language_from_cookie(request)
    rss = get_list_of_all_feeds(ui_locales)

    prep_dict = __main_dict(request, 'RSS')
    prep_dict.update({'rss': rss})
    return prep_dict


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
@validate(prep_extras_dict)
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

    prep_dict = __main_dict(request, 'ERROR')
    prep_dict.update({
        'page_notfound_viewname': path,
        'param_error': param_error,
        'revoked_content': revoked_content
    })
    return prep_dict


# ####################################
# DISCUSSION                         #
# ####################################


# content page
@view_config(route_name='discussion_init', renderer='templates/content.pt', permission='everybody')
@view_config(route_name='discussion_init_with_slash', renderer='templates/content.pt', permission='everybody')
@view_config(route_name='discussion_init_with_slug', renderer='templates/content.pt', permission='everybody')
def discussion_init(request, for_api=False, api_data=None):
    """
    View configuration for the initial discussion.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data: Dictionary, containing data of a user who logged in via API
    :return: dictionary
    """
    logger('Views', 'discussion_init', 'request.matchdict: {}'.format(request.matchdict))
    logger('Views', 'discussion_init', 'main: {}'.format(request.params))

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
    logger('Views', 'discussion_attitude', 'main: {}'.format(request.params))

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
    logger('views', 'discussion_justify', 'main: {}'.format(request.params))

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
    logger('views', 'discussion_reaction', 'main: {}'.format(request.params))

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
    logger('views', 'discussion_support', 'main: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.support, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# finish page
@view_config(route_name='discussion_finish', renderer='templates/finish.pt', permission='everybody')
@validate(check_authentication)
def discussion_finish(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    match_dict = request.matchdict
    params = request.params
    logger('views', 'discussion.finish', 'request.matchdict: {}'.format(match_dict))
    logger('views', 'discussion.finish', 'main: {}'.format(params))

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
    logger('discussion_choose', 'def', 'main: {}'.format(params))

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
    logger('views', 'discussion_jump', 'main: {}'.format(request.params))

    prepared_discussion = __call_from_discussion_step(request, discussion.jump, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# ####################################
# REVIEW                             #
# ####################################

# index page for reviews
@view_config(route_name='review_index', renderer='templates/review.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
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

    issue = issue_handler.get_issue_id(request)
    disc_ui_locales = get_discussion_language(request.matchdict, request.params, request.session, issue)

    issue_dict = issue_handler.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, False,
                                                     request.authenticated_userid)

    review_dict = review_queue_helper.get_review_queues_as_lists(request.application_url, _tn, nickname)
    count, all_rights = review_reputation_helper.get_reputation_of(nickname)

    prep_dict = __main_dict(request, _tn.get(_.review))
    prep_dict.update({
        'review': review_dict,
        'privilege_list': review_reputation_helper.get_privilege_list(_tn),
        'reputation_list': review_reputation_helper.get_reputation_list(_tn),
        'issues': issue_dict,
        'reputation': {'count': count,
                       'has_all_rights': all_rights}
    })
    return prep_dict


# content page for reviews
@view_config(route_name='review_content', renderer='templates/review-content.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def review_content(request):
    """
    View configuration for the review content.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('review_content', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    subpage_name = request.matchdict['queue']
    nickname = request.authenticated_userid
    session = request.session
    application_url = request.application_url
    subpage_dict = review_page_helper.get_subpage_elements_for(nickname, session, application_url, subpage_name, _tn)
    request.session.update(subpage_dict['session'])
    if not subpage_dict['elements'] and not subpage_dict['has_access'] and not subpage_dict['no_arguments_to_review']:
        logger('review_content', 'def', 'subpage error', error=True)
        raise HTTPNotFound()

    title = _tn.get(_.review)
    if subpage_name in review_queue_helper.title_mapping:
        title = review_queue_helper.title_mapping[subpage_name]

    prep_dict = __main_dict(request, title)
    prep_dict.update({
        'extras': request.decorated['extras'],
        'subpage': subpage_dict,
        'lock_time': review_queue_helper.max_lock_time_in_sec
    })
    return prep_dict


# history page for reviews
@view_config(route_name='review_history', renderer='templates/review-history.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
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

    history = review_history_helper.get_review_history(request.application_url, request_authenticated_userid, _tn)
    prep_dict = __main_dict(request, _tn.get(_.review_history))
    prep_dict.update({'history': history})
    return prep_dict


# history page for reviews
@view_config(route_name='review_ongoing', renderer='templates/review-history.pt', permission='use')
@validate(valid_user, check_authentication, prep_extras_dict)
def ongoing_history(request):
    """
    View configuration for the current reviews.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('ongoing_history', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    history = review_history_helper.get_ongoing_reviews(request.application_url, request.validated['user'], _tn)
    prep_dict = __main_dict(request, _tn.get(_.review_ongoing))
    prep_dict.update({'history': history})
    return prep_dict


# reputation_borders page for reviews
@view_config(route_name='review_reputation', renderer='templates/review-reputation.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def review_reputation(request):
    """
    View configuration for the review reputation_borders.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('review_reputation', 'main', 'def {}'.format(request.matchdict))
    ui_locales = get_language_from_cookie(request)
    _tn = Translator(ui_locales)

    reputation_dict = review_history_helper.get_reputation_history_of(request.authenticated_userid, _tn)
    prep_dict = __main_dict(request, _tn.get(_.reputation))
    prep_dict.update({'reputation': reputation_dict})
    return prep_dict


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
@view_config(route_name='ajax_get_all_posted_statements', renderer='json')
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
@view_config(route_name='ajax_get_all_edits', renderer='json')
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
@view_config(route_name='ajax_get_all_marked_arguments', renderer='json')
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
@view_config(route_name='ajax_get_all_marked_statements', renderer='json')
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
@view_config(route_name='ajax_get_all_argument_clicks', renderer='json')
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
@view_config(route_name='ajax_get_all_statement_clicks', renderer='json')
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
@view_config(route_name='ajax_delete_user_history', renderer='json')
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
@view_config(route_name='ajax_delete_statistics', renderer='json')
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


@view_config(request_method='POST', route_name='ajax_user_login', renderer='json')
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


@view_config(route_name='ajax_user_login_oauth', renderer='json')
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


@view_config(route_name='ajax_user_registration', renderer='json')
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

    success, info, new_user = register_user_with_ajax_data(request.validated, lang, mailer)

    return {
        'success': str(success),
        'error': '',
        'info': str(info)
    }


@view_config(route_name='ajax_user_password_request', renderer='json')
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


@view_config(route_name='ajax_set_user_setting', renderer='json')
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


@view_config(route_name='ajax_set_user_language', renderer='json')
@validate(valid_user, valid_lang_cookie_fallback)
def set_user_lang(request):
    """
    Specify new UI language for user.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_user_lang', 'request.params: {}'.format(request.json_body))
    return set_user_language(request.validated['user'], request.validated.get('lang'))


@view_config(route_name='ajax_set_discussion_properties', renderer='json')
@validate(valid_user, valid_issue, has_keywords(('property', bool), ('value', str)))
def set_discussion_properties(request):
    """
    Set availability, read-only, ... flags in the admin panel.

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_discussion_properties', 'request.params: {}'.format(request.json_body))
    _tn = Translator(get_language_from_cookie(request))

    property = request.validated['property']
    db_user = request.validated['user']
    issue = request.validated['issue']
    value = request.validated['value']
    return set_discussions_properties(db_user, issue, property, value, _tn)


# #######################################
# ADDTIONAL AJAX STUFF # SET NEW THINGS #
# #######################################

@view_config(route_name='ajax_set_new_start_argument', renderer='json')
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
    prepared_dict_pos = set_position(False, data)
    if len(prepared_dict_pos['error']) is 0:
        logger('views', 'set_new_start_argument', 'set premise/reason')
        data['premisegroups'] = [[reason]]
        data['conclusion'] = DBDiscussionSession.query(Statement).get(prepared_dict_pos['statement_uids'][0])
        prepared_dict_reas = set_positions_premise(False, data)
        return prepared_dict_reas

    return prepared_dict_pos


# ajax - send new start premise
@view_config(route_name='ajax_set_new_start_premise', renderer='json')
@validate(valid_user, valid_issue, valid_conclusion, valid_premisegroups, has_keywords(('supportive', bool)))
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
    prepared_dict = set_positions_premise(False, data)
    return prepared_dict


# ajax - send new premises
@view_config(route_name='ajax_set_new_premises_for_argument', renderer='json')
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
        'discussion_lang': get_discussion_language(request.matchdict, request.params, request.session),
        'default_locale_name': get_default_locale_name(request.registry),
        'application_url': request.application_url,
        'mailer': request.mailer
    }
    prepared_dict = set_arguments_premises(False, data)
    return prepared_dict


# ajax - set new textvalue for a statement
@view_config(route_name='ajax_set_correction_of_statement', renderer='json')
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
    prepared_dict = set_correction_of_statement(elements, db_user, _tn)
    return prepared_dict


@view_config(route_name='ajax_notifications_read', renderer='json')
@validate(valid_user, has_keywords(('ids', list)))
def set_notifications_read(request):
    """
    Set a notification as read

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_notifications_read', 'main {}'.format(request.json_body))
    prepared_dict = read_notifications(request.validated['ids'], request.validated['user'])
    return prepared_dict


@view_config(route_name='ajax_notifications_delete', renderer='json')
@validate(valid_user, has_keywords(('ids', list)))
def set_notifications_delete(request):
    """
    Request the removal of a notification

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'set_notifications_delete', 'main {}'.format(request.json_body))
    ui_locales = get_language_from_cookie(request)
    prepared_dict = delete_notifications(request.validated['ids'], request.validated['user'], ui_locales,
                                         request.application_url)
    return prepared_dict


@view_config(route_name='ajax_send_notification', renderer='json')
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
@view_config(route_name='ajax_set_new_issue', renderer='json')
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
@view_config(route_name='ajax_set_seen_statements', renderer='json')
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
@view_config(route_name='ajax_mark_statement_or_argument', renderer='json')
@validate(valid_user, has_keywords(('uid', int), ('step', str), ('is_argument', bool), ('is_supportive', bool),
                                   ('should_mark', bool)))
def mark_or_unmark_statement_or_argument(request):
    """
    Set statements as seen, when they were hidden

    :param request: current request of the server
    :return: json
    """
    logger('views', 'mark_or_unmark_statement_or_argument', 'main {}'.format(request.json_body))
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session)
    uid = request.validated['uid']
    step = request.validated['step']
    is_argument = request.validated['is_argument']
    is_supportive = request.validated['is_supportive']
    should_mark = request.validated['should_mark']
    history = request.json_body.get('history', '')
    db_user = request.validated['user']
    return mark_statement_or_argument(uid, step, is_argument, is_supportive, should_mark, history, ui_locales, db_user)


# ###################################
# ADDTIONAL AJAX STUFF # GET THINGS #
# ###################################


# ajax - getting changelog of a statement
@view_config(route_name='ajax_get_logfile_for_statements', renderer='json')
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
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session, db_issue.uid)
    return get_logfile_for_statements(uids, ui_locales, request.application_url)


# ajax - for shorten url
@view_config(route_name='ajax_get_shortened_url', renderer='json')
@validate(valid_issue, has_keywords(('url', str)))
def get_shortened_url(request):
    """
    Shortens url with the help of a python lib

    :param request: current request of the server
    :return: dictionary with shortend url
    """
    logger('views', 'get_shortened_url', 'main')
    db_issue = request.validated['issue']
    ui_locales = get_discussion_language(request.matchdict, request.params, request.session, db_issue.uid)
    return get_short_url(request.validated['url'], ui_locales)


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
@view_config(route_name='ajax_get_user_with_same_opinion', renderer='json')
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
@view_config(route_name='ajax_get_public_user_data', renderer='json')
@validate(has_keywords(('nickname', str)))
def get_public_user_data(request):
    """
    Returns dictionary with public user data

    :param request: request of the web server
    :return:
    """
    logger('views', 'get_public_user_data', 'main: {}'.format(request.json_body))
    return user.get_public_data(request.validated['nickname'], get_language_from_cookie(request))


@view_config(route_name='ajax_get_arguments_by_statement_uid', renderer='json')
@validate(valid_statement)
def get_arguments_by_statement_id(request):
    """
    Returns all arguments, which use the given statement

    :param request: current request of the server
    :return: json-dict()
    """
    logger('views', 'get_arguments_by_statement_id', 'main: {}'.format(request.json_body))
    return get_arguments_by_statement_uid(request.validated['statement'], request.application_url)


@view_config(route_name='ajax_get_references', renderer='json')
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


@view_config(route_name='ajax_set_references', renderer='json')
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
@view_config(route_name='ajax_switch_language', renderer='json')
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
@view_config(route_name='ajax_send_news', renderer='json')
@validate(valid_user, has_keywords(('title', str), ('text', str)))
def send_news(request):
    """
    ajax interface for settings news

    :param request: current request of the server
    :return: json-set with new news
    """
    logger('views', 'send_news', 'main: {}'.format(request.params))
    title = escape_string(request.validated['title'])
    text = escape_string(request.validated['text'])
    db_user = request.validated['user']
    return news_handler.set_news(title, text, db_user, request.registry.settings['pyramid.default_locale_name'],
                                 request.application_url)


# ajax - for fuzzy search
@view_config(route_name='ajax_fuzzy_search', renderer='json')
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
@view_config(route_name='ajax_additional_service', renderer='json')
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


# ajax - for flagging arguments
@view_config(route_name='ajax_flag_argument_or_statement', renderer='json')
@validate(valid_user, valid_review_reason, has_keywords(('uid', int), ('is_argument', bool)))
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
    extra_uid = request.json_body.get('extra_uid')
    is_argument = request.validated['is_argument']
    db_user = request.validated['user']
    return review_flag_helper.flag_element(uid, reason, db_user, is_argument, ui_locales, extra_uid)


# #######################################
# ADDITIONAL AJAX STUFF # REVIEW THINGS #
# #######################################


# ajax - for flagging arguments
@view_config(route_name='ajax_split_or_merge_statement', renderer='json')
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


# #######################################
# ADDITIONAL AJAX STUFF # REVIEW THINGS #
# #######################################


# ajax - for flagging arguments
@view_config(route_name='ajax_split_or_merge_premisegroup', renderer='json')
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


# ajax - for feedback on flagged arguments
@view_config(route_name='ajax_review_delete_argument', renderer='json')
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


# ajax - for feedback on flagged arguments
@view_config(route_name='ajax_review_edit_argument', renderer='json')
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


# ajax - for feedback on duplicated statements
@view_config(route_name='ajax_review_duplicate_statement', renderer='json')
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


# ajax - for feedback on optimization arguments
@view_config(route_name='ajax_review_optimization_argument', renderer='json')
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


# ajax - for feedback on a splitted premisegroup
@view_config(route_name='ajax_review_splitted_premisegroup', renderer='json')
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


# ajax - for feedback on a merged premisegroup
@view_config(route_name='ajax_review_merged_premisegroup', renderer='json')
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


# ajax - for undoing reviews
@view_config(route_name='ajax_undo_review', renderer='json')
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


# ajax - for canceling reviews
@view_config(route_name='ajax_cancel_review', renderer='json')
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


# ajax - for undoing reviews
@view_config(route_name='ajax_review_lock', renderer='json', require_csrf=False)
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


# ajax - for revoking statements
@view_config(route_name='ajax_revoke_statement_content', renderer='json', require_csrf=False)
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


# ajax - for revoking arguments
@view_config(route_name='ajax_revoke_argument_content', renderer='json', require_csrf=False)
@validate(valid_user_as_author_of_argument, valid_argument)
def revoke_argument_content(request):
    db_user = request.validated['user']
    argument = request.validated['argument']
    return revoke_author_of_argument_content(argument, db_user)
