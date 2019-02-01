"""
Google OAuth handler of D-

App is registered by the account of dbas.hhu@gmail.com

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
Manage Google Client IDs: https://console.developers.google.com/apis/credentials
"""

import json
import logging
import os

from oauthlib.oauth2.rfc6749.errors import InsecureTransportError, InvalidClientError, MissingTokenError
from requests_oauthlib.oauth2_session import OAuth2Session

from dbas.auth.oauth import get_oauth_ret_dict
from dbas.handler.user import oauth_values
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)
SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
         'https://www.googleapis.com/auth/userinfo.profile']
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'


def start_flow(**kwargs):
    """
    Starts the oauth flow. This will return a dict which causes a redirect to the providers page.

    :param kwargs: should have a redirect_uri
    :return:
    """
    redirect_uri = kwargs.get('redirect_uri')
    client_id = os.environ.get('OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_GOOGLE_CLIENTKEY', None)

    if 'service=google' not in redirect_uri:
        bind = '#' if '?' in redirect_uri else '?'
        redirect_uri = '{}{}{}'.format(redirect_uri, bind, 'service=google')

    LOG.debug("Read OAuth id/secret: none? %s/%s", client_id is None, client_secret is None)

    # OAuth endpoints given in the Google API documentation
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=SCOPE)

    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type='offline',
                                                        prompt='select_account')

    LOG.debug("Please go to %s and authorize access", authorization_url)
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(redirect_uri, authorization_response, ui_locales):
    """
    Continues the oauth flow. This will fetch the login tokens and login the user if all information were given.
    Otherwise the registration modal will be displayed.

    :param redirect_uri:
    :param authorization_response:
    :param ui_locales:
    :return:
    """
    client_id = os.environ.get('OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_GOOGLE_CLIENTKEY', None)
    _tn = Translator(ui_locales)

    LOG.debug("Read OAuth id/secret: none? %s/%s", client_id is None, client_secret is None)

    if 'service=google' not in redirect_uri:
        bind = '#' if '?' in redirect_uri else '?'
        redirect_uri = '{}{}{}'.format(redirect_uri, bind, 'service=google')

    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=SCOPE)

    try:
        token = google.fetch_token(TOKEN_URL, authorization_response=authorization_response,
                                   client_secret=client_secret)
    except InsecureTransportError:
        LOG.debug("OAuth2 MUST utilize https")
        return get_oauth_ret_dict(error_str=_tn.get(_.internalErrorHTTPS))
    except InvalidClientError:
        LOG.debug("InvalidClientError")
        return get_oauth_ret_dict(error_str=_tn.get(_.internalErrorHTTPS))
    except MissingTokenError:
        LOG.debug("MissingTokenError")
        return get_oauth_ret_dict(error_str=_tn.get(_.internalErrorHTTPS))

    LOG.debug("Token: %s", token)

    resp = google.get('https://www.googleapis.com/oauth2/v2/userinfo?alt=json')
    LOG.debug("%s", resp.text)
    parsed_resp = json.loads(resp.text)

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

    gender = 'n'
    if 'gender' in parsed_resp:
        gender = 'm' if parsed_resp['gender'] == 'male' else 'f' if parsed_resp['gender'] == 'female' else ''

    user_data = __prepare_data(parsed_resp, gender, ui_locales)
    missing_data = [key for key in oauth_values if len(user_data[key]) == 0 or user_data[key] == 'null']

    LOG.debug("user_data: %s", user_data)
    LOG.debug("missing_data: %s", missing_data)

    return get_oauth_ret_dict(user_data=user_data, missing_data=missing_data)


def __prepare_data(parsed_resp, gender, ui_locales):
    return {
        'id': parsed_resp['id'],
        'firstname': parsed_resp.get('given_name', ''),
        'lastname': parsed_resp.get('family_name', ''),
        'nickname': str(parsed_resp.get('email')).split('@')[0],
        'gender': gender,
        'email': str(parsed_resp.get('email')),
        'ui_locales': 'de' if parsed_resp['locale'] == 'de' else ui_locales
    }
