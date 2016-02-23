# Introducing an API to enable external discussions
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

from cornice import Service

from api.login import valid_token, validate_credentials
from dbas.views import Dbas
from .login import _USERS  # TODO: This is *not* an appropriate solution. Just for testing purposes


# CORS configuration
cors_policy = dict(enabled=True,
				   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
				   origins=('*',),
				   # credentials=True,  # TODO: how can i use this?
				   max_age=42)


# =============================================================================
# SERVICES - Define services for several actions of DBAS
# =============================================================================

dump       = Service(name='api_dump',
					 path='/dump',
					 description="Database Dump",
					 cors_policy=cors_policy)
users      = Service(name='login',
                     path='/login',
                     description="User management of external discussion system",
                     cors_policy=cors_policy)
news       = Service(name='api_news',
 					 path='/get_news',
 					 description="News app",
 					 cors_policy=cors_policy)
reaction   = Service(name='api_reaction',
 					 path='/{slug}/reaction/{arg_id_user}/{mode}/{arg_id_sys}',
 					 description="Discussion Reaction",
 					 cors_policy=cors_policy)
justify    = Service(name='api_justify',
					 path='/{slug}/justify/{statement_or_arg_id}/{mode}*relation',
					 description="Discussion Justify",
					 cors_policy=cors_policy)
attitude   = Service(name='api_attitude',
					 path='/{slug}/attitude/*statement_id',
					 description="Discussion Attitude",
					 cors_policy=cors_policy)
issues     = Service(name='get_issues',
 					 path='/get_issues',
 					 description="Issue Selector",
 					 cors_policy=cors_policy)
# Prefix with 'z' so it is added as the last route
zinit      = Service(name='api_init',
					 path='/{slug}',
					 description="Discussion Init",
					 cors_policy=cors_policy)
zinit_blank = Service(name='api_init_blank',
					  path='/',
					  description="Discussion Init",
					  cors_policy=cors_policy)


@news.get()
def get_news(request):
	"""
	Returns news from DBAS in JSON.
	:param request: request
	:return: Dbas(request).get_news()
	"""
	return Dbas(request).get_news()


##############################
# Discussion-related functions

@reaction.get()
def discussion_reaction(request):
	"""
	Return data from DBas discussion_reaction page
	:param request: request
	:return: Dbas(request).discussion_reaction(True)
	"""
	return Dbas(request).discussion_reaction(True)


@justify.get()
def discussion_justify(request):
	"""
	Return data from DBas discussion_justify page
	:param request: request
	:return: Dbas(request).discussion_justify(True)
	"""
	return Dbas(request).discussion_justify(True)


@attitude.get()
def discussion_attitude(request):
	"""
	Return data from DBas discussion_attitude page
	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	return Dbas(request).discussion_attitude(True)


@issues.get()
def issue_selector(request):
	"""
	Return data from DBas discussion_attitude page
	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	return Dbas(request).fuzzy_search(True)


@zinit.get()
def discussion_init(request):
	"""
	Return data from DBas discussion_init page
	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	return Dbas(request).discussion_init(True)


@zinit_blank.get()
def discussion_init(request):
	"""
	Return data from DBas discussion_init page
	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	return Dbas(request).discussion_init(True)


##########
# Database

@dump.get()
def discussion_init(request):
	"""
	Return database dump
	:param request: request
	:return: Dbas(request).get_database_dump(True)
	"""
	return Dbas(request).get_database_dump()


# =============================================================================
# POST / GET EXAMPLE
# =============================================================================

hello = Service(name='api', path='/hello', description="Simplest app", cors_policy=cors_policy)
values = Service(name='foo', path='/values/{value}', description="Cornice Demo", cors_policy=cors_policy)

_VALUES = {}


@hello.get()
def get_info(request):
	"""

	:param request:
	:return:
	"""
	return {'Hello': 'World'}


@values.get()
def get_value(request):
	"""

	:param request:
	:return:
	"""
	key = request.matchdict['value']
	return _VALUES.get(key)


@values.post()
def set_value(request):
	"""Set the value.

	Returns *True* or *False*.
	"""
	key = request.matchdict['value']
	try:
		# json_body is JSON-decoded variant of the request body
		_VALUES[key] = request.json_body
	except ValueError:
		return False
	return True


# =============================================================================
# LOGIN
# =============================================================================

############################
# Services - User Management

# TODO sample function, remove it
# @users.get(validators=valid_token)
# def get_users(request):
# 	"""
# 	Returns a list of all users
# 	"""
# 	return {'users': _USERS}

@users.post(validators=validate_credentials)
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

	_USERS[user['nickname']] = token
	return {'token': '%s-%s' % (user['nickname'], token)}
