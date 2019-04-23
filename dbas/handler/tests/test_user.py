import arrow
import transaction
from datetime import date, timedelta

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, TextVersion, ClickedArgument, ClickedStatement, ReviewEdit, \
    Statement
from dbas.handler import user
from dbas.tests.utils import TestCaseWithConfig


class UserHandlerTests(TestCaseWithConfig):
    def test_should_log_out(self):
        old_timestamp = arrow.get(2016, 5, 5)
        self.user_tobi.last_action = old_timestamp
        self.user_tobi.last_login = old_timestamp
        DBDiscussionSession.add(self.user_tobi)
        settings = self.user_tobi.settings
        settings.should_hold_the_login(False)
        DBDiscussionSession.add(settings)
        transaction.commit()

        self.assertTrue(user.should_log_out(3600, self.user_tobi))

    def test_should_log_out_with_keep_login_flag(self):
        old_timestamp = arrow.get(2016, 5, 5)
        self.user_tobi.last_action = old_timestamp
        self.user_tobi.last_login = old_timestamp
        DBDiscussionSession.add(self.user_tobi)
        settings = self.user_tobi.settings
        settings.should_hold_the_login(True)
        DBDiscussionSession.add(settings)
        transaction.commit()

        self.assertFalse(user.should_log_out(3600, self.user_tobi))

    def test_refresh_public_nickname(self):
        old_nickname = self.user_tobi.public_nickname
        new_nickname = user.refresh_public_nickname(self.user_tobi)
        self.assertNotEqual(old_nickname, new_nickname)
        self.assertIn(new_nickname.split(' ')[0], user.MOODS)
        self.assertIn(' '.join(new_nickname.split(' ')[1:]), user.ANIMALS + user.THINGS + user.FOODS)

    def test_is_admin(self):
        self.assertFalse(user.is_admin('Pascal'))
        self.assertTrue(user.is_admin('Tobias'))

    def test_get_public_data(self):
        prep_dict = user.get_public_data(1000, 'en')
        self.assertEqual(len(prep_dict), 0)

    def test_get_reviews_of(self):
        engelbert = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        self.assertGreaterEqual(user.get_reviews_of(engelbert, True), 0)
        self.assertGreaterEqual(user.get_reviews_of(engelbert, False), 0)
        rv = ReviewEdit(self.user_tobi.uid, 1, 1)
        yesterday = date.today() - timedelta(1)
        rv.timestamp = arrow.get(yesterday.strftime('%Y-%m-%d'))
        DBDiscussionSession.add(rv)
        transaction.commit()
        self.assertGreaterEqual(user.get_reviews_of(self.user_tobi, True), 0)
        self.assertGreaterEqual(user.get_reviews_of(self.user_tobi, False), 0)

    def def_get_statement_count_of(self):
        engelbert = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        self.assertEqual(user.get_statement_count_of(None, True), 0)
        self.assertEqual(user.get_statement_count_of(None, False), 0)
        self.assertEqual(user.get_statement_count_of(engelbert, True), 0)
        self.assertEqual(user.get_statement_count_of(engelbert, False), 0)

        # add statement
        db_st = Statement(True)
        DBDiscussionSession.add(db_st)
        DBDiscussionSession.flush()
        transaction.commit()
        db_tv = TextVersion('hello, here i am', engelbert.uid, db_st.uid)
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        self.assertEqual(1, user.get_statement_count_of(engelbert, True))
        self.assertEqual(1, user.get_statement_count_of(engelbert, False))

        # set older timestamp
        db_tv.timestamp = DBDiscussionSession.query(TextVersion).get(1).timestamp
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        self.assertEqual(0, user.get_statement_count_of(engelbert, True))
        self.assertEqual(1, user.get_statement_count_of(engelbert, False))

    def def_get_edit_count_of(self):
        engelbert = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        self.assertEqual(0, user.get_edit_count_of(None, True))
        self.assertEqual(0, user.get_edit_count_of(None, False))
        self.assertEqual(0, user.get_edit_count_of(engelbert, True))
        self.assertEqual(0, user.get_edit_count_of(engelbert, False))

        # add edit
        db_st = DBDiscussionSession.query(Statement).get(1)
        db_tv = TextVersion('hello, here i am again', engelbert.uid, db_st.uid)
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        self.assertEqual(1, user.get_edit_count_of(engelbert, True))
        self.assertEqual(1, user.get_edit_count_of(engelbert, False))

        # set older timestamp
        db_tv.timestamp = DBDiscussionSession.query(TextVersion).get(1).timestamp
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        self.assertEqual(0, user.get_edit_count_of(engelbert, True))
        self.assertEqual(1, user.get_edit_count_of(engelbert, False))

    def test_get_count_of_votes_of_user(self):
        self.assertEqual((0, 0), user.get_mark_count_of(None, True))
        self.assertEqual((0, 0), user.get_mark_count_of(self.user_tobi, False))
        self.assertEqual((0, 0), user.get_mark_count_of(self.user_tobi, True))

    def test_get_count_of_clicks(self):
        self.assertEqual((0, 0), user.get_click_count_of(None, True))
        self.assertEqual((0, 0), user.get_click_count_of(self.user_tobi, False))
        self.assertEqual((0, 0), user.get_click_count_of(self.user_tobi, True))

        DBDiscussionSession.add(ClickedArgument(1, self.user_tobi.uid))
        DBDiscussionSession.add(ClickedStatement(1, self.user_tobi.uid))
        self.assertEqual((1, 1), user.get_click_count_of(self.user_tobi, False))
        self.assertEqual((1, 1), user.get_click_count_of(self.user_tobi, True))
        transaction.commit()

    def test_get_textversions(self):
        d = user.get_textversions(self.user_tobi, 'en')
        self.assertGreaterEqual(0, len(d.get('statements', [])))
        self.assertGreaterEqual(0, len(d.get('edits', [])))

    def test_get_marked_elements_of(self):
        prep_dict = user.get_marked_elements_of(self.user_tobi, False, 'en')
        self.assertEqual(0, len(prep_dict))
        self.assertNotIn('uid', prep_dict)

    def test_get_clicked_elements_of(self):
        prep_array = user.get_clicked_elements_of(self.user_tobi, True, 'en')
        self.assertLessEqual(0, len(prep_array))
        prep_array = user.get_clicked_elements_of(self.user_tobi, False, 'en')
        self.assertLessEqual(0, len(prep_array))

    def test_get_information_of(self):
        prep_dict = user.get_information_of(self.user_tobi, 'en')

        self.assertIn('public_nick', prep_dict)
        self.assertIn('last_action', prep_dict)
        self.assertIn('last_login', prep_dict)
        self.assertIn('registered', prep_dict)
        self.assertIn('group', prep_dict)
        self.assertTrue(prep_dict['is_male'])
        self.assertFalse(prep_dict['is_female'])
        self.assertFalse(prep_dict['is_neutral'])

    def test_get_summary_of_today(self):
        prep_dict = user.get_summary_of_today(self.user_tobi)
        self.assertEqual(self.user_tobi.nickname, prep_dict['firstname'])
        self.assertLessEqual(0, prep_dict['discussion_arg_clicks'])
        self.assertLessEqual(0, prep_dict['discussion_stat_clicks'])
        self.assertLessEqual(0, prep_dict['statements_posted'])
        self.assertLessEqual(0, prep_dict['edits_done'])

    def test_change_password(self):
        pascal = DBDiscussionSession.query(User).filter_by(nickname='Pascal').first()
        old_pw = 'iamatestuser2016'
        new_pw = 'iamatestuser2017'

        msg, success = user.change_password(pascal, old_pw, old_pw, old_pw, 'en')
        self.assertFalse(success)

        msg, success = user.change_password(pascal, old_pw, old_pw, new_pw, 'en')
        self.assertFalse(success)

        msg, success = user.change_password(pascal, old_pw, new_pw, old_pw, 'en')
        self.assertFalse(success)

        msg, success = user.change_password(pascal, new_pw, new_pw, old_pw, 'en')
        self.assertFalse(success)

        msg, success = user.change_password(pascal, new_pw, old_pw, old_pw, 'en')
        self.assertFalse(success)

        msg, success = user.change_password(pascal, old_pw, new_pw, new_pw, 'en')
        self.assertTrue(success)

        msg, success = user.change_password(pascal, new_pw, old_pw, old_pw, 'en')
        self.assertTrue(success)
