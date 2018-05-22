"""Introducing an API to enable external discussions.

This is the entry point for the API. Here are views defined, which always
return JSON objects which can then be used in external websites.

.. note:: Methods **must not** have the same name as their assigned Service.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>

"""
import json
from typing import Callable, Any

from cornice import Service
from pyramid.httpexceptions import HTTPSeeOther

import dbas.discussion.core as discussion
import dbas.handler.history as history_handler
import dbas.views as dbas
from api.lib import extract_items_and_bubbles
from api.models import Item, Bubble
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, User, Argument
from dbas.handler.arguments import set_arguments_premises
from dbas.handler.statements import set_positions_premise, set_position
from dbas.lib import (get_all_arguments_by_statement,
                      get_all_arguments_with_text_by_statement_id,
                      get_text_for_argument_uid, resolve_issue_uid_to_slug, create_speechbubble_dict, BubbleTypes,
                      Attitudes, Relations)
from dbas.strings.translator import Keywords as _, get_translation
from dbas.validators.core import has_keywords, validate
from dbas.validators.discussion import valid_issue_by_slug, valid_position, valid_statement, valid_attitude, \
    valid_argument, valid_relation, valid_reaction_arguments, valid_new_position_in_body, valid_reason_in_body
from dbas.validators.lib import add_error
from .lib import HTTP204, flatten, json_to_dict, logger
from .login import validate_credentials, validate_login, valid_token, token_to_database, valid_token_optional
from .references import (get_all_references_by_reference_text,
                         get_reference_by_id, get_references_for_url,
                         prepare_single_reference, store_reference,
                         url_to_statement)
from .templates import error

log = logger()

#
# CORS configuration
#
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
                   origins=('*',),
                   credentials=True,  # TODO: how can i use this?
                   max_age=42)

# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

empty_route = Service(name='empty',
                      path='',
                      description="Empty route",
                      cors_policy=cors_policy)

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
                 description='End of a discussion')

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
# Add new data to D-BAS
#
start_statement = Service(name="start_statement",
                          path="/add/start_statement",
                          description="Add new position to issue",
                          cors_policy=cors_policy)

start_premise = Service(name="start_premise",
                        path="/add/start_premise",
                        description="Add new premises",
                        cors_policy=cors_policy)

justify_premise = Service(name="justify_premise",
                          path="/add/justify_premise",
                          description="Add new justifying premises",
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
                          path="/statements/{issue}/{type}/{value}",
                          description="Query database to get closest statements",
                          cors_policy=cors_policy)

