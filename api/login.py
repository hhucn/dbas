# Logic for user login, token generation and validation
#
# @author Christian Meter, Tobias Krauthoff
# @email {meter, krauthoff}@cs.uni-duesseldorf.de

import binascii
import json
import hashlib
import os

from datetime import datetime
from dbas import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.views import Dbas
from .lib import logger, HTTP401

log = logger()


def _create_token(nickname, alg='sha512'):
	"""
	Use the system's urandom function to generate a random token and convert it to ASCII.
	:return:
	"""
	salt = _create_salt(nickname)
	return hashlib.new(alg, salt).hexdigest()


def _create_salt(nickname):
	rnd = binascii.b2a_hex(os.urandom(64))
	timestamp = datetime.now().isoformat().encode('utf-8')
	nickname = nickname.encode('utf-8')
	return rnd + timestamp + nickname


def validate_login(request):
	"""
	Takes token from request and validates it. Return true if logged in, else false.
	:param request:
	:return:
	"""
	header = 'X-Messaging-Token'
	htoken = request.headers.get(header)
	if htoken is None:
		log.debug("[API] No htoken set")
		return

	valid_token(request)


def valid_token(request):
	"""
	Validate the submitted token. Checks if a user is logged in and prepares a dictionary, which is then passed to DBAS.
	:param request:
	:return:
	"""
	header = 'X-Messaging-Token'
	htoken = request.headers.get(header)
	if htoken is None:
		log.error("[API] htoken is None")
		raise HTTP401()
	try:
		user, token = htoken.split('-', 1)
	except ValueError:
		log.error("[API] ValueError")
		raise HTTP401()

	log.debug("[API] Login Attempt: %s: %s" % (user, token))

	db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()

	if not db_user:
		log.error("[API] Invalid user")
		raise HTTP401()

	if not db_user.token == token:
		log.error("[API] Invalid Token")
		raise HTTP401()

	log.debug("[API] Valid token")

	# Prepare data for DBAS
	request.validated['user'] = user
	request.validated['session_id'] = request.session.id


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
			token = _create_token(nickname)
			user = {'nickname': nickname, 'token': token}
			request.validated['user'] = user
	except TypeError:
		log.error('API Not logged in: %s' % logged_in)
		request.errors.add(logged_in)
