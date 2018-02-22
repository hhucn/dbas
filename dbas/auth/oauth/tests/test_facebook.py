import unittest
from pyramid import testing
from dbas.auth.oauth import facebook as facebook


class OAuthFacebookLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_login_facebook(self):
        redirect_uri = 'http://lvh.me:4284/discuss?service=facebook'
        resp = facebook.start_flow(redirect_uri)
        self.assertIn('authorization_url', resp)
