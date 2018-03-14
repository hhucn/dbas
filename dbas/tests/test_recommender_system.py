import unittest

import transaction

from dbas import recommender_system as rs
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument


class RecommenderSystemTests(unittest.TestCase):

    def test_get_attack_for_argument(self):
        results = {
            None: None,
            39: 'rebut',
            44: 'undermine',
            43: 'undercut'
        }
        restriction_on_args = [40]

        db_all = DBDiscussionSession.query(Argument).all()
        for arg in db_all:
            arg.set_disable(False)
            DBDiscussionSession.add(arg)
        DBDiscussionSession.flush()
        transaction.commit()

        for i in range(0, 4):
            attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                         restriction_on_attacks=None,
                                                         restriction_on_args=restriction_on_args,
                                                         last_attack=None,
                                                         history=None)
            self.assertEqual(key, results[attack_uid])
            restriction_on_args.append(attack_uid)

        attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                     restriction_on_attacks=None,
                                                     restriction_on_args=[40],
                                                     last_attack=None,
                                                     history='42/rebut/39-42/undermine/44')
        self.assertEqual(attack_uid, 43)
        self.assertEqual(key, 'undercut')

        attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                     restriction_on_attacks=None,
                                                     restriction_on_args=[40],
                                                     last_attack=None,
                                                     history='42/rebut/39-42/undercut/43')
        self.assertEqual(attack_uid, 44)
        self.assertEqual(key, 'undermine')

        attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                     restriction_on_attacks=None,
                                                     restriction_on_args=[40],
                                                     last_attack=None,
                                                     history='42/undercut/43-42/undermine/44')
        self.assertEqual(attack_uid, 39)
        self.assertEqual(key, 'rebut')

        attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                     restriction_on_attacks=[rs.Attacks.UNDERCUT],
                                                     restriction_on_args=[40],
                                                     last_attack=None,
                                                     history='42/rebut/39-42/undermine/44')
        self.assertIsNone(attack_uid)
        self.assertIsNone(key)

        attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                     restriction_on_attacks=[rs.Attacks.UNDERMINE],
                                                     restriction_on_args=[40],
                                                     last_attack=None,
                                                     history='42/rebut/39-42/undercut/43')
        self.assertIsNone(attack_uid)
        self.assertIsNone(key)

        attack_uid, key = rs.get_attack_for_argument(argument_uid=42,
                                                     restriction_on_attacks=[rs.Attacks.REBUT],
                                                     restriction_on_args=[40],
                                                     last_attack=None,
                                                     history='42/undercut/43-42/undermine/44')
        self.assertIsNone(attack_uid)
        self.assertIsNone(key)

    def get_argument_by_conclusion(self):
        for i in range(0, 5):
            argument = rs.get_argument_by_conclusion('1', True)
            self.assertTrue(argument in [1, 10, 11])

        argument = rs.get_argument_by_conclusion('1', False)
        self.assertTrue(argument, 2)

    def get_arguments_by_conclusion(self):
        arguments = rs.get_arguments_by_conclusion('1', True)
        self.assertTrue(1 in arguments)
        self.assertTrue(10 in arguments)
        self.assertTrue(11 in arguments)

        arguments = rs.get_arguments_by_conclusion('1', False)
        self.assertTrue(2 in arguments)

    def test_get_forbidden_attacks_based_on_history(self):
        urls = [
            '',
            'reaction/239/rebut/199',
            'reaction/239/rebut//199',
            'reaction/239/rebut///199',
            'reaction/239/rebut/199//',
            '/attitude/189-/justify/189/t-/reaction/239/rebut/199a-/justify/189/t',
            '/attitude/189-/justify/189/t-/reaction/239/rebut/199-/justify/189/t'
        ]

        responses = [rs.get_forbidden_attacks_based_on_history(u) for u in urls]

        equals = [
            [],
            [],
            [199],
            [],
            [],
            [],
            [199]
        ]

        for i, e in enumerate(equals):
            self.assertEqual(e, responses[i])
