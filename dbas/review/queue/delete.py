# Adaptee for the delete queue. Every deleted statement will just be disabled.
import logging
from typing import Tuple, Optional

import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerDelete, ReviewDelete, ReviewDeleteReason, ReviewCanceled, \
    Statement
from dbas.lib import get_text_for_argument_uid
from dbas.review import FlaggedBy
from dbas.review.queue import max_votes, min_difference, key_delete
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import get_base_subpage_dict, \
    get_all_allowed_reviews_for_user, get_reporter_stats_for_review, set_able_object_of_review, \
    revoke_decision_and_implications, add_vote_for, get_user_dict_for_review
from dbas.review.reputation import get_reason_by_action, ReputationReasons, \
    add_reputation_and_send_popup
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


class DeleteQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_delete

    def key(self, key=None):
        """
        Getter/setter for the key of the queue which is just the name

        :param key:
        :return:
        """
        if not key:
            return self.key
        else:
            self.key = key

    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        """
        Setup the subpage for the delete queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        LOG.debug("Entering setup for subpage of deletion queue")
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{self.key}', db_user, ReviewDelete,
                                                        LastReviewerDelete)

        rev_dict = get_base_subpage_dict(ReviewDelete, all_rev_dict['reviews'], all_rev_dict['already_seen_reviews'],
                                         all_rev_dict['first_time'], db_user, all_rev_dict['already_voted_reviews'])
        if not rev_dict['rnd_review']:
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue_titles': None,
                'extra_info': None,
                'session': session
            }

        db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(rev_dict['rnd_review'].reason_uid)
        stats = get_reporter_stats_for_review(rev_dict['rnd_review'], translator.get_lang(), application_url)

        reason = ''
        if db_reason.reason == 'offtopic':
            reason = translator.get(_.argumentFlaggedBecauseOfftopic)
        if db_reason.reason == 'spam':
            reason = translator.get(_.argumentFlaggedBecauseSpam)
        if db_reason.reason == 'harmful':
            reason = translator.get(_.argumentFlaggedBecauseHarmful)

        rev_dict['already_seen_reviews'].append(rev_dict['rnd_review'].uid)
        session[f'already_seen_{self.key}'] = rev_dict['already_seen_reviews']

        return {
            'stats': stats,
            'text': rev_dict['text'],
            'reason': reason,
            'issue_titles': rev_dict['issue_titles'],
            'extra_info': rev_dict['extra_info'],
            'session': session
        }

    def add_vote(self, db_user: User, db_review: ReviewDelete, is_okay: bool, application_url: str,
                 translator: Translator,
                 **kwargs):
        """
        Adds an vote for this queue. If any (positive or negative) limit is reached, the flagged element will be
        disabled

        :param db_user: current user who votes
        :param db_review: the review, which is voted vor
        :param is_okay: True, if the element is rightly flagged
        :param application_url: the app url
        :param translator: a instance of a translator
        :param kwargs: optional, keyworded arguments
        :return:
        """
        LOG.debug("Entering function to add a vote for review with id %s", db_review.uid)
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
                rep_reason = get_reason_by_action(ReputationReasons.success_flag)
            else:  # just close the review
                rep_reason = get_reason_by_action(ReputationReasons.bad_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_delete >= min_difference:  # just close the review
            rep_reason = get_reason_by_action(ReputationReasons.bad_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_delete - count_of_keep >= min_difference:  # disable the flagged part
            set_able_object_of_review(db_review, True)
            rep_reason = get_reason_by_action(ReputationReasons.success_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        if rep_reason:
            add_reputation_and_send_popup(db_user_created_flag, rep_reason, application_url, translator)
            DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    def add_review(self, db_user: User):
        """
        Just adds a new element

        :param db_user: current user
        :return:
        """
        pass

    def get_review_count(self, review_uid: int) -> Tuple[int, int]:
        """
        Returns total pro and con count for the given review.uid

        :param review_uid: Review.uid
        :return:
        """
        db_reviews = DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User, db_review: ReviewDelete):
        """
        Cancels any ongoing vote

        :param db_user: current user
        :param db_review: any element from a review queue
        :return:
        """
        DBDiscussionSession.query(ReviewDelete).get(db_review.uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_delete: db_review.uid},
                                            was_ongoing=True)

        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def revoke_ballot(self, db_user: User, db_review: ReviewDelete):
        """
        Revokes/Undo the implications of any successfull reviewed element

        :param db_user:
        :param db_review:
        :return:
        """
        revoke_decision_and_implications(ReviewDelete, LastReviewerDelete, db_review.uid)
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_delete: db_review.uid})
        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def element_in_queue(self, db_user: User, **kwargs) -> Optional[FlaggedBy]:
        """
        Check if the element described by kwargs is in any queue. Return a FlaggedBy object or none

        :param db_user: current user
        :param kwargs: "magic" -> atm keywords like argument_uid, statement_uid and premisegroup_uid.
        Please update this!
        """
        db_review = DBDiscussionSession.query(ReviewDelete).filter_by(
            argument_uid=kwargs.get('argument_uid'),
            statement_uid=kwargs.get('statement_uid'),
            is_executed=False,
            is_revoked=False)
        if db_review.filter_by(detector_uid=db_user.uid).count() > 0:
            return FlaggedBy.user
        if db_review.count() > 0:
            return FlaggedBy.other
        return None

    def get_history_table_row(self, db_review: ReviewDelete, entry, **kwargs):
        """
        Returns a row the the history/ongoing page for the given review element

        :param db_review: current review element
        :param entry: dictionary with some values which were already set
        :param kwargs: "magic" -> atm keywords like is_executed, short_text and full_text. Please update this!
        :return:
        """
        db_reason = DBDiscussionSession.query(ReviewDeleteReason).get(db_review.reason_uid)
        entry['reason'] = db_reason.reason
        return entry

    def get_text_of_element(self, db_review: ReviewDelete) -> str:
        """
        Returns full text of the given element

        :param db_review: current review element
        :return:
        """
        if db_review.statement_uid is None:
            return get_text_for_argument_uid(db_review.argument.uid)
        else:
            return DBDiscussionSession.query(Statement).get(db_review.statement_uid).get_text()

    def get_all_votes_for(self, db_review: ReviewDelete, application_url: str) -> Tuple[list, list]:
        """
        Reeturns all pro and con votes for the given element

        :param db_review: current review element
        :param application_url: The corresponding application URL
        :return:
        """
        db_all_votes = DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid)
        pro_votes = db_all_votes.filter_by(is_okay=True).all()
        con_votes = db_all_votes.filter_by(is_okay=False).all()

        pro_list = [get_user_dict_for_review(pro.reviewer_uid, application_url) for pro in pro_votes]
        con_list = [get_user_dict_for_review(con.reviewer_uid, application_url) for con in con_votes]

        return pro_list, con_list
