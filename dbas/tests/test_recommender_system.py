import transaction
import unittest

from sqlalchemy import engine_from_config

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
from dbas import recommender_system
from dbas.helper.tests import add_settings_to_appconfig

class RecommenerSystemTests(unittest.TestCase):

    def test_get_attack_for_argument(self):
        results = {}
        results[0] = 'end'
        results[39] = 'rebut'
        results[44] = 'undermine'
        results[43] = 'undercut'
        restriction_on_arg_uids = [40]

        db_all = DBDiscussionSession.query(Argument).all()
        for arg in db_all:
            arg.set_disable(False)
            DBDiscussionSession.add(arg)
        DBDiscussionSession.flush()
        transaction.commit()

        for i in range(0, 4):
            attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42, lang='en', restriction_on_attacks=None, restriction_on_arg_uids=restriction_on_arg_uids, last_attack=None, history=None)
            self.assertEqual(key, results[attack_uid])
            restriction_on_arg_uids.append(attack_uid)

        attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42,
                                                                     lang='en',
                                                                     restriction_on_attacks=None,
                                                                     restriction_on_arg_uids=[40],
                                                                     last_attack=None,
                                                                     history='42/rebut/39-42/undermine/44')
        self.assertEqual(attack_uid, 43)
        self.assertEqual(key, 'undercut')

        attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42,
                                                                     lang='en',
                                                                     restriction_on_attacks=None,
                                                                     restriction_on_arg_uids=[40],
                                                                     last_attack=None,
                                                                     history='42/rebut/39-42/undercut/43')
        self.assertEqual(attack_uid, 44)
        self.assertEqual(key, 'undermine')

        attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42,
                                                                     lang='en',
                                                                     restriction_on_attacks=None,
                                                                     restriction_on_arg_uids=[40],
                                                                     last_attack=None,
                                                                     history='42/undercut/43-42/undermine/44')
        self.assertEqual(attack_uid, 39)
        self.assertEqual(key, 'rebut')

        attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42,
                                                                     lang='en',
                                                                     restriction_on_attacks='undercut',
                                                                     restriction_on_arg_uids=[40],
                                                                     last_attack=None,
                                                                     history='42/rebut/39-42/undermine/44')
        self.assertEqual(attack_uid, 0)
        self.assertTrue(key in ['end', 'end_attack'])

        attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42,
                                                                     lang='en',
                                                                     restriction_on_attacks='undermine',
                                                                     restriction_on_arg_uids=[40],
                                                                     last_attack=None,
                                                                     history='42/rebut/39-42/undercut/43')
        self.assertEqual(attack_uid, 0)
        self.assertTrue(key in ['end', 'end_attack'])

        attack_uid, key = recommender_system.get_attack_for_argument(argument_uid=42,
                                                                     lang='en',
                                                                     restriction_on_attacks='rebut',
                                                                     restriction_on_arg_uids=[40],
                                                                     last_attack=None,
                                                                     history='42/undercut/43-42/undermine/44')
        self.assertEqual(attack_uid, 0)
        self.assertTrue(key in ['end', 'end_attack'])

    def get_argument_by_conclusion(self):
        for i in range(0, 5):
            argument = recommender_system.get_argument_by_conclusion('1', True)
            self.assertTrue(argument in [1, 10, 11])

        argument = recommender_system.get_argument_by_conclusion('1', False)
        self.assertTrue(argument, 2)

    def get_arguments_by_conclusion(self):
        arguments = recommender_system.get_arguments_by_conclusion('1', True)
        self.assertTrue(1 in arguments)
        self.assertTrue(10 in arguments)
        self.assertTrue(11 in arguments)

        arguments = recommender_system.get_arguments_by_conclusion('1', False)
        self.assertTrue(2 in arguments)
