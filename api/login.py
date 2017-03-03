"""
Logic for user login, token generation and validation

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

import binascii
import hashlib
import json
import os
from datetime import datetime

import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.views import user_login

from .lib import HTTP401, logger

log = logger()


def _create_salt(nickname):
    rnd = binascii.b2a_hex(os.urandom(64))
    timestamp = datetime.now().isoformat().encode('utf-8')
    nickname = nickname.encode('utf-8')
    return rnd + timestamp + nickname


def _create_token(nickname, alg='sha512'):
    """
    Use the system's urandom function to generate a random token and convert it to ASCII.

    :return:
    """
    salt = _create_salt(nickname)
    return hashlib.new(alg, salt).hexdigest()


def valid_token(request):
    """
    Validate the submitted token. Checks if a user is logged in and prepares a dictionary, which is then passed to DBAS.

    :param request:
    :return:
    """
    header = 'X-Messaging-Token'
    htoken = request.headers.get(header)
    if htoken is None or htoken == "null":
        log.debug("[API] htoken is None")
        raise HTTP401()
    try:
        user, token = htoken.split('-', 1)
    except ValueError:
        log.debug("[API] Could not split htoken: %s" % htoken)
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

    # Prepare data for DB-AS
    request.validated['user'] = user
    request.validated['user_uid'] = db_user.uid
    request.validated['session_id'] = request.session.id


def validate_login(request, **kwargs):
    """
    Takes token from request and validates it.

    :param request:
    :return:
    """
    header = 'X-Messaging-Token'
    htoken = request.headers.get(header)
    if htoken is None:
        log.debug("[API] No htoken set")
        return

    valid_token(request)


def token_to_database(nickname, token):
    """
    Store the newly created token in database.

    :param nickname: user's nickname
    :param token: new token to be stored
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    if not db_user:
        raise HTTP401()

    db_user.set_token(token)
    db_user.update_token_timestamp()
    transaction.commit()


def validate_credentials(request, **kwargs):
    """
    Parse credentials from POST request and validate it against DBA-S' database.

    :param request:
    :return:
    """
    # Decode received data
    # TODO use api.log.json_bytes_to_dict
    data = request.body.decode('utf-8')
    data = json.loads(data)
    nickname = data['nickname']
    password = data['password']

    # Check in DB-AS' database, if the user's credentials are valid
    logged_in = user_login(request, nickname, password, for_api=True)
    if isinstance(logged_in, str):
        logged_in = json.loads(logged_in)  # <-- I hate that this is necessary!

    if logged_in.get('status') == 'success':
        token = _create_token(nickname)
        user = {'nickname': nickname, 'token': token}
        token_to_database(nickname, token)
        request.validated['user'] = user
    else:
        log.error('API Not logged in: %s' % logged_in)
        request.errors.add('body', logged_in.get("error"))
