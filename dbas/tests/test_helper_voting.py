import unittest

import transaction
from pyramid import testing
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ClickedArgument, ClickedStatement, SeenStatement, SeenArgument
from dbas.helper.voting import add_seen_argument, add_seen_statement, add_click_for_argument, add_click_for_statement


class VotingHelperTest(unittest.TestCase):

    def setUp(self):
        """

        :return:
        """
        self.config = testing.setUp()
        self.user = DBDiscussionSession.query(User).get(3)

    def tearDown(self):
        """

        :return:
        """
        testing.tearDown()

    def test_add_seen_argument(self):
        """

        :return:
        """
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_seen_argument([], 1100)
        self.assertFalse(val)

        val = add_seen_argument([], self.user)
        self.assertFalse(val)

        val = add_seen_argument([0], self.user)
        self.assertFalse(val)

        val = add_seen_argument([1], self.user)
        self.assertFalse(val)

        val = add_seen_argument(None, self.user)
        self.assertFalse(val)

        val = add_seen_argument('a', self.user)
        self.assertFalse(val)

        val = add_seen_argument(1, 1100)
        self.assertFalse(val)

        val = add_seen_argument(0, 1)
        self.assertFalse(val)

        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_seen_argument(1, self.user)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 2, 1)

        val = add_seen_argument(2, self.user)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 3, 2)

        val = add_seen_argument(2, self.user)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 3, 2)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

    def test_add_seen_statement(self):
        """

        :return:
        """
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        db_user = DBDiscussionSession.query(User).get(1100)
        val = add_seen_statement([], db_user)
        self.assertFalse(val)

        val = add_seen_statement([], self.user)
        self.assertFalse(val)

        val = add_seen_statement([0], self.user)
        self.assertFalse(val)

        val = add_seen_statement([1], self.user)
        self.assertFalse(val)

        val = add_seen_statement(None, self.user)
        self.assertFalse(val)

        val = add_seen_statement('a', self.user)
        self.assertFalse(val)

        val = add_seen_statement(1, db_user)
        self.assertFalse(val)

        db_user = DBDiscussionSession.query(User).get(1)
        val = add_seen_statement(0, 1)
        self.assertFalse(val)

        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_seen_statement(1, self.user)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 1, 0)

        val = add_seen_statement(2, self.user)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 2, 0)

        val = add_seen_statement(2, self.user)
        self.assertFalse(val)
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 2, 0)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

    def test_add_vote_for_argument(self):
        """

        :return:
        """
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_click_for_argument([], 1100)
        self.assertFalse(val)

        val = add_click_for_argument([], self.user.nickname)
        self.assertFalse(val)

        val = add_click_for_argument([0], self.user.nickname)
        self.assertFalse(val)

        val = add_click_for_argument([1], self.user.nickname)
        self.assertFalse(val)

        val = add_click_for_argument(None, self.user.nickname)
        self.assertFalse(val)

        val = add_click_for_argument('a', self.user.nickname)
        self.assertFalse(val)

        val = add_click_for_argument(1, self.user.nickname + '#')
        self.assertFalse(val)

        val = add_click_for_argument(0, 1)
        self.assertFalse(val)

        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_click_for_argument(1, self.user.nickname)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 2, 1, 0, 1)

        val = add_click_for_argument(2, self.user.nickname)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 4, 2, 0, 2)

        db_votes_arg_pro = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_up_vote == True)).all()
        db_votes_arg_con = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_up_vote == False)).all()
        db_votes_sta_pro = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == self.user.uid, ClickedStatement.is_up_vote == True)).all()
        db_votes_sta_con = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == self.user.uid, ClickedStatement.is_up_vote == False)).all()
        self.assertEquals(len(db_votes_arg_pro), 2)
        self.assertEquals(len(db_votes_arg_con), 0)
        self.assertEquals(len(db_votes_sta_pro), 3)
        self.assertEquals(len(db_votes_sta_con), 1)

        # double
        val = add_click_for_argument(2, self.user.nickname)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 4, 2, 0, 2)

        db_votes_arg_pro = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_up_vote == True)).all()
        db_votes_arg_con = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_up_vote == False)).all()
        db_votes_sta_pro = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == self.user.uid, ClickedStatement.is_up_vote == True)).all()
        db_votes_sta_con = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == self.user.uid, ClickedStatement.is_up_vote == False)).all()
        self.assertEquals(len(db_votes_arg_pro), 2)
        self.assertEquals(len(db_votes_arg_con), 0)
        self.assertEquals(len(db_votes_sta_pro), 3)
        self.assertEquals(len(db_votes_sta_con), 1)

        # vote for undercut
        val = add_click_for_argument(18, self.user.nickname)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 5, 4, 0, 3)

        db_votes_arg_pro = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_up_vote == True)).all()
        db_votes_arg_con = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_up_vote == False)).all()
        db_votes_arg_val = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_valid == True)).all()
        db_votes_arg_nva = DBDiscussionSession.query(ClickedArgument).filter(and_(ClickedArgument.author_uid == self.user.uid, ClickedArgument.is_valid == False)).all()
        db_votes_sta_pro = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == self.user.uid, ClickedStatement.is_up_vote == True)).all()
        db_votes_sta_con = DBDiscussionSession.query(ClickedStatement).filter(and_(ClickedStatement.author_uid == self.user.uid, ClickedStatement.is_up_vote == False)).all()
        self.assertEquals(len(db_votes_arg_pro), 3)
        self.assertEquals(len(db_votes_arg_con), 1)
        self.assertEquals(len(db_votes_sta_pro), 4)
        self.assertEquals(len(db_votes_sta_con), 1)
        self.assertEquals(len(db_votes_arg_val), 2)
        self.assertEquals(len(db_votes_arg_nva), 2)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

    def test_add_vote_for_statement(self):
        """

        :return:
        """
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_click_for_statement([], 1100, True)
        self.assertFalse(val)

        val = add_click_for_statement([], self.user.nickname, True)
        self.assertFalse(val)

        val = add_click_for_statement([0], self.user.nickname, True)
        self.assertFalse(val)

        val = add_click_for_statement([1], self.user.nickname, True)
        self.assertFalse(val)

        val = add_click_for_statement(None, self.user.nickname, True)
        self.assertFalse(val)

        val = add_click_for_statement('a', self.user.nickname, True)
        self.assertFalse(val)

        val = add_click_for_statement(1, self.user.nickname + '#', True)
        self.assertFalse(val)

        val = add_click_for_statement(0, 1, True)
        self.assertFalse(val)

        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

        val = add_click_for_statement(1, self.user.nickname, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 1, 0, 1, 0)

        val = add_click_for_statement(2, self.user.nickname, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 2, 0, 2, 0)

        # duplicate
        val = add_click_for_statement(2, self.user.nickname, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 2, 0, 2, 0)

        # opinion change
        val = add_click_for_statement(2, self.user.nickname, False)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 3, 0, 2, 0)

        # duplicate
        val = add_click_for_statement(2, self.user.nickname, False)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 3, 0, 2, 0)

        # opinion change
        val = add_click_for_statement(2, self.user.nickname, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user, 4, 0, 2, 0)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user, 0, 0, 0, 0)

    def check_tables_of_user_for_n_rows(self, user, count_of_vote_statement, count_of_vote_argument, count_of_seen_statements, count_of_seen_arguments):
        """

        :param user:
        :param count_of_vote_argument:
        :param count_of_vote_statement:
        :param count_of_seen_statements:
        :param count_of_seen_arguments:
        :return:
        """
        db_vote_argument = DBDiscussionSession.query(ClickedArgument).filter_by(author_uid=user.uid).all()
        db_vote_statement = DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=user.uid).all()
        db_seen_statements = DBDiscussionSession.query(SeenStatement).filter_by(user_uid=user.uid).all()
        db_seen_arguments = DBDiscussionSession.query(SeenArgument).filter_by(user_uid=user.uid).all()
        self.assertEquals(len(db_vote_statement), count_of_vote_statement)
        self.assertEquals(len(db_vote_argument), count_of_vote_argument)
        self.assertEquals(len(db_seen_statements), count_of_seen_statements)
        self.assertEquals(len(db_seen_arguments), count_of_seen_arguments)

    def clear_every_vote(self):
        DBDiscussionSession.query(ClickedArgument).delete()
        DBDiscussionSession.query(ClickedStatement).delete()
        DBDiscussionSession.query(SeenStatement).delete()
        DBDiscussionSession.query(SeenArgument).delete()
        DBDiscussionSession.flush()
        transaction.commit()
