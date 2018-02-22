import transaction
import unittest
import arrow
from datetime import date, timedelta

from pyramid import testing

from nose.tools import assert_false, assert_true, assert_not_equal, assert_in, assert_not_in, assert_equal, \
    assert_greater_equal, assert_less_equal
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Settings, TextVersion, ClickedArgument, ClickedStatement, ReviewEdit, \
    Statement
from dbas.handler import user


class UserHandlerTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()

    def test_update_last_action(self):
        assert_false(user.update_last_action(''))
        user.update_last_action('Tobias')
        assert_false(user.update_last_action('Tobias'))

        old_ts = arrow.get(2016, 5, 5)
        self.user.last_action = old_ts
        self.user.last_login = old_ts
        DBDiscussionSession.add(self.user)
        settings = DBDiscussionSession.query(Settings).filter_by(author_uid=self.user.uid).first()
        settings.should_hold_the_login(False)
        DBDiscussionSession.add(settings)
        transaction.commit()

        assert_true(user.update_last_action('Tobias'))
        assert_false(user.update_last_action('Tobias'))

    def test_refresh_public_nickname(self):
        old_nickname = self.user.public_nickname
        new_nickname = user.refresh_public_nickname(self.user)
        assert_not_equal(old_nickname, new_nickname)
        assert_in(new_nickname.split(' ')[0], user.moodlist)
        assert_in(' '.join(new_nickname.split(' ')[1:]), user.animallist + user.thingslist + user.foodlist)

    def test_is_in_group(self):
        assert_false(user.is_in_group('', 'bla'))
        assert_false(user.is_in_group(self.user.nickname, 'bla'))
        assert_false(user.is_in_group('', 'admin'))
        assert_true(user.is_in_group(self.user.nickname, 'admins'))

    def test_is_admin(self):
        assert_false(user.is_admin('Pascal'))
        assert_true(user.is_admin('Tobias'))

    def test_get_public_data(self):
        prep_dict = user.get_public_data('CantHitThat', 'en')
        assert_equal(len(prep_dict), 0)

    def test_get_reviews_of(self):
        engelbert = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        assert_greater_equal(user.get_reviews_of(engelbert, True), 0)
        assert_greater_equal(user.get_reviews_of(engelbert, False), 0)
        rv = ReviewEdit(self.user.uid, 1, 1)
        yesterday = date.today() - timedelta(1)
        rv.timestamp = arrow.get(yesterday.strftime('%Y-%m-%d'))
        DBDiscussionSession.add(rv)
        transaction.commit()
        assert_greater_equal(user.get_reviews_of(self.user, True), 0)
        assert_greater_equal(user.get_reviews_of(self.user, False), 0)

    def def_get_statement_count_of(self):
        engelbert = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        assert_equal(user.get_statement_count_of(None, True), 0)
        assert_equal(user.get_statement_count_of(None, False), 0)
        assert_equal(user.get_statement_count_of(engelbert, True), 0)
        assert_equal(user.get_statement_count_of(engelbert, False), 0)

        # add statement
        db_st = Statement(True, 2)
        DBDiscussionSession.add(db_st)
        DBDiscussionSession.flush()
        transaction.commit()
        db_tv = TextVersion('hello, here i am', engelbert.uid, db_st.uid)
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        assert_equal(1, user.get_statement_count_of(engelbert, True))
        assert_equal(1, user.get_statement_count_of(engelbert, False))

        # set older timestamp
        db_tv.timestamp = DBDiscussionSession.query(TextVersion).get(1).timestamp
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        assert_equal(0, user.get_statement_count_of(engelbert, True))
        assert_equal(1, user.get_statement_count_of(engelbert, False))

    def def_get_edit_count_of(self):
        engelbert = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        assert_equal(0, user.get_edit_count_of(None, True))
        assert_equal(0, user.get_edit_count_of(None, False))
        assert_equal(0, user.get_edit_count_of(engelbert, True))
        assert_equal(0, user.get_edit_count_of(engelbert, False))

        # add edit
        db_st = DBDiscussionSession.query(Statement).get(1)
        db_tv = TextVersion('hello, here i am again', engelbert.uid, db_st.uid)
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        assert_equal(1, user.get_edit_count_of(engelbert, True))
        assert_equal(1, user.get_edit_count_of(engelbert, False))

        # set older timestamp
        db_tv.timestamp = DBDiscussionSession.query(TextVersion).get(1).timestamp
        DBDiscussionSession.add(db_tv)
        DBDiscussionSession.flush()
        transaction.commit()
        assert_equal(0, user.get_edit_count_of(engelbert, True))
        assert_equal(1, user.get_edit_count_of(engelbert, False))

    def test_get_count_of_votes_of_user(self):
        assert_equal((0, 0), user.get_mark_count_of(None, True))
        assert_equal((0, 0), user.get_mark_count_of(self.user, False))
        assert_equal((0, 0), user.get_mark_count_of(self.user, True))

    def test_get_count_of_clicks(self):
        assert_equal((0, 0), user.get_click_count_of(None, True))
        assert_equal((0, 0), user.get_click_count_of(self.user, False))
        assert_equal((0, 0), user.get_click_count_of(self.user, True))

        DBDiscussionSession.add(ClickedArgument(1, self.user.uid))
        DBDiscussionSession.add(ClickedStatement(1, self.user.uid))
        assert_equal((1, 1), user.get_click_count_of(self.user, False))
        assert_equal((1, 1), user.get_click_count_of(self.user, True))
        transaction.commit()

    def test_get_textversions(self):
        d = user.get_textversions(self.user, 'en')
        assert_greater_equal(0, len(d.get('statements', [])))
        assert_greater_equal(0, len(d.get('edits', [])))

    def test_get_marked_elements_of(self):
        prep_dict = user.get_marked_elements_of(self.user, False, 'en')
        assert_equal(0, len(prep_dict))
        assert_not_in('uid', prep_dict)

    def test_get_clicked_elements_of(self):
        prep_array = user.get_clicked_elements_of(self.user, True, 'en')
        assert_less_equal(0, len(prep_array))
        prep_array = user.get_clicked_elements_of(self.user, False, 'en')
        assert_less_equal(0, len(prep_array))

    def test_get_information_of(self):
        prep_dict = user.get_information_of(self.user, 'en')
        assert_in('public_nick', prep_dict)
        assert_in('last_action', prep_dict)
        assert_in('last_login', prep_dict)
        assert_in('registered', prep_dict)
        assert_in('group', prep_dict)
        assert_true(prep_dict['is_male'])
        assert_false(prep_dict['is_female'])
        assert_false(prep_dict['is_neutral'])

    def test_get_summary_of_today(self):
        prep_dict = user.get_summary_of_today('', 'en')
        assert_equal(len(prep_dict), 0)

        prep_dict = user.get_summary_of_today(self.user.nickname, 'en')
        assert_equal(self.user.nickname, prep_dict['firstname'])
        assert_less_equal(0, prep_dict['discussion_arg_clicks'])
        assert_less_equal(0, prep_dict['discussion_stat_clicks'])
        assert_less_equal(0, prep_dict['statements_posted'])
        assert_less_equal(0, prep_dict['edits_done'])

    def test_change_password(self):
        pascal = DBDiscussionSession.query(User).filter_by(nickname='Pascal').first()
        old_pw = 'iamatestuser2016'
        new_pw = 'iamatestuser2017'

        msg, success = user.change_password(pascal, old_pw, old_pw, old_pw, 'en')
        assert_false(success)

        msg, success = user.change_password(pascal, old_pw, old_pw, new_pw, 'en')
        assert_false(success)

        msg, success = user.change_password(pascal, old_pw, new_pw, old_pw, 'en')
        assert_false(success)

        msg, success = user.change_password(pascal, new_pw, new_pw, old_pw, 'en')
        assert_false(success)

        msg, success = user.change_password(pascal, new_pw, old_pw, old_pw, 'en')
        assert_false(success)

        msg, success = user.change_password(pascal, old_pw, new_pw, new_pw, 'en')
        assert_true(success)

        msg, success = user.change_password(pascal, new_pw, old_pw, old_pw, 'en')
        assert_true(success)

    def test_set_new_user(self):
        # TODO
        return True

    def test_set_new_oauth_user(self):
        # TODO
        return True

    def test_get_users_with_same_opinion(self):
        # TODO
        return True
