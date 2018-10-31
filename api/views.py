"""Introducing an API to enable external discussions.

This is the entry point for the API. Here are views defined, which always
return JSON objects which can then be used in external websites.

.. note:: Methods **must not** have the same name as their assigned Service.
"""
import logging
from typing import List

from cornice import Service
from cornice.resource import resource, view
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.interfaces import IRequest
from pyramid.request import Request

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
import dbas.views.discussion as dbas
from api.lib import extract_items_and_bubbles
from api.models import DataItem, DataBubble, DataReference
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, User, Argument, StatementToIssue, StatementReferences
from dbas.handler.arguments import set_arguments_premises
from dbas.handler.statements import set_positions_premise, set_position
from dbas.handler.user import set_new_oauth_user
from dbas.lib import (get_all_arguments_by_statement,
                      get_text_for_argument_uid, create_speechbubble_dict, BubbleTypes,
                      Attitudes, Relations)
from dbas.strings.matcher import get_all_statements_by_levensthein_similar_to
from dbas.strings.translator import Keywords as _, get_translation, Translator
from dbas.validators.common import valid_q_parameter
from dbas.validators.core import has_keywords, validate, has_maybe_keywords
from dbas.validators.discussion import valid_issue_by_slug, valid_position, valid_statement, valid_attitude, \
    valid_reason_and_position_not_equal, \
    valid_argument, valid_relation, valid_reaction_arguments, valid_new_position_in_body, valid_reason_in_body
from dbas.validators.eden import valid_optional_origin
from search.requester import get_statements_with_similarity_to
from .lib import logger
from .login import validate_credentials, valid_token, token_to_database, valid_token_optional, \
    valid_api_token
from .references import (get_all_references_by_reference_text,
                         get_reference_by_id, get_references_for_url, store_reference)
from .templates import error

log = logger()
LOG = logging.getLogger(__name__)

#
# CORS configuration
#
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'X-Authentication'),
                   origins=('*',),
                   credentials=True,  # TODO: how can i use this?
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
                            path='/{slug}/justify/{statement_id:\d+}/{attitude:(' + '|'.join(
                                map(str, Attitudes)) + ')}',
                            description='Discussion Justify',
                            cors_policy=cors_policy)

dontknow_argument = Service(name='api_dontknow_argument',
                            path='/{slug}/justify/{argument_id:\d+}/dontknow',
                            description='Discussion Dont Know',
                            cors_policy=cors_policy)

justify_argument = Service(name='api_justify_argument',
                           path='/{slug}/justify/{argument_id:\d+}' +
                                '/{attitude:(' + '|'.join(map(str, Attitudes)) + ')}' +
                                '/{relation:(' + '|'.join(map(str, Relations)) + ')}',
                           description='Discussion Justify',
                           cors_policy=cors_policy)

attitude = Service(name='api_attitude',
                   path='/{slug}/attitude/{position_id:\d+}',
                   description='Discussion Attitude',
                   cors_policy=cors_policy)

finish = Service(name='api_finish',
                 path='/{slug}/finish/{argument_id:\d+}',
                 description='End of a discussion',
                 cors_policy=cors_policy)

