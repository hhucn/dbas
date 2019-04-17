from datetime import date

import transaction

from dbas import lib
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, Statement, TextVersion, Issue, Premise
from dbas.helper.url import UrlManager
from dbas.lib import get_enabled_issues_as_query, get_enabled_statement_as_query, get_enabled_arguments_as_query, \
    get_enabled_premises_as_query, get_visible_issues_for_user
from dbas.tests.utils import TestCaseWithConfig


class LibTests(TestCaseWithConfig):

    def test_escape_string(self):
        self.assertEqual('', lib.escape_string(text=''))

        # normal string
        self.assertEqual('str', lib.escape_string(text='str'))

        # strings with html special chars
        self.assertEqual('&amp;', lib.escape_string(text='&'))

        self.assertEqual('&quot; str &amp; str2', lib.escape_string(text='" str & str2'))

        long_str_with_special_char = 'str' + '"' * 1000
        long_str_without_special_char = 'str' + '&quot;' * 1000
        self.assertEqual(long_str_without_special_char, lib.escape_string(long_str_with_special_char))

    def test_python_datetime_pretty_print(self):
        # datetime corresponding to Gregorian ordinal
        d = date.fromordinal(736132)

        # Verify, that if 'lang' is 'de' format of date is 'day. month.'
        self.assertEqual(lib.pretty_print_timestamp(ts=d, lang='de'), '17. Jun.')

        # Verify, that if 'lang' is not 'de' format of date is 'month. day. '
        self.assertEqual(lib.pretty_print_timestamp(ts=d, lang='en'), 'Jun. 17.')

        self.assertEqual(lib.pretty_print_timestamp(ts='2016-01-01', lang=''), 'Jan. 01.')

    def test_get_text_for_premisegroup_uid(self):
        # premise, which is in db_premises and premise_group contains only one premise
        self.assertEqual(lib.get_text_for_premisegroup_uid(uid=2), 'cats are very independent')

        # premise_group with more than one premises
        self.assertNotEqual(lib.get_text_for_premisegroup_uid(uid=13), 'cats are fluffy und cats are small')

        val = lib.get_text_for_premisegroup_uid(uid=12)
        sol1 = 'cats are fluffy and cats are small'
        sol2 = 'cats are small and cats are fluffy'
        self.assertIn(val, [sol1, sol2])

        # premise, which is not in db_premises
        self.assertEqual(lib.get_text_for_premisegroup_uid(uid=0), '')

        # negative uid
        self.assertEqual(lib.get_text_for_premisegroup_uid(uid=-1), '')

        # language is empty string
        self.assertEqual(lib.get_text_for_premisegroup_uid(uid=0), '')

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
                                                     rearrange_intro=True), '')

        # unknown conclusion id
        argument3 = Argument(premisegroup=0, is_supportive=True, author=0, issue=0, conclusion=0)
        self.assertEqual(lib.get_text_for_conclusion(argument=argument3,
                                                     start_with_intro=False,
                                                     rearrange_intro=True), '')

    def test_get_all_attacking_arg_uids_from_history(self):
        none_history = None
        correct_history = "/attitude/60-/justify/60/agree-/reaction/52/rebut/53"
        broken_history = "/attitude/60/justify/60/agree/broooken/52/rebut/53"
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(correct_history), ['53'], "Missing element")
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(broken_history), [], "Should match nothing")
        self.assertEqual(lib.get_all_attacking_arg_uids_from_history(none_history), [],
                         "No history has no elements in list")

    def test_get_all_arguments_by_statement(self):
        argument_list = lib.get_all_arguments_by_statement(3)
        self.assertEqual(len(argument_list), 4)
        for argument in argument_list:
            self.assertTrue(argument.uid in [4, 5, 6, 7])
        self.assertEqual(len(lib.get_all_arguments_by_statement(70, True)), 2)
        self.assertEqual(len(lib.get_all_arguments_by_statement(12, True)), 1)
        self.assertEqual(lib.get_all_arguments_by_statement(-1), None)

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


class TestPrettyPrintOptions(TestCaseWithConfig):
    def test_pretty_print_options(self):
        self.assertEqual(lib.pretty_print_options('hallo'), 'Hallo.')
        self.assertEqual(lib.pretty_print_options('<bla>hallo'), '<bla>Hallo.')
        self.assertEqual(lib.pretty_print_options('<bla>hallo</bla>'), '<bla>Hallo.</bla>')


class TestAuthorship(TestCaseWithConfig):
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


class TestGravatar(TestCaseWithConfig):
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


class TestAuthorData(TestCaseWithConfig):
    def test_get_author_data(self):
        db_user, author_string, some_boolean = lib.get_author_data(0)
        self.assertFalse(some_boolean)
        self.assertIsNone(db_user)

        user = DBDiscussionSession.query(User).get(1)
        _, author_string, some_boolean = lib.get_author_data(1, gravatar_on_right_side=False)
        self.assertTrue(some_boolean)
        self.assertIn('{}'.format(user.nickname), author_string)
        self.assertIn('right', author_string)

        _, author_string, some_boolean = lib.get_author_data(1, gravatar_on_right_side=True)
        self.assertTrue(some_boolean)
        self.assertIn('{}'.format(user.nickname), author_string)
        self.assertIn('left', author_string)


