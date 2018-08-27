from dbas.tests.utils import TestCaseWithConfig
from graph.partial_graph import get_partial_graph_for_argument, get_partial_graph_for_statement


class PartialGraphTest(TestCaseWithConfig):

    def test_get_partial_graph_for_statement(self):
        ret_dict, error = get_partial_graph_for_statement(2, self.issue_cat_or_dog, '')
        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))

    def test_get_partial_graph_for_argument(self):
        ret_dict, error = get_partial_graph_for_argument(11, self.issue_cat_or_dog)

        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))
