"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

from typing import Callable, Any

import graphene
import pkg_resources
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import get_renderer
from pyramid.security import forget
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from webob_graphql import serve_graphql_request

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
import dbas.handler.issue as issue_handler
import dbas.handler.news as news_handler
import dbas.review.helper.history as review_history_helper
import dbas.review.helper.queues as review_queue_helper
import dbas.review.helper.reputation as review_reputation_helper
import dbas.review.helper.subpage as review_page_helper
from api.v2.graphql.core import Query
from dbas.auth.login import oauth_providers
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Issue
from dbas.handler import user
from dbas.handler.issue import get_issues_overiew
from dbas.handler.language import set_language_for_visit, get_language_from_cookie
from dbas.handler.rss import get_list_of_all_feeds
from dbas.helper.decoration import prep_extras_dict
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.validation import validate, valid_user, invalid_user, check_authentication
from dbas.helper.views import preparation_for_view
from dbas.input_validator import is_integer
from dbas.lib import escape_string, get_changelog, nick_of_anonymous_user
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import get_port


name = 'D-BAS'
version = '1.5.5'
full_version = version
project_name = name + ' ' + full_version


def base_layout():
    return get_renderer('../templates/basetemplate.pt').implementation()


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
    set_language_for_visit(request)

    return {
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
        'last_topic': last_topic,
        'port': get_port(request)
    }


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
        request.session.invalidate()
        headers = forget(request)
        location = request.application_url + 'discuss?session_expired=true',
        return HTTPFound(
            location=location,
            headers=headers
        )

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
@view_config(route_name='main_page', renderer='../templates/index.pt', permission='everybody')
@forbidden_view_config(renderer='../templates/index.pt')
@validate(check_authentication, prep_extras_dict)
def main_page(request):
    """
    View configuration for the main page

    :param request: current request of the server
    :return: HTTP 200 with several information
    """
    logger('main_page', 'def', 'request.matchdict: {}'.format(request.matchdict))

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
@view_config(route_name='main_settings', renderer='../templates/settings.pt', permission='use')
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
@view_config(route_name='main_notification', renderer='../templates/notifications.pt', permission='use')
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
@view_config(route_name='main_news', renderer='../templates/news.pt', permission='everybody')
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
@view_config(route_name='main_user', renderer='../templates/user.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_user(request):
    """
    View configuration for the public user page.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    match_dict = request.matchdict
    logger('main_user', 'def', 'request.matchdict: {}'.format(match_dict))

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
@view_config(route_name='main_imprint', renderer='../templates/imprint.pt', permission='everybody')
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
@view_config(route_name='main_faq', renderer='../templates/faq.pt', permission='everybody')
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
@view_config(route_name='main_experiment', renderer='../templates/fieldtest.pt', permission='everybody')
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
@view_config(route_name='main_mydiscussions', renderer='../templates/discussions.pt', permission='use')
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
@view_config(route_name='main_docs', renderer='../templates/docs.pt', permission='everybody')
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
@view_config(route_name='main_rss', renderer='../templates/rss.pt', permission='everybody')
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
@notfound_view_config(renderer='../templates/404.pt')
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
           ', matchdict: {}'.format(request.matchdict) +
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
@view_config(route_name='discussion_init', renderer='../templates/content.pt', permission='everybody')
@view_config(route_name='discussion_init_with_slash', renderer='../templates/content.pt', permission='everybody')
@view_config(route_name='discussion_init_with_slug', renderer='../templates/content.pt', permission='everybody')
def discussion_init(request, for_api=False, api_data=None):
    """
    View configuration for the initial discussion.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data: Dictionary, containing data of a user who logged in via API
    :return: dictionary
    """
    logger('Views', 'discussion_init', 'request.matchdict: {}'.format(request.matchdict))

    prepared_discussion = __call_from_discussion_step(request, discussion.init, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    # redirect to oauth url after login and redirecting
    if request.authenticated_userid and 'service' in request.params and request.params['service'] in oauth_providers:
        url = request.session['oauth_redirect_url']
        return HTTPFound(location=url)

    return prepared_discussion


# attitude page
@view_config(route_name='discussion_attitude', renderer='../templates/content.pt', permission='everybody')
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

    prepared_discussion = __call_from_discussion_step(request, discussion.attitude, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# justify page
@view_config(route_name='discussion_justify', renderer='../templates/content.pt', permission='everybody')
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

    prepared_discussion = __call_from_discussion_step(request, discussion.justify, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# reaction page
@view_config(route_name='discussion_reaction', renderer='../templates/content.pt', permission='everybody')
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

    prepared_discussion = __call_from_discussion_step(request, discussion.reaction, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# support page
@view_config(route_name='discussion_support', renderer='../templates/content.pt', permission='everybody')
def discussion_support(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where we will present another supportive argument.

    :param request: request of the web server
    :param for_api: Boolean
    :param api_data:
    :return: dictionary
    """
    logger('views', 'discussion_support', 'request.matchdict: {}'.format(request.matchdict))

    prepared_discussion = __call_from_discussion_step(request, discussion.support, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# finish page
@view_config(route_name='discussion_finish', renderer='../templates/content.pt', permission='everybody')
@validate(check_authentication)
def discussion_finish(request, for_api=False, api_data=None):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    logger('views', 'discussion_finish', 'request.matchdict: {}'.format(request.matchdict))

    prepared_discussion = __call_from_discussion_step(request, discussion.finish, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# exit page
@view_config(route_name='discussion_exit', renderer='../templates/exit.pt', permission='everybody')
def discussion_exit(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    match_dict = request.matchdict
    logger('views', 'discussion_exit', 'request.matchdict: {}'.format(match_dict))

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

    prepared_discussion = discussion.dexit(request_dict)
    prepared_discussion['layout'] = base_layout()
    prepared_discussion['language'] = str(get_language_from_cookie(request))
    prepared_discussion['show_summary'] = len(prepared_discussion['summary']) != 0
    return prepared_discussion


# choosing page
@view_config(route_name='discussion_choose', renderer='../templates/content.pt', permission='everybody')
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
    logger('discussion_choose', 'def', 'request.matchdict: {}'.format(match_dict))

    prepared_discussion = __call_from_discussion_step(request, discussion.choose, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# jump page
@view_config(route_name='discussion_jump', renderer='../templates/content.pt', permission='everybody')
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

    prepared_discussion = __call_from_discussion_step(request, discussion.jump, for_api, api_data)
    if not prepared_discussion:
        raise HTTPNotFound()

    return prepared_discussion


# ####################################
# REVIEW                             #
# ####################################

# index page for reviews
@view_config(route_name='review_index', renderer='../templates/review.pt', permission='use')
@validate(check_authentication, prep_extras_dict)
def main_review(request):
    """
    View configuration for the review index.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_review', 'main', 'def {}'.format(request.matchdict))
    nickname = request.authenticated_userid

    issue = issue_handler.get_issue_id(request)

    db_user = DBDiscussionSession.query(User).filter_by(
        nickname=nickname if nickname else nick_of_anonymous_user).first()
    issue_dict = issue_handler.prepare_json_of_issue(issue, request.application_url, False, db_user)

    _tn = Translator(issue_dict['lang'])
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
@view_config(route_name='review_content', renderer='../templates/review-content.pt', permission='use')
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
@view_config(route_name='review_history', renderer='../templates/review-history.pt', permission='use')
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
@view_config(route_name='review_ongoing', renderer='../templates/review-history.pt', permission='use')
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
@view_config(route_name='review_reputation', renderer='../templates/review-reputation.pt', permission='use')
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
