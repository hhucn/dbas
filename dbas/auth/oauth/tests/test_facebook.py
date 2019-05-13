import unittest

from pyramid import testing
from pyramid.request import Request

from dbas.auth.oauth import facebook as facebook
from dbas.tests.utils import construct_dummy_request


class OAuthFacebookLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def test_login_facebook(self):
        request: Request = construct_dummy_request()
        redirect_uri = 'http://lvh.me:4284/discuss?service=facebook'
        resp = facebook.start_flow(request, redirect_uri=redirect_uri)
        self.assertIn('authorization_url', resp)
