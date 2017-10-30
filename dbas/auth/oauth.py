"""
OAuth handler of D-BAS

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
Manage Google Client IDs: https://console.developers.google.com/apis/credentials
"""

import os
from requests_oauthlib.oauth2_session import OAuth2Session

from dbas.logger import logger


def start_google_flow(redirect_uri):
    """

    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTKEY', None)

    logger('oauth2', 'start_google_flow', 'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    # OAuth endpoints given in the Google API documentation
    authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'

    scope = ['https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile']
    google = OAuth2Session(
        client_id,
        # redirect_uri=redirect_uri,
        redirect_uri='https://dbas.cs.hhu.de',  # for testing
        scope=scope)

    authorization_url, state = google.authorization_url(
        authorization_base_url,
        access_type='offline',
        prompt='select_account')

    logger('oauth2', 'start_google_flow', 'Please go to {} and authorize access'.format(authorization_url))
    # TODO: HOW TO TEST WITH LOCALHOST
    return {'authorization_url': authorization_url}


def continue_google_flow(mainpage, authorization_response):
    """

    :param redirect_uri:
    :param authorization_response: Response uri given by user after clicking on 'authorization_url' of flow start
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_GOOGLE_CLIENTKEY', None)

    logger('oauth2', 'continue_google_flow', 'Read OAuth id: none? {}'.format(client_id is None))
    logger('oauth2', 'continue_google_flow', 'Read OAuth secret: none? {}'.format(client_secret is None))

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
    logger('oauth2', 'start_google_flow', 'Token: {}'.format(token))

    r = google.get('https://www.googleapis.com/oauth2/v2/userinfo?alt=json')

    logger('oauth2', 'start_google_flow', str(r))
    return None
