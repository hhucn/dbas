import unittest

from pyramid import testing

from dbas.views import mark_or_unmark_statement_or_argument as ajax, mark_or_unmark_statement_or_argument, \
    switch_language, fuzzy_search, fuzzy_nickname_search


class AjaxTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.include('pyramid_mailer.testing')

    def tearDown(self):
        testing.tearDown()

    def test_fuzzy_search_mode_0(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 0, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_1(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 1, 'statement_uid': 1, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_2(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 2, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_3(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 3, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_4(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 4, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_5(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 5, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_nickname_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_8(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 8, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_mode_9(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': 9, 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertIn('values', response)

    def test_fuzzy_search_failure_mode(self):
        request = testing.DummyRequest(json_body={'value': 'cat', 'type': '6', 'statement_uid': 0, 'issue': 2})
        response = fuzzy_search(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_switch_language(self):
        for lang in ['de', 'en']:
            request = testing.DummyRequest(json_body={'lang': lang})
            response = switch_language(request)
            print(lang)
            print(response)
            self.assertTrue(response['_LOCALE_'] == lang)

    def test_switch_language_failure(self):
        request = testing.DummyRequest(json_body={'lang': 'sw'})
        response = switch_language(request)
        self.assertEqual(400, response.status_code)

    def test_mark_statement_or_argument(self):
        request = testing.DummyRequest(json_body={'ui_locales': 'en'})
        response = mark_or_unmark_statement_or_argument(request)
        self.assertEqual(400, response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        for b1 in [True, False]:
            for b2 in [True, False]:
                for b3 in [True, False]:
                    request = testing.DummyRequest(
                        json_body={'uid': 4, 'is_argument': b1, 'should_mark': b2, 'step': 'reaction/4/undercut/6',
                                   'is_supportive': b3})
                    response = ajax(request)
                    self.assertTrue(len(response['text']) > 0)
