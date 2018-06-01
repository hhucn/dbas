# Adaptee for the edit queue. Every edit results in a new textversion of a statement.
import difflib

import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerEdit, ReviewEdit, ReviewEditValue
from dbas.handler.statements import correct_statement
from dbas.logger import logger
from dbas.review import rep_reason_success_edit, rep_reason_bad_edit, max_votes, min_difference
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import add_vote_for, add_reputation_and_check_review_access, \
    get_all_allowed_reviews_for_user, get_base_subpage_dict, get_reporter_stats_for_review
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class EditQueue(QueueABC):
    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        logger('ReviewSubpagerHelper', 'main')
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{key_edit}', db_user, ReviewEdit,
                                                        LastReviewerEdit)

        rev_dict = get_base_subpage_dict(ReviewEdit, all_rev_dict['reviews'], all_rev_dict['already_seen_reviews'],
                                         all_rev_dict['first_time'], db_user, all_rev_dict['already_voted_reviews'])
        if not rev_dict['rnd_review']:
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None,
                'session': session
            }

        reason = translator.get(_.argumentFlaggedBecauseEdit)

        # build correction
        db_edit_value = DBDiscussionSession.query(ReviewEditValue).filter_by(
            review_edit_uid=rev_dict['rnd_review'].uid).first()
        stats = get_reporter_stats_for_review(rev_dict['rnd_review'], translator.get_lang(), application_url)

        if not db_edit_value:
            rnd_review = rev_dict['rnd_review']
            logger('ReviewSubpagerHelper', f'ReviewEdit {rnd_review.uid} has no edit value!', error=True)
            # get all valid reviews
            db_allowed_reviews = DBDiscussionSession.query(ReviewEdit).filter(
                ReviewEdit.uid.in_(DBDiscussionSession.query(ReviewEditValue.review_edit_uid))).all()

            if len(db_allowed_reviews) > 0:  # get new one
                return self.get_queue_information(db_user, session, application_url, application_url, translator)
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue_titles': None,
                'extra_info': None,
                'session': session
            }

        correction_list = [char for char in rev_dict['text']]
        self.__difference_between_string(rev_dict['text'], db_edit_value.content, correction_list)
        correction = ''.join(correction_list)

        rev_dict[f'already_seen_{key_edit}'].append(not rev_dict['rnd_review'].uid)
        session[f'already_seen_{key_edit}'] = rev_dict[f'already_seen_{key_edit}']

        return {
            'stats': stats,
            'text': rev_dict['text'],
            'corrected_version': db_edit_value.content,
            'corrections': correction,
            'reason': reason,
            'issue_titles': rev_dict['issue_titles'],
            'extra_info': rev_dict['extra_info'],  # TODO KILL
            'session': session
        }

    @staticmethod
    def __difference_between_string(a: str, b: str, correction_list: list(str)):
        """
        Colors the difference between two strings

        :param a: first string
        :param b: second string
        :param correction_list: character list of the first string
        :return: modified correction list with html strings around the modified characters
        """
        base = '<strong><span class="text-{}">'
        tag_p = base.format('success')
        tag_m = base.format('danger')
        tag_e = '</span></strong>'

        for i, s in enumerate(difflib.ndiff(a, b)):
            if i >= len(correction_list):
                correction_list.append('')
            if s[0] == ' ':
                correction_list[i] = s[-1]
                continue
            elif s[0] == '-':
                correction_list[i] = tag_m + s[-1] + tag_e
            elif s[0] == '+':
                correction_list[i] = tag_p + s[-1] + tag_e

    def add_vote(self, db_user: User, db_review: ReviewEdit, is_okay: bool, application_url: str,
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

        add_reputation_and_check_review_access(db_user_created_flag, rep_reason, application_url, translator)
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
