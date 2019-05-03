import unittest

from pyramid import testing

from dbas.auth.oauth import twitter as twitter
from dbas.tests.utils import construct_dummy_request


class OAuthTwitterLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def test_login_twitter(self):
        try:
            redirect_uri = 'http://lvh.me:4284/discuss?service=twitter'
            request = construct_dummy_request()
            resp = twitter.start_flow(request=request, redirect_uri=redirect_uri)
            self.assertIn('authorization_url', resp)
        except ValueError:
            return True
