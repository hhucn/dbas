import transaction
import unittest

from typing import List

from dbas.lib import relations_mapping, Relations
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
from dbas.handler import attacks


class AttackHandlerTests(unittest.TestCase):

    def test_get_attack_for_argument(self):
        results = {
            None: None,
            39: relations_mapping[Relations.REBUT],
            44: relations_mapping[Relations.UNDERMINE],
            43: relations_mapping[Relations.UNDERCUT]
        }

        restriction_on_args = [40]

        db_all: List[Argument] = DBDiscussionSession.query(Argument).all()
        for arg in db_all:
            arg.set_disabled(False)
        transaction.commit()

        for i in range(0, 4):
            attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                              restrictive_attacks=None,
                                                              restrictive_arg_uids=restriction_on_args,
                                                              last_attack=None,
                                                              history='')
            self.assertEqual(key, results[attack_uid])
            restriction_on_args.append(attack_uid)

    def test_get_attack_for_argument_with_restrictive_arguments(self):

        attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                          restrictive_attacks=None,
                                                          restrictive_arg_uids=[40],
                                                          last_attack=None,
                                                          history='42/rebut/39-42/undermine/44')
        self.assertEqual(attack_uid, 43)
        self.assertEqual(key, relations_mapping[Relations.UNDERCUT])

        attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                          restrictive_attacks=None,
                                                          restrictive_arg_uids=[40],
                                                          last_attack=None,
                                                          history='42/rebut/39-42/undercut/43')
        self.assertEqual(attack_uid, 44)
        self.assertEqual(key, relations_mapping[Relations.UNDERMINE])

        attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                          restrictive_attacks=None,
                                                          restrictive_arg_uids=[40],
                                                          last_attack=None,
                                                          history='42/undercut/43-42/undermine/44')
        self.assertEqual(attack_uid, 39)
        self.assertEqual(key, relations_mapping[Relations.REBUT])

    def test_get_attack_for_argument_with_undercut_restriction(self):
        attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                          restrictive_attacks=[Relations.UNDERCUT],
                                                          restrictive_arg_uids=[40],
                                                          last_attack=None,
                                                          history='42/rebut/39-42/undermine/44')
        self.assertIsNone(attack_uid)
        self.assertIsNone(key)

    def test_get_attack_for_argument_with_undermine_restriction(self):

        attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                          restrictive_attacks=[Relations.UNDERMINE],
                                                          restrictive_arg_uids=[40],
                                                          last_attack=None,
                                                          history='42/rebut/39-42/undercut/43')
        self.assertIsNone(attack_uid)
        self.assertIsNone(key)

    def test_get_attack_for_argument_with_rebut_restriction(self):

        attack_uid, key = attacks.get_attack_for_argument(argument_uid=42,
                                                          restrictive_attacks=[Relations.REBUT],
                                                          restrictive_arg_uids=[40],
                                                          last_attack=None,
                                                          history='42/undercut/43-42/undermine/44')
        self.assertIsNone(attack_uid)
        self.assertIsNone(key)

    def get_arguments_by_conclusion(self):
        arguments = attacks.get_arguments_by_conclusion(1, True)
        self.assertTrue(1 in arguments)
        self.assertTrue(10 in arguments)
        self.assertTrue(11 in arguments)

        arguments = attacks.get_arguments_by_conclusion(1, False)
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

        responses = [attacks.get_forbidden_attacks_based_on_history(u) for u in urls]

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
