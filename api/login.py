"""
Logic for user login, token generation and validation

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import binascii
import hashlib
import json
import os
from datetime import datetime
from typing import Union

import transaction

from admin.lib import check_api_token
from dbas.auth.login import login_local_user
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.lib import get_user_by_case_insensitive_nickname, nick_of_anonymous_user
from dbas.validators.lib import add_error
from .lib import json_to_dict, logger

log = logger()


def __create_salt(nickname):
    rnd = binascii.b2a_hex(os.urandom(64))
    timestamp = datetime.now().isoformat().encode('utf-8')
    nickname = nickname.encode('utf-8')
    return rnd + timestamp + nickname


def __create_token(nickname, alg='sha512') -> hashlib:
    """
    Use the system's urandom function to generate a random token and convert it
    to ASCII.

    :type nickname: str
    :return:
    """
    salt = __create_salt(nickname)
    return hashlib.new(alg, salt).hexdigest()


def token_to_database(db_user: User, token: Union[str, None]) -> None:
    """
    Store the newly created token in database.

    :param db_user: User
    :param token: new token to be stored
    :return:
    """
    db_user.set_token(token)
    db_user.update_token_timestamp()
    transaction.commit()


# #############################################################################
# Dispatch API attempts by type

def check_auth_token(request, nickname: str, token: str) -> bool:
    log.info("[API] Login attempt from user {}".format(nickname))
    db_user: User = get_user_by_case_insensitive_nickname(nickname)

    if not db_user or db_user.uid == 1:
        add_error(request, "Unknown user", status_code=401, location="header")
        return False

    if db_user.token and db_user.token == token:
        request.validated['user'] = db_user
        request.validated['auth-by-api-token'] = False
        return True

    if check_api_token(token):
        request.validated['user'] = db_user
        request.validated['auth-by-api-token'] = True
        return True

    else:
        add_error(request, "Invalid token", status_code=401, location="header")
        return False


# #############################################################################
# Validators


def validate_login(request, **_kwargs):
    valid_token(request)


def valid_token_optional(request, **_kwargs):
    """
    Look for token in header. If it is provided, it has to be valid. Else return the anonymous user.

    :param request: Request
    :param _kwargs: unused renderer etc.
    :return:
    """
    if 'X-Authentication' in request.headers:
        try:
            payload = json_to_dict(request.headers.get('X-Authentication'))

            if payload.get('nickname') == nick_of_anonymous_user:
                request.validated['user'] = DBDiscussionSession.query(User).get(1)
            else:
                valid_token(request)

        except json.decoder.JSONDecodeError:
            add_error(request, "Invalid JSON in token")
            return False
    else:
        request.validated['user'] = DBDiscussionSession.query(User).get(1)


def valid_token(request, **_kwargs) -> bool:
    """
    Validate the submitted token. Checks if a user is logged in and prepares a
    dictionary, which is then passed to DBAS.

    :param request:
    :return:
    """
    header = 'X-Authentication'
    htoken = request.headers.get(header)
    if not htoken or htoken == "null":
        add_error(request, "Received invalid or empty authentication token",
                  verbose_long="Please provide the authentication token in the X-Authentication field!",
                  location="header", status_code=401)
        return False

    try:
        payload = json_to_dict(htoken)
        return check_auth_token(request, payload.get('nickname'), payload.get('token'))
    except json.decoder.JSONDecodeError:
        add_error(request, "Invalid JSON in token")


def valid_api_token(request, **kwargs) -> bool:
    valid_token(request, **kwargs)
    if request.validated.get('auth-by-api-token', False):
        return True
    else:
        add_error(request, "This method is only allowed with an API-token!")
        return False


def validate_credentials(request, **_kwargs) -> None:
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
    logged_in = login_local_user(nickname, password, request.mailer)
    db_user: User = logged_in.get('user')
    if db_user:
        token = __create_token(db_user.nickname)
        token_to_database(db_user, token)
        request.validated['nickname']: str = db_user.nickname
        request.validated['user']: User = db_user
        request.validated['token'] = token
    else:
        add_error(request, 'Could not login user', location="header", status_code=401)
