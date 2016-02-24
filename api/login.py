# Logic for user login, token generation and validation
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import binascii
import json
import os

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
	return binascii.b2a_hex(os.urandom(20))


def valid_token(request):
	"""
	Validate the submitted token. Checks if a user is logged in.
	:param request:
	:return:
	"""
	header = 'X-Messaging-Token'
	htoken = request.headers.get(header)
	if htoken is None:
		log.error("htoken is None")
		raise response401()
	try:
		user, token = htoken.split('-', 1)
	except ValueError:
		log.error("ValueError")
		raise response401()

	log.debug("API Login Attempt: %s: %s" % (user, token))

	users = DBDiscussionSession.query(User).all()
	tokens = filter(None, [user.token for user in users])
	for token in tokens:
		print(token)

	print(tokens)
	for user in users:
		print(user.nickname)

	valid = user in users and token in tokens

	if not valid:
		log.error("API Invalid token")
		raise response401()

	log.debug("API Remote login successful")
	request.validated['user'] = user


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
			user = {'nickname': nickname, 'token': _create_token()}
			request.validated['user'] = user
	except TypeError:
		log.error('API Not logged in: %s' % logged_in)
		request.errors.add(logged_in)
