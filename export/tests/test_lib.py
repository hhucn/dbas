import unittest

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config
from export.lib import get_dump, get_minimal_graph_export

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class LibTest(unittest.TestCase):

    def test_get_dump(self):
        self.assertTrue(len(get_dump(0, 'en')) == 0)

        ret_dict = get_dump('1', 'en')
        self.assertTrue('issue' in ret_dict)
        self.assertTrue('user' in ret_dict)
        self.assertTrue('statement' in ret_dict)
        self.assertTrue('textversion' in ret_dict)
        self.assertTrue('argument' in ret_dict)
        self.assertTrue('premisegroup' in ret_dict)
        self.assertTrue('premise' in ret_dict)
        self.assertTrue('vote_argument' in ret_dict)
        self.assertTrue('vote_statement' in ret_dict)
        self.assertTrue(len(ret_dict['issue']) > 0)
        self.assertTrue(len(ret_dict['user']) > 0)
        self.assertTrue(len(ret_dict['statement']) > 0)
        self.assertTrue(len(ret_dict['textversion']) > 0)
        self.assertTrue(len(ret_dict['argument']) > 0)
        self.assertTrue(len(ret_dict['premisegroup']) > 0)
        self.assertTrue(len(ret_dict['premise']) > 0)
        self.assertTrue(len(ret_dict['vote_argument']) > 0)
        self.assertTrue(len(ret_dict['vote_statement']) > 0)

    def test_get_minimal_graph_export(self):
        ret_dict = get_minimal_graph_export(1)
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
