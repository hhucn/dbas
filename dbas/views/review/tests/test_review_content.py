import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, get_now
from dbas.helper.test import verify_dictionary_of_view, clear_clicks_of, clear_seen_by_of
from dbas.review import review_queues
from dbas.views.review.rendered import queue_details


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
            try:
                response = queue_details(request)
                self.assertEqual(HTTPNotFound, type(response))
            except HTTPNotFound:
                pass

    def test_queue_pages_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        for key in review_queues:
            request = testing.DummyRequest(matchdict={'queue': key})
            response = queue_details(request)
            self.assertEqual(dict, type(response))
            verify_dictionary_of_view(response)
            self.assertTrue(response['subpage']['button_set']['is_' + key])
