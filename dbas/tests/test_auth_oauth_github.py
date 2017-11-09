import unittest
from pyramid import testing
from dbas.auth.oauth import github as github


class OAuthGithubLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_login_github(self):
        redirect_uri = 'http://lvh.me:4284/discuss?service=github'
        resp = github.start_flow()
        self.assertIn('authorization_url', resp)
