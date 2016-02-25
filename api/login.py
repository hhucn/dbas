# Logic for user login, token generation and validation
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import binascii
import json
import os

from pyramid.security import authenticated_userid, remember

from dbas import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.views import Dbas
from .lib import logger, response401

log = logger()
_USERS = {}


def _create_token():
	"""
	Use the system's urandom function to generate a random token and convert it to ASCII.
	:return:
	"""
	return binascii.b2a_hex(os.urandom(64))


def valid_token(request):
	"""
	Validate the submitted token. Checks if a user is logged in.
	:param request:
	:return:
	"""
	print(request)
	request.headers = request.token

	#try:
	#	token = request.token
	#except AttributeError:
	#	raise response401(msg=u'token is empty')
	user_id = authenticated_userid(request)
	print(user_id)
	print(request.authenticated_userid)

	if user_id is None:
		raise response401(msg=u"token cannot parse to a valid username")
	# header = 'X-Messaging-Token'
	# htoken = request.headers.get(header)
	# if htoken is None:
	# 	log.error("htoken is None")
	# 	raise response401()
	# try:
	# 	user, token = htoken.split('-', 1)
	# except ValueError:
	# 	log.error("ValueError")
	# 	raise response401()
	#
	# log.debug("API Login Attempt: %s: %s" % (user, token))
	#
	# print(request)
	#
	# db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
	#
	# if not db_user:
	# 	log.error("API Invalid user")
	# 	raise response401()
	#
	# if not db_user.token == token:
	# 	log.error("API Invalid Token")
	# 	raise response401()
	#
	# log.debug("API Valid token")
	# request.validated['user'] = user


def validate_credentials(request):
	"""
	Parse credentials from POST request and validate it against DBAS' database
	:param request:
	:return:
	"""
	# Decode received data
	data = request.body.decode('utf-8')
	data = json.loads(data)
	nickname = data['nickname']
	password = data['password']

	# Check in DBAS' database, if the user's credentials are valid
	logged_in = Dbas(request).user_login(nickname, password, for_api=True)

	try:
		if logged_in['status'] == 'success':
			print("ping")
			db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
			print("pong")
			if db_user:
				cookie = remember(request, nickname)
				db_user.set_token(cookie)
				request.validated['user'] = db_user
	except TypeError:
		log.error('API Not logged in: %s' % logged_in)
		request.errors.add(logged_in)
