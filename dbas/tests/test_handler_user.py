import transaction
import unittest
import arrow
from datetime import date, timedelta

from pyramid import testing

from nose.tools import assert_false, assert_true, assert_not_equal, assert_in, assert_not_in, assert_less, assert_equal, \
    assert_greater_equal
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Settings, TextVersion, ClickedArgument, ClickedStatement, ReviewEdit
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

    def test_get_count_of_statements(self):
        kurt = DBDiscussionSession.query(User).filter_by(nickname='Engelbert').first()
        assert_greater_equal(user.get_count_of_statements(None, True, False), 0)
        assert_greater_equal(user.get_count_of_statements(kurt, False, False), 0)
        assert_greater_equal(user.get_count_of_statements(kurt, True, False), 0)
        assert_greater_equal(user.get_count_of_statements(kurt, False, True), 0)
        assert_greater_equal(user.get_count_of_statements(kurt, True, True), 0)

        tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=1).first()
        tv.author_uid = self.user.uid
        DBDiscussionSession.add(tv)
        DBDiscussionSession.add(TextVersion(content=tv.content + '-', author=self.user.uid, statement_uid=1))
        transaction.commit()
        a = user.get_count_of_statements(self.user, False, True)
        b = user.get_count_of_statements(self.user, True, True)
        assert_less(b, a)

    def test_get_count_of_votes_of_user(self):
        assert_equal(user.get_count_of_votes_of_user(None, True), (0, 0))
        assert_equal(user.get_count_of_votes_of_user(self.user, False), (0, 0))
        assert_equal(user.get_count_of_votes_of_user(self.user, True), (0, 0))

    def test_get_count_of_clicks(self):
        assert_equal(user.get_count_of_clicks(None, True), (0, 0))
        assert_equal(user.get_count_of_clicks(self.user, False), (0, 0))
        assert_equal(user.get_count_of_clicks(self.user, True), (0, 0))

        DBDiscussionSession.add(ClickedArgument(1, self.user.uid))
        DBDiscussionSession.add(ClickedStatement(1, self.user.uid))
        assert_equal(user.get_count_of_clicks(self.user, False), (1, 1))
        assert_equal(user.get_count_of_clicks(self.user, True), (1, 1))
        transaction.commit()

    def test_get_textversions(self):

        d = user.get_textversions(self.user, 'en')
        assert_greater_equal(len(d.get('statements', [])), 0)
        assert_greater_equal(len(d.get('edits', [])), 0)

    def test_get_marked_elements_of_user(self):
        prep_dict = user.get_marked_elements_of_user(self.user, False, 'en')
        assert_equal(len(prep_dict), 0)
        assert_not_in('uid', prep_dict)

    def test_get_arg_clicks_of_user(self):
        prep_array = user.get_clicked_element_of_user(self.user, True, 'en')
        assert_greater_equal(len(prep_array), 0)

    def test_get_stmt_clicks_of_user(self):
        prep_array = user.get_clicked_element_of_user(self.user, False, 'en')
        assert_greater_equal(len(prep_array), 0)

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

        prep_dict = user.get_summary_of_today('Tobias', 'en')
        assert_equal(prep_dict['firstname'], self.user.firstname)
        assert_equal(prep_dict['discussion_arg_clicks'], 1)
        assert_equal(prep_dict['discussion_stat_clicks'], 1)
        assert_equal(prep_dict['statements_posted'], 2)
        assert_equal(prep_dict['edits_done'], 1)

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
