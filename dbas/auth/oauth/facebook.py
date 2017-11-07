"""
Facebook OAuth handler of D-

App is registered by xxx account

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
Manage Google Client IDs: https://console.developers.google.com/apis/credentials
"""

import os
# import json
from requests_oauthlib.oauth2_session import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from dbas.logger import logger
from dbas.handler.user import values


def start_flow(redirect_uri):
    """

    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_FACEBOOK_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_FACEBOOK_CLIENTKEY', None)

    logger('Facebook OAuth', 'start_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    authorization_base_url = 'https://www.facebook.com/dialog/oauth'

    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
    facebook = facebook_compliance_fix(facebook)

    authorization_url, state = facebook.authorization_url(authorization_base_url)

    logger('Facebook OAuth', 'start_flow', 'Please go to {} and authorize access'.format(authorization_url))
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(redirect_uri, redirect_response):
    """

    :param redirect_uri:
    :param redirect_response:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_FACEBOOK_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_FACEBOOK_CLIENTKEY', None)
    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)

    logger('Facebook OAuth', 'continue_github_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    token_url = 'https://graph.facebook.com/oauth/access_token'
    facebook.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

    resp = facebook.get('https://graph.facebook.com/me?')
    logger('Facebook OAuth', 'continue_flow', str(resp.text))
    # parsed_resp = json.loads(resp.text)

    user_data = {}

    missing_data = [key for key in values if len(user_data[key]) == 0]

    return {
        'user': user_data,
        'missing': missing_data
    }
