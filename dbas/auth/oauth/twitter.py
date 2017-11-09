"""
!!! CURRENTLY NOT USED !!!

Twitter OAuth handler of D-BAS

App is registered by the account of Tobias Krauthoff

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/examples.html
Manage Google Client IDs: https://apps.twitter.com/
"""

import os
# import twitter
from requests_oauthlib.oauth1_session import OAuth1Session
from dbas.logger import logger
from dbas.handler.user import oauth_values


def start_flow(request, redirect_uri):
    """

    :param request:
    :param redirect_uri:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTKEY', None)

    logger('Twitter OAuth', 'start_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorization_url = 'https://api.twitter.com/oauth/authorize'

    oauth_client = OAuth1Session(client_id, client_secret=client_secret, callback_uri=redirect_uri)
    resp = oauth_client.fetch_request_token(request_token_url)
    url = oauth_client.authorization_url(authorization_url)

    request.session['twitter_oauth_token'] = resp.get('oauth_token')
    request.session['twitter_oauth_token_secret'] = resp.get('oauth_token_secret')

    logger('Twitter OAuth', 'start_flow', 'Please go to {} and authorize access'.format(authorization_url))
    return {'authorization_url': url, 'error': ''}


def continue_flow(request, redirect_response):
    """

    :param request:
    :param redirect_response:
    :return:
    """
    client_id = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTID', None)
    client_secret = os.environ.get('DBAS_OAUTH_TWITTER_CLIENTKEY', None)

    logger('Twitter OAuth', 'continue_flow',
           'Read OAuth id/secret: none? {}'.format(client_id is None, client_secret is None))

    pincode = redirect_response.split('oauth_verifier=')[1]

    access_token_url = 'https://api.twitter.com/oauth/access_token'

    oauth_token = request.session['twitter_oauth_token']
    oauth_token_secret = request.session['twitter_oauth_token_secret']

    oauth_client = OAuth1Session(client_id, client_secret=client_secret,
                                 resource_owner_key=oauth_token,
                                 resource_owner_secret=oauth_token_secret,
                                 verifier=pincode)

    resp = oauth_client.fetch_access_token(access_token_url)

    # api = twitter.Api(consumer_key=client_id,
    #                   consumer_secret=client_secret,
    #                   access_token_key=oauth_token,
    #                   access_token_secret=oauth_token_secret)

    user_data = {
        'id': resp['id'],
        'nickname': resp['screen_name']
    }

    missing_data = [key for key in oauth_values if len(user_data[key]) == 0]

    return {
        'user': user_data,
        'missing': missing_data,
        'error': ''
    }
