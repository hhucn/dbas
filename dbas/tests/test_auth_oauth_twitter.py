import unittest
from pyramid import testing
from dbas.auth.oauth import twitter as twitter


class OAuthTwitterLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_login_google(self):
        redirect_uri = 'http://lvh.me:4284/discuss?service=twitter'
        resp = twitter.start_flow(redirect_uri)
        self.assertIn('authorization_url', resp)
