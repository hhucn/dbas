import unittest

from pyramid import testing
from pyramid.request import Request
from pyramid.testing import DummyRequest

from dbas.auth.oauth import facebook as facebook


class OAuthFacebookLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()


    def test_login_facebook(self):
        request: Request = DummyRequest()
        redirect_uri = 'http://lvh.me:4284/discuss?service=facebook'
        resp = facebook.start_flow(request, redirect_uri=redirect_uri)
        self.assertIn('authorization_url', resp)
