# Introducing an API to enable external discussions
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

from cornice import Service

from .lib import json_bytes_to_dict, HTTP204
from .references import store_reference
from api.login import valid_token, validate_credentials, validate_login
from dbas.views import Dbas

#
# CORS configuration
#
cors_policy = dict(enabled=True,
				   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
				   origins=('*',),
				   # credentials=True,  # TODO: how can i use this?
				   max_age=42)


# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

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
# Add new data to DBAS
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


@reaction.get(validators=validate_login)
def discussion_reaction(request):
	"""
	Return data from DBas discussion_reaction page
	:param request: request
	:return: Dbas(request).discussion_reaction(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_reaction(for_api=True, api_data=api_data)


@justify.get(validators=validate_login)
def discussion_justify(request):
	"""
	Return data from DBas discussion_justify page
	:param request: request
	:return: Dbas(request).discussion_justify(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_justify(for_api=True, api_data=api_data)


@attitude.get(validators=validate_login)
def discussion_attitude(request):
	"""
	Return data from DBas discussion_attitude page
	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_attitude(for_api=True, api_data=api_data)


@issues.get(validators=validate_login)
def issue_selector(request):
	"""
	Return data from DBas discussion_attitude page
	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).fuzzy_search(for_api=True, api_data=api_data)


@zinit.get(validators=validate_login)
def discussion_init(request):
	"""
	Return data from DBas discussion_init page
	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_init(for_api=True, api_data=api_data)


@zinit_blank.get(validators=validate_login)
def discussion_init(request):
	"""
	Return data from DBas discussion_init page
	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	api_data = prepare_user_information(request)
	return Dbas(request).discussion_init(for_api=True, api_data=api_data)


#
# Add new statements / positions
#
@start_statement.post(validators=validate_login)
def add_start_statement(request):
	"""
	Add new start statement to issue.
	:param request:
	:return:
	"""
	api_data = prepare_user_information(request)
	if api_data:
		data = json_bytes_to_dict(request.body)
		api_data.update(data)
		return_dict = Dbas(request).set_new_start_statement(for_api=True, api_data=api_data)
		store_reference(api_data, return_dict["statement_uid"])
	else:
		raise HTTP204()


@start_premise.post(validators=validate_login)
def add_start_premise(request):
	"""
	Add new premise group.
	:param request:
	:return:
	"""
	api_data = prepare_user_information(request)
	if api_data:
		data = json_bytes_to_dict(request.body)
		api_data.update(data)
		store_reference(api_data)
		return Dbas(request).set_new_start_premise(for_api=True, api_data=api_data)
	else:
		raise HTTP204()


@justify_premise.post(validators=validate_login)
def add_justify_premise(request):
	"""
	Add new justifying premise group.
	:param request:
	:return:
	"""
	api_data = prepare_user_information(request)
	if api_data:
		data = json_bytes_to_dict(request.body)
		api_data.update(data)
		store_reference(api_data)
		return Dbas(request).set_new_premises_for_argument(for_api=True, api_data=api_data)
	else:
		raise HTTP204()


# =============================================================================
# USER MANAGEMENT
# =============================================================================

@login.get(validators=valid_token)  # TODO test this permission='use'
def testing(request):
	"""
	Test user's credentials, return success if valid token and username is provided.
	:param request:
	:return:
	"""
	Dbas(request).main_notifications()
	return {'status': 'success'}


@login.post(validators=validate_credentials)
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

	return {'token': '%s-%s' % (user['nickname'], token)}


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