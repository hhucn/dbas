# Introducing an API to enable external discussions
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

from cornice import Service

import transaction

from api.lib import response401
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
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
# Other Services
#
dump = Service(name='api_dump',
			   path='/dump',
			   description="Database Dump",
			   cors_policy=cors_policy)
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

@reaction.get()
def discussion_reaction(request):
	"""
	Return data from DBas discussion_reaction page
	:param request: request
	:return: Dbas(request).discussion_reaction(True)
	"""
	return Dbas(request).discussion_reaction(for_api=True)


@justify.get()
def discussion_justify(request):
	"""
	Return data from DBas discussion_justify page
	:param request: request
	:return: Dbas(request).discussion_justify(True)
	"""
	return Dbas(request).discussion_justify(for_api=True)


@attitude.get()
def discussion_attitude(request):
	"""
	Return data from DBas discussion_attitude page
	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	return Dbas(request).discussion_attitude(for_api=True)


@issues.get()
def issue_selector(request):
	"""
	Return data from DBas discussion_attitude page
	:param request: request
	:return: Dbas(request).discussion_attitude(True)
	"""
	return Dbas(request).fuzzy_search(for_api=True)


@zinit.get(validators=validate_login)
def discussion_init(request):
	"""
	Return data from DBas discussion_init page
	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	return Dbas(request).discussion_init(for_api=True)


@zinit_blank.get(validators=validate_login)
def discussion_init(request):
	"""
	Return data from DBas discussion_init page
	:param request: request
	:return: Dbas(request).discussion_init(True)
	"""
	val = request.validated
	try:
		api_data = {"nickname": val["user"],
		            "session_id": val["session_id"],
		            "logged_in": val["logged_in"]}
	except KeyError:
		api_data = None

	return Dbas(request).discussion_init(for_api=True, api_data=api_data)


# =============================================================================
# OTHER REQUESTS
# =============================================================================

#
# Database
#
@dump.get()
def discussion_init(request):
	"""
	Return database dump
	:param request: request
	:return: Dbas(request).get_database_dump(True)
	"""
	return Dbas(request).get_database_dump()


@news.get()
def get_news(request):
	"""
	Returns news from DBAS in JSON.
	:param request: request
	:return: Dbas(request).get_news()
	"""
	return Dbas(request).get_news()


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

	db_user = DBDiscussionSession.query(User).filter_by(nickname=user['nickname']).first()

	if not db_user:
		raise response401()

	db_user.set_token(token)
	db_user.update_token_timestamp()
	transaction.commit()
	return {'token': '%s-%s' % (user['nickname'], token)}
