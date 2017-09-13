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

from dbas.auth.login import login_user
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from .lib import HTTP401, json_to_dict, logger

log = logger()


def _create_salt(nickname):
    rnd = binascii.b2a_hex(os.urandom(64))
    timestamp = datetime.now().isoformat().encode('utf-8')
    nickname = nickname.encode('utf-8')
    return rnd + timestamp + nickname


def _create_token(nickname, alg='sha512'):
    """
    Use the system's urandom function to generate a random token and convert it
    to ASCII.

    :return:

    """
    salt = _create_salt(nickname)
    return hashlib.new(alg, salt).hexdigest()


def _get_user_by_nickname(nickname):
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        log.info("[API] Invalid user")
        raise HTTP401()
    return db_user


# #############################################################################
# Dispatch API attempts by type

def process_user(request, payload):
    htoken = payload["token"]
    try:
        user, token = htoken.split('-', 1)
    except ValueError:
        log.info("[API] Could not split htoken: {}".format(htoken))
        raise HTTP401()

    log.info("[API] Login Attempt: {}: {}".format(user, token))

    db_user = _get_user_by_nickname(user)

    if not db_user.token == token:
        log.info("[API] Invalid Token")
        raise HTTP401()

    log.info("[API] Valid token")

    # Prepare data for DB-AS
    request.validated['user'] = user
    request.validated['user_uid'] = db_user.uid
    request.validated['session_id'] = request.session.id


# #############################################################################
# Validators

# Map containing the correct functions depending on the type specified in the
# header
dispatch_type = {"user": process_user}


def valid_token(request):
    """
    Validate the submitted token. Checks if a user is logged in and prepares a
    dictionary, which is then passed to DBAS.

    :param request:
    :return:

    """
    header = 'X-Authentication'
    htoken = request.headers.get(header)

    payload = json_to_dict(htoken)
    request_type = payload["type"]
    f = dispatch_type.get(payload["type"])

    if f:
        f(request, payload)
    else:
        log.info("[API] Could not dispatch by type. Is request_type '{}' defined?".format(request_type))
        raise HTTP401()


def validate_login(request, **kwargs):
    """Takes token from request and validates it.

    :param request:
    :return:

    """
    header = 'X-Authentication'
    htoken = request.headers.get(header)
    if htoken is None or htoken == "null":
        log.info("[API] No htoken set")
        return
    valid_token(request)


def token_to_database(nickname, token):
    """Store the newly created token in database.

    :param nickname: user's nickname
    :param token: new token to be stored
    :return:

    """
    db_user = _get_user_by_nickname(nickname)
    db_user.set_token(token)
    db_user.update_token_timestamp()
    transaction.commit()


def validate_credentials(request, **kwargs):
    """Parse credentials from POST request and validate it against DBA-S'
    database.

    :param request:
    :return:

    """
    data = json_to_dict(request.json_body)
    nickname = data.get('nickname')
    password = data.get('password')

    if nickname and password:
        # Check in DB-AS' database, if the user's credentials are valid
        logged_in = login_user(request, nickname, password, for_api=True)
        if isinstance(logged_in, str):
            logged_in = json.loads(logged_in)  # <-- I hate that this is necessary!

        if logged_in.get('status') == 'success':
            token = _create_token(nickname)
            user = {'nickname': nickname, 'token': token}
            token_to_database(nickname, token)
            request.validated['user'] = user
        else:
            log.info('API Not logged in: %s' % logged_in)
            request.errors.add('body', logged_in.get("error"))
    else:
        raise HTTP401
