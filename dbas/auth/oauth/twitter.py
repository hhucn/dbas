"""
!!! CURRENTLY NOT USED !!!

Twitter OAuth handler of D-BAS

App is registered by the account of Tobias Krauthoff

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/examples.html
Manage Google Client IDs: https://apps.twitter.com/
"""

import logging
import os
from requests_oauthlib.oauth1_session import OAuth1Session

from dbas.auth.oauth import get_oauth_ret_dict
from dbas.handler.user import oauth_values

LOG = logging.getLogger(__name__)
CLIENT_ID = os.environ.get('OAUTH_TWITTER_CLIENTID', None)
CLIENT_SECRET = os.environ.get('OAUTH_TWITTER_CLIENTKEY', None)


def start_flow(**kwargs):
    """
    Starts the oauth flow. This will return a dict which causes a redirect to the providers page.

    :param kwargs: should have a redirect_uri and a request
    :return:
    """
    redirect_uri = kwargs.get('redirect_uri')
    request = kwargs.get('request')

    LOG.debug("Read OAuth id/secret: none? %s/%s", CLIENT_ID is None, CLIENT_SECRET is None)

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorization_url = 'https://api.twitter.com/oauth/authorize'

    oauth_client = OAuth1Session(CLIENT_ID, client_secret=CLIENT_SECRET, callback_uri=redirect_uri)
    resp = oauth_client.fetch_request_token(request_token_url)
    url = oauth_client.authorization_url(authorization_url)

    request.session['twitter_oauth_token'] = resp.get('oauth_token')
    request.session['twitter_oauth_token_secret'] = resp.get('oauth_token_secret')

    LOG.debug("Please go to %s and authorize access", authorization_url)
    return {'authorization_url': url, 'error': ''}


def continue_flow(request, redirect_response):
    """
    Continues the oauth flow. This will fetch the login tokens and login the user if all information were given.
    Otherwise the registration modal will be displayed.

    :param request:
    :param redirect_response:
    :return:
    """
    client_id = os.environ.get('OAUTH_TWITTER_CLIENTID', None)
    client_secret = os.environ.get('OAUTH_TWITTER_CLIENTKEY', None)

    LOG.debug("Read OAuth id/secret: none? %s/%s", client_id is None, client_secret is None)

    pincode = redirect_response.split('oauth_verifier=')[1]

    access_token_url = 'https://api.twitter.com/oauth/access_token'

    oauth_token = request.session['twitter_oauth_token']
    oauth_token_secret = request.session['twitter_oauth_token_secret']

    oauth_client = OAuth1Session(client_id, client_secret=client_secret,
                                 resource_owner_key=oauth_token,
                                 resource_owner_secret=oauth_token_secret,
                                 verifier=pincode)

    resp = oauth_client.fetch_access_token(access_token_url)

    user_data = {
        'id': resp['id'],
        'nickname': resp['screen_name']
    }

    missing_data = [key for key in oauth_values if len(user_data[key]) == 0]

    return get_oauth_ret_dict(user_data=user_data, missing_data=missing_data)
