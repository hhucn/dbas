"""
Google OAuth handler of D-

App is registered by dbas.hhu@gmail.com's Account

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
Manage Google Client IDs: https://console.developers.google.com/apis/credentials
"""

import os
import json
from slugify import slugify
from requests_oauthlib.oauth2_session import OAuth2Session
from dbas.logger import logger


def start_flow(redirect_uri):
    """

    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTKEY', None)

    logger('Google OAuth', 'start_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    # OAuth endpoints given in the Google API documentation
    authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'

    scope = ['https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile']
    google = OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        # redirect_uri='https://dbas.cs.hhu.de',  # TODO: FOR TESTING
        scope=scope)

    authorization_url, state = google.authorization_url(
        authorization_base_url,
        access_type='offline',
        prompt='select_account')

    logger('Google OAuth', 'start_flow', 'Please go to {} and authorize access'.format(authorization_url))
    # TODO: HOW TO TEST WITH LOCALHOST
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(mainpage, authorization_response):
    """

    :param mainpage:
    :param authorization_response: Response uri given by user after clicking on 'authorization_url' of flow start
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTKEY', None)

    logger('oauth2', 'continue_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    scope = ['https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile']

    google = OAuth2Session(
        client_id,
        redirect_uri=mainpage,
        scope=scope)

    token_url = 'https://accounts.google.com/o/oauth2/token'

    token = google.fetch_token(
        token_url,
        authorization_response=authorization_response,
        client_secret=client_secret)
    logger('Google OAuth', 'continue_flow', 'Token: {}'.format(token))

    resp = google.get('https://www.googleapis.com/oauth2/v2/userinfo?alt=json')
    logger('Google OAuth', 'continue_flow', str(resp.text))
    parsed_resp = json.loads(resp.text)

    user_data = {
        'given_name': parsed_resp['ad'],
        'lastname': parsed_resp['family_name'],
        'nickname': slugify(parsed_resp['name']),  # TODO: NICKNAME
        'gender': 'm' if parsed_resp['gender'] == 'male' else 'f' if parsed_resp['gender'] == 'female' else 'n',
        'email': parsed_resp['email'],
        'password': parsed_resp['ad'],  # TODO: PASSWORD
        'ui_locales': 'de' if parsed_resp['locale'] == 'de' else 'en'
    }
    # example response
    # 'family_name': 'Krauthoff',
    # 'locale': 'de',
    # 'picture': 'https://lh3.googleusercontent.com/-oHifqnhsSEI/AAAAAAAAAAI/AAAAAAAAA_E/FOOl5HaFX4E/photo.jpg',
    # 'email': 'tobias.krauthoff@googlemail.com',
    # 'id': '112556997662022178084',
    # 'verified_email': True,
    # 'name': 'Tobias Krauthoff',
    # 'gender': 'male',
    # 'given_name': 'Tobias',
    # 'link': 'https://plus.google.com/112556997662022178084'}

    return user_data
