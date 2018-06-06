import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.review.mapper import get_queue_by_key
from dbas.review.queue import review_queues
from dbas.review.queue.adapter import QueueAdapter
from dbas.strings.translator import Translator


class QueueTest(unittest.TestCase):

    def test_get_subpage_of_queue(self):
        db_user = DBDiscussionSession.query(User).get(2)

        for key in review_queues:
            queue = get_queue_by_key(key)
            adapter = QueueAdapter(queue=queue(), db_user=db_user, application_url='main', translator=Translator('en'))

            subpage = adapter.get_subpage_of_queue({}, key)
            self.assertIn('elements', subpage)
            self.assertIn('no_arguments_to_review', subpage)
            self.assertIn('button_set', subpage)
            self.assertIn('session', subpage)
            self.assertTrue(key, subpage['elements']['page_name'])
            self.assertIn('reviewed_element', subpage['elements'])
