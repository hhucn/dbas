"""Introducing an API to enable external discussions.

This is the entry point for the API. Here are views defined, which always
return JSON objects which can then be used in external websites.

.. note:: Methods **must not** have the same name as their assigned Service.
"""
import logging
from typing import List

from cornice import Service
from cornice.resource import resource, view
from pyramid.httpexceptions import HTTPSeeOther, HTTPUnauthorized, HTTPBadRequest, HTTPNotFound, HTTPCreated, \
    HTTPException
from pyramid.interfaces import IRequest
from pyramid.request import Request

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
from api.lib import extract_items_and_bubbles, flatten, split_url, shallow_patch
from api.models import DataItem, DataBubble, DataReference, DataOrigin
from api.origins import add_origin_for_list_of_statements
from dbas.auth.login import register_user_with_json_data
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, User, Argument, StatementToIssue, StatementReference
from dbas.events import UserStatementAttitude
from dbas.handler.arguments import set_arguments_premises
from dbas.handler.statements import set_positions_premise, set_position
from dbas.handler.user import set_new_oauth_user
from dbas.lib import (get_all_arguments_by_statement,
                      get_text_for_argument_uid, create_speechbubble_dict, BubbleTypes,
                      Attitudes, Relations)
from dbas.strings.matcher import get_all_statements_matching
from dbas.strings.translator import Keywords as _, get_translation, Translator
from dbas.validators.common import valid_q_parameter, valid_language
from dbas.validators.core import has_keywords_in_json_path, validate, has_maybe_keywords, has_keywords_in_path
from dbas.validators.discussion import valid_issue_by_slug, valid_position, valid_statement, valid_attitude, \
    valid_reason_and_position_not_equal, \
    valid_argument, valid_relation, valid_reaction_arguments, valid_new_position_in_body, valid_reason_in_body, \
    valid_support, valid_new_issue, valid_history_object
from dbas.validators.eden import valid_optional_origin
from dbas.views import jump, emit_participation
from dbas.views.discussion.json import create_issue_after_validation
from .login import validate_credentials, valid_token, valid_token_optional, valid_api_token, check_jwt, encode_payload
from .references import (get_all_references_by_reference,
                         store_reference)

LOG = logging.getLogger(__name__)

#
# CORS configuration
#
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'X-Authentication'),
                   origins=('*',),
                   credentials=True,  # TODO: how can I use this?
                   max_age=42)

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

ahello = Service(name='hello',
                 path='/hello',
                 description="Say hello to remote users",
                 cors_policy=cors_policy)

whoami = Service(name='whoami',
                 path='/whoami',
                 description='Send nickname and token to D-BAS and validate yourself',
                 cors_policy=cors_policy)

# Argumentation stuff
reaction = Service(name='api_reaction',
                   path='/{slug}/reaction/{arg_id_user}/{relation}/{arg_id_sys}',
                   description='Discussion Reaction',
                   cors_policy=cors_policy)

justify_statement = Service(name='api_justify_statement',
                            path=r'/{slug}/justify/{statement_id:\d+}/{attitude:(' + '|'.join(
                                map(str, Attitudes)) + ')}',
                            description='Discussion Justify',
                            cors_policy=cors_policy)

dontknow_argument = Service(name='api_dontknow_argument',
                            path=r'/{slug}/justify/{argument_id:\d+}/dontknow',
                            description='Discussion Dont Know',
                            cors_policy=cors_policy)

justify_argument = Service(name='api_justify_argument',
                           path=r'/{slug}/justify/{argument_id:\d+}' +
                                r'/{attitude:(' + '|'.join(map(str, Attitudes)) + ')}' +
                                r'/{relation:(' + '|'.join(map(str, Relations)) + ')}',
                           description='Discussion Justify',
                           cors_policy=cors_policy)

attitude = Service(name='api_attitude',
                   path=r'/{slug}/attitude/{position_id:\d+}',
                   description='Discussion Attitude',
                   cors_policy=cors_policy)

