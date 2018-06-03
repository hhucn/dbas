# Adaptee for the edit queue. Every edit results in a new textversion of a statement.
import difflib
from typing import List

import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerEdit, ReviewEdit, ReviewEditValue, TextVersion, \
    ReviewCanceled, Statement, Argument, Premise
from dbas.handler.textversion import propose_new_textversion_for_statement
from dbas.logger import logger
from dbas.review.queue import max_votes, min_difference, key_edit, Code
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import get_all_allowed_reviews_for_user, get_base_subpage_dict, \
    get_reporter_stats_for_review
from dbas.review.queues import add_vote_for
from dbas.review.reputation import get_reason_by_action, add_reputation_and_check_review_access, ReputationReasons
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class EditQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_edit

    def key(self, key=None):
        """

        :param key:
        :return:
        """
        if not key:
            return key
        else:
            self.key = key

    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        """
        Setup the subpage for the edit queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        logger('EditQueue', 'main')
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{self.key}', db_user, ReviewEdit,
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
            logger('EditQueue', f'ReviewEdit {rnd_review.uid} has no edit value!', error=True)
            # get all valid reviews
            db_allowed_reviews = DBDiscussionSession.query(ReviewEdit).filter(
                ReviewEdit.uid.in_(DBDiscussionSession.query(ReviewEditValue.review_edit_uid))).all()

            if len(db_allowed_reviews) > 0:  # get new one
                return self.get_queue_information(db_user, session, application_url, translator)
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

        rev_dict[f'already_seen_reviews'].append(not rev_dict['rnd_review'].uid)
        session[f'already_seen_{self.key}'] = rev_dict[f'already_seen_reviews']

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
    def __difference_between_string(a: str, b: str, correction_list: List[str]):
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
                rep_reason = get_reason_by_action(ReputationReasons.success_edit)
            else:  # just close the review
                rep_reason = get_reason_by_action(ReputationReasons.bad_edit)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_edit - count_of_dont_edit >= min_difference:  # accept the edit
            self.__accept_edit_review(db_review)
            rep_reason = get_reason_by_action(ReputationReasons.success_edit)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_dont_edit - count_of_edit >= min_difference:  # decline edit
            rep_reason = get_reason_by_action(ReputationReasons.bad_edit)
            db_review.set_executed(True)
            db_review.update_timestamp()

        if rep_reason:
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
            propose_new_textversion_for_statement(db_user, value.statement_uid, value.content)

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        """

        :param review_uid:
        :return:
        """
        db_reviews = DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User, db_review: ReviewEdit):
        """

        :param db_user:
        :param db_review:
        :return:
        """
        DBDiscussionSession.query(ReviewEdit).filter_by(uid=db_review.uid).delete()
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).first().set_revoked(True)
        DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_edit: db_review.uid}, was_ongoing=True)

        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()

    def revoke_ballot(self, db_user: User, db_review: ReviewEdit):
        """

        :param db_user:
        :param db_review:
        :return:
        """
        db_review = DBDiscussionSession.query(ReviewEdit).get(db_review.uid)
        db_review.set_revoked(True)
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).delete()
        db_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid)
        content = db_value.first().content
        db_value.delete()
        # delete forbidden textversion
        DBDiscussionSession.query(TextVersion).filter_by(content=content).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_edit: db_review.uid})
        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()

    def add_edit_reviews(self, db_user: User, uid: int, text: str):
        """
        Setup a new ReviewEdit row

        :param db_user: User
        :param uid: Statement.uid
        :param text: New content for statement
        :return: -1 if the statement of the element does not exists, -2 if this edit already exists, 1 on success, 0 otherwise
        """
        db_statement = DBDiscussionSession.query(Statement).get(uid)
        if not db_statement:
            logger('review.lib', f'statement {uid} not found (return {Code.DOESNT_EXISTS})')
            return Code.DOESNT_EXISTS

        # already set an correction for this?
        if self.is_statement_in_edit_queue(uid):  # if we already have an edit, skip this
            logger('review.lib', f'statement {uid} already got an edit (return {Code.DUPLICATE})')
            return Code.DUPLICATE

        # is text different?
        db_tv = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)
        if len(text) > 0 and db_tv.content.lower().strip() != text.lower().strip():
            logger('review.lib', f'added review element for {uid} (return {Code.SUCCESS})')
            DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, statement=uid))
            return Code.SUCCESS

        logger('review.lib', f'no case for {uid} (return {Code.ERROR})')
        return Code.ERROR

    @staticmethod
    def add_edit_values_review(db_user: User, uid: int, text: str):
        """
        Setup a new ReviewEditValue row

        :param db_user: User
        :param uid: Statement.uid
        :param text: New content for statement
        :return: 1 on success, 0 otherwise
        """
        db_statement = DBDiscussionSession.query(Statement).get(uid)
        if not db_statement:
            logger('review.lib', f'{uid} not found')
            return Code.ERROR

        db_textversion = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)

        if len(text) > 0 and db_textversion.content.lower().strip() != text.lower().strip():
            db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.detector_uid == db_user.uid,
                                                                          ReviewEdit.statement_uid == uid).order_by(
                ReviewEdit.uid.desc()).first()
            DBDiscussionSession.add(ReviewEditValue(db_review_edit.uid, uid, 'statement', text))
            logger('review.lib', f'{uid} - \'{text}\' accepted')
            return Code.SUCCESS

        logger('review.lib', f'{uid} - \'{text}\' malicious edit')
        return Code.ERROR

    @staticmethod
    def is_statement_in_edit_queue(uid: int, is_executed: bool = False) -> bool:
        """
        Returns true if the statement is not in the edit queue

        :param uid: Statement.uid
        :param is_executed: Bool
        :return: Boolean
        """
        db_already_edit_count = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.statement_uid == uid,
                                                                             ReviewEdit.is_executed == is_executed).count()
        return db_already_edit_count > 0

    @staticmethod
    def is_arguments_premise_in_edit_queue(db_argument: Argument, is_executed: bool = False) -> bool:
        """
        Returns true if the premises of an argument are not in the edit queue

        :param db_argument: Argument
        :param is_executed: Bool
        :return: Boolean
        """
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).all()
        statement_uids = [db_premise.statement_uid for db_premise in db_premises]
        db_already_edit_count = DBDiscussionSession.query(ReviewEdit).filter(
            ReviewEdit.statement_uid.in_(statement_uids),
            ReviewEdit.is_executed == is_executed).count()
        return db_already_edit_count > 0
