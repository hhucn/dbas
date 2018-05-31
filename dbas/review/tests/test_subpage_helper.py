import unittest

from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.review import review_queues
import dbas.review.subpage as rph
from dbas.strings.translator import Translator


class SubPageHelperTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.user = DBDiscussionSession.query(User).get(2)

    def tearDown(self):
        testing.tearDown()

    def test_get_subpage_failure_page(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        ret_dict = rph.get_subpage_elements_for(self.user, request.session, 'url', 'some page', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_empty_session(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        ret_dict = rph.get_subpage_elements_for(self.user, {}, 'url', review_queues[0], Translator('en'))
        self.assertIsNotNone(ret_dict['elements'])
        self.assertFalse(ret_dict['no_arguments_to_review'])
        self.assertTrue(ret_dict['has_access'])
        self.assertTrue(el.startswith('is_' + review_queues[0][0:4]) for el in ret_dict['button_set'])

    def test_get_all_subpages(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        for queue in review_queues:
            ret_dict = rph.get_subpage_elements_for(self.user, request.session, 'url', queue, Translator('en'))
            self.assertIsNotNone(ret_dict['elements'])
            self.assertFalse(ret_dict['no_arguments_to_review'])
            self.assertTrue(ret_dict['has_access'])
            self.assertTrue(el.startswith('is_' + queue[0:4]) for el in ret_dict['button_set'])
