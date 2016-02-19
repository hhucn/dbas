""" Cornice services.
"""
from cornice import Service
from dbas.views import Dbas

# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

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
login      = Service(name='login',
					 path='/login',
					 description="Log into account of external discussion system",
					 cors_policy=cors_policy)
# news       = Service(name='api_news',
# 					 path='/get_news',
# 					 description="News app",
# 					 cors_policy=cors_policy)
# reaction   = Service(name='api_reaction',
# 					 path='/{slug}/reaction/{arg_id_user}/{mode}*arg_id_sys',
# 					 description="Discussion Reaction",
# 					 cors_policy=cors_policy)
# justify    = Service(name='api_justify',
# 					 path='/{slug}/justify/{statement_or_arg_id}/{mode}*relation',
# 					 description="Discussion Justify",
# 					 cors_policy=cors_policy)
# attitude   = Service(name='api_attitude',
# 					 path='/{slug}/attitude/*statement_id',
# 					 description="Discussion Attitude",
# 					 cors_policy=cors_policy)
# init       = Service(name='api_init',
# 					 path='/{slug}',
# 					 description="Discussion Init",
# 					 cors_policy=cors_policy)
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


##################################

import os
import binascii
import json

from webob import Response, exc
from cornice import Service

users = Service(name='users', path='/users', description="Users")
_USERS = {}


#
# Helpers
#
def _create_token():
	"""
	Use the system's urandom function to generate a random token and convert it to ASCII.
	"""
	return binascii.b2a_hex(os.urandom(20))


class _401(exc.HTTPError):
	"""
	Return a 401 HTTP Error message if user is not authenticated
	"""
	def __init__(self, msg='Unauthorized'):
		body = {'status': 401, 'message': msg}
		Response.__init__(self, json.dumps(body))
		self.status = 401
		self.content_type = 'application/json'


def valid_token(request):
	"""
	Validate the submitted token. Checks if a user is logged in.

	:param request:
	:return:
	"""
	header = 'X-Messaging-Token'
	htoken = request.headers.get(header)
	if htoken is None:
		raise _401()
	try:
		user, token = htoken.split('-', 1)
	except ValueError:
		raise _401()

	valid = user in _USERS and _USERS[user] == token
	if not valid:
		raise _401()

	request.validated['user'] = user


def unique(request):
	name = request.body
	if name in _USERS:
		request.errors.add('url', 'name', 'This user exists!')
	else:
		user = {'name': name, 'token': _create_token()}
		request.validated['user'] = user


#
# Services - User Management
#
@users.get(validators=valid_token)
def get_users(request):
	"""Returns a list of all users."""
	return {'users': _USERS}


@users.post(validators=unique)
def login(request):
	"""Adds a new user."""
	user = request.validated['user']
	if type(user['name'] == bytes):
		_USERS[user['name'].decode('utf-8')] = user['token'].decode('utf-8')
	else:
		_USERS[user['name']]= user['token']
	return {'token': '%s-%s' % (user['name'], user['token'])}

########################
# Historical functions #
########################
#@users.post(validators=unique)
#def create_user(request):
#	"""Adds a new user."""
#	user = request.validated['user']
#	if type(user['name'] == bytes):
#		_USERS[user['name'].decode('utf-8')] = user['token'].decode('utf-8')
#	else:
#		_USERS[user['name']]= user['token']
#	return {'token': '%s-%s' % (user['name'], user['token'])}