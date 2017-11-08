"""
Twitter OAuth handler of D-BAS

App is registered by the account of Tobias Krauthoff

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/examples.html
Manage Google Client IDs: https://apps.twitter.com/
"""

import os
import json
from requests_oauthlib.oauth2_session import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError
from dbas.logger import logger
from dbas.handler.user import values
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _


def start_flow():
    """

    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTKEY', None)

    logger('Twitter OAuth', 'start_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    authorization_base_url = 'https://api.twitter.com/oauth2/token'
    twitter = OAuth2Session(client_id)
    authorization_url, state = twitter.authorization_url(authorization_base_url)

    logger('Twitter OAuth', 'start_flow', 'Please go to {} and authorize access'.format(authorization_url))
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(redirect_response, ui_locales):
    """

    :param redirect_response:
    :param ui_locales:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTKEY', None)
    twitter = OAuth2Session(client_id)

    logger('Twitter OAuth', 'continue_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    try:
        token_url = 'https://twitter.com/oauth/request_token'
    except InsecureTransportError:
        logger('Twitter OAuth', 'continue_flow', 'OAuth 2 MUST utilize https', error=True)
        _tn = Translator(ui_locales)
        return {'user': '', 'missing': '', 'error': _tn.get(_.internalErrorHTTPS)}

    twitter.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

    resp = twitter.get('https://api.github.com/user')
    logger('Twitter OAuth', 'continue_flow', str(resp.text))
    parsed_resp = json.loads(resp.text)

    user_data = {}

    missing_data = [key for key in values if len(user_data[key]) == 0]

    return {
        'user': user_data,
        'missing': missing_data,
        'error': ''
    }
