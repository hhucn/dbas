"""
Logic for user login, token generation and validation

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import binascii
import hashlib
import json
import os
from datetime import datetime

import transaction
from pyramid.httpexceptions import HTTPUnauthorized

from admin.lib import check_token
from dbas.auth.login import login_user
from dbas.lib import get_user_by_case_insensitive_nickname
from .lib import HTTP401, json_to_dict, logger

log = logger()


def add_error(request, msg, status_code=400):
    """
    Log and add errors to the request object.

    :param request:
    :param msg: error msg
    :param status_code: http status code
    :return:
    """
    log.info("[API] " + msg)
    request.errors.add('body', msg)
    request.errors.status = status_code


def __raise_401(msg):
    log.info("[API] " + msg)
    raise HTTP401(msg)


def __create_salt(nickname):
    rnd = binascii.b2a_hex(os.urandom(64))
    timestamp = datetime.now().isoformat().encode('utf-8')
    nickname = nickname.encode('utf-8')
    return rnd + timestamp + nickname


def __create_token(nickname, alg='sha512'):
    """
    Use the system's urandom function to generate a random token and convert it
    to ASCII.

    :type nickname: str
    :return:
    """
    salt = __create_salt(nickname)
    return hashlib.new(alg, salt).hexdigest()


# #############################################################################
# Dispatch API attempts by type

def process_user(request, htoken):
    try:
        nickname, token = htoken.rsplit('-', 1)  # The 1 is important, because nicknames may have their own minus.
    except ValueError:
        raise HTTPUnauthorized()

    log.info("[API] Login Attempt with user {}".format(nickname))

    db_user = get_user_by_case_insensitive_nickname(nickname)

    if not db_user.token == token and not check_token(token):
        __raise_401("Invalid Token")

    log.info("[API] Valid token")

    # Prepare data for DB-AS
    request.validated['user'] = nickname
    request.validated['db_user'] = db_user
    request.validated['user_uid'] = db_user.uid
    request.validated['session_id'] = request.session.id


# #############################################################################
# Validators


def validate_login(request):
    """
    Validate the submitted token. Checks if a user is logged in and prepares a
    dictionary, which is then passed to DBAS.

    :param request:
    :return:
    """
    header = 'X-Authentication'
    htoken = request.headers.get(header)
    if not htoken or htoken == "null":
        msg = "Received invalid or empty authentication token"
        log.info("[API] " + msg)
        raise HTTP401(msg)

    try:
        payload = json_to_dict(htoken)
        process_user(request, payload["token"])
    except json.decoder.JSONDecodeError:
        msg = "Invalid JSON in token"
        log.info("[API] " + msg)
        raise HTTP401("Invalid JSON in token")


def token_to_database(nickname, token):
    """
    Store the newly created token in database.

    :param nickname: user's nickname
    :param token: new token to be stored
    :return:
    """
    db_user = get_user_by_case_insensitive_nickname(nickname)
    db_user.set_token(token)
    db_user.update_token_timestamp()
    transaction.commit()


def validate_credentials(request, **kwargs):
    """
    Parse credentials from POST request and validate it against DBA-S'
    database.

    :param request:
    :return:
    """
    if request.errors:
        return

    nickname = request.validated['nickname']
    password = request.validated['password']

    # Check in DB-AS' database, if the user's credentials are valid
    logged_in = login_user(nickname, password, request.mailer)
    if 'user' in logged_in:
        token = __create_token(nickname)
        token_to_database(nickname, token)
        user = {'nickname': nickname, 'token': token}
        request.validated['db_user'] = logged_in['user']
        request.validated['user'] = user
    else:
        add_error(request, 'Could not login user', 401)
