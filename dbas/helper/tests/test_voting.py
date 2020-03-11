import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ClickedArgument, ClickedStatement, SeenStatement, SeenArgument, \
    Statement, Argument
from dbas.handler.voting import add_seen_argument, add_seen_statement, add_click_for_argument, add_click_for_statement
from dbas.tests.utils import TestCaseWithConfig


class VotingHelperTest(TestCaseWithConfig):
    def test_add_seen_argument(self):
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        val = add_seen_argument([], 1100)
        self.assertFalse(val)

        val = add_seen_argument([], self.user_christian)
        self.assertFalse(val)

        val = add_seen_argument([0], self.user_christian)
        self.assertFalse(val)

        val = add_seen_argument([1], self.user_christian)
        self.assertFalse(val)

        val = add_seen_argument(None, self.user_christian)
        self.assertFalse(val)

        val = add_seen_argument('a', self.user_christian)
        self.assertFalse(val)

        val = add_seen_argument(1, 1100)
        self.assertFalse(val)

        val = add_seen_argument(0, 1)
        self.assertFalse(val)

        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        val = add_seen_argument(1, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 2, 1)

        val = add_seen_argument(2, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 3, 2)

        val = add_seen_argument(2, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 3, 2)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

    def test_add_seen_statement_anonymous_user_is_not_tracked(self):
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        db_anon = DBDiscussionSession.query(User).get(1)

        val = add_seen_statement(1, db_anon)
        self.assertFalse(val)

    def test_add_seen_statement(self):
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        val = add_seen_statement(self.first_position_cat_or_dog, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 1, 0)

        val = add_seen_statement(self.second_position_cat_or_dog, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 2, 0)

        val = add_seen_statement(self.second_position_cat_or_dog, self.user_christian)
        self.assertFalse(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 2, 0)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

    def test_add_vote_for_argument(self):
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        db_arg_1 = DBDiscussionSession.query(Argument).get(1)
        db_arg_2 = DBDiscussionSession.query(Argument).get(2)
        db_arg_18 = DBDiscussionSession.query(Argument).get(18)

        val = add_click_for_argument(db_arg_1, DBDiscussionSession.query(User).get(1))
        self.assertFalse(val)

        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        val = add_click_for_argument(db_arg_1, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 2, 1, 0, 1)

        # double it
        for i in range(0, 2):
            val = add_click_for_argument(db_arg_2, self.user_christian)
            self.assertTrue(val)
            self.check_tables_of_user_for_n_rows(self.user_christian, 4, 2, 0, 2)

            db_votes_arg_pro = DBDiscussionSession.query(ClickedArgument).filter(
                ClickedArgument.author_uid == self.user_christian.uid, ClickedArgument.is_up_vote == True).all()
            db_votes_arg_con = DBDiscussionSession.query(ClickedArgument).filter(
                ClickedArgument.author_uid == self.user_christian.uid, ClickedArgument.is_up_vote == False).all()
            db_votes_sta_pro = DBDiscussionSession.query(ClickedStatement).filter(
                ClickedStatement.author_uid == self.user_christian.uid, ClickedStatement.is_up_vote == True).all()
            db_votes_sta_con = DBDiscussionSession.query(ClickedStatement).filter(
                ClickedStatement.author_uid == self.user_christian.uid, ClickedStatement.is_up_vote == False).all()
            self.assertEquals(2, len(db_votes_arg_pro))
            self.assertEquals(0, len(db_votes_arg_con))
            self.assertEquals(3, len(db_votes_sta_pro))
            self.assertEquals(1, len(db_votes_sta_con))

        # vote for undercut
        val = add_click_for_argument(db_arg_18, self.user_christian)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 5, 4, 0, 3)

        db_votes_arg_pro = DBDiscussionSession.query(ClickedArgument).filter(
            ClickedArgument.author_uid == self.user_christian.uid, ClickedArgument.is_up_vote == True).all()
        db_votes_arg_con = DBDiscussionSession.query(ClickedArgument).filter(
            ClickedArgument.author_uid == self.user_christian.uid, ClickedArgument.is_up_vote == False).all()
        db_votes_arg_val = DBDiscussionSession.query(ClickedArgument).filter(
            ClickedArgument.author_uid == self.user_christian.uid, ClickedArgument.is_valid == True).all()
        db_votes_arg_nva = DBDiscussionSession.query(ClickedArgument).filter(
            ClickedArgument.author_uid == self.user_christian.uid, ClickedArgument.is_valid == False).all()
        db_votes_sta_pro = DBDiscussionSession.query(ClickedStatement).filter(
            ClickedStatement.author_uid == self.user_christian.uid, ClickedStatement.is_up_vote == True).all()
        db_votes_sta_con = DBDiscussionSession.query(ClickedStatement).filter(
            ClickedStatement.author_uid == self.user_christian.uid, ClickedStatement.is_up_vote == False).all()
        self.assertEquals(3, len(db_votes_arg_pro))
        self.assertEquals(1, len(db_votes_arg_con))
        self.assertEquals(4, len(db_votes_sta_pro))
        self.assertEquals(1, len(db_votes_sta_con))
        self.assertEquals(2, len(db_votes_arg_val))
        self.assertEquals(2, len(db_votes_arg_nva))

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

    def test_add_vote_for_statement(self):
        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

        db_stmt_1 = DBDiscussionSession.query(Statement).get(1)
        db_stmt_2 = DBDiscussionSession.query(Statement).get(2)

        val = add_click_for_statement(db_stmt_1, self.user_christian, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 1, 0, 1, 0)

        val = add_click_for_statement(db_stmt_2, self.user_christian, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 2, 0, 2, 0)

        # duplicate
        val = add_click_for_statement(db_stmt_2, self.user_christian, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 2, 0, 2, 0)

        # opinion change
        val = add_click_for_statement(db_stmt_2, self.user_christian, False)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 3, 0, 2, 0)

        # duplicate
        val = add_click_for_statement(db_stmt_2, self.user_christian, False)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 3, 0, 2, 0)

        # opinion change
        val = add_click_for_statement(db_stmt_2, self.user_christian, True)
        self.assertTrue(val)
        self.check_tables_of_user_for_n_rows(self.user_christian, 4, 0, 2, 0)

        self.clear_every_vote()
        self.check_tables_of_user_for_n_rows(self.user_christian, 0, 0, 0, 0)

    def check_tables_of_user_for_n_rows(self, user: User, count_of_vote_statement, count_of_vote_argument,
                                        count_of_seen_statements, count_of_seen_arguments):
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
        db_seen_statements = DBDiscussionSession.query(SeenStatement).filter_by(user=user).all()
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
