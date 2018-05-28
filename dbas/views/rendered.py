"""
Collection of pyramids views components of D-BAS' core.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import graphene
import pkg_resources
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from webob_graphql import serve_graphql_request

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
import dbas.handler.issue as issue_handler
import dbas.handler.news as news_handler
from api.v2.graphql.core import Query
from dbas.auth.login import oauth_providers
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Statement, Argument
from dbas.handler import user
from dbas.handler.issue import get_issues_overiew
from dbas.handler.language import set_language_for_visit, get_language_from_cookie
from dbas.handler.rss import get_list_of_all_feeds
from dbas.helper.decoration import prep_extras_dict
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.input_validator import is_integer
from dbas.lib import escape_string, get_changelog, nick_of_anonymous_user
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate, has_keywords_in_path
from dbas.validators.discussion import valid_issue_by_slug, valid_attitude, \
    valid_relation, valid_argument, valid_statement, valid_reaction_arguments, valid_support, \
    valid_list_of_premisegroups_in_path, valid_premisegroup_in_path
from dbas.validators.user import valid_user, valid_user_optional
from dbas.views.helper import name, full_version, modify_discussion_url, modify_discussion_bubbles, \
    modifiy_issue_overview_url, prepare_request_dict, append_extras_dict, main_dict, \
    append_extras_dict_during_justification_argument, append_extras_dict_during_justification_statement


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
    logger('main_page', 'request.matchdict: {}'.format(request.matchdict))

    set_language_for_visit(request)
    session_expired = 'session_expired' in request.params and request.params['session_expired'] == 'true'
    ui_locales = get_language_from_cookie(request)

    prep_dict = main_dict(request, name + ' ' + full_version)
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
    logger('main_settings', 'main: {}'.format(request.params))

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

    prep_dict = main_dict(request, Translator(ui_locales).get(_.settings))
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
    logger('main_notifications', 'main')
    _tn = Translator(get_language_from_cookie(request))
    return main_dict(request, _tn.get(_.message))


# news page for everybody
@view_config(route_name='main_news', renderer='../templates/news.pt', permission='everybody')
@validate(valid_user_optional, check_authentication, prep_extras_dict)
def main_news(request):
    """
    View configuration for the news.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_news', 'main')

    ui_locales = get_language_from_cookie(request)
    db_user = request.validated['user']
    is_author = db_user.is_admin() or db_user.is_author()

    prep_dict = main_dict(request, 'News')
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
    logger('main_user', 'request.matchdict: {}'.format(match_dict))

    uid = match_dict.get('uid', 0)
    logger('main_user', 'uid: {}'.format(uid))

    if not is_integer(uid):
        raise HTTPNotFound

    current_user = DBDiscussionSession.query(User).get(uid)
    if current_user is None or current_user.nickname == nick_of_anonymous_user:
        logger('main_user', 'no user: {}'.format(uid), error=True)
        raise HTTPNotFound()

    ui_locales = get_language_from_cookie(request)
    user_dict = user.get_information_of(current_user, ui_locales)

    db_user_of_request = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    can_send_notification = False
    if db_user_of_request:
        can_send_notification = current_user.uid != db_user_of_request.uid

    prep_dict = main_dict(request, user_dict['public_nick'])
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
    logger('main_imprint', 'main')
    # add version of pyramid
    request.decorated['extras'].update({'pyramid_version': pkg_resources.get_distribution('pyramid').version})

    prep_dict = main_dict(request, Translator(get_language_from_cookie(request)).get(_.imprint))
    prep_dict.update({'imprint': get_changelog(5)})
    return prep_dict


