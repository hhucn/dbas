import unittest

import transaction
from paste.httpexceptions import HTTPNotFound
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, get_now
from dbas.helper.test import verify_dictionary_of_view, clear_clicks_of, clear_seen_by_of
from dbas.review import review_queues
from dbas.views.review.rendered import index, reputation, ongoing, history, queue_details


class MainReviewViewTestsNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = testing.DummyRequest()
        response = index(request)
        self.assertEqual(response.status_code, 400)


class MainReviewViewTestsLoggedIn(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_page_not_logged_in(self):
        request = testing.DummyRequest()
        response = index(request)
        self.assertEqual(response.status_code, 400)

    def test_page(self):
        request = testing.DummyRequest()
        response = index(request)
        verify_dictionary_of_view(response)

        self.assertIn('review', response)
        self.assertIn('privilege_list', response)
        self.assertIn('reputation_list', response)
        self.assertIn('reputation', response)
        self.assertFalse(response['reputation']['has_all_rights'])
        self.assertTrue(response['reputation']['count'] == 0)


class ReviewReputationViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page_not_logged_in(self):
        request = testing.DummyRequest()
        response = reputation(request)
        self.assertEqual(response.status_code, 400)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = testing.DummyRequest()
        response = reputation(request)
        verify_dictionary_of_view(response)
        self.assertIn('reputation', response)
        self.assertTrue(len(response['reputation']) != 0)


class ReviewContentViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        clear_clicks_of('Tobias')
        clear_seen_by_of('Tobias')
        self.db_tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        self.last_login_of_tobias = self.db_tobias.last_login
        self.db_tobias.last_login = get_now()
        DBDiscussionSession.add(self.db_tobias)
        DBDiscussionSession.flush()
        transaction.commit()

    def tearDown(self):
        testing.tearDown()
        clear_clicks_of('Tobias')
        clear_seen_by_of('Tobias')
        self.db_tobias.last_login = self.last_login_of_tobias
        DBDiscussionSession.add(self.db_tobias)
        DBDiscussionSession.flush()
        transaction.commit()

    def test_queue_pages_not_logged_in(self):
        for key in review_queues:
            request = testing.DummyRequest(matchdict={'queue': key})
            response = queue_details(request)
            self.assertEqual(response.status_code, 400)

    def test_queue_pages_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        try:
            request = testing.DummyRequest(matchdict={'queue': 'foobaar'})
            response = queue_details(request)
            self.assertEqual(HTTPNotFound, type(response))
        except HTTPNotFound:
            pass

        for key in review_queues:
            request = testing.DummyRequest(matchdict={'queue': key})
            response = queue_details(request)
            self.assertEqual(dict, type(response))
            verify_dictionary_of_view(response)
            self.assertTrue(response['subpage']['button_set']['is_' + key])


class ReviewOngoingViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page_not_logged_in(self):
        request = testing.DummyRequest()
        response = ongoing(request)
        self.assertEqual(response.status_code, 400)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = testing.DummyRequest()
        response = ongoing(request)
        verify_dictionary_of_view(response)

        self.assertIn('history', response)
        self.assertTrue(len(response['history']) != 0)


class ReviewHistoryViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_page(self):
        request = testing.DummyRequest()
        response = history(request)
        verify_dictionary_of_view(response)

        self.assertIn('history', response)
        self.assertTrue(len(response['history']) == 0)

    def test_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = testing.DummyRequest()
        response = history(request)
        verify_dictionary_of_view(response)

        self.assertIn('history', response)
        self.assertTrue(len(response['history']) != 0)
