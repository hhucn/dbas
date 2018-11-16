import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.review.queue import review_queues
from dbas.review.queue.abc_queue import subclass_by_name
from dbas.review.queue.adapter import QueueAdapter
from dbas.strings.translator import Translator


class QueueInfosTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.user = DBDiscussionSession.query(User).get(2)


    def test_get_subpage_empty_session(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        queue = subclass_by_name(review_queues[0])
        adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='url', translator=Translator('en'))
        subpage_dict = adapter.get_subpage_of_queue({}, review_queues[0])
        self.assertIsNotNone(subpage_dict['elements'])
        self.assertFalse(subpage_dict['no_arguments_to_review'])
        self.assertTrue(f'is_{review_queues[0]}' in subpage_dict['button_set'].keys())

    def test_get_all_subpages(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        for key in review_queues:
            queue = subclass_by_name(key)
            adapter = QueueAdapter(queue=queue(), db_user=self.user, application_url='url', translator=Translator('en'))
            subpage_dict = adapter.get_subpage_of_queue(request.session, key)
            self.assertIsNotNone(subpage_dict['elements'])
            self.assertFalse(subpage_dict['no_arguments_to_review'])
            self.assertTrue(f'is_{key}' in subpage_dict['button_set'].keys())
