"""
Google OAuth handler of D-

App is registered by the account of dbas.hhu@gmail.com

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
Manage Google Client IDs: https://console.developers.google.com/apis/credentials
"""

import os
import json
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError, InvalidClientError, MissingTokenError
from requests_oauthlib.oauth2_session import OAuth2Session
from dbas.logger import logger
from dbas.handler.user import oauth_values
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _

scope = ['https://www.googleapis.com/auth/userinfo.email',
         'https://www.googleapis.com/auth/userinfo.profile']
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'


def start_flow(redirect_uri):
    """

    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTKEY', None)

    if 'service=google' not in redirect_uri:
        bind = '#' if '?' in redirect_uri else '?'
        redirect_uri = '{}{}{}'.format(redirect_uri, bind, 'service=google')

    logger('Google OAuth', 'start_flow',
           'Read OAuth id/secret: none? {}/{}'.format(client_id is None, client_secret is None))

    # OAuth endpoints given in the Google API documentation
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    authorization_url, state = google.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')

    logger('Google OAuth', 'start_flow', 'Please go to {} and authorize access'.format(authorization_url))
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(redirect_uri, authorization_response, ui_locales):
    """

    :param redirect_uri:
    :param authorization_response:
    :param ui_locales:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTKEY', None)

    logger('Google OAuth', 'continue_flow',
           'Read OAuth id/secret: none? {}/{}'.format(client_id is None, client_secret is None))

    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    try:
        token = google.fetch_token(token_url, authorization_response=authorization_response, client_secret=client_secret)
    except InsecureTransportError:
        logger('Google OAuth', 'continue_flow', 'OAuth 2 MUST utilize https', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}
    except InvalidClientError:
        logger('Google OAuth', 'continue_flow', 'InvalidClientError', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}
    except MissingTokenError:
        logger('Google OAuth', 'continue_flow', 'MissingTokenError', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}

    logger('Google OAuth', 'continue_flow', 'Token: {}'.format(token))

    resp = google.get('https://www.googleapis.com/oauth2/v2/userinfo?alt=json')
    logger('Google OAuth', 'continue_flow', str(resp.text))
    parsed_resp = json.loads(resp.text)

    user_data = {
        'id': parsed_resp['id'],
        'firstname': parsed_resp['given_name'],
        'lastname': parsed_resp['family_name'],
        'nickname': '',
        'gender': 'm' if parsed_resp['gender'] == 'male' else 'f' if parsed_resp['gender'] == 'female' else '',
        'email': parsed_resp['email'],
        'password': '',
        'ui_locales': 'de' if parsed_resp['locale'] == 'de' else ui_locales
    }

    missing_data = [key for key in oauth_values if len(user_data[key]) == 0]

    # example response
    # 'id': '112556997662022178084'
    # 'name': 'Tobias Krauthoff'
    # 'given_name': 'Tobias'
    # 'family_name': 'Krauthoff'
    # 'gender': 'male'
    # 'email': 'tobias.krauthoff@googlemail.com'
    # 'link': 'https://plus.google.com/112556997662022178084'
    # 'verified_email': True
    # 'locale': 'de'
    # 'picture': 'https://lh3.googleusercontent.com/-oHifqnhsSEI/AAAAAAAAAAI/AAAAAAAAA_E/FOOl5HaFX4E/photo.jpg'

    return {
        'user': user_data,
        'missing': missing_data,
        'error': ''
    }