# add new stuff
positions = Service(name='Positions',
                    path='/{slug}/positions',
                    description='Positions of a specific issue',
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

issues = Service(name="issues",
                 path="/issues",
                 description="Get issues",
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
                            path="/{slug}/jump/{arg_uid}",
                            description="Jump to an argument",
                            cors_policy=cors_policy)

#
# User Management
#
login = Service(name='login',
                path='/login',
                description="Log into external discussion system",
                cors_policy=cors_policy)

logout = Service(name='logout',
                 path='/logout',
                 description="Logout user",
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
    db_issue = request.validated['issue']
    intro = get_translation(_.initialPositionInterest, db_issue.lang)

    bubbles = [
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
@validate(valid_issue_by_slug, valid_token_optional, valid_position)
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
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.attitude(db_issue, db_user, db_position, history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attitudes': dict(zip(keys, items))
    }


@justify_statement.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_statement(location='path'), valid_attitude)
def discussion_justify_statement(request) -> dict:
    """
    Pick attitude from path and query the statement. Show the user some statements to follow the discussion.

    Path: /{slug}/justify/{statement_id}/{attitude}

    :param request: request
    :return: dict
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.justify_statement(db_issue, db_user, request.validated['statement'],
                                                       request.validated['attitude'], history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    return {
        'bubbles': bubbles,
        'items': items
    }


@dontknow_argument.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_argument(location='path'))
def discussion_dontknow_argument(request) -> dict:
    """
    Dont know an argument.

    /{slug}/justify/{argument_id}/dontknow

    :param request:
    :return:
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    hist = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.dont_know_argument(db_issue, db_user, request.validated['argument'], hist,
                                                        request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attacks': dict(zip(keys, items))
    }


@justify_argument.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_argument(location='path'), valid_attitude, valid_relation)
def discussion_justify_argument(request) -> dict:
    """
    Justify an argument. Attitude and relation are important to show the correct items for the user.

    /{slug}/justify/{argument_id}/{attitude}/{relation}

    :param request:
    :return:
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.justify_argument(db_issue, db_user, request.validated['argument'],
                                                      request.validated['attitude'], request.validated['relation'],
                                                      history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    return {
        'bubbles': bubbles,
        'items': items
    }


@reaction.get()
@validate(valid_issue_by_slug, valid_token_optional, valid_reaction_arguments, valid_relation)
def discussion_reaction(request):
    """
    Return data from DBas discussion_reaction page.

    Path: /{slug}/reaction/{arg_id_user}/{relation}/{arg_id_sys}

    :param request: request
    :return: bubbles for information and items for the next step
    """
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.reaction(db_issue, db_user,
                                              request.validated['arg_user'],
                                              request.validated['arg_sys'],
                                              request.validated['relation'],
                                              history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    keys = [item['attitude'] for item in prepared_discussion['items']['elements']]

    return {
        'bubbles': bubbles,
        'attacks': dict(zip(keys, items))
    }


@finish.get()
@validate(valid_token_optional, valid_argument(location='path', depends_on={valid_issue_by_slug}))
def discussion_finish(request):
    db_user = request.validated['user']
    db_issue = request.validated['issue']
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    prepared_discussion = discussion.finish(db_issue, db_user,
                                            request.validated['argument'], history)

    return {'bubbles': extract_items_and_bubbles(prepared_discussion)[0]}


# =============================================================================
# REFERENCES - Get references from database
# =============================================================================

@references.get()
def get_references(request: Request):
    """
    Query database to get stored references from site. Generate a list with text versions of references.

    :param request: request
    :return: References assigned to the queried URL
    """
    host = request.host
    path = request.path
    log.debug("Querying references for host: {}, path: {}".format(host, path))
    refs_db: List[StatementReferences] = get_references_for_url(host, path)
    return {
        "references": [DataReference(ref) for ref in refs_db]
    }


@reference_usages.get()
def get_reference_usages(request: Request):
    """
    Return a JSON object containing all information about the stored reference and its usages.

    :param request:
    :return: JSON with all information about the stored reference
    :rtype: list
    """
    ref_uid = request.matchdict["ref_uid"]
    db_ref = get_reference_by_id(ref_uid)
    if db_ref:
        return get_all_references_by_reference_text(db_ref.reference)
    return error("Reference could not be found")


# =============================================================================
# USER MANAGEMENT
# =============================================================================

@login.post(require_csrf=False)
@validate(has_keywords(('nickname', str), ('password', str)), validate_credentials)
def user_login(request):
    """
    Check provided credentials and return a token, if it is a valid user. The function body is only executed,
    if the validator added a request.validated field.

    :param request:
    :return: token and nickname
    """
    nickname = request.validated['nickname']
    log.debug('User authenticated: {}'.format(nickname))
    return {
        'nickname': nickname,
        'token': request.validated['token']
    }


@logout.get(require_csrf=False)
@validate(valid_token)
def user_logout(request):
    """
    If user is logged in and has token, remove the token from the database and perform logout.

    :param request:
    :return:
    """
    nickname = request.validated['user']
    log.debug('User logged out: {}'.format(nickname))
    request.session.invalidate()
    token_to_database(request.validated['user'], None)
    return {
        'status': 'ok',
        'message': 'Successfully logged out'
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
    try:
        return get_statements_with_similarity_to(query_string)
    except Exception as ex:
        LOG.warning("Could not request data from elasticsearch because of error: %s", ex)
    return get_all_statements_by_levensthein_similar_to(query_string)


# =============================================================================
# JUMPING - jump to specific position in the discussion
# =============================================================================

def jump_preparation(request):
    """
    Prepare api_data and extract all relevant information from the request.

    :param request:
    :return:

    """
    slug = request.matchdict["slug"]
    arg_uid = int(request.matchdict["arg_uid"])
    nickname = None
    session_id = None
    return {"slug": slug, "arg_uid": arg_uid, "nickname": nickname, "session_id": session_id}


@jump_to_zargument.get()
def jump_to_argument_fn(request):
    """
    Given a slug, arg_uid and a nickname, jump directly to an argument to provoke user interaction.

    :param request:
    :return: Argument with a list of possible interactions

    """
    return dbas.jump(request)


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

@issues.get()
def get_issues(_request):
    """
    Returns a list of active issues.

    :param _request:
    :return: List of active issues.
    """
    return DBDiscussionSession.query(Issue).filter(Issue.is_disabled == False,
                                                   Issue.is_private == False).all()


# -----------------------------------------------------------------------------
# Posts

def __join_list_to_string(list_of_strings) -> str:
    return ", ".join(str(elem) for elem in list_of_strings)


def __http_see_other_with_cors_header(location: str) -> HTTPSeeOther:
    """
    Add CORS Headers to HTTPSeeOther response.

    :param location: URL to route to
    :return: HTTPSeeOther with CORS Header
    """
    return HTTPSeeOther(
        location=location,
        headers={
            'Access-Control-Allow-Origin': __join_list_to_string(cors_policy.get('origins')),
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, HEAD',
            'Access-Control-Allow-Headers': __join_list_to_string(cors_policy.get('headers')),
        }
    )


@zinit.post(require_csrf=False)
@positions.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_new_position_in_body, valid_reason_in_body,
          valid_reason_and_position_not_equal)
def add_position_with_premise(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    new_position = set_position(db_user, db_issue, request.validated['position-text'])

    conclusion_id: int = new_position['statement_uids'][0]
    db_conclusion: Statement = DBDiscussionSession.query(Statement).get(conclusion_id)

    pd = set_positions_premise(db_issue, db_user, db_conclusion, [[request.validated['reason-text']]], True, history,
                               request.mailer)

    return __http_see_other_with_cors_header('/api' + pd['url'])


@justify_statement.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_reason_in_body, valid_statement(location="path"),
          valid_attitude, has_maybe_keywords(('reference', str, None)), valid_optional_origin)
def add_premise_to_statement(request: IRequest):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    db_statement: Statement = request.validated['statement']
    reference_text: str = request.validated["reference"]
    is_supportive = request.validated['attitude'] == Attitudes.AGREE
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    if reference_text:
        store_reference(reference_text, request.host, request.path, db_user, db_statement, db_issue)

    pd = set_positions_premise(db_issue, db_user, db_statement, [[request.validated['reason-text']]], is_supportive,
                               history,
                               request.mailer)

    return __http_see_other_with_cors_header('/api' + pd['url'])


@justify_argument.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_reason_in_body, valid_argument(location="path"), valid_relation,
          valid_attitude, has_maybe_keywords(('reference', str, None)))
def add_premise_to_argument(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    db_argument: Argument = request.validated['argument']
    reference_text: str = request.validated['reference']
    relation: Relations = request.validated['relation']
    history = history_handler.save_and_set_cookie(request, db_user, db_issue)

    if reference_text:
        for premise in db_argument.premisegroup.premises:
            store_reference(reference_text, request.host, request.path, db_user, premise.statement, db_issue)

    pd = set_arguments_premises(db_issue, db_user, db_argument, [[request.validated['reason-text']]], relation,
                                history,
                                request.mailer)

    return __http_see_other_with_cors_header('/api' + pd['url'])


@resource(collection_path='/users', path='/users/{id:\d+}', cors_policy=cors_policy)
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
              has_keywords(('firstname', str), ('lastname', str), ('nickname', str), ('email', str), ('gender', str),
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
