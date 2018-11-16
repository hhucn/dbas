import unittest

from pyramid import testing

from dbas.auth.oauth import google as google


class OAuthGoogleLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def test_login_google(self):
        redirect_uri = 'http://lvh.me:4284/discuss?service=google'
        resp = google.start_flow(redirect_uri=redirect_uri)
        self.assertIn('authorization_url', resp)
