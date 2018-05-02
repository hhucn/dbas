"""
Facebook OAuth handler of D-BAS

App is registered by the account of Tobias Krauthoff

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
Manage Google Client IDs: https://developers.facebook.com/apps/
"""

import os
import json
from requests_oauthlib.oauth2_session import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError, InvalidClientError, MissingTokenError
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from dbas.logger import logger
from dbas.handler.user import oauth_values
from dbas.strings.translator import Translator
from dbas.strings.keywords import Keywords as _


def start_flow(redirect_uri):
    """

    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('OAUTH_FACEBOOK_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_FACEBOOK_CLIENTKEY', None)

    logger('Facebook OAuth', 'Read OAuth id/secret: none? {}/{}'.format(client_id is None, client_secret is None))

    if 'service=facebook' not in redirect_uri:
        bind = '#' if '?' in redirect_uri else '?'
        redirect_uri = '{}{}{}'.format(redirect_uri, bind, 'service=facebook')

    authorization_base_url = 'https://www.facebook.com/dialog/oauth'

    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
    facebook = facebook_compliance_fix(facebook)

    authorization_url, state = facebook.authorization_url(authorization_base_url)

    logger('Facebook OAuth', 'Please go to {} and authorize access'.format(authorization_url))
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(redirect_uri, authorization_response, ui_locales):
    """

    :param redirect_uri:
    :param authorization_response:
    :param ui_locales:
    :return:
    """
    client_id = os.environ.get('OAUTH_FACEBOOK_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_FACEBOOK_CLIENTKEY', None)

    bind = '#' if '?' in redirect_uri else '?'
    if 'service=facebook' not in redirect_uri:
        redirect_uri = '{}{}{}'.format(redirect_uri, bind, 'service=facebook')
    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)

    logger('Facebook OAuth', 'Read OAuth id/secret: none? {}/{}'.format(client_id is None, client_secret is None))
    logger('Facebook OAuth', 'authorization_response: ' + authorization_response)

    token_url = 'https://graph.facebook.com/oauth/access_token'
    try:
        facebook.fetch_token(token_url, client_secret=client_secret, authorization_response=authorization_response)
    except InsecureTransportError:
        logger('Facebook OAuth', 'OAuth 2 MUST utilize https', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}
    except InvalidClientError:
        logger('Facebook OAuth', 'InvalidClientError', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}
    except MissingTokenError:
        logger('Facebook OAuth', 'MissingTokenError', error=True)
        _tn = Translator(ui_locales)
        return {'user': {}, 'missing': {}, 'error': _tn.get(_.internalErrorHTTPS)}

    resp = facebook.get('https://graph.facebook.com/me?fields=name,email,first_name,last_name,gender,locale')
    logger('Facebook OAuth', str(resp.text))
    parsed_resp = json.loads(resp.text)

    # example response
    # 'id': '1918366001511208'
    # 'first_name': 'Tobias'
    # 'name': 'Tobias Kraut'
    # 'last_name': 'Kraut'
    # 'gender': 'male'
    # 'locale': 'de_DE'

    gender = 'n'
    if 'gender' in parsed_resp:
        if parsed_resp['gender'] == 'male':
            gender = 'm'
        if parsed_resp['gender'] == 'female':
            gender = 'f'

    user_data = __prepare_data(parsed_resp, gender, ui_locales)
    missing_data = [key for key in oauth_values if len(user_data[key]) == 0 or user_data[key] is 'null']

    logger('Facebook OAuth', 'user_data: ' + str(user_data))
    logger('Facebook OAuth', 'missing_data: ' + str(missing_data))

    return {
        'user': user_data,
        'missing': missing_data,
        'error': ''
    }


def __prepare_data(parsed_resp, gender, ui_locales):
    return {
        'id': parsed_resp['id'],
        'firstname': parsed_resp.get('first_name', ''),
        'lastname': parsed_resp.get('last_name', ''),
        'nickname': parsed_resp.get('name', '').replace(' ', ''),
        'gender': gender,
        'email': str(parsed_resp.get('email')),
        'ui_locales': 'de' if parsed_resp['locale'] == 'de_DE' else ui_locales
    }