class TestChangeLog(TestCaseWithConfig):
    def test_get_changelog(self):
        self.assertEqual(len(lib.get_changelog(1)), 1)
        self.assertEqual(len(lib.get_changelog(3)), 3)
        self.assertIsInstance(lib.get_changelog(1), list)
        self.assertIsInstance(lib.get_changelog(1)[0], dict)


class TestDiscussionLanguage(TestCaseWithConfig):
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


class TestGetTextForEntities(TestCaseWithConfig):
    def test_get_text_for_premise(self):
        self.assertIsNone(lib.get_text_for_premise(0))
        self.assertEqual(lib.get_text_for_premise(12), 'cats are fluffy')
        self.assertNotIn('data-argumentation-type', lib.get_text_for_premise(12, False))
        self.assertEqual(lib.get_text_for_premise(52),
                         'das Unfallrisiko steigt, da die Autos kaum Geräusche verursachen')
        self.assertIn('data-argumentation-type', lib.get_text_for_premise(12, True))

    def test_get_all_arguments_with_text_by_statement_id(self):
        res = lib.get_all_arguments_with_text_by_statement_id(0)
        self.assertEqual(res, [])

        results = {
            47: 'we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them',
            48: 'Other participants said that we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them. You did not agree with this because schools need the swimming pools for their sports lessons.',
            49: 'we should close public swimming pools does not hold, because the rate of non-swimmers is too high'
        }
        res = lib.get_all_arguments_with_text_by_statement_id(38)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIn(r['uid'], results)

    def test_get_all_arguments_with_text_and_url_by_statement_id(self):
        um = UrlManager(slug='slug')

        results = {
            47: 'we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them',
            48: 'Someone argued that we should close public swimming pools because our swimming pools are very old and it would take a major investment to repair them. Other participants said that schools need the swimming pools for their sports lessons.',
            49: 'we should close public swimming pools does not hold, because the rate of non-swimmers is too high'
        }
        db_statement = DBDiscussionSession.query(Statement).get(38)
        res = lib.get_all_arguments_with_text_and_url_by_statement(db_statement, um)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIn(r['uid'], results)

    def test_get_all_arguments_with_text_and_url_by_statement_id_with_color(self):
        um = UrlManager(slug='slug')

        results = {
            47: '<span data-argumentation-type="position">we should close public swimming pools</span> because our swimming pools are very old and it would take a major investment to repair them',
            48: 'Someone argued that <span data-argumentation-type="position">we should close public swimming pools</span> because our swimming pools are very old and it would take a major investment to repair them. Other participants said that schools need the swimming pools for their sports lessons.',
            49: '<span data-argumentation-type="position">we should close public swimming pools</span> does not hold, because the rate of non-swimmers is too high'
        }

        db_statement = DBDiscussionSession.query(Statement).get(38)
        res = lib.get_all_arguments_with_text_and_url_by_statement(db_statement, um, color_statement=True)
        self.assertEqual(3, len(res))
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertEqual(results[r['uid']], r['text'])

    def test_get_all_arguments_with_text_and_url_by_statement_id_with_color_and_jump(self):
        um = UrlManager(slug='slug')

        results = {
            47: '<span data-argumentation-type="position">we should close public swimming pools</span> because our swimming pools are very old and it would take a major investment to repair them.',
            48: 'our swimming pools are very old and it would take a major investment to repair them is not a good reason for <span data-argumentation-type="position">we should close public swimming pools</span>. Because schools need the swimming pools for their sports lessons.',
            49: '<span data-argumentation-type="position">we should close public swimming pools</span> does not hold because the rate of non-swimmers is too high.'
        }

        db_statement = DBDiscussionSession.query(Statement).get(38)
        res = lib.get_all_arguments_with_text_and_url_by_statement(db_statement, um, color_statement=True,
                                                                   is_jump=True)
        self.assertEqual(len(res), 3)
        for r in res:
            self.assertIn(r['uid'], results)
            self.assertIn('jump', r['url'])
            self.assertEqual(results[r['uid']], r['text'])


