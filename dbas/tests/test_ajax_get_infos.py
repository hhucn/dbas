import unittest

import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import History


class AjaxGetInfosTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

        # test every ajax method, which is not used in other classes

    def tearDown(self):
        testing.tearDown()

    def get_logfile_for_statements1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_logfile_for_some_statements
        request = testing.DummyRequest(params={
            'uids': [1, 2, 3],
            'issue': 1
        }, matchdict={})
        response = get_logfile_for_some_statements(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) == 3)
        self.assertTrue(len(response['error']) == 0)

    def get_logfile_for_statements2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_logfile_for_some_statements
        request = testing.DummyRequest(params={
            'uids': [1, 2, 300],
            'issue': 1
        }, matchdict={})
        response = get_logfile_for_some_statements(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) == 2)
        self.assertTrue(len(response['error']) == 0)

    def get_logfile_for_statements_failure(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_logfile_for_some_statements
        request = testing.DummyRequest(params={
            'uid': [1, 2],
            'issue': 1
        }, matchdict={})
        response = get_logfile_for_some_statements(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_get_shortened_url(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_shortened_url as ajax
        request = testing.DummyRequest(json_body={'url': 'https://dbas.cs.uni-duesseldorf.de'})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['url']) != 0)
        self.assertTrue(len(response['service']) != 0)
        self.assertTrue(len(response['service_url']) != 0)

    def test_get_shortened_url_failure(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_shortened_url as ajax
        request = testing.DummyRequest(json_body={})
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_get_arguments_by_statement_uid(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_arguments_by_statement_id as ajax
        request = testing.DummyRequest(json_body={'uid': 3})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertIn('arguments', response)
        for element in response['arguments']:
            self.assertIn('uid', element)
            self.assertIn('text', element)
            self.assertIn('url', element)

    def test_get_arguments_by_statement_uid_failure1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_arguments_by_statement_id as ajax
        request = testing.DummyRequest(json_body={'uids': 1})
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_get_arguments_by_statement_uid_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_arguments_by_statement_id as ajax
        request = testing.DummyRequest(json_body={'uid': 'a'})
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_get_infos_about_argument(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_infos_about_argument as ajax
        request = testing.DummyRequest(json_body={'uid': 7, 'lang': 'en'})
        response = ajax(request)
        self.assertIn('supporter', response)
        self.assertIn('gravatars', response)
        self.assertIn('public_page', response)
        self.assertIn('vote_count', response)
        self.assertIn('author', response)
        self.assertIn('timestamp', response)
        self.assertIn('text', response)

    def test_get_infos_about_argument_failure1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_infos_about_argument as ajax
        request = testing.DummyRequest(json_body={'uid': 100, 'lang': 'en'})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_get_infos_about_argument_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_infos_about_argument as ajax
        request = testing.DummyRequest(json_body={'uids': 1, 'lang': 'en'})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_get_user_with_same_opinion(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_users_with_opinion as ajax
        request = testing.DummyRequest(params={}, matchdict={}, json_body={})
        response = ajax(request)
        self.assertIsNotNone(response)

    def test_get_public_user_data(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        # more tests for get_public_user_data are in test_handler_opinion
        from dbas.views import get_public_user_data as ajax
        request = testing.DummyRequest(json_body={'nickname': 'Torben'})
        response = ajax(request)
        self.assertIsNotNone(response)

    def test_get_user_history(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        DBDiscussionSession.add(History(author_uid=3, path='http://localhost:4284/discuss/cat-or-dog'))
        transaction.commit()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_user_history as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) >= 0)

    def test_get_user_history_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import get_user_history as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_delete_user_history(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        DBDiscussionSession.add(History(author_uid=3, path='http://localhost:4284/discuss/cat-or-dog'))
        transaction.commit()
        from dbas.views import delete_user_history as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        transaction.commit()
        self.assertIsNotNone(response)
        self.assertTrue(response['removed_data'] == 'true')
        db_his = len(DBDiscussionSession.query(History).filter_by(author_uid=2).all())
        self.assertTrue(db_his == 0)

    def test_delete_statistics(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import delete_statistics as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(response['removed_data'] == 'true')

    def test_delete_statistics_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import delete_statistics as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(response['removed_data'] == 'false')

    def test_get_all_edits(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_all_edits_of_user as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_edits_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import get_all_edits_of_user as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_posted_statements(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_all_posted_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_posted_statements_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import get_all_posted_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_argument_votes(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_all_argument_clicks as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_argument_votes_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import get_all_argument_clicks as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_statement_votes(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import get_all_argument_clicks as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_statement_votes_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import get_all_argument_clicks as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)
