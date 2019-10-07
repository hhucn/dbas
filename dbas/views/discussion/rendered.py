import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from dbas.auth.login import oauth_providers
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument, User
from dbas.discussion import core as discussion
from dbas.events import ParticipatedInDiscussion, UserArgumentAgreement
from dbas.handler import issue as issue_handler, history as history_handler
from dbas.handler.history import SessionHistory
from dbas.handler.issue import get_issues_overview_for
from dbas.handler.language import get_language_from_cookie
from dbas.helper.decoration import prep_extras_dict
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.lib import nick_of_anonymous_user
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.validators.common import check_authentication
from dbas.validators.core import validate
from dbas.validators.discussion import valid_issue_by_slug, valid_statement, valid_attitude, valid_argument, \
    valid_relation, valid_reaction_arguments, valid_support, valid_list_of_premisegroups_in_path, valid_history_object
from dbas.validators.user import valid_user_optional
from dbas.views.helper import main_dict, modify_discussion_url, modify_discussion_bubbles, prepare_request_dict, \
    append_extras_dict, append_extras_dict_during_justification_statement, \
    append_extras_dict_during_justification_argument, modifiy_issue_main_url

LOG = logging.getLogger(__name__)


def emit_participation(request: Request):
    if request.validated['user'] and request.validated['issue']:
        event = ParticipatedInDiscussion(request.validated['user'], request.validated['issue'])
        request.registry.notify(event)


def emit_agreement_with_argument(request: Request):
    if request.validated['user'] and request.validated['argument']:
        event = UserArgumentAgreement(request.validated['user'], request.validated['argument'])
        request.registry.notify(event)


@view_config(route_name='discussion_overview', renderer='../../templates/discussion/myoverview.pt', permission='use')
@validate(check_authentication, prep_extras_dict, valid_user_optional)
def discussion_overview(request):
    """

    :param request: current request of the server
    :return: dictionary with title and project name as well as a value whether the user is logged in
    """
    LOG.debug("Return a discussion overview dictionary")
    ui_locales = get_language_from_cookie(request)
    issue_dict = get_issues_overview_for(request.validated['user'], request.application_url)

    prep_dict = main_dict(request, Translator(ui_locales).get(_.myDiscussions))
    modifiy_issue_main_url(issue_dict)

    prep_dict.update({
        'issues': issue_dict
    })
    return prep_dict


@view_config(route_name='discussion_start', renderer='../../templates/discussion/start.pt', permission='everybody')
@view_config(route_name='discussion_start_with_slash', renderer='../../templates/discussion/start.pt',
             permission='everybody')
@validate(check_authentication, valid_user_optional, prep_extras_dict)
def start(request):
    """
    View configuration for the initial discussion overview.

    :param request: request of the web server
    :return: dictionary
    """
    LOG.debug("Return configuration for initial discussion overview")
    ui_locales = get_language_from_cookie(request)
    issue_dict = issue_handler.get_issues_overview_on_start(request.validated['user'])
    prep_dict = main_dict(request, Translator(ui_locales).get(_.discussionStart))

    prep_dict.update(issue_dict)
    return prep_dict