class TestGetTextForArgumentByUid(TestCaseWithConfig):
    def test_get_text_for_argument_uid(self):
        s47 = 'we should close public swimming pools because our swimming pools are very old and it would take a ' \
              'major investment to repair them'
        s48 = 'Other participants said that we should close public swimming pools because our swimming pools are ' \
              'very old and it would take a major investment to repair them. You did not agree with this because ' \
              'schools need the swimming pools for their sports lessons.'
        s49 = 'we should close public swimming pools does not hold, because the rate of non-swimmers is too high'

        self.assertEqual(lib.get_text_for_argument_uid(47), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, attack_type='doesnt-matter-parameter-should-be-a-boolean'),
                         s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, attack_type='doesnt-matter-parameter-should-be-a-boolean'),
                         s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, attack_type='doesnt-matter-parameter-should-be-a-boolean'),
                         s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, attack_type='jump'), '{}.'.format(s47))
        self.assertEqual(lib.get_text_for_argument_uid(48, attack_type='jump'),
                         'our swimming pools are very old and it would take a major investment to repair them is not '
                         'a good reason for we should close public swimming pools. Because schools need the swimming '
                         'pools for their sports lessons.')
        self.assertEqual(lib.get_text_for_argument_uid(49, attack_type='jump'),
                         'we should close public swimming pools does not hold because the rate of non-swimmers is too '
                         'high.')

        self.assertEqual(lib.get_text_for_argument_uid(47, with_html_tag=True),
                         '<span>we should close public swimming pools</span> because our swimming pools are very old '
                         'and it would take a major investment to repair them')
        self.assertEqual(lib.get_text_for_argument_uid(48, with_html_tag=True),
                         'Other participants said that we should close public swimming pools because our swimming '
                         'pools are very old and it would take a major investment to repair them. You did not agree '
                         'with this because<span data-argumentation-type="position"> schools need the swimming pools '
                         'for their sports lessons.')
        self.assertEqual(lib.get_text_for_argument_uid(49, with_html_tag=True),
                         '<span>we should close public swimming pools</span> <span> does not hold</span>, because the '
                         'rate of non-swimmers is too high')

        self.assertEqual(lib.get_text_for_argument_uid(47, start_with_intro=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, start_with_intro=True), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, start_with_intro=True), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, first_arg_by_user=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, first_arg_by_user=True),
                         'We should close public swimming pools because our swimming pools are very old and it would '
                         'take a major investment to repair them. Now you agree that schools need the swimming pools '
                         'for their sports lessons.')
        self.assertEqual(lib.get_text_for_argument_uid(49, first_arg_by_user=True), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, is_users_opinion=False), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, is_users_opinion=False), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, is_users_opinion=False), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, rearrange_intro=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, rearrange_intro=True), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, rearrange_intro=True), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, support_counter_argument=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, support_counter_argument=True), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, support_counter_argument=True), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, nickname='Dieter'), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, nickname='Dieter'), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, nickname='Dieter'), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, minimize_on_undercut=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, minimize_on_undercut=True), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, minimize_on_undercut=True), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, colored_position=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, colored_position=True), s48)
        self.assertEqual(lib.get_text_for_argument_uid(49, colored_position=True), s49)

        self.assertEqual(lib.get_text_for_argument_uid(47, user_changed_opinion=True), s47)
        self.assertEqual(lib.get_text_for_argument_uid(48, user_changed_opinion=True),
                         'Earlier you argued that we should close public swimming pools because our swimming pools '
                         'are very old and it would take a major investment to repair them. Other participants '
                         'convinced you that schools need the swimming pools for their sports lessons.')
        self.assertEqual(lib.get_text_for_argument_uid(49, user_changed_opinion=True), s49)


class TestVisibilityOfDisabledEntities(TestCaseWithConfig):
    def test_get_enabled_statement_as_query(self):
        query_len = get_enabled_statement_as_query().count()
        res_len = DBDiscussionSession.query(Statement).filter_by(is_disabled=False).count()
        self.assertEqual(res_len, query_len)

    def test_get_enabled_arguments_as_query(self):
        query_len = get_enabled_arguments_as_query().count()
        res_len = DBDiscussionSession.query(Argument).filter_by(is_disabled=False).count()
        self.assertEqual(res_len, query_len)

    def test_get_enabled_premises_as_query(self):
        query_len = get_enabled_premises_as_query().count()
        res_len = DBDiscussionSession.query(Premise).filter_by(is_disabled=False).count()
        self.assertEqual(res_len, query_len)

    def test_get_enabled_issues_as_query(self):
        query_len = get_enabled_issues_as_query().count()
        res_len = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).count()
        self.assertEqual(res_len, query_len)

    def test_get_visible_issues_for_user_as_query(self):
        issue_uids = [issue.uid for issue in get_visible_issues_for_user(self.user_christian)]
        self.assertCountEqual(issue_uids, [2, 3, 4, 5, 7, 8])

    def test_is_argument_disabled_due_to_disabled_statements(self):
        arg1 = DBDiscussionSession.query(Argument).get(1)
        arg2 = DBDiscussionSession.query(Argument).get(2)

        self.assertFalse(lib.is_argument_disabled_due_to_disabled_statements(arg2))
        self.assertTrue(lib.is_argument_disabled_due_to_disabled_statements(arg1))


class TestUnhtmlify(TestCaseWithConfig):
    def test_unhtmlify(self):
        self.assertEqual(lib.unhtmlify(''), '')
        self.assertEqual(lib.unhtmlify('str'), 'str')
        self.assertEqual(lib.unhtmlify('<a>str</a>'), 'str')
        self.assertEqual(lib.unhtmlify('<a> str </a>'), ' str ')
        self.assertEqual(lib.unhtmlify('<a>str'), 'str')
        self.assertEqual(lib.unhtmlify('a <tag> b'), 'a  b')
        self.assertEqual(lib.unhtmlify('a.<tag> b'), 'a. b')
