# Adaptee for the edit queue. Every edit results in a new textversion of a statement.
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerEdit, ReviewEdit, ReviewEditValue
from dbas.handler.statements import correct_statement
from dbas.logger import logger
from dbas.review import rep_reason_success_edit, rep_reason_bad_edit
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import min_difference, max_votes, add_vote_for, add_reputation_and_check_access_to_review
from dbas.strings.translator import Translator





class EditQueue(QueueABC):
    def get_queue_information(self):
        pass

    def add_vote(self, db_user: User, db_review: ReviewEdit, is_okay: bool, main_page: str, translator: Translator,
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
        logger('EditQueue', 'main')
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        rep_reason = None

        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerEdit)

        # get all keep and delete votes
        count_of_edit, count_of_dont_edit = self.get_review_count(db_review.uid)

        # do we reached any limit?
        reached_max = max(count_of_edit, count_of_dont_edit) >= max_votes
        if reached_max:
            if count_of_dont_edit < count_of_edit:  # accept the edit
                self.__accept_edit_review(db_review)
                rep_reason = rep_reason_success_edit
            else:  # just close the review
                rep_reason = rep_reason_bad_edit
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_edit - count_of_dont_edit >= min_difference:  # accept the edit
            self.__accept_edit_review(db_review)
            rep_reason = rep_reason_success_edit
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_dont_edit - count_of_edit >= min_difference:  # decline edit
            rep_reason = rep_reason_bad_edit
            db_review.set_executed(True)
            db_review.update_timestamp()

        add_reputation_and_check_access_to_review(db_user_created_flag, rep_reason, main_page, translator)
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    @staticmethod
    def __accept_edit_review(db_review: ReviewEdit):
        """
        Add correction for each value affected by the review

        :param db_review: Review
        :return: None
        """
        db_values = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid).all()
        db_user = DBDiscussionSession.query(User).get(db_review.detector_uid)
        for value in db_values:
            correct_statement(db_user, value.statement_uid, value.content)

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User):
        pass

    def revoke_ballot(self, db_user: User):
        pass