@view_config(route_name='discussion_init_with_slug', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@view_config(route_name='discussion_init_with_slug_with_slash', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@validate(check_authentication, valid_issue_by_slug, valid_user_optional)
def init(request):
    """
    View configuration for the initial discussion.

    :param request: request of the web server
    :return: dictionary
    """
    LOG.debug("Configuration for initial discussion. %s", request.matchdict)
    emit_participation(request)

    prepared_discussion = discussion.init(request.validated['issue'], request.validated['user'])
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    session_history = SessionHistory()
    request.session.update({'session_history': session_history})

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


@view_config(route_name='discussion_attitude', renderer='../../templates/discussion/main.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_statement(location='path', depends_on={valid_issue_by_slug}),
          valid_history_object)
def attitude(request):
    """
    View configuration for discussion step, where we will ask the user for her attitude towards a statement.
    Route: /discuss/{slug}/attitude/{position_id}

    :param request: request of the web server
    :return: dictionary
    """
    LOG.debug("View attitude: %s", request.matchdict)
    emit_participation(request)

    db_statement = request.validated['statement']
    db_issue = request.validated['issue']
    db_user = request.validated['user']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.attitude(db_issue, db_user, db_statement, session_history, request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    rdict = prepare_request_dict(request)

    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion


@view_config(route_name='discussion_justify_statement', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@validate(check_authentication, valid_user_optional, valid_statement(location='path', depends_on={valid_issue_by_slug}),
          valid_attitude, valid_history_object)
def justify_statement(request) -> dict:
    r"""
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    Path: /discuss/{slug}/justify/{statement_id:\d+}/{attitude}

    :param request: request of the web server
    :return: dict
    """
    LOG.debug("Justify a statement. %s", request.matchdict)
    emit_participation(request)

    db_statement: Statement = request.validated['statement']

    db_issue = request.validated['issue']
    db_user = request.validated['user']
    inner_attitude = request.validated['attitude']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.justify_statement(db_issue, db_user, db_statement, inner_attitude, session_history,
                                                       request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    append_extras_dict_during_justification_statement(request, db_user, db_issue, db_statement, prepared_discussion,
                                                      inner_attitude)

    return prepared_discussion


@view_config(route_name='discussion_dontknow_argument', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}),
          valid_history_object)
def dontknow_argument(request) -> dict:
    r"""
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    Path: /discuss/{slug}/justify/{argument_id:\d+}/dontknow}

    :param request: request of the web server
    :return: dict
    """
    LOG.debug("Do not know an argument for this step. %s", request.matchdict)
    emit_participation(request)

    db_argument: Argument = request.validated['argument']

    db_issue = request.validated['issue']
    db_user = request.validated['user']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.dont_know_argument(db_issue, db_user, db_argument, session_history, request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    append_extras_dict_during_justification_argument(request, db_user, db_issue, prepared_discussion)

    return prepared_discussion


@view_config(route_name='discussion_justify_argument', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}),
          valid_attitude, valid_relation, valid_history_object)
def justify_argument(request) -> dict:
    r"""
    View configuration for discussion step, where we will ask the user for her a justification of her opinion/interest.

    Path: /discuss/{slug}/justify/{argument_id:\d+}/{attitude}/{relation}

    :param request: request of the web server
    :return: dict
    """
    LOG.debug("Justify an argument. %s", request.matchdict)
    emit_participation(request)

    db_argument: Argument = request.validated['argument']
    db_issue = request.validated['issue']
    db_user = request.validated['user']
    inner_attitude = request.validated['attitude']
    relation = request.validated['relation']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.justify_argument(db_issue, db_user, db_argument, inner_attitude, relation,
                                                      session_history,
                                                      request.path)
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    append_extras_dict_during_justification_argument(request, db_user, db_issue, prepared_discussion)

    return prepared_discussion


@view_config(route_name='discussion_reaction', renderer='../../templates/discussion/main.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_reaction_arguments, valid_relation, valid_history_object)
def reaction(request):
    r"""
    View configuration for discussion step, where we will ask the user for her reaction (support, undercut, rebut)...

    Path: /discuss/{slug}/reaction/{arg_id_user:\d+}/{relation}/{arg_id_sys:\d+}

    :param request: request of the web server
    :return: dictionary
    """
    LOG.debug("React to a step. %s", request.validated)
    emit_participation(request)

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.reaction(db_issue, db_user,
                                              request.validated['arg_user'],
                                              request.validated['arg_sys'],
                                              request.validated['relation'],
                                              session_history, request.path)
    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, True)

    return prepared_discussion


@view_config(route_name='discussion_support', renderer='../../templates/discussion/main.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_support, valid_history_object)
def support(request):
    """
    View configuration for discussion step, where we will present another supportive argument.

    :param request: request of the web server
    :return: dictionary
    """
    LOG.debug("Support a statement. %s", request.matchdict)
    emit_participation(request)

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.support(db_issue, db_user,
                                             request.validated['arg_user'],
                                             request.validated['arg_sys'],
                                             session_history, request.path)
    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion


@view_config(route_name='discussion_finish', renderer='../../templates/discussion/main.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}),
          valid_history_object)
def finish(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    LOG.debug("Finish the discussion. %s", request.matchdict)
    emit_participation(request)
    emit_agreement_with_argument(request)

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    if session_history is not None:
        LOG.debug(vars(request.validated['session_history']))

    prepared_discussion = discussion.finish(db_issue,
                                            db_user,
                                            request.validated['argument'],
                                            session_history)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, prepare_request_dict(request), request.authenticated_userid, True)

    return prepared_discussion


@view_config(route_name='discussion_exit', renderer='../../templates/discussion/exit.pt', permission='use')
@validate(check_authentication, valid_user_optional)
def dexit(request):
    """
    View configuration for discussion step, where we present a small/daily summary on the end

    :param request: request of the web server
    :return:
    """
    LOG.debug("Exit discussion. %s", request.matchdict)

    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
    dh = DictionaryHelper(get_language_from_cookie(request))
    prepared_discussion = discussion.exit(get_language_from_cookie(request), db_user)
    prepared_discussion['extras'] = dh.prepare_extras_dict_for_normal_page(request.registry, request.application_url,
                                                                           request.path, db_user)
    prepared_discussion['language'] = str(get_language_from_cookie(request))
    prepared_discussion['show_summary'] = len(prepared_discussion['summary']) != 0
    prepared_discussion['discussion'] = {'broke_limit': False}
    return prepared_discussion


@view_config(route_name='discussion_choose', renderer='../../templates/discussion/main.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_issue_by_slug, valid_list_of_premisegroups_in_path,
          valid_history_object)
def choose(request):
    """
    View configuration for discussion step, where the user has to choose between given statements.

    This step is shown when the user has given multiple reasons at the same time for/against a statement. The
    corresponding premisegroup ids are given in the url.

    :param request: request of the web server
    :return: dictionary
    """
    # '/discuss/{slug}/choose/*pgroup_ids'
    LOG.debug("Choose a statement. %s", request.matchdict)
    emit_participation(request)

    db_user: User = request.validated['user']
    db_issue = request.validated['issue']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.choose(db_issue, db_user,
                                            request.validated['pgroup_uids'],
                                            session_history, request.path)

    rdict = prepare_request_dict(request)

    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)

    return prepared_discussion


@view_config(route_name='discussion_jump', renderer='../../templates/discussion/main.pt', permission='everybody')
@validate(check_authentication, valid_user_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}),
          valid_history_object)
def jump(request):
    """
    View configuration for the jump view.

    :param request: request of the web server
    :return: dictionary
    """
    emit_participation(request)

    db_user = request.validated['user']
    db_issue = request.validated['issue']

    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.jump(db_issue, db_user, request.validated['argument'], session_history,
                                          request.path)

    rdict = prepare_request_dict(request)

    if not request.validated.get("from_api", False):
        modify_discussion_url(prepared_discussion)

    modify_discussion_bubbles(prepared_discussion, request.registry)
    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, True)

    return prepared_discussion
