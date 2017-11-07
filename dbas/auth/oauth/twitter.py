"""
Twitter OAuth handler of D-BAS

App is registered by the account of Tobias Krauthoff

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/examples.html
Manage Google Client IDs: https://apps.twitter.com/
"""

import os
import json
from slugify import slugify
from requests_oauthlib.oauth2_session import OAuth2Session
from dbas.logger import logger
from dbas.handler.user import values


def start_flow(redirect_uri):
    """

    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTKEY', None)

    logger('Twitter OAuth', 'start_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    return None


def continue_flow(mainpage, authorization_response):
    """

    :param mainpage:
    :param authorization_response:
    :return:
    """

    user_data = {}

    missing_data = [key for key in values if len(user_data[key]) == 0]

    return {
        'user': user_data,
        'missing': missing_data
    }
