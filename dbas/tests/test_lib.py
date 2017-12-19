import unittest
from datetime import date

from dbas import lib
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, Statement, Issue


class LibTests(unittest.TestCase):

    def test_escape_string(self):
        self.assertEqual(lib.escape_string(text=''), '')

        # normal string
        self.assertEqual(lib.escape_string(text='str'), 'str')

        # strings with html special chars
        self.assertEqual(lib.escape_string(text='&'), '&amp;')

        self.assertEqual(lib.escape_string(text='" str & str2'), '&quot; str &amp; str2')

        long_str_with_special_char = 'str' + '"' * 1000
        long_str_without_special_char = 'str' + '&quot;' * 1000
        self.assertEqual(lib.escape_string(long_str_with_special_char), long_str_without_special_char)

    def test_python_datetime_pretty_print(self):
        # datetime corresponding to Gregorian ordinal
        d = date.fromordinal(736132)

        # Verify, that if 'lang' is 'de' format of date is 'day. month.'
        self.assertEqual(lib.python_datetime_pretty_print(ts=d, lang='de'), '17. Jun.')

        # Verify, that if 'lang' is not 'de' format of date is 'month. day. '
        self.assertEqual(lib.python_datetime_pretty_print(ts=d, lang='en'), 'Jun. 17.')

        self.assertEqual(lib.python_datetime_pretty_print(ts='2016-01-01', lang=''), 'Jan. 01.')

    def test_get_text_for_premisesgroup_uid(self):
        # premise, which is in db_premises and premise_group contains only one premise
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=2), ('cats are very independent', ['5']))

        # premise_group with more than one premises
        self.assertNotEqual(lib.get_text_for_premisesgroup_uid(uid=13), ('cats are fluffy und cats are small', ['14', '15']))

        values = lib.get_text_for_premisesgroup_uid(uid=12)
        solution1 = 'cats are fluffy and cats are small', ['15', '16']
        solution2 = 'cats are small and cats are fluffy', ['16', '15']
        if values[1] == solution1[1]:
            self.assertEqual(values, solution1)
        else:
            self.assertEqual(values, solution2)

        # premise, which is not in db_premises
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0), ('', []))

        # negative uid
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=-1), ('', []))

        # language is empty string
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0), ('', []))

    def test_get_text_for_statement_uid(self):
        # id for no statement
        self.assertIsNone(lib.get_text_for_statement_uid(uid=0))

        self.assertIsNone(lib.get_text_for_statement_uid(uid='22222222'))
        self.assertIsNone(lib.get_text_for_statement_uid(uid="str"))

        # id for statement, which ends with '.'
        self.assertEqual(lib.get_text_for_statement_uid(uid=3), 'we should get a dog')

        # id for statement, which ends with '!'
        self.assertEqual(lib.get_text_for_statement_uid(uid=31), 'it is important, that pets are small and fluffy')

        # negative uid
        self.assertIsNone(lib.get_text_for_statement_uid(uid=-30))

    def test_get_text_for_conclusion(self):
        argument1 = Argument(premisegroup=4, issupportive=True, author=1, conclusion=3, issue=1)
        # 'argument' is an argument
        self.assertEqual(lib.get_text_for_conclusion(argument=argument1,
                                                     start_with_intro=False,
                                                     rearrange_intro=False), 'we should get a dog')

        argument2 = Argument(premisegroup=1, issupportive=False, author=1, issue=1)
        # 'argument' is a statement
        self.assertEqual(lib.get_text_for_conclusion(argument=argument2,
                                                     start_with_intro=True,
                                                     rearrange_intro=True), None)

        # unknown conclusion id
        argument3 = Argument(premisegroup=0, issupportive=True, author=0, conclusion=0, issue=0)
        self.assertEqual(lib.get_text_for_conclusion(argument=argument3,
                                                     start_with_intro=False,
                                                     rearrange_intro=True), None)

    def test_resolve_issue_uid_to_slug(self):
        # id for issue
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=1), 'town-has-to-cut-spending')
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=5), 'unterstutzung-der-sekretariate')

        # id for no issue
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=0), None)
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=22222222), None)
        self.assertEqual(lib.resolve_issue_uid_to_slug(uid=-4), None)

    def test_get_all_attacking_arg_uids_from_history(self):
        none_history = None
        correct_history = "/attitude/60-/justify/60/t-/reaction/52/rebut/53"
        broken_history = "/attitude/60/justify/60/t/broooken/52/rebut/53"
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(correct_history), ['53'], "Missing element")
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(broken_history), [], "Should match nothing")
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(none_history), [], "No history has no elements in list")

    def test_get_all_arguments_by_statement(self):
        argument_list = lib.get_all_arguments_by_statement(3)
        self.assertEqual(len(argument_list), 4)
        for argument in argument_list:
            self.assertTrue(argument.uid in [4, 5, 6, 7])
        self.assertEqual(len(lib.get_all_arguments_by_statement(70, True)), 2)
        self.assertEqual(len(lib.get_all_arguments_by_statement(12, True)), 1)
        self.assertEqual(lib.get_all_arguments_by_statement(-1), None)

    def test_get_global_url(self):
        self.assertIn('dbas.cs.uni-duesseldorf.de', lib.get_global_url())

    def test_get_user_by_private_or_public_nickname(self):
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('tobias'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('Antonia'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('Jutta'))

    def test_get_user_by_case_insensitive_nickname(self):
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('tobias'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('tobiaS'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('TobiaS'))
        self.assertIsNone(lib.get_user_by_case_insensitive_nickname('puh_der_bär'))

    def test_get_user_by_case_insensitive_public_nickname(self):
        self.assertIsNotNone(lib.get_user_by_case_insensitive_public_nickname('tobias'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_public_nickname('tobiaS'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_public_nickname('TobiaS'))
        self.assertIsNone(lib.get_user_by_case_insensitive_public_nickname('puh_der_bär'))

    def test_pretty_print_options(self):
        self.assertTrue('Hallo.', lib.pretty_print_options('hallo'))
        self.assertTrue('Hallo.', lib.pretty_print_options('<bla>hallo'))
        self.assertTrue('Hallo.', lib.pretty_print_options('<bla>hallo</bla>'))

    def test_is_user_author_or_admin(self):
        self.assertTrue(lib.is_user_admin('Tobias'))
        self.assertFalse(lib.is_user_admin('Pascal'))

    def test_is_user_admin(self):
        self.assertTrue(lib.is_user_admin('Tobias'))
        self.assertFalse(lib.is_user_admin('Pascal'))

    def test_is_author_of_statement(self):
        self.assertTrue(lib.is_author_of_statement('Christian', 36))
        self.assertFalse(lib.is_author_of_statement('Christian', 2))
        self.assertFalse(lib.is_author_of_statement('Chris', 36))
        self.assertFalse(lib.is_author_of_statement('Christian', 0))
        self.assertFalse(lib.is_author_of_statement('Chris', 0))

    def test_is_author_of_argument(self):
        self.assertTrue(lib.is_author_of_argument('Christian', 32))
        self.assertFalse(lib.is_author_of_argument('Christian', 4))
        self.assertFalse(lib.is_author_of_argument('Chris', 34))
        self.assertFalse(lib.is_author_of_argument('Tobias', 0))
        self.assertFalse(lib.is_author_of_argument('Chris', 0))

    def test_get_profile_picture(self):
        user = DBDiscussionSession.query(User).get(1)
        self.assertIn('gravatar.com', lib.get_profile_picture(user))
        self.assertIn('80', lib.get_profile_picture(user))
        self.assertIn('gravatar.com', lib.get_profile_picture(user, size=120))
        self.assertIn('120', lib.get_profile_picture(user, size=120))

    def test_get_public_profile_picture(self):
        user = DBDiscussionSession.query(User).get(1)
        self.assertIn('gravatar.com', lib.get_profile_picture(user))
        self.assertIn('80', lib.get_profile_picture(user))
        self.assertIn('gravatar.com', lib.get_profile_picture(user, size=120))
        self.assertIn('120', lib.get_profile_picture(user, size=120))

    def test_get_author_data(self):
        u, s, b = lib.get_author_data('main_page', 0)
        self.assertFalse(b)
        self.assertIsNone(u)

        user = DBDiscussionSession.query(User).get(1)
        u, s, b = lib.get_author_data('main_page', 1, gravatar_on_right_side=False)
        self.assertTrue(b)
        self.assertIn(' {}'.format(user.nickname), s)

        u, s, b = lib.get_author_data('main_page', 1, gravatar_on_right_side=True)
        self.assertTrue(b)
        self.assertIn('{} '.format(user.nickname), s)

    def test_bubbles_already_last_in_list(self):
        return True

    def test_get_changelog(self):
        self.assertEqual(1, len(lib.get_changelog(1)))
        self.assertEqual(3, len(lib.get_changelog(3)))
        self.assertEqual(type(list()), type(lib.get_changelog(1)))
        self.assertEqual(type(dict()), type(lib.get_changelog(1)[0]))

    def test_get_discussion_language(self):
        matchdict, params, session, current_issue_uid = {}, {}, {}, {}
        self.assertEqual('en', lib.get_discussion_language(matchdict, params, session, current_issue_uid))

        current_issue_uid = 4
        self.assertEqual('de', lib.get_discussion_language(matchdict, params, session, current_issue_uid))

        matchdict, params, session, current_issue_uid = {'issue': 1}, {}, {}, {}
        self.assertEqual('en', lib.get_discussion_language(matchdict, params, session, current_issue_uid))

        matchdict, params, session, current_issue_uid = {}, {'issue': 1}, {}, {}
        self.assertEqual('en', lib.get_discussion_language(matchdict, params, session, current_issue_uid))

        matchdict, params, session, current_issue_uid = {}, {}, {'issue': 1}, {}
        self.assertEqual('en', lib.get_discussion_language(matchdict, params, session, current_issue_uid))

    def test_get_slug_by_statement_uid(self):
        statement = DBDiscussionSession.query(Statement).get(1)
        issue = DBDiscussionSession.query(Issue).get(statement.issue_uid)
        self.assertEqual(issue.slug, lib.get_slug_by_statement_uid(1))

    def test_get_text_for_premise(self):
        self.assertIsNone(lib.get_text_for_premise(0))
        self.assertEqual(lib.get_text_for_premise(12), 'cats are fluffy')
        self.assertNotIn('data-argumentation-type', lib.get_text_for_premise(12, False))
        self.assertEqual(lib.get_text_for_premise(52), 'das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen')
        self.assertIn('data-argumentation-type', lib.get_text_for_premise(12, True))

    def test_is_argument_disabled_due_to_disabled_statements(self):
        arg = DBDiscussionSession.query(Argument).get(2)
        self.assertFalse(lib.is_argument_disabled_due_to_disabled_statements(arg))

        arg = DBDiscussionSession.query(Argument).get(1)
        self.assertTrue(lib.is_argument_disabled_due_to_disabled_statements(arg))

    def test_get_all_arguments_with_text_by_statement_id(self):
        res = lib.get_all_arguments_with_text_by_statement_id(0)
        self.assertIsNone(res)

        results = {
            3: 'we should get a cat  does not hold, because  cats are capricious',
            18: 'Other participants said that we should get a cat because cats are very independent. You did not agree with this because the purpose of a pet is to have something to take care of.',
            22: 'Other participants said that it is false that  we should get a cat because cats are capricious. You did not agree with this because this is based on the cats race and a little bit on the breeding.',
            12: 'we should get a cat because cats are fluffy and cats are small',
            25: 'Other participants said that we should get a cat because a dog costs taxes and will be more expensive than a cat. You did not agree with this because this is just a claim without any justification.',
            14: "We should get a cat because cats are fluffy and cats are small. Now you agree that fluffy animals losing much hair and I'm allergic to animal hair. You did not agree with this because you could use a automatic vacuum cleaner.",
            2: 'we should get a cat because cats are very independent',
            13: "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.",
            11: 'we should get a cat because a dog costs taxes and will be more expensive than a cat'
        }
        res = lib.get_all_arguments_with_text_by_statement_id(2)
        self.assertEqual(9, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_all_arguments_with_text_and_url_by_statement_id(self):
        from dbas.url_manager import UrlManager
        um = UrlManager(application_url='', slug='slug', for_api=True)

        res = lib.get_all_arguments_with_text_and_url_by_statement_id(0, um)
        self.assertEqual([], res)

        results = {
            3: 'we should get a cat  does not hold, because  cats are capricious',
            18: 'Someone argued that we should get a cat because cats are very independent. Other participants said that the purpose of a pet is to have something to take care of.',
            22: 'Someone argued that it is false that  we should get a cat because cats are capricious. Other participants said that this is based on the cats race and a little bit on the breeding.',
            12: 'we should get a cat because cats are fluffy and cats are small',
            25: 'Someone argued that we should get a cat because a dog costs taxes and will be more expensive than a cat. Other participants said that this is just a claim without any justification.',
            14: "Someone argued that we should get a cat because cats are fluffy and cats are small. Other participants said that fluffy animals losing much hair and I'm allergic to animal hair. Then other participants said that you could use a automatic vacuum cleaner.",
            2: 'we should get a cat because cats are very independent',
            13: "Someone argued that we should get a cat because cats are fluffy and cats are small. Other participants said that fluffy animals losing much hair and I'm allergic to animal hair.",
            11: 'we should get a cat because a dog costs taxes and will be more expensive than a cat'
        }
        res = lib.get_all_arguments_with_text_and_url_by_statement_id(2, um)
        self.assertEqual(9, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_text_for_argument_uid(self):
        self.assertTrue(lib.get_text_for_argument_uid(5), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(7), "Other participants said that it is false that  we should get a dog because you have to take the dog for a walk every day, which is tedious. You did not agree with this because going for a walk with the dog every day is good for social interaction and physical exercise.")
        self.assertTrue(lib.get_text_for_argument_uid(8), "we could get both, a cat and a dog because it would be no problem")
        self.assertTrue(lib.get_text_for_argument_uid(9), "Other participants said that we could get both, a cat and a dog because it would be no problem. You did not agree with this because a cat and a dog will generally not get along well and won't be best friends.")
        self.assertTrue(lib.get_text_for_argument_uid(10), "it would be no problem  does not hold, because  we do not have enough money for two pets")
        self.assertTrue(lib.get_text_for_argument_uid(11), "we should get a cat because a dog costs taxes and will be more expensive than a cat")
        self.assertTrue(lib.get_text_for_argument_uid(12), "we should get a cat because cats are fluffy and cats are small")
        self.assertTrue(lib.get_text_for_argument_uid(13), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")
        self.assertTrue(lib.get_text_for_argument_uid(14), "We should get a cat because cats are fluffy and cats are small. Now you agree that fluffy animals losing much hair and I'm allergic to animal hair. You did not agree with this because you could use a automatic vacuum cleaner.")

        for attack in ['', None, 'jump']:
            self.assertTrue(lib.get_text_for_argument_uid(5, anonymous_style=True, attack_type=attack), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
            self.assertTrue(lib.get_text_for_argument_uid(6, anonymous_style=True, attack_type=attack), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
            self.assertTrue(lib.get_text_for_argument_uid(7, anonymous_style=True, attack_type=attack), "Other participants said that it is false that  we should get a dog because you have to take the dog for a walk every day, which is tedious. You did not agree with this because going for a walk with the dog every day is good for social interaction and physical exercise.")
            self.assertTrue(lib.get_text_for_argument_uid(8, anonymous_style=True, attack_type=attack), "we could get both, a cat and a dog because it would be no problem")
            self.assertTrue(lib.get_text_for_argument_uid(9, anonymous_style=True, attack_type=attack), "Other participants said that we could get both, a cat and a dog because it would be no problem. You did not agree with this because a cat and a dog will generally not get along well and won't be best friends.")
            self.assertTrue(lib.get_text_for_argument_uid(10, anonymous_style=True, attack_type=attack), "it would be no problem  does not hold, because  we do not have enough money for two pets")
            self.assertTrue(lib.get_text_for_argument_uid(11, anonymous_style=True, attack_type=attack), "we should get a cat because a dog costs taxes and will be more expensive than a cat")
            self.assertTrue(lib.get_text_for_argument_uid(12, anonymous_style=True, attack_type=attack), "we should get a cat because cats are fluffy and cats are small")
            self.assertTrue(lib.get_text_for_argument_uid(13, anonymous_style=True, attack_type=attack), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")
            self.assertTrue(lib.get_text_for_argument_uid(14, anonymous_style=True, attack_type=attack), "We should get a cat because cats are fluffy and cats are small. Now you agree that fluffy animals losing much hair and I'm allergic to animal hair. You did not agree with this because you could use a automatic vacuum cleaner.")

        self.assertTrue(lib.get_text_for_argument_uid(5, with_html_tag=True), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, with_html_tag=True), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, with_html_tag=True), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")

        self.assertTrue(lib.get_text_for_argument_uid(5, start_with_intro=True), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, start_with_intro=True), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, start_with_intro=True), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")

        self.assertTrue(lib.get_text_for_argument_uid(5, first_arg_by_user=True), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, first_arg_by_user=True), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, first_arg_by_user=True), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")

        self.assertTrue(lib.get_text_for_argument_uid(5, is_users_opinion=False), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, is_users_opinion=False), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, is_users_opinion=True), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")

        self.assertTrue(lib.get_text_for_argument_uid(5, rearrange_intro=True), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, rearrange_intro=True), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, rearrange_intro=True), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")

        self.assertTrue(lib.get_text_for_argument_uid(5, support_counter_argument=True), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, support_counter_argument=True), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, support_counter_argument=True), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")

        self.assertTrue(lib.get_text_for_argument_uid(5, nickname='Dieter'), "we should get a dog  does not hold, because  you have to take the dog for a walk every day, which is tedious")
        self.assertTrue(lib.get_text_for_argument_uid(6, nickname='Dieter'), "Other participants said that we should get a dog because dogs can act as watch dogs. You did not agree with this because we have no use for a watch dog.")
        self.assertTrue(lib.get_text_for_argument_uid(13, nickname='Dieter'), "Other participants said that we should get a cat because cats are fluffy and cats are small. You did not agree with this because fluffy animals losing much hair and I'm allergic to animal hair.")
