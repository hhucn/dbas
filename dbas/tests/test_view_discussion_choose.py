import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPFound

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Premise, StatementSeenBy
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class DiscussionChhoseViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.pgroup_ids = [15, 17]

    def tearDown(self):
        testing.tearDown()

    def test_discussion_choose_page(self):
        from dbas.views import discussion_choose as d

        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'is_argument': 'f',
            'supportive': 't',
            'id': 5,
            'pgroup_ids': self.pgroup_ids,
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).all())
        # not logged in, no change
        self.assertEqual(len_db_seen1, len_db_seen2)

    def test_discussion_choose_page_logged_in(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import discussion_choose as d

        len_db_seen1 = len(DBDiscussionSession.query(StatementSeenBy).all())

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'is_argument': 'f',
            'supportive': 't',
            'id': 5,
            'pgroup_ids': self.pgroup_ids,
        }
        response = d(request)
        verify_dictionary_of_view(self, response)

        len_db_seen2 = len(DBDiscussionSession.query(StatementSeenBy).all())

        count = 0
        for group_id in self.pgroup_ids:
            count += len(DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group_id).all())

        self.assertEqual(len_db_seen1 + count, len_db_seen2)

    def test_discussion_choose_page_fail(self):
        from dbas.views import discussion_choose as d

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-dog',
            'is_argument': 'f',
            'supportive': 't',
            'id': 5,
            'pgroup_ids': [15, 17, 'a'],
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-doggy-dog',
            'is_argument': 'f',
            'supportive': 't',
            'id': 5,
            'pgroup_ids': [15, 17, 'a'],
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)

        request = testing.DummyRequest()
        request.matchdict = {
            'slug': 'cat-or-doggy-dog',
            'is_argument': 'f',
            'supportive': 't',
            'id': 5,
            'pgroup_ids': [15, 17, 55],
        }
        response = d(request)
        self.assertTrue(type(response) is HTTPFound)
