"""
Introducing an API to enable external discussions.

This is the entry point for the API. Here are views defined, which always return JSON objects
which can then be used in external websites.

.. note:: Methods **must not** have the same name as their assigned Service.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import json

from api.extractor import extract_reference_information
from api.login import validate_credentials, validate_login
from cornice import Service
from dbas.views import Dbas

from .lib import HTTP204, flatten, json_bytes_to_dict, logger, merge_dicts, get_reference_by_id, get_references_for_url
from .references import store_reference, url_to_statement

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

# Argumentation stuff
reaction = Service(name='api_reaction',
				   path='/{slug}/reaction/{arg_id_user}/{mode}/{arg_id_sys}',
				   description="Discussion Reaction",
				   cors_policy=cors_policy)
justify  = Service(name='api_justify',
				   path='/{slug}/justify/{statement_or_arg_id}/{mode}*relation',
				   description="Discussion Justify",
				   cors_policy=cors_policy)
attitude = Service(name='api_attitude',
				   path='/{slug}/attitude/*statement_id',
				   description="Discussion Attitude",
				   cors_policy=cors_policy)
issues   = Service(name='get_issues',
				   path='/get_issues',
				   description="Issue Selector",
				   cors_policy=cors_policy)
# Prefix with 'z' so it is added as the last route
zinit    = Service(name='api_init',
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

#
# Other Services
#
news = Service(name='api_news',
			   path='/get_news',
			   description="News app",
			   cors_policy=cors_policy)

#
# User Management
#
login = Service(name='login',
				path='/login',
				description="Log into external discussion system",
				cors_policy=cors_policy)


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
		return_dict_json = func(for_api=True, api_data=api_data)
		return_dict = json.loads(return_dict_json)
		statement_uids = return_dict["statement_uids"]
		if statement_uids:
			statement_uids = flatten(statement_uids)
			if type(statement_uids) is int:
				statement_uids = [statement_uids]
			list(map(lambda statement: store_reference(api_data, statement), statement_uids))  # need list() to execute the functions
		return return_dict_json
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
	:return: Dbas(request).discussion_reaction(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_reaction(for_api=True, api_data=api_data)


@justify.get(validators=validate_login)
def discussion_justify(request):
	"""
	Return data from DBas discussion_justify page.

	:param request: request
	:return: Dbas(request).discussion_justify(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_justify(for_api=True, api_data=api_data)


@attitude.get(validators=validate_login)
def discussion_attitude(request):
	"""
	Return data from DBas discussion_attitude page.

	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_attitude(for_api=True, api_data=api_data)


# @issues.get(validators=validate_login)
# def issue_selector(request):
# 	"""
# 	Return data from DBas discussion_attitude page.
#
# 	:param request: request
# 	:return: Dbas(request).discussion_attitude(True)
# 	"""
# 	api_data = prepare_user_information(request)
# 	return Dbas(request).fuzzy_search(for_api=True, api_data=api_data)


@zinit.get(validators=validate_login)
def discussion_init(request):
	"""
	Return data from DBas discussion_init page.

	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_init(for_api=True, api_data=api_data)


@zinit_blank.get(validators=validate_login)
def discussion_init(request):
	"""
	Return data from DBas discussion_init page.

	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_init(for_api=True, api_data=api_data)


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
	return prepare_data_assign_reference(request, Dbas(request).set_new_start_statement)


@start_premise.post(validators=validate_login, require_csrf=False)
def add_start_premise(request):
	"""
	Add new premise group.

	:param request:
	:return:
	"""
	return prepare_data_assign_reference(request, Dbas(request).set_new_start_premise)


@justify_premise.post(validators=validate_login, require_csrf=False)
def add_justify_premise(request):
	"""
	Add new justifying premise group.

	:param request:
	:return:
	"""
	return prepare_data_assign_reference(request, Dbas(request).set_new_premises_for_argument)


#
# Get data from D-BAS' database
#
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
		log.debug("[API/Reference] Returning references for %s%s" % (host, path))
		refs_db = get_references_for_url(host, path)
		if refs_db is not None:
			for ref in refs_db:
				url = url_to_statement(ref.issue_uid, ref.statement_uid)
				refs.append({"uid": ref.uid, "text": ref.reference, "url": url})
			return {"references": refs}
		else:
			log.error("[API/Reference] Returned no references: Database error")
			return {"status": "error", "message": "Could not retrieve references"}
	else:
		log.error("[API/Reference] Could not parse host and / or path")
		return {"status": "error", "message": "Could not parse your origin"}


@reference_usages.get()
def get_reference_usages(request):
	"""
	Return a JSON object containing all information about the stored reference and its usages.
	Currently, this might be the same as get_references, but this will change in the future.

	:param request:
	:return: JSON with all information about the stored reference
	:rtype: list
	"""
	ref_uid = request.matchdict["ref_uid"]
	db_ref = get_reference_by_id(ref_uid)
	ref = extract_reference_information(db_ref)
	refs = list()
	if db_ref:
		refs.append({"uid": db_ref.uid,
		             "reference": db_ref.reference})
		print("\n\n\n##################")
		print(db_ref)
		print(db_ref.uid)

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
	results = Dbas(request).fuzzy_search(for_api=True, api_data=api_data)

	return_dict = dict()
	return_dict["distance_name"] = results["distance_name"]
	return_dict["issue"] = api_data["issue"]
	return_dict["values"] = []

	for statement in results["values"]:
		statement_uid = statement["statement_uid"]
		statement["url"] = url_to_statement(api_data["issue"], statement_uid)
		return_dict["values"].append(statement)
	return json.dumps(return_dict, True)


# =============================================================================
# OTHER REQUESTS
# =============================================================================

@news.get()
def get_news(request):
	"""
	Returns news from DBAS in JSON.

	.. deprecated:: 0.5.8
	   Unused.

	:param request: request
	:return: Dbas(request).get_news()
	"""
	return Dbas(request).get_news()
