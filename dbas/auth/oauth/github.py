"""
Github OAuth handler of D-BAS

App is registered by the account of hhucn

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/github.html
Manage Github Client IDs: https://github.com/organizations/**YOUR_ACCOUNT**/settings/applications
"""

import os
import json
from requests_oauthlib.oauth2_session import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError, InvalidClientError, MissingTokenError
from dbas.logger import logger
from slugify import slugify
from dbas.handler.user import oauth_values
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
scope = ['user:email']


def start_flow():
    """

    :return:
    """
    client_id = os.environ.get('OAUTH_GITHUB_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_GITHUB_CLIENTKEY', None)

    logger('Github OAuth', 'Read OAuth id/secret: none? {}/{}'.format(client_id is None, client_secret is None))

    github = OAuth2Session(client_id, scope=scope)
    authorization_url, state = github.authorization_url(authorization_base_url)

    logger('Github OAuth', 'Please go to {} and authorize access'.format(authorization_url))
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(authorization_response, ui_locales):
    """

    :param authorization_response:
    :param ui_locales:
    :return:
    """
    client_id = os.environ.get('OAUTH_GITHUB_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_GITHUB_CLIENTKEY', None)
    github = OAuth2Session(client_id)

    logger('Github OAuth', 'Read OAuth id/secret: none? {}/{}'.format(client_id is None, client_secret is None))
    logger('Github OAuth', 'authorization_response: ' + authorization_response)

    try:
        github.fetch_token(token_url, client_secret=client_secret, authorization_response=authorization_response)
    except InsecureTransportError:
        logger('Github OAuth', 'OAuth 2 MUST utilize https', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}
    except InvalidClientError:
        logger('Github OAuth', 'InvalidClientError', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}
    except MissingTokenError:
        logger('Github OAuth', 'MissingTokenError', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}

    resp = github.get('https://api.github.com/user')
    logger('Github OAuth', str(resp.text))
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

    logger('Github OAuth', 'user_data: ' + str(user_data))
    logger('Github OAuth', 'missing_data: ' + str(missing_data))

    return {
        'user': user_data,
        'missing': missing_data,
        'error': ''
    }


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
