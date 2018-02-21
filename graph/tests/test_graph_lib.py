import unittest

from dbas.database import DBDiscussionSession, get_dbas_db_configuration
from dbas.helper.test import add_settings_to_appconfig
from graph.lib import get_d3_data

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))


class LibTest(unittest.TestCase):

    def test_get_review_array(self):
        self.assertTrue(len(get_d3_data(0)) == 0)

        ret_dict, error = get_d3_data(1)
        self.assertFalse(error)
        self.assertIn('nodes', ret_dict)
        self.assertIn('edges', ret_dict)
        self.assertIn('extras', ret_dict)
        self.assertLess(0, len(ret_dict['nodes']))
        self.assertLess(0, len(ret_dict['edges']))
        self.assertLess(0, len(ret_dict['extras']))