statement_attitude = Service(name='api_statement_attitude',
                             path=r'/attitude/{statement_id:\d+}/{attitude:(' + '|'.join(
                                 map(str, Attitudes)) + ')}',
                             description='Save Attitude to Statement',
                             cors_policy=cors_policy)

finish = Service(name='api_finish',
                 path=r'/{slug}/finish/{argument_id:\d+}',
                 description='End of a discussion',
                 cors_policy=cors_policy)

support = Service(name='api_support',
                  path=r'/{slug}/support/{arg_id_user:\d+}/{arg_id_sys:\d+}',
                  description='Discussion Support',
                  cors_policy=cors_policy)

# add new stuff
positions = Service(name='Positions',
                    path='/{slug}/positions',
                    description='Positions of a specific issue',
                    cors_policy=cors_policy)

issue = Service(name="issue",
                path="/issue",
                description="Adds a new issue",
                cors_policy=cors_policy)

# Prefix with 'z' so it is added as the last route
zinit = Service(name='api_init',
                path='/{slug}',
                description="Discussion Init",
                cors_policy=cors_policy)

#
# Get data from D-BAS' database
#
references = Service(name="references",
                     path="/references",
                     description="Query database to get stored references from site",
                     cors_policy=cors_policy)

reference_usages = Service(name="reference_usages",
                           path="/reference/usages/{ref_uid}",
                           description="Return dict containing all information about the usages of this reference",
                           cors_policy=cors_policy)

find_statements = Service(name="find_statements",
                          path="/search",
                          description="Query database to get closest statements",
                          cors_policy=cors_policy)

#
# Build text-blocks
#
text_for_argument = Service(name="argument_text_block",
                            path="/get/argument/texts/{lang}/{statement_uid}",
                            description="Get textblock for argument as seen in the bubbles",
                            cors_policy=cors_policy)

#
# Jump into the discussion
#
jump_to_zargument = Service(name="jump_to_argument",  # Need this 'z' to call this after the other jumps
                            path="/{slug}/jump/{argument_id}",
                            description="Jump to an argument",
                            cors_policy=cors_policy)

#
# User Management
#
login = Service(name='login',
                path='/login',
                description="Log into external discussion system",
                cors_policy=cors_policy)

local_user_registration = Service(name="local_user_registration",
                                  path="/user",
                                  description="Register a new user",
                                  cors_policy=cors_policy)


# =============================================================================
# SYSTEM: Say hello to new visitors
# =============================================================================


@ahello.get()
def hello(_):
    """
    Return data from DBas discussion_reaction page.

    :return: dbas.discussion_reaction(True)
    """
    return {
        "status": "ok",
        "message": "Connection established. \"Back when PHP had less than 100 functions and the function hashing "
                   "mechanism was strlen()\" -- Author of PHP"
    }


@whoami.get()
@validate(valid_token)
def whoami_fn(request):
    """
    Test-route to validate token and nickname from headers.

    :return: welcome-dict
    """
    nickname = request.validated["user"].nickname
    return {
        "status": "ok",
        "nickname": nickname,
        "message": "Hello " + nickname + ", nice to meet you."
    }


# =============================================================================
# DISCUSSION-RELATED REQUESTS
# =============================================================================

@positions.get()
@zinit.get()
@validate(valid_issue_by_slug)
def discussion_init(request):
    """
    Given a slug, show its positions.

    :param request: Request
    :return:
    """
    db_issue: Issue = request.validated['issue']
    intro = get_translation(_.initialPositionInterest, db_issue.lang)

    bubbles: List[DataBubble] = [
        create_speechbubble_dict(BubbleTypes.SYSTEM, uid='start', content=intro, omit_bubble_url=True,
                                 lang=db_issue.lang)
    ]

    issues_statements = [el.statement_uid for el in
                         DBDiscussionSession.query(StatementToIssue).filter_by(issue_uid=db_issue.uid).all()]
    db_positions = DBDiscussionSession.query(Statement).filter(Statement.is_disabled == False,
                                                               Statement.uid.in_(issues_statements),
                                                               Statement.is_position == True).all()

    positions = [DataItem([pos.get_textversion().content], "/{}/attitude/{}".format(db_issue.slug, pos.uid))
                 for pos in db_positions]

    return {
        'bubbles': [DataBubble(bubble) for bubble in bubbles],
        'positions': positions
    }


