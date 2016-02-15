""" Cornice services.
"""
from cornice import Service
from dbas.views import Dbas

# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

# CORS configuration
# cors_policy = dict(enabled=True,
# 				   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
# 				   origins=('*',),
# 				   # credentials=True,  # how can i use this?
# 				   max_age=42)
#
#
# # =============================================================================
# # SERVICES - Define services for several actions of DBAS
# # =============================================================================
#
# dump       = Service(name='api_dump',
# 				     path='/dump',
# 				     description="Database Dump",
# 				     cors_policy=cors_policy)
# login      = Service(name='login',
# 					 path='/login',
# 					 description="Log into account of external discussion system",
# 					 cors_policy=cors_policy)
# news       = Service(name='api_news',
# 				     path='/get_news',
# 				     description="News app",
# 				     cors_policy=cors_policy)
# reaction   = Service(name='api_reaction',
# 				     path='/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys',
# 				     description="Discussion Reaction",
# 				     cors_policy=cors_policy)
# justify    = Service(name='api_justify',
# 				     path='/{slug}/justify/{statement_or_arg_id}/{mode}*relation',
# 				     description="Discussion Justify",
# 				     cors_policy=cors_policy)
# attitude   = Service(name='api_attitude',
# 				     path='/{slug}/attitude/*statement_id',
# 				     description="Discussion Attitude",
# 				     cors_policy=cors_policy)
# init       = Service(name='api_init',
# 				     path='/{slug}',
# 				     description="Discussion Init",
# 				     cors_policy=cors_policy)
# init_blank = Service(name='api_init_blank',
# 					 path='/',
# 					 description="Discussion Init",
# 					 cors_policy=cors_policy)
#
#
# @news.get()
# def get_news(request):
# 	"""
# 	Returns news from DBAS in JSON.
# 	:param request: request
# 	:return: Dbas(request).get_news()
# 	"""
# 	return Dbas(request).get_news()
#
#
# ##############################
# # Discussion-related functions
#
# @reaction.get()
# def discussion_reaction(request):
# 	"""
# 	Return data from DBas discussion_reaction page
# 	:param request: request
# 	:return: Dbas(request).discussion_reaction(True)
# 	"""
# 	return Dbas(request).discussion_reaction(True)
#
#
# @justify.get()
# def discussion_justify(request):
# 	"""
# 	Return data from DBas discussion_justify page
# 	:param request: request
# 	:return: Dbas(request).discussion_justify(True)
# 	"""
# 	return Dbas(request).discussion_justify(True)
#
#
# @attitude.get()
# def discussion_attitude(request):
# 	"""
# 	Return data from DBas discussion_attitude page
# 	:param request: request
# 	:return: Dbas(request).discussion_attitude(True)
# 	"""
# 	return Dbas(request).discussion_attitude(True)
#
#
# @init.get()
# def discussion_init(request):
# 	"""
# 	Return data from DBas discussion_init page
# 	:param request: request
# 	:return: Dbas(request).discussion_init(True)
# 	"""
# 	return Dbas(request).discussion_init(True)
#
#
# @init_blank.get()
# def discussion_init(request):
# 	"""
# 	Return data from DBas discussion_init page
# 	:param request: request
# 	:return: Dbas(request).discussion_init(True)
# 	"""
# 	return Dbas(request).discussion_init(True)
#
#
# ################
# # Login / Logout
#
# @login.post()
# def login(request):
# 	"""
# 	"""
# 	user = request.matchdict['user']
# 	password = request.matchdict['password']
# 	print(user)
# 	try:
# 		pass
# 	except ValueError:
# 		return False
# 	return True
#
#
# ##########
# # Database
#
# @dump.get()
# def discussion_init(request):
# 	"""
# 	Return database dump
# 	:param request: request
# 	:return: Dbas(request).get_database_dump(True)
# 	"""
# 	return Dbas(request).get_database_dump()
#
#
# # =============================================================================
# # POST / GET EXAMPLE
# # =============================================================================
#
# hello = Service(name='api', path='/hello', description="Simplest app", cors_policy=cors_policy)
# values = Service(name='foo', path='/values/{value}', description="Cornice Demo", cors_policy=cors_policy)
#
# _VALUES = {}
#
#
# @hello.get()
# def get_info(request):
# 	"""
#
# 	:param request:
# 	:return:
# 	"""
# 	return {'Hello': 'World'}
#
#
# @values.get()
# def get_value(request):
# 	"""
#
# 	:param request:
# 	:return:
# 	"""
# 	key = request.matchdict['value']
# 	return _VALUES.get(key)
#
#
# @values.post()
# def set_value(request):
# 	"""Set the value.
#
# 	Returns *True* or *False*.
# 	"""
# 	key = request.matchdict['value']
# 	try:
# 		# json_body is JSON-decoded variant of the request body
# 		_VALUES[key] = request.json_body
# 	except ValueError:
# 		return False
# 	return True



from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid, effective_principals
from pyramid.view import view_config

info_desc = """\
This service is useful to get and set data for a user.
"""


user_info = Service(name='users', path='/{username}/info',
                    description=info_desc)

_USERS = defaultdict(dict)


@user_info.get()
def get_info(request):
    """Returns the public information about a **user**.

    If the user does not exists, returns an empty dataset.
    """
    username = request.matchdict['username']
    print("Lookup: " + username)
    return _USERS[username]


@user_info.post()
def set_info(request):
    """Set the public information for a **user**.

    You have to be that user, and *authenticated*.

    Returns *True* or *False*.
    """
    print("Post")
    username = authenticated_userid(request)
    if request.matchdict["username"] != username:
        raise Forbidden()
    _USERS[username] = request.json_body
    print("success")
    return {'success': True}


@view_config(route_name="whoami", permission="authenticated", renderer="json")
def whoami(request):
    """View returning the authenticated user's credentials."""
    username = authenticated_userid(request)
    principals = effective_principals(request)
    return {"username": username, "principals": principals}