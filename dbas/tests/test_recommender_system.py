import unittest

import transaction

from dbas import recommender_system
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement


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

    def test_get_uids_of_best_positions(self):
        db_statements = DBDiscussionSession.query(Statement).all()
        response = recommender_system.get_uids_of_best_positions(db_statements)
        self.assertEqual(len(response), len(db_statements))

        response = recommender_system.get_uids_of_best_positions(db_statements[0:3])
        self.assertEqual(len(response), 3)

        response = recommender_system.get_uids_of_best_positions(None)
        self.assertEqual(len(response), 0)

    def test_get_uids_of_best_statements_for_justify_position(self):
        db_arguments = DBDiscussionSession.query(Argument).all()
        response = recommender_system.get_uids_of_best_positions(db_arguments)
        self.assertEqual(len(response), len(db_arguments))

        response = recommender_system.get_uids_of_best_positions(db_arguments[0:3])
        self.assertEqual(len(response), 3)

        response = recommender_system.get_uids_of_best_positions(None)
        self.assertEqual(len(response), 0)

    def test_get_uids_of_best_statements_for_justify_argument(self):
        db_arguments = DBDiscussionSession.query(Argument).all()
        response = recommender_system.get_uids_of_best_positions(db_arguments)
        self.assertEqual(len(response), len(db_arguments))

        response = recommender_system.get_uids_of_best_positions(db_arguments[0:3])
        self.assertEqual(len(response), 3)

        response = recommender_system.get_uids_of_best_positions(None)
        self.assertEqual(len(response), 0)

    def test_get_forbidden_attacks_based_on_history(self):
        s1 = ''
        s2 = 'reaction/239/rebut/199'
        s3 = 'reaction/239/rebut//199'
        s4 = 'reaction/239/rebut///199'
        s5 = 'reaction/239/rebut/199//'
        s6 = '/attitude/189-/justify/189/t-/reaction/239/rebut/199a-/justify/189/t'
        s7 = '/attitude/189-/justify/189/t-/reaction/239/rebut/199-/justify/189/t'

        response1 = recommender_system.get_forbidden_attacks_based_on_history(s1)
        response2 = recommender_system.get_forbidden_attacks_based_on_history(s2)
        response3 = recommender_system.get_forbidden_attacks_based_on_history(s3)
        response4 = recommender_system.get_forbidden_attacks_based_on_history(s4)
        response5 = recommender_system.get_forbidden_attacks_based_on_history(s5)
        response6 = recommender_system.get_forbidden_attacks_based_on_history(s6)
        response7 = recommender_system.get_forbidden_attacks_based_on_history(s7)

        self.assertEqual(response1, [])
        self.assertEqual(response2, [])
        self.assertEqual(response3, [199])
        self.assertEqual(response4, [])
        self.assertEqual(response5, [])
        self.assertEqual(response6, [])
        self.assertEqual(response7, [199])
