"""
Github OAuth handler of D-BAS

App is registered by the account of hhucn

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/github.html
Manage Github Client IDs: https://github.com/organizations/**YOUR_ACCOUNT**/settings/applications
"""

import json
import logging
import os
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError, InvalidClientError, MissingTokenError
from requests_oauthlib.oauth2_session import OAuth2Session
from slugify import slugify

from dbas.auth.oauth import get_oauth_ret_dict
from dbas.handler.user import oauth_values
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

CLIENT_ID = os.environ.get('OAUTH_GITHUB_CLIENTID', None)
CLIENT_SECRET = os.environ.get('OAUTH_GITHUB_CLIENTKEY', None)
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'
SCOPE = ['user:email']


def start_flow():
    """
    Starts the oauth flow. This will return a dict which causes a redirect to the providers page.

    """

    log = logging.getLogger(__name__)
    log.debug("Read OAuth id/secret: none? %s/%s", CLIENT_ID is None, CLIENT_SECRET is None)

    github = OAuth2Session(CLIENT_ID, scope=SCOPE)
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)

    log.debug("Please go to %s and authorize access", authorization_url)
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(authorization_response, ui_locales):
    """
    Continues the oauth flow. This will fetch the login tokens and login the user if all information were given.
    Otherwise the registration modal will be displayed.

    :param authorization_response:
    :param ui_locales:
    :return:
    """
    github = OAuth2Session(CLIENT_ID)
    _tn = Translator(ui_locales)

    log = logging.getLogger(__name__)
    log.debug("Read OAuth id/secret: none? %s/%s", CLIENT_ID is None, CLIENT_SECRET is None)
    log.debug("authorization_response: %s", authorization_response)

    try:
        github.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=authorization_response)
    except InsecureTransportError:
        log.debug("Oauth2 MUST utilize https")
        return get_oauth_ret_dict(error_str=_tn.get(_.internalErrorHTTPS))
    except InvalidClientError:
        log.debug("InvalidClientError")
        return get_oauth_ret_dict(error_str=_tn.get(_.internalErrorHTTPS))
    except MissingTokenError:
        log.debug("MissingTokenError")
        return get_oauth_ret_dict(error_str=_tn.get(_.internalErrorHTTPS))

    resp = github.get('https://api.github.com/user')
    log.debug("%s", resp.text)
    parsed_resp = json.loads(resp.text)

    # 'login': 'tkrauthoff'
    # 'id': 5970416
    # 'avatar_url': 'https://avatars0.githubusercontent.com/u/5970416?v=4'
    # 'gravatar_id': ''
    # 'url': 'https://api.github.com/users/tkrauthoff'
    # 'html_url': 'https://github.com/tkrauthoff'
    # 'followers_url': 'https://api.github.com/users/tkrauthoff/followers'
    # 'following_url': 'https://api.github.com/users/tkrauthoff/following{/other_user'
    # 'gists_url': 'https://api.github.com/users/tkrauthoff/gists{/gist_id'
    # 'starred_url': 'https://api.github.com/users/tkrauthoff/starred{/owner}{/repo'
    # 'subscriptions_url': 'https://api.github.com/users/tkrauthoff/subscriptions'
    # 'organizations_url': 'https://api.github.com/users/tkrauthoff/orgs'
    # 'repos_url': 'https://api.github.com/users/tkrauthoff/repos'
    # 'events_url': 'https://api.github.com/users/tkrauthoff/events{/privacy'
    # 'received_events_url': 'https://api.github.com/users/tkrauthoff/received_events'
    # 'type': 'User'
    # 'site_admin': false
    # 'name': 'Tobias Krauthoff'
    # 'company': 'hhucn '
    # 'blog': 'http://www.tsn.hhu.de/en/ourgroup/scientists/tobias-krauthoff.html'
    # 'location': 'Duesseldorf'
    # 'email': null
    # 'hireable': null
    # 'bio': 'Computer scientist and doctoral student'
    # 'public_repos': 4
    # 'public_gists': 0
    # 'followers': 4
    # 'following': 4
    # 'created_at': 2013-11-18T15:19:32Z
    # 'updated_at': 2017-10-24T07:01:29Z

    user_data = __prepare_data(parsed_resp)
    missing_data = [key for key in oauth_values if len(user_data[key]) == 0 or user_data[key] is 'null']

    log.debug("user_data: %s", user_data)
    log.debug("missing_data: %s", missing_data)

    return get_oauth_ret_dict(user_data=user_data, missing_data=missing_data)


def __prepare_data(parsed_resp):
    return {
        'id': parsed_resp.get('id', ''),
        'firstname': parsed_resp.get('name', '').rsplit(' ', 1)[0],
        'lastname': parsed_resp.get('name', '').rsplit(' ', 1)[1],
        'nickname': slugify(parsed_resp.get('login', '')),
        'gender': 'n',
        'email': str(parsed_resp.get('email')),
        'ui_locales': 'en'
    }
