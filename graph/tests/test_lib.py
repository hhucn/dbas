from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.tests.utils import TestCaseWithConfig
from graph import lib


class LibTest(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.issue_elektroautos = DBDiscussionSession.query(Issue).get(4)

    def test_get_d3_data(self):
        ret_dict, error = lib.get_d3_data(self.issue_elektroautos)
        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))

    def test_get_opinion_data(self):
        self.assertNotEqual(len(lib.get_opinion_data(self.issue_elektroautos)), 0)

    def test_get_path_of_user(self):
        response = lib.get_path_of_user('http://localhost:4284/', '?history=/attitude/2', self.issue_elektroautos)
        self.assertEqual(len(response), 0)

        path = [
            '?history=/attitude/2-/justify/2/agree',
            '?history=/attitude/2-/justify/2/agree-/reaction/2/undercut/18-/justify/2/agree',
            '?history=/attitude/2-/justify/2/agree-/reaction/12/undercut/13-/justify/13/agree/undercut'
        ]
        for p in path:
            response = lib.get_path_of_user('http://localhost:4284/', p, self.issue_elektroautos)
            self.assertNotEqual(len(response), 0)
