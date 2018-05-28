import unittest

from pyramid import testing

from dbas.review import review_queues
import dbas.review.subpage as rph
from dbas.strings.translator import Translator


class rphTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_get_subpage_failure_page(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        ret_dict = rph.get_subpage_elements_for('Tobias', request.session, 'url', 'some page', Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_failure_nick(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='some nick', permissive=True)

        ret_dict = rph.get_subpage_elements_for('some nick', request.session, 'url', review_queues[0], Translator('en'))
        self.assertIsNone(ret_dict['elements'])
        self.assertFalse(ret_dict['has_access'])
        self.assertFalse(ret_dict['no_arguments_to_review'])

    def test_get_subpage_empty_session(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        ret_dict = rph.get_subpage_elements_for('Tobias', {}, 'url', review_queues[0], Translator('en'))
        self.assertIsNotNone(ret_dict['elements'])
        self.assertFalse(ret_dict['no_arguments_to_review'])
        self.assertTrue(ret_dict['has_access'])
        self.assertTrue(el.startswith('is_' + review_queues[0][0:4]) for el in ret_dict['button_set'])

    def test_get_all_subpages(self):
        request = testing.DummyRequest()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        for queue in review_queues:
            ret_dict = rph.get_subpage_elements_for('Tobias', request.session, 'url', queue, Translator('en'))
            self.assertIsNotNone(ret_dict['elements'])
            self.assertFalse(ret_dict['no_arguments_to_review'])
            self.assertTrue(ret_dict['has_access'])
            self.assertTrue(el.startswith('is_' + queue[0:4]) for el in ret_dict['button_set'])
