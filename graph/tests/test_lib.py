import unittest

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config
from graph.lib import get_d3_data

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class LibTest(unittest.TestCase):

    def test_get_review_array(self):
        self.assertTrue(len(get_d3_data(0, 'Tobias')) == 0)

        ret_dict, error = get_d3_data(1, 'Tobias')
        self.assertFalse(error)
        self.assertTrue('nodes' in ret_dict)
        self.assertTrue('edges' in ret_dict)
        self.assertTrue('extras' in ret_dict)
        self.assertTrue(len(ret_dict['nodes']) > 0)
        self.assertTrue(len(ret_dict['edges']) > 0)
        self.assertTrue(len(ret_dict['extras']) > 0)