# privacy policy
@view_config(route_name='main_privacy', renderer='../templates/privacy.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_privacy(request):
    """
    View configuration for the privacy.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_privacy', 'main')
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.privacy_policy))


# faq
@view_config(route_name='main_faq', renderer='../templates/faq.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_faq(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_faq', 'main')
    return main_dict(request, 'FAQ')


# fieldtest
@view_config(route_name='main_experiment', renderer='../templates/fieldtest.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_experiment(request):
    """
    View configuration for fieldtest.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_experiment', 'main')
    ui_locales = get_language_from_cookie(request)
    return main_dict(request, Translator(ui_locales).get(_.fieldtest))


# my discussions
@view_config(route_name='main_discussions_overview', renderer='../templates/discussion-overview.pt', permission='use')
@validate(check_authentication, prep_extras_dict, valid_user_optional)
def main_discussions_overview(request):
    """
    View configuration for FAQs.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_discussions_overview', 'main')
    ui_locales = get_language_from_cookie(request)
    issue_dict = get_issues_overiew(request.validated['user'], request.application_url)

    prep_dict = main_dict(request, Translator(ui_locales).get(_.myDiscussions))
    modifiy_issue_overview_url(issue_dict)
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
    logger('main_docs', 'main')
    return main_dict(request, Translator(get_language_from_cookie(request)).get(_.docs))


# imprint
@view_config(route_name='main_rss', renderer='../templates/rss.pt', permission='everybody')
@validate(check_authentication, prep_extras_dict)
def main_rss(request):
    """
    View configuration for the RSS feed.

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value, weather the user is logged in
    """
    logger('main_rss', 'main')
    ui_locales = get_language_from_cookie(request)
    rss = get_list_of_all_feeds(ui_locales)

    prep_dict = main_dict(request, 'RSS')
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
    logger('main_graphiql', 'main')
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

    logger('notfound', 'main in {}'.format(request.method) + '-request' +
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

    prep_dict = main_dict(request, '404 Error')
    prep_dict.update({
        'page_notfound_viewname': path,
        'param_error': param_error,
        'revoked_content': revoked_content,
        'discussion': {'broke_limit': False}
    })
    return prep_dict


@view_config(route_name='discussion_start', renderer='../templates/discussion-start.pt', permission='everybody')
@view_config(route_name='discussion_start_with_slash', renderer='../templates/discussion-start.pt',
             permission='everybody')
@validate(check_authentication, valid_user_optional, prep_extras_dict)
def discussion_start(request):
    """
    View configuration for the initial discussion overview.

    :param request: request of the web server
    :return: dictionary
    """
    logger('discussion_start', 'main')
    ui_locales = get_language_from_cookie(request)
    issue_dict = issue_handler.get_issues_overview_on_start(request.validated['user'])
    for i in range(len(issue_dict['issues'])):
        issue_dict['issues'][i]['url'] = '/discuss' + issue_dict['issues'][i]['url']

    prep_dict = main_dict(request, Translator(ui_locales).get(_.discussionStart))

    prep_dict.update(issue_dict)
    return prep_dict


# ####################################
# DISCUSSION                         #
# ####################################


# content page
@view_config(route_name='discussion_init_with_slug', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_issue_by_slug, valid_user_optional)
def discussion_init(request):
    """
    View configuration for the initial discussion.

    :param request: request of the web server
    :return: dictionary
    """
    logger('discussion_init', 'request.matchdict: {}'.format(request.matchdict))

    prepared_discussion = discussion.init(request.validated['issue'], request.validated['user'])
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    rdict = prepare_request_dict(request)

    # redirect to oauth url after login and redirecting
    if request.authenticated_userid and 'service' in request.params and request.params['service'] in oauth_providers:
        url = request.session['oauth_redirect_url']
        return HTTPFound(location=url)

    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)
    if len(prepared_discussion['items']['elements']) == 1:
        _dh = DictionaryHelper(rdict['ui_locales'], prepared_discussion['issues']['lang'])
        nickname = request.authenticated_userid if request.authenticated_userid else nick_of_anonymous_user
        _dh.add_discussion_end_text(prepared_discussion['discussion'], prepared_discussion['extras'], nickname,
                                    at_start=True)

    return prepared_discussion


# attitude page
@view_config(route_name='discussion_attitude', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_statement(location='path', depends_on={valid_issue_by_slug}))
def discussion_attitude(request):
    """
    View configuration for discussion step, where we will ask the user for her attitude towards a statement.
    Route: /discuss/{slug}/attitude/{position_id}

    :param request: request of the web server
    :return: dictionary
    """
    logger('discussion_attitude', 'request.matchdict: {}'.format(request.matchdict))

    db_statement = request.validated['statement']
    db_issue = request.validated['issue']
    db_user = request.validated['user']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    prepared_discussion = discussion.attitude(db_issue, db_user, db_statement, history, request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    rdict = prepare_request_dict(request)

    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion


# justify page
@view_config(route_name='discussion_justify_statement', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_statement(location='path', depends_on={valid_issue_by_slug}),
          valid_attitude)
def discussion_justify_statement(request) -> dict:
    """
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    Path: /discuss/{slug}/justify/{statement_id:\d+}/{attitude}

    :param request: request of the web server
    :return: dict
    """
    logger('discussion_justify_statement', 'request.matchdict: {}'.format(request.matchdict))

    db_statement: Statement = request.validated['statement']

    db_issue = request.validated['issue']
    db_user = request.validated['user']
    attitude = request.validated['attitude']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    prepared_discussion = discussion.justify_statement(db_issue, db_user, db_statement, attitude, history, request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    append_extras_dict_during_justification_statement(request, db_user, db_issue, db_statement, prepared_discussion,
                                                      attitude)

    return prepared_discussion


@view_config(route_name='discussion_dontknow_argument', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}))
def discussion_dontknow_argument(request) -> dict:
    """
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    Path: /discuss/{slug}/justify/{argument_id:\d+}/dontknow}

    :param request: request of the web server
    :return: dict
    """
    logger('discussion_dontknow_argument', 'request.matchdict: {}'.format(request.matchdict))

    db_argument: Argument = request.validated['argument']

    db_issue = request.validated['issue']
    db_user = request.validated['user']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    prepared_discussion = discussion.dont_know_argument(db_issue, db_user, db_argument, history, request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    append_extras_dict_during_justification_argument(request, db_user, db_issue, prepared_discussion)

    return prepared_discussion


@view_config(route_name='discussion_justify_argument', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}),
          valid_attitude, valid_relation)
def discussion_justify_argument(request) -> dict:
    """
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    Path: /discuss/{slug}/justify/{argument_id:\d+}/{attitude}/{relation}

    :param request: request of the web server
    :return: dict
    """
    logger('discussion_justify_argument', 'request.matchdict: {}'.format(request.matchdict))

    db_argument: Argument = request.validated['argument']
    db_issue = request.validated['issue']
    db_user = request.validated['user']
    attitude = request.validated['attitude']
    relation = request.validated['relation']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    prepared_discussion = discussion.justify_argument(db_issue, db_user, db_argument, attitude, relation, history,
                                                      request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    append_extras_dict_during_justification_argument(request, db_user, db_issue, prepared_discussion)

    return prepared_discussion


@view_config(route_name='discussion_reaction', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_reaction_arguments, valid_relation)
def discussion_reaction(request):
    """
    View configuration for discussion step, where we will ask the user for her reaction (support, undercut, rebut)...

    Path: /discuss/{slug}/reaction/{arg_id_user:\d+}/{relation}/{arg_id_sys:\d+}

    :param request: request of the web server
    :return: dictionary
    """
    logger('discussion_reaction', 'request.validated: {}'.format(request.validated))

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    prepared_discussion = discussion.reaction(db_issue, db_user,
                                              request.validated['arg_user'],
                                              request.validated['arg_sys'],
                                              request.validated['relation'],
                                              history, request.path)
    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, True)

    return prepared_discussion


@view_config(route_name='discussion_support', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_support)
def discussion_support(request):
    """
    View configuration for discussion step, where we will present another supportive argument.

    :param request: request of the web server
    :return: dictionary
    """
    logger('discussion_support', 'request.matchdict: {}'.format(request.matchdict))

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)
    prepared_discussion = discussion.support(db_issue, db_user,
                                             request.validated['arg_user'],
                                             request.validated['arg_sys'],
                                             history, request.path)
    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion


@view_config(route_name='discussion_finish', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}))
def discussion_finish(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    logger('discussion_finish', 'request.matchdict: {}'.format(request.matchdict))

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.finish(db_issue,
                                            db_user,
                                            request.validated['argument'],
                                            history)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, prepare_request_dict(request), request.authenticated_userid, True)

    return prepared_discussion


@view_config(route_name='discussion_exit', renderer='../templates/exit.pt', permission='use')
@validate(check_authentication, valid_user_optional)
def discussion_exit(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    match_dict = request.matchdict
    logger('discussion_exit', 'request.matchdict: {}'.format(match_dict))

    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    dh = DictionaryHelper(get_language_from_cookie(request))
    prepared_discussion = discussion.exit(get_language_from_cookie(request), db_user)
    prepared_discussion['extras'] = dh.prepare_extras_dict_for_normal_page(request.registry, request.application_url,
                                                                           request.path, db_user)
    prepared_discussion['language'] = str(get_language_from_cookie(request))
    prepared_discussion['show_summary'] = len(prepared_discussion['summary']) != 0
    return prepared_discussion


@view_config(route_name='discussion_choose', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_issue_by_slug, valid_premisegroup_in_path,
          valid_list_of_premisegroups_in_path, has_keywords_in_path(('is_argument', bool), ('is_supportive', bool)))
def discussion_choose(request):
    """
    View configuration for discussion step, where the user has to choose between given statements.

    :param request: request of the web server
    :return: dictionary
    """
    # '/discuss/{slug}/choose/{is_argument}/{supportive}/{id}*pgroup_ids'
    match_dict = request.matchdict
    logger('discussion_choose', 'request.matchdict: {}'.format(match_dict))

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.choose(db_issue, db_user,
                                            request.validated['is_argument'],
                                            request.validated['is_supportive'],
                                            request.validated['pgroup_uid'],
                                            request.validated['pgroup_uids'],
                                            history, request.path)

    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion


@view_config(route_name='discussion_jump', renderer='../templates/discussion.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}))
def discussion_jump(request):
    """
    View configuration for the jump view.

    :param request: request of the web server
    :return: dictionary
    """
    # '/discuss/{slug}/jump/{arg_id}'

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.jump(db_issue, db_user, request.validated['argument'], history, request.path)

    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion

# ####################################
# REVIEW                             #
# ####################################

# index page for reviews


# content page for reviews


# history page for reviews


# history page for reviews


# reputation_borders page for reviews
