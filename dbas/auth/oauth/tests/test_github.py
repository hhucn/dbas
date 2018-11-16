import unittest

from pyramid import testing

from dbas.auth.oauth import github as github


class OAuthGithubLoginTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()


    def test_login_github(self):
        resp = github.start_flow()
        self.assertIn('authorization_url', resp)
