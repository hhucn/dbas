# Adaptee for the split queue.
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerSplit, ReviewSplit, ReviewSplitValues, Premise, Issue, \
    Statement, PremiseGroup, PremiseGroupSplitted, Argument, ArgumentsAddedByPremiseGroupSplit, \
    StatementReplacementsByPremiseGroupSplit
from dbas.handler.statements import set_statement
from dbas.logger import logger
from dbas.review import rep_reason_success_flag, rep_reason_bad_flag
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import min_difference, max_votes, add_vote_for, add_reputation_and_check_access_to_review
from dbas.strings.translator import Translator



class SplitQueue(QueueABC):
    def get_queue_information(self):
        pass

    def add_vote(self, db_user: User, db_review: ReviewSplit, is_okay: bool, main_page: str, translator: Translator,
                 **kwargs):
        """

        :param db_user:
        :param db_review:
        :param is_okay:
        :param main_page:
        :param translator:
        :param kwargs:
        :return:
        """
        logger('SplitQueue', 'main {}'.format(db_review.uid))
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        rep_reason = None

        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerSplit)

        # get all keep and delete votes
        count_of_split, count_of_keep = self.get_review_count(db_review.uid)

        # do we reached any limit?
        reached_max = max(count_of_split, count_of_keep) >= max_votes
        if reached_max:
            if count_of_split > count_of_keep:  # split pgroup
                self.__split_premisegroup(db_review)
                rep_reason = rep_reason_success_flag
            else:  # just close the review
                rep_reason = rep_reason_bad_flag
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_split >= min_difference:  # just close the review
            rep_reason = rep_reason_bad_flag
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_split - count_of_keep >= min_difference:  # split pgroup
            self.__split_premisegroup(db_review)
            rep_reason = rep_reason_success_flag
            db_review.set_executed(True)
            db_review.update_timestamp()

        add_reputation_and_check_access_to_review(db_user_created_flag, rep_reason, main_page, translator)
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    @staticmethod
    def __split_premisegroup(db_review: ReviewSplit):
        """
        Splits a premisegroup into the items, which are mapped with the given review

        :param db_review: ReviewSplit.uid
        :return: None
        """
        db_values = DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=db_review.uid).all()
        db_old_premises = DBDiscussionSession.query(Premise).filter_by(
            premisegroup_uid=db_review.premisegroup_uid).all()
        db_issue = DBDiscussionSession.query(Issue).get(db_old_premises[0].issue_uid)
        db_old_statement_ids = [p.statement_uid for p in db_old_premises]
        db_first_old_statement = DBDiscussionSession.query(Statement).get(db_old_premises[0].uid)
        db_user = DBDiscussionSession.query(User).get(db_review.detector_uid)

        if db_values:
            logger('SplitQueue', 'split given premisegroup into the mapped, new statements')
            db_statements = []
            for value in db_values:
                new_statement, tmp = set_statement(value.content, db_user, db_first_old_statement.is_position, db_issue)
                db_statements.append(new_statement)
        else:
            logger('SplitQueue', 'just split the premisegroup')
            db_statements = DBDiscussionSession.query(Statement).filter(Statement.uid.in_(db_old_statement_ids)).all()

        # new premisegroups, for each statement a new one
        new_premisegroup_ids = []
        new_premise_ids = []
        for statement in db_statements:
            db_new_premisegroup = PremiseGroup(author=db_user.uid)
            DBDiscussionSession.add(db_new_premisegroup)
            DBDiscussionSession.flush()
            new_premisegroup_ids.append(db_new_premisegroup.uid)

            db_new_premise = Premise(db_new_premisegroup.uid, statement.uid, False, db_user.uid, db_issue.uid)
            DBDiscussionSession.add(db_new_premise)
            DBDiscussionSession.flush()
            new_premise_ids.append(db_new_premise.uid)

            # note new added pgroup
            DBDiscussionSession.add(
                PremiseGroupSplitted(db_review.uid, db_review.premisegroup_uid, db_new_premisegroup.uid))

        # swap the premisegroup occurence in every argument and add new arguments for the new premises
        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_review.premisegroup_uid).all()
        for argument in db_arguments:
            argument.set_premisegroup(new_premisegroup_ids[0])
            DBDiscussionSession.add(argument)

            for uid in new_premisegroup_ids[1:]:
                argument = Argument(uid, argument.is_supportive, argument.author_uid, argument.issue_uid,
                                    argument.conclusion_uid, argument.argument_uid, argument.is_disabled)
                DBDiscussionSession.add(argument)
                DBDiscussionSession.flush()
                DBDiscussionSession.add(ArgumentsAddedByPremiseGroupSplit(db_review.uid, argument.uid))

        # swap the conclusion in every argument
        new_statements_uids = [s.uid for s in db_statements]
        for old_statement_uid in db_old_statement_ids:
            db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=old_statement_uid).all()
            for argument in db_arguments:
                argument.set_conclusion(new_statements_uids[0])
                DBDiscussionSession.add(argument)
                DBDiscussionSession.add(
                    StatementReplacementsByPremiseGroupSplit(db_review.uid, old_statement_uid, new_statements_uids[0]))
                DBDiscussionSession.flush()

                for statement_uid in new_statements_uids[1:]:
                    db_argument = Argument(argument.premisegroup_uid, argument.is_supportive, argument.author_uid,
                                           argument.issue_uid, statement_uid, argument.argument_uid,
                                           argument.is_disabled)
                    DBDiscussionSession.add(db_argument)
                    DBDiscussionSession.add(
                        StatementReplacementsByPremiseGroupSplit(db_review.uid, old_statement_uid, statement_uid))
                    DBDiscussionSession.flush()

        # finish
        DBDiscussionSession.flush()
        transaction.commit()

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(should_split=True).count()
        count_of_not_okay = db_reviews.filter_by(should_split=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User):
        pass

    def revoke_ballot(self, db_user: User):
        pass
