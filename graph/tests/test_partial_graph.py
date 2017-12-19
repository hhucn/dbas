import unittest

from dbas.database import DBDiscussionSession, get_dbas_db_configuration
from dbas.helper.tests import add_settings_to_appconfig
from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))


class PartialGraphTest(unittest.TestCase):

    def test_get_partial_graph_for_statement(self):
        uid = 2  # We should get a cat
        issue = 2
        path = ''
        ret_dict, error = get_partial_graph_for_statement(uid, issue, path)
        self.assertFalse(error)
        self.assertTrue('nodes' in ret_dict)
        self.assertTrue('edges' in ret_dict)
        self.assertTrue('extras' in ret_dict)
        self.assertTrue(len(ret_dict['nodes']) > 0)
        self.assertTrue(len(ret_dict['edges']) > 0)
        self.assertTrue(len(ret_dict['extras']) > 0)

    def test_get_partial_graph_for_statement_errors(self):
        uid = 2  # We should get a cat
        issue = 0
        path = ''
        ret_dict = get_partial_graph_for_statement(uid, issue, path)
        self.assertEqual(ret_dict, {})

    def test_get_partial_graph_for_argument(self):
        uid = 11  # We should get a cat because a dog costs taxes and will be more expensive than a cat.
        issue = 2
        ret_dict, error = get_partial_graph_for_argument(uid, issue)

        self.assertFalse(error)
        self.assertTrue('nodes' in ret_dict)
        self.assertTrue('edges' in ret_dict)
        self.assertTrue('extras' in ret_dict)
        self.assertTrue(len(ret_dict['nodes']) > 0)
        self.assertTrue(len(ret_dict['edges']) > 0)
        self.assertTrue(len(ret_dict['extras']) > 0)

    def test_get_partial_graph_for_argument_errors(self):
        uid = 2  # We should get a cat
        issue = 0
        ret_dict = get_partial_graph_for_argument(uid, issue)
        self.assertEqual(ret_dict, {})