@attitude.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_position, valid_history_object)
def discussion_attitude(request):
    """
    Return data from DBas discussion_attitude page.

    /{slug}/attitude/{position_id}

    :param request: request
    :return: dbas.discussion_attitude(True)
    """
    db_position = request.validated['position']
    db_issue = request.validated['issue']
    db_user = request.validated['user']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.attitude(db_issue, db_user, db_position, session_history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attitudes': dict(zip(keys, items))
    }


@justify_statement.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_statement(location='path'), valid_attitude,
          valid_history_object)
def discussion_justify_statement(request) -> dict:
    """
    Pick attitude from path and query the statement. Show the user some statements to follow the discussion.

    Path: /{slug}/justify/{statement_id}/{attitude}

    :param request: request
    :return: dict
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.justify_statement(db_issue, db_user, request.validated['statement'],
                                                       request.validated['attitude'], session_history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    return {
        'bubbles': bubbles,
        'items': items
    }


@dontknow_argument.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_argument(location='path'), valid_history_object)
def discussion_dontknow_argument(request) -> dict:
    """
    Dont know an argument.

    /{slug}/justify/{argument_id}/dontknow

    :param request:
    :return:
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.dont_know_argument(db_issue, db_user, request.validated['argument'],
                                                        session_history,
                                                        request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attacks': dict(zip(keys, items))
    }


@justify_argument.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_argument(location='path'), valid_attitude, valid_relation,
          valid_history_object)
def discussion_justify_argument(request) -> dict:
    """
    Justify an argument. Attitude and relation are important to show the correct items for the user.

    /{slug}/justify/{argument_id}/{attitude}/{relation}

    :param request:
    :return:
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.justify_argument(db_issue, db_user, request.validated['argument'],
                                                      request.validated['attitude'], request.validated['relation'],
                                                      session_history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    return {
        'bubbles': bubbles,
        'items': items
    }


@reaction.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_reaction_arguments, valid_relation, valid_history_object)
def discussion_reaction(request):
    """
    Return data from DBas discussion_reaction page.

    Path: /{slug}/reaction/{arg_id_user}/{relation}/{arg_id_sys}

    :param request: request
    :return: bubbles for information and items for the next step
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.reaction(db_issue, db_user,
                                              request.validated['arg_user'],
                                              request.validated['arg_sys'],
                                              request.validated['relation'],
                                              session_history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attacks': dict(zip(keys, items))
    }


