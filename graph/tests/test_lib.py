import unittest

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from graph import lib


class LibTest(unittest.TestCase):

    def test_get_d3_data(self):
        db_issue = DBDiscussionSession.query(Issue).get(2)
        ret_dict, error = lib.get_d3_data(db_issue)
        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))

    def test_get_opinion_data(self):
        db_issue = DBDiscussionSession.query(Issue).get(2)
        self.assertNotEqual(0, len(lib.get_opinion_data(db_issue)))

    def test_get_path_of_user(self):
        db_issue = DBDiscussionSession.query(Issue).get(2)
        response = lib.get_path_of_user('http://localhost:4284/', '?history=/attitude/2', db_issue)
        self.assertEqual(0, len(response))

        path = [
            '?history=/attitude/2-/justify/2/agree',
            '?history=/attitude/2-/justify/2/agree-/reaction/2/undercut/18-/justify/2/agree',
            '?history=/attitude/2-/justify/2/agree-/reaction/12/undercut/13-/justify/13/agree/undercut'
        ]
        for p in path:
            response = lib.get_path_of_user('http://localhost:4284/', p, db_issue)
            self.assertNotEqual(0, len(response))
