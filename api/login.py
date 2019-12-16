"""
Logic for user login, token generation and validation
"""
import datetime
import json
import time
from typing import Union

import jwt
from pyramid.request import Request

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

    return check_jwt(request, token) and check_not_temporary_token(request)


def check_not_temporary_token(request) -> bool:
    payload = request.validated['token-payload']

    if 'sub' in payload and payload['sub'] == 'tmp':
        add_error(request, "Temporary token",
                  verbose_long="You can use a temporary token only with an application token to get a general user token",
                  status_code=401, location="header")
        return False
    return True


def decode_jwt(request, token) -> dict:
    secret = request.registry.settings['public_key']
    return jwt.decode(token, secret, algorithms=['ES256', 'ES512', 'ES384'])


def check_jwt(request, token) -> bool:
    try:
        payload = decode_jwt(request, token)
    except jwt.ExpiredSignatureError as e:
        add_error(request, "Token expired", verbose_long=str(e), status_code=401, location="header")
        return False
    except jwt.InvalidTokenError:
        add_error(request, "Invalid token", status_code=401, location="header")
        return False

    user_by_id: User = DBDiscussionSession.query(User).get(payload['id'])
    if user_by_id is None:
        add_error(request, "Invalid token: user id is unknown", status_code=401, location="header")
        return False

    nickname_from_token = payload.get('nickname')
    if nickname_from_token is not None and nickname_from_token != user_by_id.nickname:
        add_error(request, "Invalid token: nickname and id do not match", status_code=401, location="header")
        return False

    request.validated['token-payload'] = payload
    request.validated['user'] = user_by_id
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


def encode_payload(request: Request, payload: dict) -> str:
    if 'iat' not in payload:
        payload['iat'] = int(
            time.time())  # 'issued at' may be used for make all tokens before a specific time invalid (e.g. password change, "logout of all services")

    return jwt.encode(payload, request.registry.settings['secret_key'], algorithm='ES256').decode("utf-8")


def user_payload(user: User):
    return {
        'nickname': user.nickname,
        'id': user.uid,
        'group': user.group.name
    }


def get_api_token(request: Request, user: User, expires: Union[datetime.datetime, int] = None) -> str:
    payload = user_payload(user)
    if expires:
        payload['exp'] = expires

    return encode_payload(request, payload)


def get_expiring_api_token(request: Request, user: User, minutes: int) -> str:
    expires = int(time.time()) + (minutes * 60)  # seconds

    return get_api_token(request, user, expires)


def get_tmp_token_for_external_service(request: Request, user: User, minutes: int = None) -> str:
    payload = user_payload(user)
    payload['sub'] = 'tmp'

    if minutes:
        payload['exp'] = int(time.time()) + (minutes * 60)

    return encode_payload(request, payload)


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
    del request.validated['password']

    # Check in DB-AS' database, if the user's credentials are valid
    logged_in = login_local_user(nickname, password, request.mailer)
    db_user: User = logged_in.get('user')
    if db_user:
        request.validated['nickname']: str = db_user.nickname
        request.validated['user']: User = db_user
        request.validated['token'] = get_api_token(request, db_user)
    else:
        add_error(request, 'Could not login user', location="header", status_code=401)
