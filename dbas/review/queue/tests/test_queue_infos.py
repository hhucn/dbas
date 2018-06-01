import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.review.mapper import queue_mapping
from dbas.review.queue import review_queues
from dbas.strings.translator import Translator


class QueueInfosTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.user = DBDiscussionSession.query(User).get(2)

    def tearDown(self):
        testing.tearDown()

    def test_get_subpage_empty_session(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        queue = queue_mapping.get(review_queues[0])
        subpage_dict = queue(db_user=self.user, application_url='url',
                             translator=Translator('en')).get_queue_information({}, review_queues[0])
        self.assertIsNotNone(subpage_dict['elements'])
        self.assertFalse(subpage_dict['no_arguments_to_review'])
        self.assertTrue(review_queues[0] in subpage_dict['button_set'])

    def test_get_all_subpages(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        for key in queue_mapping:
            queue = queue_mapping[key]
            subpage_dict = queue(db_user=self.user, application_url='url',
                                 translator=Translator('en')).get_queue_information(request.session, queue)
            self.assertIsNotNone(subpage_dict['elements'])
            self.assertFalse(subpage_dict['no_arguments_to_review'])
            self.assertTrue(key in subpage_dict['button_set'])
