import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.helper.test import verify_dictionary_of_view, clear_clicks_of, clear_seen_by_of


class ReviewContentViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Tobias')

    def tearDown(self):
        testing.tearDown()
        clear_clicks_of('Tobias')
        clear_seen_by_of('Tobias')

    def test_page_deletes(self):
        from dbas.views import review_content as d

        request = testing.DummyRequest(matchdict={'queue': 'deletes'})
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

    def test_page_edits(self):
        from dbas.views import review_content as d

        request = testing.DummyRequest(matchdict={'queue': 'edits'})
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

    def test_page_optimizations(self):
        from dbas.views import review_content as d

        request = testing.DummyRequest(matchdict={'queue': 'optimizations'})
        try:
            response = d(request)
            self.assertTrue(type(response) is HTTPNotFound)
        except HTTPNotFound:
            pass

    def test_page_deletes_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_content as d

        request = testing.DummyRequest(matchdict={'queue': 'deletes'})
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertTrue(len(response['subpage']['elements']) > 0)
        self.assertTrue(response['subpage']['button_set']['is_delete'])
        self.assertFalse(response['subpage']['button_set']['is_edit'])
        self.assertFalse(response['subpage']['button_set']['is_optimize'])

    def test_page_edits_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_content as d

        request = testing.DummyRequest(matchdict={'queue': 'edits'})
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertTrue(len(response['subpage']['elements']) > 0)
        self.assertFalse(response['subpage']['button_set']['is_delete'])
        self.assertTrue(response['subpage']['button_set']['is_edit'])
        self.assertFalse(response['subpage']['button_set']['is_optimize'])

    def test_page_optimizations_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_content as d

        request = testing.DummyRequest(matchdict={'queue': 'optimizations'})
        response = d(request)
        verify_dictionary_of_view(self, response)
        self.assertTrue(len(response['subpage']['elements']) > 0)
        self.assertFalse(response['subpage']['button_set']['is_delete'])
        self.assertFalse(response['subpage']['button_set']['is_edit'])
        self.assertTrue(response['subpage']['button_set']['is_optimize'])
