# Adaptee for the delete queue. Every deleted statement will just be disabled.
import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerDelete, ReviewDelete, ReviewDeleteReason
from dbas.logger import logger
from dbas.review.lib import set_able_object_of_review, get_reputation_reason_by_action
from dbas.review.queue import max_votes, min_difference
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import add_vote_for, add_reputation_and_check_review_access, get_base_subpage_dict, \
    get_all_allowed_reviews_for_user, get_reporter_stats_for_review
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class DeleteQueue(QueueABC):
    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        """
        Setup the subpage for the delete queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        logger(DeleteQueue, 'main')
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_delete}', db_user, ReviewDelete,
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
        session[f'already_seen_{key_delete}'] = rev_dict['already_seen_reviews']

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

        :param db_user:
        :param db_review:
        :param is_okay:
        :param application_url:
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
                rep_reason = get_reputation_reason_by_action('success_flag')
            else:  # just close the review
                rep_reason = get_reputation_reason_by_action('bad_flag')
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_delete >= min_difference:  # just close the review
            rep_reason = get_reputation_reason_by_action('bad_flag')
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_delete - count_of_keep >= min_difference:  # disable the flagged part
            set_able_object_of_review(db_review, True)
            rep_reason = get_reputation_reason_by_action('success_flag')
            db_review.set_executed(True)
            db_review.update_timestamp()

        add_reputation_and_check_review_access(db_user_created_flag, rep_reason, application_url, translator)
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