@support.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_support, valid_history_object)
def discussion_support(request):
    """
    View configuration for discussion step, where we will present another supportive argument.

    Path: /{slug}/support/{arg_id_user}/{arg_id_sys}

    :param request: request
    :return: bubbles for information and items for the next step
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

    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attacks': dict(zip(keys, items))
    }


@finish.get()
@validate(valid_token_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}), valid_history_object)
def discussion_finish(request):
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    prepared_discussion = discussion.finish(db_issue, db_user,
                                            request.validated['argument'], session_history)

    return {'bubbles': extract_items_and_bubbles(prepared_discussion)[0]}


# =============================================================================
# REFERENCES - Get references from database
# =============================================================================

@references.get()
@validate(has_keywords_in_path(('host', str), ('path', str), location="params"))
def get_references(request: Request):
    """
    Query database to get stored references from site. Generate a list with text versions of references.

    :param request: request
    :return: References assigned to the queried URL
    """
    host = request.validated["host"]
    path = request.validated["path"]
    LOG.debug("Querying references for host: {}, path: {}".format(host, path))
    refs_db: List[StatementReference] = DBDiscussionSession.query(StatementReference).filter_by(host=host,
                                                                                                path=path).all()
    return {
        "references": [DataReference(ref) for ref in refs_db]
    }


@reference_usages.get()
@validate(has_keywords_in_path(('ref_uid', int)))
def get_reference_usages(request: Request):
    """
    Return a JSON object containing all information about the stored reference and its usages.

    :param request:
    :return: JSON with all information about the stored reference
    :rtype: list
    """
    ref_uid = request.validated["ref_uid"]
    LOG.debug(f"Retrieving reference usages for ref_uid {ref_uid}")
    db_ref: StatementReference = DBDiscussionSession.query(StatementReference).get(ref_uid)
    if db_ref:
        return get_all_references_by_reference(db_ref)
    return HTTPNotFound("Reference could not be found")


# =============================================================================
# USER MANAGEMENT
# =============================================================================

@login.post(require_csrf=False)
@validate(has_keywords_in_json_path(('nickname', str), ('password', str)), validate_credentials)
def user_login(request):
    """
    Check provided credentials and return a token, if it is a valid user. The function body is only executed,
    if the validator added a request.validated field.

    :param request:
    :return: token and nickname
    """
    user: User = request.validated['user']
    LOG.debug('User authenticated: {}'.format(user.public_nickname))
    return {
        'nickname': user.public_nickname,
        'uid': user.uid,
        'token': request.validated['token']
    }


# =============================================================================
# FINDING STATEMENTS
# =============================================================================

@find_statements.get()
@validate(valid_q_parameter)
def find_statements_fn(request):
    """
    Receives search requests, queries database to find all occurrences and returns these results with the correct URL
    to get directly access to the location in the discussion.

    :param request:
    :return: json conform dictionary of all occurrences
    """
    query_string = request.validated['query']

    return {
        "results": get_all_statements_matching(query_string)
    }


# =============================================================================
# JUMPING - jump to specific position in the discussion
# =============================================================================

@jump_to_zargument.get()
@validate(valid_argument(location='path', depends_on={valid_issue_by_slug}))
def jump_to_argument_fn(request):
    """
    Jump directly to an argument to provoke user interaction.

    :param request:
    :return: Argument with a list of possible interactions
    """
    request.validated["from_api"] = True
    response = jump(request)
    bubbles, items = extract_items_and_bubbles(response)
    return {
        'bubbles': bubbles,
        'items': items
    }


# =============================================================================
# TEXT BLOCKS - create text-blocks as seen in the bubbles
# =============================================================================

@text_for_argument.get()
def get_text_for_argument(request):
    statement = int(request.matchdict["statement_uid"])
    args = get_all_arguments_by_statement(statement)
    return list(map(lambda arg: {"uid": arg.uid, "text": get_text_for_argument_uid(arg.uid)}, args))


# =============================================================================
# GET INFORMATION - several functions to get information from the database
# =============================================================================


@resource(collection_path='/issues', path=r'/issues/{slug:[a-z0-9]+(?:-[a-z0-9]+)*}', cors_policy=cors_policy)
class ApiIssue(object):
    modifiable = frozenset({"title", "info", "long_info"})

    def __init__(self, request, context=None):
        self.request: Request = request

    def get(self):
        return self._get(self.request)

    @staticmethod
    @validate(valid_issue_by_slug)
    def _get(request):
        return request.validated['issue']

    @view(require_csrf=False)
    def patch(self):
        return self._patch(self.request)

    @staticmethod
    @validate(valid_token, valid_issue_by_slug)
    def _patch(request: Request):
        db_issue: Issue = request.validated['issue']
        db_user: User = request.validated['user']
        if db_user.is_admin() or db_user is db_issue.author:
            shallow_patch(db_issue, request.json_body, allowed_fields=ApiIssue.modifiable)
            return db_issue
        else:
            return HTTPUnauthorized()

    def collection_get(self):
        return DBDiscussionSession.query(Issue).filter(Issue.is_disabled == False,
                                                       Issue.is_private == False).all()


# -----------------------------------------------------------------------------
# Posts

def _join_list_to_string(list_of_strings) -> str:
    return ", ".join(str(elem) for elem in list_of_strings)


def _http_see_other_with_cors_header(location: str) -> HTTPSeeOther:
    """
    Add CORS Headers to HTTPSeeOther response.

    :param location: URL to route to
    :return: HTTPSeeOther with CORS Header
    """
    return HTTPSeeOther(
        location=location,
        headers={
            'Access-Control-Allow-Origin': _join_list_to_string(cors_policy.get('origins')),
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, HEAD',
            'Access-Control-Allow-Headers': _join_list_to_string(cors_policy.get('headers')),
        }
    )


def _store_origin_and_reference(db_issue: Issue, db_user: User, origin: DataOrigin, host: str, path: str,
                                reference_text: str, statement_uids: List[int]):
    """
    Takes all newly created statements and stores the reference and origin for it, if provided.
    """
    if reference_text:
        for statement_uid in statement_uids:
            LOG.info("Assigning reference to statement_uid %s", statement_uid)
            db_new_statement: Statement = DBDiscussionSession.query(Statement).get(statement_uid)
            store_reference(reference_text, host, path, db_user, db_new_statement, db_issue)
    if origin:
        add_origin_for_list_of_statements(origin, statement_uids)


# -----------------------------------------------------------------------------

@zinit.post(require_csrf=False)
@positions.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_new_position_in_body, valid_reason_in_body,
          valid_reason_and_position_not_equal, has_maybe_keywords(('reference', str, None)), valid_optional_origin,
          valid_history_object)
def add_position_with_premise(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    reference_text: str = request.validated['reference']
    origin: DataOrigin = request.validated['origin']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')
    host, path = split_url(request.environ.get("HTTP_REFERER"))

    new_position = set_position(db_user, db_issue, request.validated['position-text'])

    if new_position['errors']:
        return new_position['errors']

    conclusion_id: int = new_position['statement_uids'][0]
    db_conclusion: Statement = DBDiscussionSession.query(Statement).get(conclusion_id)

    pd = set_positions_premise(db_issue, db_user, db_conclusion, [[request.validated['reason-text']]], True,
                               session_history,
                               request.mailer)

    if pd['error']:
        LOG.debug(f"Errors occurred in prepared_dictionary: {pd['error']}")
        return HTTPBadRequest(pd["error"])

    statement_uids: List[int] = flatten(pd['statement_uids'])
    LOG.info("Created %d statements: %s", len(statement_uids), statement_uids)
    _store_origin_and_reference(db_issue, db_user, origin, host, path, reference_text, statement_uids)

    if origin:
        add_origin_for_list_of_statements(origin, new_position['statement_uids'])
        add_origin_for_list_of_statements(origin, flatten(pd['statement_uids']))

    return _http_see_other_with_cors_header('/api' + pd['url'])


@justify_statement.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_reason_in_body, valid_statement(location="path"),
          valid_attitude, has_maybe_keywords(('reference', str, None)), valid_optional_origin, valid_history_object)
def add_premise_to_statement(request: IRequest):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    db_statement: Statement = request.validated['statement']
    reference_text: str = request.validated['reference']
    is_supportive = request.validated['attitude'] == Attitudes.AGREE
    origin: DataOrigin = request.validated['origin']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    host, path = split_url(request.environ.get("HTTP_REFERER"))

    pd = set_positions_premise(db_issue, db_user, db_statement, [[request.validated['reason-text']]], is_supportive,
                               session_history, request.mailer)

    _store_origin_and_reference(db_issue, db_user, origin, host, path, reference_text, flatten(pd['statement_uids']))

    return _http_see_other_with_cors_header('/api' + pd['url'])


@justify_argument.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_reason_in_body, valid_argument(location="path"), valid_relation,
          valid_attitude, has_maybe_keywords(('reference', str, None)), valid_optional_origin, valid_history_object)
def add_premise_to_argument(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    db_argument: Argument = request.validated['argument']
    reference_text: str = request.validated['reference']
    relation: Relations = request.validated['relation']
    origin: DataOrigin = request.validated['origin']
    history_handler.save_and_set_cookie(request, db_user, db_issue)
    session_history = request.validated.get('session_history')

    host, path = split_url(request.environ.get("HTTP_REFERER"))

    if reference_text:
        for premise in db_argument.premisegroup.premises:
            store_reference(reference_text, host, path, db_user, premise.statement, db_issue)

    pd = set_arguments_premises(db_issue, db_user, db_argument, [[request.validated['reason-text']]], relation,
                                session_history, request.mailer)

    _store_origin_and_reference(db_issue, db_user, origin, host, path, reference_text, pd['statement_uids'])

    return _http_see_other_with_cors_header('/api' + pd['url'])


@statement_attitude.post(require_csrf=False)
@validate(valid_token, valid_statement(location="path"), valid_attitude)
def add_statement_attitude(request):
    db_user: User = request.validated['user']
    db_statement: Statement = request.validated['statement']
    is_supportive = request.validated['attitude'] == Attitudes.AGREE

    event = UserStatementAttitude(db_user, db_statement, is_supportive)
    request.registry.notify(event)

    return HTTPCreated()


@issue.post(require_csrf=False)
@validate(valid_token, valid_language, valid_new_issue,
          has_keywords_in_json_path(('is_public', bool), ('is_read_only', bool)))
def add_issue(request):
    # set_new_issue already checks for validity of mandatory fields in json
    return create_issue_after_validation(request)


@resource(collection_path='/users', path=r'/users/{id:\d+}', cors_policy=cors_policy)
class ApiUser(object):
    def __init__(self, request, context=None):
        self.request = request

    @staticmethod
    def external_view(db_user: User):
        return {
            'id': db_user.uid,
            'nickname': db_user.public_nickname
        }

    def get(self):
        db_user: User = DBDiscussionSession.query(User).get(int(self.request.matchdict['id']))
        if db_user:
            return ApiUser.external_view(db_user)
        else:
            self.request.response.status = 404
            return "This user-id does not exist."

    @staticmethod
    def collection_get():
        db_users: List[User] = DBDiscussionSession.query(User).all()
        return [ApiUser.external_view(db_user) for db_user in db_users]

    @view(require_csrf=False)
    def collection_post(self):
        return self._collection_post(self.request)

    @staticmethod
    @validate(valid_api_token,
              has_keywords_in_json_path(('firstname', str), ('lastname', str), ('nickname', str), ('email', str),
                                        ('gender', str),
                                        ('id', int), ('locale', str), ('service', str)))
    def _collection_post(request):
        result = set_new_oauth_user(request.json_body,
                                    request.json_body['id'],
                                    request.json_body['service'],
                                    Translator(request.json_body['locale']))

        if result["success"]:
            request.response.status = 201
            return {"id": result["user"].uid}
        else:
            request.response.status = 400
            return result["error"]


@local_user_registration.post(require_csrf=False)
@validate(valid_token,
          has_keywords_in_json_path(('firstname', str), ('lastname', str), ('nickname', str), ('email', str),
                                    ('gender', str), ('password', str), ('lang', str)))
def user_registration(request: Request) -> HTTPException:
    LOG.debug(f"Register new user {request.validated['nickname']} via API.")
    mailer = request.mailer

    request.validated["passwordconfirm"] = request.validated["password"]
    success_message, error_message, _ = register_user_with_json_data(request.validated, request.validated["lang"],
                                                                     mailer)

    if success_message:
        return HTTPCreated(detail=success_message)
    else:
        return HTTPBadRequest(detail=error_message)


@resource(path=r'/pubkey')
class PubKey(object):
    def __init__(self, request, context=None):
        self.request: Request = request

    def get(self):
        response = self.request.response
        response.content_type = "text/plain"
        response.text = self.request.registry.settings["public_key"]
        return response


@resource(path=r'/refresh-token')
class TempToken():
    def __init__(self, request, context=None):
        self.request: Request = request
        self.secret = request.registry.settings['secret_key']

    @view(require_csrf=False)
    def post(self):
        return self._post(self.request)

    @staticmethod
    @validate(valid_api_token,
              has_keywords_in_json_path(('token', str)))
    def _post(request):
        token = request.json_body['token']

        if check_jwt(request, token):
            payload = request.validated['token-payload']
            if 'sub' in payload:
                del payload['sub']
                del payload['exp']

            del payload['iat']
            response = request.response
            response.content_type = "text/plain"
            response.text = encode_payload(request, payload)
            return response
