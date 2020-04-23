# Adaptee for the edit queue. Every edit results in a new textversion of a statement.
import difflib
import logging
from typing import List, Tuple, Optional

import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerEdit, ReviewEdit, ReviewEditValue, TextVersion, \
    ReviewCanceled, Statement, Argument, Premise
from dbas.handler.textversion import propose_new_textversion_for_statement
from dbas.lib import get_text_for_argument_uid
from dbas.review import FlaggedBy, txt_len_history_page
from dbas.review.queue import max_votes, min_difference, key_edit, Code
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import get_all_allowed_reviews_for_user, get_base_subpage_dict, \
    get_reporter_stats_for_review, add_vote_for, get_user_dict_for_review
from dbas.review.reputation import get_reason_by_action, ReputationReasons, \
    add_reputation_and_send_popup
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


class EditQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_edit

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
        Setup the subpage for the edit queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        LOG.debug("Setting up the page for the edit queue")
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

        rev_dict['already_seen_reviews'].append(rev_dict['rnd_review'].uid)
        session[f'already_seen_{self.key}'] = rev_dict['already_seen_reviews']

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

    def add_vote(self, db_user: User, db_review: ReviewEdit, is_okay: bool, application_url: str,
                 translator: Translator,
                 **kwargs):
        """
        Adds an vote for this queue. If any (positive or negative) limit is reached, the flagged element get a new
        textversion

        :param db_user: current user who votes
        :param db_review: the review, which is voted vor
        :param is_okay: True, if the element is rightly flagged
        :param application_url: the app url
        :param translator: a instance of a translator
        :param kwargs: optional, keyworded arguments
        :return:
        """
        LOG.debug("Add a vote for edit queue")
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
        db_reviews = DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User, db_review: ReviewEdit):
        """
        Cancels any ongoing vote

        :param db_user: current user
        :param db_review: any element from a review queue
        :return:
        """
        DBDiscussionSession.query(ReviewEdit).get(db_review.uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).delete()
        DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_edit: db_review.uid}, was_ongoing=True)

        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def revoke_ballot(self, db_user: User, db_review: ReviewEdit):
        """
        Revokes/Undo the implications of any successfull reviewed element

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
        return True

    def element_in_queue(self, db_user: User, **kwargs) -> Optional[FlaggedBy]:
        """
        Check if the element described by kwargs is in any queue. Return a FlaggedBy object or none

        :param db_user: current user
        :param kwargs: "magic" -> atm keywords like argument_uid, statement_uid and premisegroup_uid. Please update
        this!
        """
        db_review = DBDiscussionSession.query(ReviewEdit).filter_by(
            argument_uid=kwargs.get('argument_uid'),
            statement_uid=kwargs.get('statement_uid'),
            is_executed=False,
            is_revoked=False)
        if db_review.filter_by(detector_uid=db_user.uid).count() > 0:
            return FlaggedBy.user
        if db_review.count() > 0:
            return FlaggedBy.other
        return None

    def get_history_table_row(self, db_review: ReviewEdit, entry: dict, **kwargs) -> Optional[dict]:
        """
        Returns a row the the history/ongoing page for the given review element

        :param db_review: current element which is the source of the row
        :param entry: dictionary with some values which were already set
        :param kwargs: "magic" -> atm keywords like is_executed, short_text and full_text. Please update this!
        :return:
        """
        if kwargs.get('is_executed'):
            db_textversions = DBDiscussionSession.query(TextVersion).filter_by(
                statement_uid=db_review.statement_uid).order_by(
                TextVersion.uid.desc()).all()
            if len(db_textversions) <= 1:
                LOG.warning(f'Review {db_review.uid} is malicious, has only {len(db_textversions)} textversions')
                entry = None
            else:
                entry['argument_oem_shorttext'] = db_textversions[1].content[0:txt_len_history_page]
                entry['argument_oem_fulltext'] = db_textversions[1].content
        else:
            db_edit_value = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=db_review.uid).first()
            if not db_edit_value:
                entry = None
            else:
                entry['argument_oem_shorttext'] = kwargs.get('short_text')
                entry['argument_oem_fulltext'] = kwargs.get('full_text')
                if len(kwargs.get('full_text')) > txt_len_history_page:
                    entry['argument_shorttext'] = db_edit_value.content[0:txt_len_history_page] + '...'
                else:
                    entry['argument_shorttext'] = db_edit_value.content
                entry['argument_fulltext'] = db_edit_value.content
        return entry

    def get_text_of_element(self, db_review: ReviewEdit) -> str:
        """
        Returns full text of the given element

        :param db_review: current review element
        :return:
        """
        if db_review.statement_uid is None:
            return get_text_for_argument_uid(db_review.argument_uid)
        else:
            return DBDiscussionSession.query(Statement).get(db_review.statement_uid).get_text()

    def get_all_votes_for(self, db_review: ReviewEdit, application_url: str) -> Tuple[list, list]:
        """
        Returns all pro and con votes for the given element

        :param db_review: current review element
        :param application_url: The applications URL
        :return:
        """
        db_all_votes = DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid)
        pro_votes = db_all_votes.filter_by(is_okay=True).all()
        con_votes = db_all_votes.filter_by(is_okay=False).all()

        pro_list = [get_user_dict_for_review(pro.reviewer_uid, application_url) for pro in pro_votes]
        con_list = [get_user_dict_for_review(con.reviewer_uid, application_url) for con in con_votes]

        return pro_list, con_list

    def add_edit_reviews(self, user: User, uid: int, text: str):
        """
        Setup a new ReviewEdit row

        :param user: User who want to add a edit_review
        :param uid: Statement.uid
        :param text: New content for statement
        :return: -1 if the statement of the element does not exists, -2 if this edit already exists, 1 on success,
        0 otherwise
        """
        statement: Statement = DBDiscussionSession.query(Statement).get(uid)
        if not statement:
            LOG.warning("Statement %s not found (return %s)", uid, Code.DOESNT_EXISTS)
            return Code.DOESNT_EXISTS

        # already set an correction for this?
        if self.is_statement_in_edit_queue(uid):  # if we already have an edit, skip this
            LOG.warning("Statement %s already got an edit (return %s)", uid, Code.DUPLICATE)
            return Code.DUPLICATE

        # is text different?
        textversion: TextVersion = statement.textversion
        if len(text) > 0 and textversion.content.lower().strip() != text.lower().strip():
            LOG.debug("Added review element for %s. (return %s)", uid, Code.SUCCESS)
            DBDiscussionSession.add(ReviewEdit(detector=user, statement=statement))
            return Code.SUCCESS

        LOG.debug("No case for %s (return %s)", uid, Code.ERROR)
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
        statement: Statement = DBDiscussionSession.query(Statement).get(uid)
        if not statement:
            LOG.debug("ID %s not found while setting up ReviewEditValue", uid)
            return Code.ERROR

        textversion: TextVersion = statement.textversion

        if len(text) > 0 and textversion.content.lower().strip() != text.lower().strip():
            db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.detector_uid == db_user.uid,
                                                                          ReviewEdit.statement_uid == uid).order_by(
                ReviewEdit.uid.desc()).first()
            DBDiscussionSession.add(ReviewEditValue(db_review_edit.uid, uid, 'statement', text))
            LOG.debug("%s - '%s' accepted", uid, text)
            return Code.SUCCESS

        LOG.debug("%s - '%s' malicious edit", uid, text)
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
                                                                             ReviewEdit.is_executed == is_executed) \
            .count()
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
            propose_new_textversion_for_statement(db_user, value.statement, value.content)
