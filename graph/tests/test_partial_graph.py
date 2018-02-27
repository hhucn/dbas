import unittest

from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement


class PartialGraphTest(unittest.TestCase):

    def test_get_partial_graph_for_statement(self):
        uid = 2  # We should get a cat
        issue = 2
        path = ''
        ret_dict, error = get_partial_graph_for_statement(uid, issue, path)
        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))

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
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))

    def test_get_partial_graph_for_argument_errors(self):
        uid = 2  # We should get a cat
        issue = 0
        ret_dict = get_partial_graph_for_argument(uid, issue)
        self.assertEqual(ret_dict, {})
