# Adaptee for the delete queue. Every deleted statement will just be disabled.
import transaction
from requests import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerDelete, ReviewDelete
from dbas.logger import logger
from dbas.review import rep_reason_success_flag, rep_reason_bad_flag, max_votes, min_difference
from dbas.review.lib import set_able_object_of_review
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import add_vote_for, add_reputation_and_check_review_access
from dbas.strings.translator import Translator


class DeleteQueue(QueueABC):
    def get_queue_information(self, db_user: User, session: Session, application_url: str, queue_name: str,
                              translator: Translator):
        pass

    def add_vote(self, db_user: User, db_review: ReviewDelete, is_okay: bool, main_page: str, translator: Translator,
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
        logger('DeleteQueue', 'main')
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        rep_reason = None

        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerDelete)

        # get all keep and delete votes
        count_of_delete, count_of_keep = self.get_review_count(db_review.uid)

        # do we reached any limit?
        reached_max = max(count_of_keep, count_of_delete) >= max_votes
        if reached_max:
            if count_of_delete > count_of_keep:  # disable the flagged part
                set_able_object_of_review(db_review, True)
                rep_reason = rep_reason_success_flag
            else:  # just close the review
                rep_reason = rep_reason_bad_flag
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_delete >= min_difference:  # just close the review
            rep_reason = rep_reason_bad_flag
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_delete - count_of_keep >= min_difference:  # disable the flagged part
            set_able_object_of_review(db_review, True)
            rep_reason = rep_reason_success_flag
            db_review.set_executed(True)
            db_review.update_timestamp()

        add_reputation_and_check_review_access(db_user_created_flag, rep_reason, main_page, translator)
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User):
        pass

    def revoke_ballot(self, db_user: User):
        pass
