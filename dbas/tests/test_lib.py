import unittest
from datetime import date

import transaction

from dbas import lib
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, Statement, Issue, TextVersion
from dbas.helper.url import UrlManager


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
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=2), ('cats are very independent'))

        # premise_group with more than one premises
        self.assertNotEqual(lib.get_text_for_premisesgroup_uid(uid=13), ('cats are fluffy und cats are small'))

        values = lib.get_text_for_premisesgroup_uid(uid=12)
        solution1 = 'cats are fluffy and cats are small', ['15', '16']
        solution2 = 'cats are small and cats are fluffy', ['16', '15']
        if values[1] == solution1[1]:
            self.assertEqual(values, solution1)
        else:
            self.assertEqual(values, solution2)

        # premise, which is not in db_premises
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0), (''))

        # negative uid
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=-1), (''))

        # language is empty string
        self.assertEqual(lib.get_text_for_premisesgroup_uid(uid=0), (''))

    def test_get_text_for_statement_uid(self):
        # id for no statement
        self.assertIsNone(lib.get_text_for_statement_uid(uid=0))

        # id for statement, which ends with '.'
        self.assertEqual(lib.get_text_for_statement_uid(uid=3), 'we should get a dog')

        # id for statement, which ends with '!'
        self.assertEqual(lib.get_text_for_statement_uid(uid=31), 'it is important, that pets are small and fluffy')

        # negative uid
        self.assertIsNone(lib.get_text_for_statement_uid(uid=-30))

    def test_get_text_for_conclusion(self):
        argument1 = Argument(premisegroup=4, is_supportive=True, author=1, issue=1, conclusion=3)
        # 'argument' is an argument
        self.assertEqual(lib.get_text_for_conclusion(argument=argument1,
                                                     start_with_intro=False,
                                                     rearrange_intro=False), 'we should get a dog')

        argument2 = Argument(premisegroup=1, is_supportive=False, author=1, issue=1)
        # 'argument' is a statement
        self.assertEqual(lib.get_text_for_conclusion(argument=argument2,
                                                     start_with_intro=True,
                                                     rearrange_intro=True), None)

        # unknown conclusion id
        argument3 = Argument(premisegroup=0, is_supportive=True, author=0, issue=0, conclusion=0)
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
        correct_history = "/attitude/60-/justify/60/agree-/reaction/52/rebut/53"
        broken_history = "/attitude/60/justify/60/agree/broooken/52/rebut/53"
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
        self.assertIsNone(lib.get_user_by_case_insensitive_nickname('puh_der_bär'))

    def test_get_user_by_case_insensitive_nickname(self):
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('tobias'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('tobiaS'))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_nickname('TobiaS'))
        self.assertIsNone(lib.get_user_by_case_insensitive_nickname('puh_der_bär'))

    def test_get_user_by_case_insensitive_public_nickname(self):
        user = DBDiscussionSession.query(User).get(2)
        self.assertIsNotNone(lib.get_user_by_case_insensitive_public_nickname(user.public_nickname.lower()))
        self.assertIsNotNone(lib.get_user_by_case_insensitive_public_nickname(user.public_nickname.upper()))
        self.assertIsNone(lib.get_user_by_case_insensitive_public_nickname('puh_der_bär'))

    def test_pretty_print_options(self):
        self.assertTrue('Hallo.', lib.pretty_print_options('hallo'))
        self.assertTrue('Hallo.', lib.pretty_print_options('<bla>hallo'))
        self.assertTrue('Hallo.', lib.pretty_print_options('<bla>hallo</bla>'))

    def test_is_user_author_or_admin(self):
        db_user1 = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user2 = DBDiscussionSession.query(User).filter_by(nickname='Pascal').first()
        self.assertTrue(db_user1.is_admin() or db_user1.is_author())
        self.assertFalse(db_user2.is_admin() or db_user2.is_author())

    def test_is_user_admin(self):
        self.assertTrue(DBDiscussionSession.query(User).filter_by(nickname='Tobias').first().is_admin())
        self.assertFalse(DBDiscussionSession.query(User).filter_by(nickname='Pascal').first().is_admin())

    def test_is_author_of_statement(self):
        tv = DBDiscussionSession.query(TextVersion).get(35)
        tv.author_uid = 2
        DBDiscussionSession.add(tv)
        DBDiscussionSession.flush()
        transaction.commit()
        user36 = DBDiscussionSession.query(User).get(tv.author_uid)
        self.assertTrue(lib.is_author_of_statement(user36, tv.statement_uid))
        self.assertFalse(lib.is_author_of_statement(user36, 3))

    def test_is_author_of_argument(self):
        arg = DBDiscussionSession.query(Argument).get(36)
        arg.author_uid = 2
        DBDiscussionSession.add(arg)
        DBDiscussionSession.flush()
        transaction.commit()
        user36 = DBDiscussionSession.query(User).get(arg.author_uid)
        self.assertTrue(lib.is_author_of_argument(user36, 36))
        self.assertFalse(lib.is_author_of_argument(user36, 2))

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
        u, s, b = lib.get_author_data(0)
        self.assertFalse(b)
        self.assertIsNone(u)

        user = DBDiscussionSession.query(User).get(1)
        u, s, b = lib.get_author_data(1, gravatar_on_right_side=False)
        self.assertTrue(b)
        self.assertIn(' {}'.format(user.nickname), s)

        u, s, b = lib.get_author_data(1, gravatar_on_right_side=True)
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
        self.assertEqual(res, [])

        results = {
            47: 'we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them',
            48: 'Other participants said that we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them. You did not agree with this because schools need the swimming pools for their sports lessons.',
            49: 'we should close public swimming pools does not hold, because the rate of non-swimmers is too high'
        }
        res = lib.get_all_arguments_with_text_by_statement_id(38)
        self.assertEqual(3, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_all_arguments_with_text_and_url_by_statement_id(self):
        um = UrlManager(slug='slug')

        results = {
            47: 'we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them',
            48: 'Someone argued that we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them. Other participants said that schools need the swimming pools for their sports lessons.',
            49: 'we should close public swimming pools does not hold, because the rate of non-swimmers is too high'
        }

        db_statement = DBDiscussionSession.query(Statement).get(38)
        res = lib.get_all_arguments_with_text_and_url_by_statement_id(db_statement, um)
        self.assertEqual(3, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_all_arguments_with_text_and_url_by_statement_id_with_color(self):
        um = UrlManager(slug='slug')

        results = {
            47: '<span data-argumentation-type="position">we should close public swimming pools</span> because our swimming pools are very old and it would take a major investment to repair them',
            48: 'Someone argued that <span data-argumentation-type="position">we should close public swimming pools</span> because our swimming pools are very old and it would take a major investment to repair them. Other participants said that schools need the swimming pools for their sports lessons.',
            49: '<span data-argumentation-type="position">we should close public swimming pools</span> does not hold, because the rate of non-swimmers is too high'
        }

        db_statement = DBDiscussionSession.query(Statement).get(38)
        res = lib.get_all_arguments_with_text_and_url_by_statement_id(db_statement, um, color_statement=True)
        self.assertEqual(3, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_all_arguments_with_text_and_url_by_statement_id_with_color_and_jump(self):
        um = UrlManager(slug='slug')

        results = {
            47: '<span data-argumentation-type="position">we should close public swimming pools</span> because our swimming pools are very old and it would take a major investment to repair them.',
            48: 'our swimming pools are very old and it would take a major investment to repair them <span data-attitude="con">is not a good reason for</span> <span data-argumentation-type="position">we should close public swimming pools</span>. Because schools need the swimming pools for their sports lessons.',
            49: '<span data-argumentation-type="position">we should close public swimming pools</span> <span data-attitude="con">does not hold</span> because the rate of non-swimmers is too high.'
        }

        db_statement = DBDiscussionSession.query(Statement).get(38)
        res = lib.get_all_arguments_with_text_and_url_by_statement_id(db_statement, um, color_statement=True, is_jump=True)
        self.assertEqual(3, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertIn('jump', r['url'])
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_text_for_argument_uid(self):
        s47 = 'we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them'
        s48 = 'Other participants said that we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them. You did not agree with this because schools need the swimming pools for their sports lessons.'
        s49 = 'we should close public swimming pools does not hold, because the rate of non-swimmers is too high'

        self.assertTrue(lib.get_text_for_argument_uid(47), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49), s49)

        for attack in ['', None, 'jump']:
            self.assertTrue(lib.get_text_for_argument_uid(47, attack_type=attack), s47)
            self.assertTrue(lib.get_text_for_argument_uid(48, attack_type=attack), s48)
            self.assertTrue(lib.get_text_for_argument_uid(49, attack_type=attack), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, with_html_tag=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, with_html_tag=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, with_html_tag=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, start_with_intro=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, start_with_intro=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, start_with_intro=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, first_arg_by_user=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, first_arg_by_user=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, first_arg_by_user=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, is_users_opinion=False), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, is_users_opinion=False), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, is_users_opinion=False), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, rearrange_intro=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, rearrange_intro=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, rearrange_intro=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, support_counter_argument=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, support_counter_argument=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, support_counter_argument=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, nickname='Dieter'), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, nickname='Dieter'), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, nickname='Dieter'), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, minimize_on_undercut=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, minimize_on_undercut=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, minimize_on_undercut=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, colored_position=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, colored_position=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, colored_position=True), s49)

        self.assertTrue(lib.get_text_for_argument_uid(47, user_changed_opinion=True), s47)
        self.assertTrue(lib.get_text_for_argument_uid(48, user_changed_opinion=True), s48)
        self.assertTrue(lib.get_text_for_argument_uid(49, user_changed_opinion=True), s49)
