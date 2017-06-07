import unittest

from dbas.database import DBDiscussionSession, get_dbas_db_configuration
from dbas.helper.tests import add_settings_to_appconfig
from graph.lib import get_d3_data

settings = add_settings_to_appconfig()

DBDiscussionSession.configure(bind=get_dbas_db_configuration('discussion', settings))


class LibTest(unittest.TestCase):

    def test_get_review_array(self):
        self.assertTrue(len(get_d3_data(0)) == 0)

        ret_dict, error = get_d3_data(1)
        self.assertFalse(error)
        self.assertTrue('nodes' in ret_dict)
        self.assertTrue('edges' in ret_dict)
        self.assertTrue('extras' in ret_dict)
        self.assertTrue(len(ret_dict['nodes']) > 0)
        self.assertTrue(len(ret_dict['edges']) > 0)
        self.assertTrue(len(ret_dict['extras']) > 0)
