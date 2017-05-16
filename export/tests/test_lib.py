import unittest

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from dbas.helper.database import dbas_db_configuration
from export.lib import get_dump, get_doj_nodes, get_doj_user

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=dbas_db_configuration('discussion', settings))


class LibTest(unittest.TestCase):

    def test_get_dump(self):
        self.assertTrue(len(get_dump(0)) == 0)

        ret_dict = get_dump('1')
        self.assertTrue('issue' in ret_dict)
        self.assertTrue('user' in ret_dict)
        self.assertTrue('statement' in ret_dict)
        self.assertTrue('textversion' in ret_dict)
        self.assertTrue('argument' in ret_dict)
        self.assertTrue('premisegroup' in ret_dict)
        self.assertTrue('premise' in ret_dict)
        self.assertTrue('marked_argument' in ret_dict)
        self.assertTrue('marked_statement' in ret_dict)
        self.assertTrue(len(ret_dict['issue']) > 0)
        self.assertTrue(len(ret_dict['user']) > 0)
        self.assertTrue(len(ret_dict['statement']) > 0)
        self.assertTrue(len(ret_dict['textversion']) > 0)
        self.assertTrue(len(ret_dict['argument']) > 0)
        self.assertTrue(len(ret_dict['premisegroup']) > 0)
        self.assertTrue(len(ret_dict['premise']) > 0)
        self.assertTrue(len(ret_dict['marked_argument']) >= 0)
        self.assertTrue(len(ret_dict['marked_statement']) >= 0)

    def test_get_doj_nodes(self):
        ret_dict = get_doj_nodes(1)
        self.assertTrue('nodes' in ret_dict)
        self.assertTrue('inferences' in ret_dict)
        self.assertTrue('undercuts' in ret_dict)

        for element in ret_dict['inferences']:
            self.assertTrue('id' in element)
            self.assertTrue('premises' in element)
            self.assertTrue('conclusion' in element)

        for element in ret_dict['undercuts']:
            self.assertTrue('id' in element)
            self.assertTrue('premises' in element)
            self.assertTrue('conclusion' in element)

    def get_doj_user(self):
        ret_dict = get_doj_user(1)
        self.assertTrue('marked_statements' in ret_dict)
        self.assertTrue('marked_arguments' in ret_dict)
        self.assertTrue('rejected_arguments' in ret_dict)
        self.assertTrue('accepted_statements' in ret_dict)
        self.assertTrue('rejected_statements' in ret_dict)

        ret_dict = get_doj_user(0)
        self.assertFalse('marked_statements' in ret_dict)
        self.assertFalse('marked_arguments' in ret_dict)
        self.assertFalse('rejected_arguments' in ret_dict)
        self.assertFalse('accepted_statements' in ret_dict)
        self.assertFalse('rejected_statements' in ret_dict)

        ret_dict = get_doj_user('a')
        self.assertFalse('marked_statements' in ret_dict)
        self.assertFalse('marked_arguments' in ret_dict)
        self.assertFalse('rejected_arguments' in ret_dict)
        self.assertFalse('accepted_statements' in ret_dict)
        self.assertFalse('rejected_statements' in ret_dict)
