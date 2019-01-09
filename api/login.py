"""
Logic for user login, token generation and validation

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import json

import jwt

from admin.lib import check_api_token, is_api_token
from dbas.auth.login import login_local_user
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.lib import get_user_by_case_insensitive_nickname, nick_of_anonymous_user
from dbas.validators.lib import add_error
from .lib import json_to_dict, logger

log = logger()


# #############################################################################
# Dispatch API attempts by type

def check_auth_token(request, nickname: str, token: str) -> bool:
    log.info("[API] Login attempt from user {}".format(nickname))
    if is_api_token(token):
        if check_api_token(token):
            request.validated['user'] = get_user_by_case_insensitive_nickname(nickname)
            request.validated['auth-by-api-token'] = True
            return True
        else:
            add_error(request, "Invalid token", status_code=401, location="header")
            return False

    return check_jwt(request, token)


def check_jwt(request, token) -> bool:
    secret = request.registry.settings['public_key']
    try:
        payload = jwt.decode(token, secret, algorithms=['ES256', 'ES512', 'ES384'])
    except jwt.DecodeError as e:
        add_error(request, "Invalid token", status_code=401, location="header")
        return False

    request.validated['user'] = DBDiscussionSession.query(User).get(payload['id'])
    request.validated['auth-by-api-token'] = False
    return True

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
    if 'X-Authentication' in request.headers:
        htoken = request.headers.get('X-Authentication')

        if not htoken or htoken == "null":
            add_error(request, "Received invalid or empty authentication token",
                      verbose_long="Please provide the authentication token in the X-Authentication or Authorization field! Consult the docs.",
                      location="header", status_code=401)
            return False

        try:
            payload = json_to_dict(htoken)
            return check_auth_token(request, payload.get('nickname'), payload.get('token'))
        except json.decoder.JSONDecodeError:
            add_error(request, "Invalid JSON in token")

    elif 'Authorization' in request.headers:
        # Bearer looks like this
        # "Bearer eyJ0eXAiOiJKV1QiLCJbhGciOiJFUzI1NiJ9.eyJuaWNrbmFtZSI6IkNocmlzdGlhbiIsImlkIjozfQ.VWsWZ8vNTwe0rlYcr9kgI9ZjlUBnBZRJm3flXtOKzLR4lMLxVhhoe89ufu04UFfLhksFu7IMj9qGqIzZhhblaA"
        head, token = request.headers.get('Authorization').split(maxsplit=2)
        if head == "Bearer":
            return check_jwt(request, token)

    add_error(request, "Received invalid or empty authentication token",
              verbose_long="Please provide the authentication token in the X-Authentication or Authorization field! Consult the docs.",
              location="header", status_code=401)
    return False



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

    secret = request.registry.settings['secret_key']

    nickname = request.validated['nickname']
    password = request.validated['password']
    del request.validated['password']

    # Check in DB-AS' database, if the user's credentials are valid
    logged_in = login_local_user(nickname, password, request.mailer)
    db_user: User = logged_in.get('user')
    if db_user:
        token = jwt.encode({'nickname': db_user.nickname, 'id': db_user.uid}, secret, algorithm='ES256')
        request.validated['nickname']: str = db_user.nickname
        request.validated['user']: User = db_user
        request.validated['token'] = token
    else:
        add_error(request, 'Could not login user', location="header", status_code=401)
