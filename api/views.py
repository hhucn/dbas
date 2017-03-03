"""
Introducing an API to enable external discussions.

This is the entry point for the API. Here are views defined, which always return JSON objects
which can then be used in external websites.

.. note:: Methods **must not** have the same name as their assigned Service.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import json

from cornice import Service
import dbas.views as dbas
from dbas.lib import get_text_for_argument_uid, get_all_arguments_by_statement, \
    get_all_arguments_with_text_by_statement_id, resolve_issue_uid_to_slug

from .lib import HTTP204, flatten, json_bytes_to_dict, logger, merge_dicts
from .login import validate_credentials, validate_login
from .references import store_reference, url_to_statement, get_references_for_url, get_all_references_by_reference_text, get_reference_by_id, \
    prepare_single_reference

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

ahello = Service(name='hello',
                 path='/hello',
                 description="Say hello to remote users",
                 cors_policy=cors_policy)

# Argumentation stuff
reaction = Service(name='api_reaction',
                   path='/{slug}/reaction/{arg_id_user}/{mode}/{arg_id_sys}',
                   description="Discussion Reaction",
                   cors_policy=cors_policy)
justify = Service(name='api_justify',
                  path='/{slug}/justify/{statement_or_arg_id}/{mode}*relation',
                  description="Discussion Justify",
                  cors_policy=cors_policy)
attitude = Service(name='api_attitude',
                   path='/{slug}/attitude/*statement_id',
                   description="Discussion Attitude",
                   cors_policy=cors_policy)
issues = Service(name='get_issues',
                 path='/get_issues',
                 description="Issue Selector",
                 cors_policy=cors_policy)
# Prefix with 'z' so it is added as the last route
zinit = Service(name='api_init',
                path='/{slug}',
                description="Discussion Init",
                cors_policy=cors_policy)
zinit_blank = Service(name='api_init_blank',
                      path='/',
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
                     path="/get/references",
                     description="Query database to get stored references from site",
                     cors_policy=cors_policy)

reference_usages = Service(name="reference_usages",
                           path="/get/reference/usages/{ref_uid}",
                           description="Return dict containing all information about the usages of this reference",
                           cors_policy=cors_policy)

find_statements = Service(name="find_statements",
                          path="/get/statements/{issue}/{type}/{value}",
                          description="Query database to get closest statements",
                          cors_policy=cors_policy)

statement_url_service = Service(name="statement_url",
                                path="/get/statement/url/{issue_uid}/{statement_uid}/{agree}",
                                description="Get URL to a statement inside the discussion for direct jumping to it",
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


# =============================================================================
# SYSTEM: Say hello to new visitors
# =============================================================================

@ahello.get()
def hello(_):
    """
    Return data from DBas discussion_reaction page.

    :return: dbas.discussion_reaction(True)
    """
    return {"status": "ok",
            "message": "Connection established. \"Back when PHP had less than 100 functions and the function hashing mechanism was strlen()\" -- Author of PHP"}


# =============================================================================
# DISCUSSION-RELATED REQUESTS
# =============================================================================

def append_csrf_to_dict(request, return_dict):
    """
    Append CSRF token to response.

    :param request: needed to extract the token
    :param return_dict: dictionary, which gets merged with the CSRF token
    :return:
    """
    csrf = request.session.get_csrf_token()
    csrf_dict = {"csrf": csrf}
    return merge_dicts(csrf_dict, return_dict)


def prepare_user_information(request):
    """
    Check if user is authenticated, return prepared data for D-BAS.

    :param request:
    :return:
    """
    val = request.validated
    try:
        api_data = {"nickname": val["user"],
                    "user_uid": val["user_uid"],
                    "session_id": val["session_id"]}
    except KeyError:
        api_data = None
    return api_data


def prepare_data_assign_reference(request, func):
    """
    Collect user information, prepare submitted data and store references into database.

    :param request:
    :param func:
    :return:
    """
    api_data = prepare_user_information(request)
    if api_data:
        data = json_bytes_to_dict(request.body)
        api_data.update(data)
        return_dict_json = func(request, for_api=True, api_data=api_data)
        return_dict = json.loads(return_dict_json)
        statement_uids = return_dict["statement_uids"]
        if statement_uids:
            statement_uids = flatten(statement_uids)
            if type(statement_uids) is int:
                statement_uids = [statement_uids]
            refs_db = list(map(lambda statement: store_reference(api_data, statement), statement_uids))
            refs = list()  # Convert all references
            for ref in refs_db:
                refs.append(prepare_single_reference(ref))
            return_dict["references"] = refs
        return return_dict
    else:
        raise HTTP204()


def parse_host_and_path(request):
    """
    Prepare provided host and path of external article.

    :param request: request
    :return: host and path parsed from request
    :rtype: str
    """
    try:
        host = request.headers["X-Host"]
        path = request.headers["X-Path"]
        return host, path
    except AttributeError:
        log.error("[API/Reference] Could not look up origin.")
    except KeyError:
        log.error("[API/Reference] Missing fields in HTTP header (X-Host / X-Path).")
    return None, None


@reaction.get(validators=validate_login)
def discussion_reaction(request):
    """
    Return data from DBas discussion_reaction page.

    :param request: request
    :return: dbas.discussion_reaction(True)
    """
    api_data = prepare_user_information(request)
    return dbas.discussion_reaction(request, for_api=True, api_data=api_data)


@justify.get(validators=validate_login)
def discussion_justify(request):
    """
    Return data from DBas discussion_justify page.

    :param request: request
    :return: dbas.discussion_justify(True)
    """
    api_data = prepare_user_information(request)
    return dbas.discussion_justify(request, for_api=True, api_data=api_data)


@attitude.get(validators=validate_login)
def discussion_attitude(request):
    """
    Return data from DBas discussion_attitude page.

    :param request: request
    :return: dbas.discussion_attitude(True)
    """
    api_data = prepare_user_information(request)
    return dbas.discussion_attitude(request, for_api=True, api_data=api_data)


@zinit.get(validators=validate_login)
def discussion_init(request):
    """
    Return data from DBas discussion_init page.

    :param request: request
    :return: dbas.discussion_init(True)
    """
    api_data = prepare_user_information(request)
    return dbas.discussion_init(request, for_api=True, api_data=api_data)


@zinit_blank.get(validators=validate_login)
def discussion_init_blank(request):
    """
    Return data from DBas discussion_init page.

    :param request: request
    :return: dbas.discussion_init(True)
    """
    api_data = prepare_user_information(request)
    return dbas.discussion_init(request, for_api=True, api_data=api_data)


#
# Add new statements / positions
#
@start_statement.post(validators=validate_login, require_csrf=False)
def add_start_statement(request):
    """
    Add new start statement to issue.

    :param request:
    :return:
    """
    return prepare_data_assign_reference(request, dbas.set_new_start_statement)


@start_premise.post(validators=validate_login, require_csrf=False)
def add_start_premise(request):
    """
    Add new premise group.

    :param request:
    :return:
    """
    return prepare_data_assign_reference(request, dbas.set_new_start_premise)


@justify_premise.post(validators=validate_login, require_csrf=False)
def add_justify_premise(request):
    """
    Add new justifying premise group.

    :param request:
    :return:
    """
    return prepare_data_assign_reference(request, dbas.set_new_premises_for_argument)


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
    host, path = parse_host_and_path(request)
    if host and path:
        refs = []
        refs_db = get_references_for_url(host, path)
        if refs_db is not None:
            for ref in refs_db:
                refs.append(prepare_single_reference(ref))
            return {"references": refs}
        else:
            log.error("[API/Reference] Returned no references: Database error")
            return {"status": "error", "message": "Could not retrieve references"}
    log.error("[API/Reference] Could not parse host and / or path")
    return {"status": "error", "message": "Could not parse your origin"}


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
    log.error("[API/GET Reference Usages] Error when trying to find matching reference for id " + ref_uid)
    return {"status": "error", "message": "Reference could not be found"}


# =============================================================================
# USER MANAGEMENT
# =============================================================================

@login.get()  # TODO test this permission='use'
def get_csrf_token(request):
    """
    Test user's credentials, return success if valid token and username is provided.

    :param request:
    :return:
    """
    log.debug("[API/CSRF] Returning CSRF token.")
    return append_csrf_to_dict(request, {})


@login.post(validators=validate_credentials, require_csrf=False)
def user_login(request):
    """
    Check provided credentials and return a token, if it is a valid user.
    The function body is only executed, if the validator added a request.validated field.

    :param request:
    :return: token
    """
    user = request.validated['user']
    # Convert bytes to string
    if type(user['token']) == bytes:
        token = user['token'].decode('utf-8')
    else:
        token = user['token']

    return_dict = {'token': '%s-%s' % (user['nickname'], token)}
    return append_csrf_to_dict(request, return_dict)


# =============================================================================
# FINDING STATEMENTS
# =============================================================================

@find_statements.get()
def find_statements_fn(request):
    """
    Receives search requests, queries database to find all occurrences and returns these results
    with the correct URL to get directly access to the location in the discussion.

    :param request:
    :return: json conform dictionary of all occurrences
    """
    api_data = dict()
    api_data["issue"] = request.matchdict["issue"]
    api_data["mode"] = request.matchdict["type"]
    api_data["value"] = request.matchdict["value"]
    results = dbas.fuzzy_search(request, for_api=True, api_data=api_data)

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
def fn_jump_to_argument(request):
    """
    Given a slug, arg_uid and a nickname, jump directly to an argument to
    provoke user interaction.

    :param request:
    :return: Argument with a list of possible interactions
    """
    api_data = jump_preparation(request)
    return dbas.discussion_jump(request, for_api=True, api_data=api_data)


# =============================================================================
# TEXT BLOCKS - create text-blocks as seen in the bubbles
# =============================================================================

@text_for_argument.get()
def get_text_for_argument(request):
    statement = int(request.matchdict["statement_uid"])

    args = get_all_arguments_by_statement(statement)
    results = list()

    for argument in args:
        results.append({"uid": argument.uid,
                        "text": get_text_for_argument_uid(argument.uid)})
    return results


# =============================================================================
# GET INFORMATION - several functions to get information from the database
# =============================================================================

@statement_url_service.get()
def get_statement_url(request):
    """
    Given an issue, the statement_uid and an (dis-)agreement, produce a url to the statement inside
    the corresponding discussion.

    :param request:
    :return:
    """
    issue_uid = request.matchdict["issue_uid"]
    statement_uid = request.matchdict["statement_uid"]
    agree = request.matchdict["agree"]
    return_dict = {"url": url_to_statement(issue_uid, statement_uid, agree)}
    return return_dict
