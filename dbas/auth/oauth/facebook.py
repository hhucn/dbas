"""
Facebook OAuth handler of D-BAS

App is registered by the account of Tobias Krauthoff

Used lib: http://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
Manage Google Client IDs: https://developers.facebook.com/apps/
"""

import logging
import os
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.request import Request
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from requests_oauthlib.oauth2_session import OAuth2Session

LOG = logging.getLogger(__name__)
CLIENT_ID = os.environ.get('OAUTH_FACEBOOK_CLIENTID', None)
CLIENT_SECRET = os.environ.get('OAUTH_FACEBOOK_CLIENTKEY', None)
AUTHORIZATION_BASE_URL = 'https://www.facebook.com/v3.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v3.0/oauth/access_token'
SCOPE = ['email']  # https://developers.facebook.com/docs/facebook-login/permissions/
REDIRECT_PATH = '/oauth/facebook'


def start_flow(request: Request, redirect_uri: str = None) -> dict:
    """
    Starts the oauth flow. This will return a dict which causes a redirect to the providers page.

    :param request: The Pyramid Request associated with the OAuth request.
    :param redirect_uri: The URL to redirect to.
    :return:
    """
    next_url = request.application_url + '/discuss' if not redirect_uri else redirect_uri
    LOG.debug("Read OAuth id/secret: none? %s/%s", CLIENT_ID is None, CLIENT_SECRET is None)
    oauth_session = OAuth2Session(CLIENT_ID, scope=','.join(SCOPE),
                                  redirect_uri=(request.application_url + REDIRECT_PATH))
    oauth_session = facebook_compliance_fix(oauth_session)

    authorization_url, state = oauth_session.authorization_url(AUTHORIZATION_BASE_URL)
    request.session['oauth_session'] = oauth_session
    request.session['csrf'] = state
    request.session['next'] = next_url

    LOG.debug("Please go to %s and authorize access", authorization_url)
    return {'authorization_url': authorization_url, 'error': ''}


def continue_flow(request: Request):
    if 'csrf' not in request.session or request.session['csrf'] != request.params['state']:
        raise HTTPBadRequest('CSRF Error')

    oauth_session = request.session['oauth_session']
    LOG.debug("Read OAuth id/secret: none? %s/%s", CLIENT_ID is None, CLIENT_SECRET is None)

    oauth_session.fetch_token(TOKEN_URL,
                              client_secret=CLIENT_SECRET,
                              code=request.params['code'])
    data = oauth_session.get('https://graph.facebook.com/v3.0/me?fields=id,name,email,first_name,last_name').json()

    user_data = {
        'id': data['id'],
        'firstname': data.get('first_name'),
        'lastname': data.get('last_name'),
        'nickname': data.get('name').replace(' ', ''),
        'gender': 'n',
        'email': data.get('email')
    }

    return user_data, request.session['next']
