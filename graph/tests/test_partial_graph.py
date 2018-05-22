import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement


class PartialGraphTest(unittest.TestCase):

    def test_get_partial_graph_for_statement(self):
        db_issue = DBDiscussionSession.query(Issue).get(2)
        ret_dict, error = get_partial_graph_for_statement(2, db_issue, '')
        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))

    def test_get_partial_graph_for_argument(self):
        db_issue = DBDiscussionSession.query(Issue).get(2)
        ret_dict, error = get_partial_graph_for_argument(11, db_issue)

        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))