statement_url_service = Service(name="statement_url",
                                path="/statement/url/{issue_uid}/{statement_uid}/{agree}",
                                description="Get URL to a statement inside the discussion for direct jumping to it",
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

@empty_route.get()
def empty(request):
    """
    Returns 404 because no route is given

    :return: 404
    """
    add_error(request, 'Route not found', 'There was no route given')


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
        create_speechbubble_dict(BubbleTypes.SYSTEM, uid='start', message=intro, omit_url=True, lang=db_issue.lang)
    ]

    db_positions = DBDiscussionSession.query(Statement).filter(Statement.is_disabled == False,
                                                               Statement.issue_uid == db_issue.uid,
                                                               Statement.is_position == True).all()

    items = [Item([pos.get_textversion().content], "{}/attitude/{}".format(db_issue.slug, pos.uid))
             for pos in db_positions]

    return {
        'bubbles': [Bubble(bubble) for bubble in bubbles],
        'items': items
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
    history = history_handler.handle_history(request, db_user, db_issue)

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
    history = history_handler.handle_history(request, db_user, db_issue)

    prepared_discussion = dbas.discussion.justify_statement(db_issue, db_user, request.validated['statement'],
                                                            request.validated['attitude'], history, request.path)
    bubbles, items = extract_items_and_bubbles(prepared_discussion)

    return {
        'bubbles': bubbles,
        'items': items
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
    history = history_handler.handle_history(request, db_user, db_issue)

    prepared_discussion = dbas.discussion.justify_argument(db_issue, db_user, request.validated['argument'],
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
    history = history_handler.handle_history(request, db_user, db_issue)

    prepared_discussion = dbas.discussion.reaction(db_issue, db_user,
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
    history = history_handler.handle_history(request, db_user, db_issue)

    prepared_discussion = dbas.discussion.finish(db_issue, db_user,
                                                 request.validated['argument'], history)

    return {'bubbles': extract_items_and_bubbles(prepared_discussion)[0]}


# -----------------------------------------------------------------------------

def prepare_user_information(request):
    """
    Check if user is authenticated, return prepared data for D-BAS.

    :param request:
    :return:
    """
    val = request.validated
    try:
        api_data = {
            "nickname": val["user"],
            "user": val["user"],
            "user_uid": val["user_uid"],
            "session_id": val["session_id"]
        }
    except KeyError:
        api_data = None
    return api_data


def prepare_data_assign_reference(request, func: Callable[[bool, dict], Any]):
    """
    Collect user information, prepare submitted data and store references into database.

    :param request:
    :param func:
    :return:
    """
    api_data = prepare_user_information(request)
    if not api_data:
        raise HTTP204()

    log.info(str(request.matched_route))
    data = json_to_dict(request.body)

    if "issue_id" in data:
        db_issue = DBDiscussionSession.query(Issue).get(data["issue_id"])

        if not db_issue:
            request.errors.add("body", "Issue not found", "The given issue_id is invalid")
            request.status = 400

    elif "slug" in data:
        db_issue = DBDiscussionSession.query(Issue).filter_by(slug=data["slug"]).one()

        if not db_issue:
            request.errors.add("body", "Issue not found", "The given slug is invalid")
            request.status = 400

        api_data["issue_id"] = db_issue.uid

    else:
        request.errors.add("body", "Issue not found", "There was no issue_id or slug given")
        request.status = 400
        return

    api_data["issue"] = db_issue

    api_data.update(data)
    api_data['application_url'] = request.application_url

    return_dict = func(True, api_data)

    if isinstance(return_dict, str):
        return_dict = json.loads(return_dict)

    statement_uids = return_dict["statement_uids"]
    if statement_uids:
        statement_uids = flatten(statement_uids)
        if type(statement_uids) is int:
            statement_uids = [statement_uids]
        refs_db = [store_reference(api_data, statement) for statement in statement_uids]
        return_dict["references"] = list(map(prepare_single_reference, refs_db))
    return return_dict


@start_statement.post(validators=validate_login, require_csrf=False)
def add_start_statement(request):
    """
    Add new start statement to issue.

    :param request:
    :return:
    """
    return prepare_data_assign_reference(request, set_position)


@start_premise.post(validators=validate_login, require_csrf=False)
def add_start_premise(request):
    """
    Add new premise group.

    :param request:
    :return:
    """
    return prepare_data_assign_reference(request, set_positions_premise)


@justify_premise.post(validators=validate_login, require_csrf=False)
def add_justify_premise(request):
    """
    Add new justifying premise group.

    :param request:
    :return:
    """
    return prepare_data_assign_reference(request, set_arguments_premises)


# =============================================================================
# REFERENCES - Get references from database
# =============================================================================

@references.get()
def get_references(request):
    """
    Query database to get stored references from site. Generate a list with text versions of references.

    :param request: request
    :return: References assigned to the queried URL

    """
    host = request.GET.get("host")
    path = request.GET.get("path")
    if host and path:
        refs_db = get_references_for_url(host, path)
        if refs_db is not None:
            return {
                "references": list(map(lambda ref:
                                       prepare_single_reference(ref), refs_db))
            }
        else:
            return error("Could not retrieve references", "API/Reference")
    return error("Could not parse your origin", "API/Reference")


@reference_usages.get()
def get_reference_usages(request):
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
    return error("Reference could not be found",
                 "API/GET Reference Usages",
                 "Error when trying to find matching reference for id")


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
    return {
        'nickname': request.validated['nickname'],
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
def find_statements_fn(request):
    """
    Receives search requests, queries database to find all occurrences and returns these results with the correct URL
    to get directly access to the location in the discussion.

    :param request:
    :return: json conform dictionary of all occurrences

    """
    api_data = dict()
    api_data["issue"] = request.matchdict["issue"]
    api_data["mode"] = request.matchdict["type"]
    api_data["value"] = request.matchdict["value"]
    results = dbas.fuzzy_search(request, api_data=api_data)

    issue_uid = api_data["issue"]

    return_dict = dict()
    return_dict["distance_name"] = results["distance_name"]
    return_dict["values"] = []

    for statement in results["values"]:
        statement_uid = statement["statement_uid"]
        statement["issue"] = {"uid": issue_uid, "slug": resolve_issue_uid_to_slug(issue_uid)}
        statement["url"] = url_to_statement(api_data["issue"], statement_uid)  # TODO I think I do not use this any more
        statement["arguments"] = get_all_arguments_with_text_by_statement_id(statement_uid)
        return_dict["values"].append(statement)
    return return_dict


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
    # api_data = jump_preparation(request)
    return dbas.discussion.jump(request)


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

@statement_url_service.get()
def get_statement_url(request):
    """
    Given an issue, the statement_uid and an (dis-)agreement, produce a url to the statement inside the corresponding
    discussion.

    :param request:
    :return:

    """
    issue_uid = request.matchdict["issue_uid"]
    statement_uid = request.matchdict["statement_uid"]
    agree = request.matchdict["agree"]
    return {"url": url_to_statement(issue_uid, statement_uid, agree)}


@issues.get()
def get_issues(_request):
    """
    Returns a list of active issues.

    :param _request:
    :return: List of active issues.
    """
    return DBDiscussionSession.query(Issue).filter(Issue.is_disabled == False,
                                                   Issue.is_private == False).all()


@positions.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_new_position_in_body, valid_reason_in_body)
def add_position_with_premise(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    history = history_handler.handle_history(request, db_user, db_issue)

    new_position = set_position(db_user, db_issue, request.validated['position-text'])

    conslusion_id: int = new_position['statement_uids'][0]
    db_conclusion: Statement = DBDiscussionSession.query(Statement).get(conslusion_id)

    pd = set_positions_premise(db_issue, db_user, db_conclusion, [[request.validated['reason-text']]], True, history,
                               request.mailer)

    return HTTPSeeOther(location='/api' + pd['url'])


@justify_statement.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_reason_in_body, valid_statement(location="path"),
          valid_attitude)
def add_premise_to_statement(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    db_statement: Statement = request.validated['statement']
    is_supportive = request.validated['attitude'] == Attitudes.AGREE
    history = history_handler.handle_history(request, db_user, db_issue)

    pd = set_positions_premise(db_issue, db_user, db_statement, [[request.validated['reason-text']]], is_supportive,
                               history,
                               request.mailer)

    return HTTPSeeOther(location='/api' + pd['url'])


@justify_argument.post(require_csrf=False)
@validate(valid_token, valid_issue_by_slug, valid_reason_in_body, valid_argument(location="path"), valid_relation,
          valid_attitude)
def add_premise_to_argument(request):
    db_user: User = request.validated['user']
    db_issue: Issue = request.validated['issue']
    db_argument: Argument = request.validated['argument']
    relation: Relations = request.validated['relation']
    history = history_handler.handle_history(request, db_user, db_issue)

    pd = set_arguments_premises(db_issue, db_user, db_argument, [[request.validated['reason-text']]], relation,
                                history,
                                request.mailer)

    return HTTPSeeOther(location='/api' + pd['url'])
