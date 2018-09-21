# Adaptee for the optimizations queue. Every accepted optimization will be an edit.
import logging
import random
import transaction
from beaker.session import Session
from typing import Tuple, Optional

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerOptimization, ReviewOptimization, ReviewEdit, \
    ReviewEditValue, Statement, Issue, Argument, Premise, ReviewCanceled, OptimizationReviewLocks, get_now
from dbas.lib import get_text_for_argument_uid, get_all_arguments_by_statement
from dbas.review import FlaggedBy
from dbas.review.queue import max_votes, key_optimization, max_lock_time_in_sec
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import get_issues_for_statement_uids, \
    get_reporter_stats_for_review, get_all_allowed_reviews_for_user, revoke_decision_and_implications, \
    get_user_dict_for_review
from dbas.review.reputation import get_reason_by_action, ReputationReasons, \
    add_reputation_and_send_popup
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


class OptimizationQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_optimization

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
        Setup the subpage for the optimization queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        LOG.debug("Setting up the sub-page for the optimization-queue")
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{self.key}', db_user,
                                                        ReviewOptimization, LastReviewerOptimization)

        extra_info = ''
        # if we have no reviews, try again with fewer restrictions
        if not all_rev_dict['reviews']:
            all_rev_dict['already_seen_reviews'] = list()
            extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
            db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(
                ReviewOptimization.is_executed == False,
                ReviewOptimization.detector_uid != db_user.uid)
            if len(all_rev_dict['already_voted_reviews']) > 0:
                db_reviews = db_reviews.filter(~ReviewOptimization.uid.in_(all_rev_dict['already_voted_reviews']))
            all_rev_dict['reviews'] = db_reviews.all()

        if not all_rev_dict['reviews']:
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue_titles': None,
                'context': [],
                'extra_info': None,
                'session': session
            }

        rnd_review = random.choice(all_rev_dict['reviews'])
        if rnd_review.statement_uid is None:
            db_argument = DBDiscussionSession.query(Argument).get(rnd_review.argument_uid)
            text = get_text_for_argument_uid(db_argument.uid)
            issue_titles = [DBDiscussionSession.query(Issue).get(db_argument.issue_uid).title]
            parts = self.__get_text_parts_of_argument(db_argument)
            context = [text]
        else:
            db_statement = DBDiscussionSession.query(Statement).get(rnd_review.statement_uid)
            text = db_statement.get_text()
            issue_titles = [issue.title for issue in get_issues_for_statement_uids([rnd_review.statement_uid])]
            parts = [self.__get_part_dict('statement', text, 0, rnd_review.statement_uid)]
            context = []
            args = get_all_arguments_by_statement(rnd_review.statement_uid)
            if args:
                html_wrap = '<span class="text-info"><strong>{}</strong></span>'
                context = [get_text_for_argument_uid(arg.uid).replace(text, html_wrap.format(text)) for arg in args]

        reason = translator.get(_.argumentFlaggedBecauseOptimization)

        stats = get_reporter_stats_for_review(rnd_review, translator.get_lang(), application_url)

        all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
        session[f'already_seen_{self.key}'] = all_rev_dict['already_seen_reviews']

        return {
            'stats': stats,
            'text': text,
            'reason': reason,
            'issue_titles': issue_titles,
            'extra_info': extra_info,
            'context': context,
            'parts': parts,
            'session': session
        }

    def add_vote(self, db_user: User, db_review: ReviewOptimization, is_okay: bool, application_url: str,
                 translator: Translator, **kwargs):
        """
        Adds an vote for this queue. If any (positive or negative) limit is reached, the flagged element will be
        a new edit element

        :param db_user: current user who votes
        :param db_review: the review, which is voted vor
        :param is_okay: True, if the element is rightly flagged
        :param application_url: the app url
        :param translator: a instance of a translator
        :param kwargs: optional, keyworded arguments
        :return:
        """
        LOG.debug("Add a vote for optimization")
        # add new review
        db_new_review = LastReviewerOptimization(db_user.uid, db_review.uid, not is_okay)
        DBDiscussionSession.add(db_new_review)
        DBDiscussionSession.flush()
        transaction.commit()

        if is_okay:
            self.__proposal_for_the_element(db_review, kwargs['new_data'], db_user)
        else:
            self.__keep_the_element_of_optimization_review(db_review, application_url, translator)

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
        db_reviews = DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User, db_review: ReviewOptimization):
        """
        Cancels any ongoing vote

        :param db_user: current user
        :param db_review: any element from a review queue
        :return:
        """
        DBDiscussionSession.query(ReviewOptimization).get(db_review.uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_optimization: db_review.uid},
                                            was_ongoing=True)

        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def revoke_ballot(self, db_user: User, db_review: ReviewOptimization):
        """
        Revokes/Undo the implications of any successfull reviewed element

        :param db_user:
        :param db_review:
        :return:
        """
        revoke_decision_and_implications(ReviewOptimization, LastReviewerOptimization, db_review.uid)
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_optimization: db_review.uid})
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
        db_review = DBDiscussionSession.query(ReviewOptimization).filter_by(
            argument_uid=kwargs.get('argument_uid'),
            statement_uid=kwargs.get('statement_uid'),
            is_executed=False,
            is_revoked=False)
        if db_review.filter_by(detector_uid=db_user.uid).count() > 0:
            return FlaggedBy.user
        if db_review.count() > 0:
            return FlaggedBy.other
        return None

    def get_text_of_element(self, db_review: ReviewOptimization) -> str:
        """
        Returns full text of the given element

        :param db_review: current review element
        :return:
        """
        if db_review.statement_uid is None:
            return get_text_for_argument_uid(db_review.argument_uid)
        else:
            return DBDiscussionSession.query(Statement).get(db_review.statement_uid).get_text()

    def get_all_votes_for(self, db_review: ReviewOptimization, application_url: str) -> Tuple[list, list]:
        """
        Returns all pro and con votes for the given element

        :param db_review: current review element
        :param application_url: The applications URL
        :return:
        """
        db_all_votes = DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid)
        pro_votes = db_all_votes.filter_by(is_okay=True).all()
        con_votes = db_all_votes.filter_by(is_okay=False).all()

        pro_list = [get_user_dict_for_review(pro.reviewer_uid, application_url) for pro in pro_votes]
        con_list = [get_user_dict_for_review(con.reviewer_uid, application_url) for con in con_votes]

        return pro_list, con_list

    def get_history_table_row(self, db_review: ReviewOptimization, entry, **kwargs):
        """
        Returns nothing because this reviews SHOULD NOT be in the history!

        :param db_review:
        :param entry:
        :param kwargs:
        :return:
        """
        pass

    def lock_optimization_review(self, db_user: User, db_review: ReviewOptimization, translator: Translator):
        """
        Locks a ReviewOptimization

        :param db_user:
        :param db_review:
        :param translator:
        :return:
        """
        LOG.debug("Lock an Optimization-Review")
        # check if author locked an item and maybe tidy up old locks
        db_locks = DBDiscussionSession.query(OptimizationReviewLocks).filter_by(author_uid=db_user.uid).first()
        if db_locks:
            if self.is_review_locked(db_locks.review_optimization_uid):
                LOG.debug("Review was already locked")
                return {
                    'success': '',
                    'info': translator.get(_.dataAlreadyLockedByYou),
                    'is_locked': True
                }
            else:
                DBDiscussionSession.query(OptimizationReviewLocks).filter_by(author_uid=db_user.uid).delete()

        # is already locked?
        if self.is_review_locked(db_review.uid):
            LOG.warning("Already locked case")
            return {
                'success': '',
                'info': translator.get(_.dataAlreadyLockedByOthers),
                'is_locked': True
            }

        DBDiscussionSession.add(OptimizationReviewLocks(db_user.uid, db_review.uid))
        DBDiscussionSession.flush()
        transaction.commit()
        success = translator.get(_.dataAlreadyLockedByYou)

        LOG.debug("Review locked")
        return {
            'success': success,
            'info': '',
            'is_locked': True
        }

    def unlock_optimization_review(self, db_review: ReviewOptimization, translator: Translator):
        """
        Unlock the OptimizationReviewLocks

        :param db_review:
        :param translator:
        :return:
        """
        self.tidy_up_optimization_locks()
        LOG.debug("Unlocking Optimization-Review")
        DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=db_review.uid).delete()
        DBDiscussionSession.flush()
        transaction.commit()
        return {
            'is_locked': False,
            'success': translator.get(_.dataUnlocked),
            'info': ''
        }

    def is_review_locked(self, review_uid):
        """
        Is the OptimizationReviewLocks set?

        :param review_uid: OptimizationReviewLocks.uid
        :return: Boolean
        """
        self.tidy_up_optimization_locks()
        LOG.debug("Check whether review %s is locked.", review_uid)
        db_lock = DBDiscussionSession.query(OptimizationReviewLocks).filter_by(
            review_optimization_uid=review_uid).first()
        if not db_lock:
            return False
        return (get_now() - db_lock.locked_since).seconds < max_lock_time_in_sec

    @staticmethod
    def tidy_up_optimization_locks():
        """
        Tidy up all expired locks

        :return: None
        """
        LOG.debug("Enter Tidy up function")
        db_locks = DBDiscussionSession.query(OptimizationReviewLocks).all()
        for lock in db_locks:
            if (get_now() - lock.locked_since).seconds >= max_lock_time_in_sec:
                DBDiscussionSession.query(OptimizationReviewLocks).filter_by(
                    review_optimization_uid=lock.review_optimization_uid).delete()

    def __get_text_parts_of_argument(self, db_argument: Argument):
        """
        Get all parts of an argument as string

        :param db_argument: Argument.uid
        :return: list of strings
        """
        LOG.debug("Get all parts of an argument as string")
        ret_list = list()

        # get premise of current argument
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).all()
        premises_uids = [premise.uid for premise in db_premises]
        for uid in premises_uids:
            LOG.debug("Add premise of argument %s", db_argument.uid)
            statement = DBDiscussionSession.query(Statement).get(uid)
            ret_list.append(self.__get_part_dict('premise', statement.get_text(), db_argument.uid, uid))

        if db_argument.argument_uid is None:  # get conclusion of current argument
            conclusion = db_argument.get_conclusion_text()
            LOG.debug("Add statement of argument %s", db_argument.uid)
            ret_list.append(self.__get_part_dict('conclusion', conclusion, db_argument.uid, db_argument.conclusion_uid))
        else:  # or get the conclusions argument
            db_conclusions_argument = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)

            while db_conclusions_argument.argument_uid is not None:  # get further conclusions arguments

                # get premise of conclusions arguments
                db_premises = DBDiscussionSession.query(Premise).filter_by(
                    premisegroup_uid=db_argument.premisegroup_uid).all()
                premises_uids = [premise.uid for premise in db_premises]
                for uid in premises_uids:
                    statement = DBDiscussionSession.query(Statement).get(uid)
                    LOG.debug("Add premise of argument %s", db_conclusions_argument.uid)
                    ret_list.append(
                        self.__get_part_dict('premise', statement.get_text(), db_conclusions_argument.uid, uid))

                db_conclusions_argument = DBDiscussionSession.query(Argument).get(db_conclusions_argument.argument_uid)

            # get the last conclusion of the chain
            conclusion = db_conclusions_argument.get_conclusion_text()
            LOG.debug("Add statement of argument %s", db_conclusions_argument.uid)
            ret_list.append(self.__get_part_dict('conclusion', conclusion, db_conclusions_argument.uid,
                                                 db_conclusions_argument.conclusion_uid))

        return ret_list[::-1]

    @staticmethod
    def __get_part_dict(typeof: str, text: str, argument_uid: int, conclusion_uid: int):
        """
        Collects the aprts of the argument-string and builds up a little dict

        :param typeof: String
        :param text: String
        :param argument_uid: Argument.uid
        :return: dict()
        """
        return {
            'type': typeof,
            'text': text,
            'argument_uid': argument_uid,
            'statement_uid': conclusion_uid
        }

    @staticmethod
    def __keep_the_element_of_optimization_review(db_review: ReviewOptimization, main_page: str,
                                                  translator: Translator):
        """
        Adds row for LastReviewerOptimization

        :param db_review: ReviewOptimization
        :param main_page: URL
        :param translator: Translator
        :return: None
        """
        # add new vote
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)

        # get all keep and delete votes
        db_keep_version = DBDiscussionSession.query(LastReviewerOptimization).filter(
            LastReviewerOptimization.review_uid == db_review.uid,
            LastReviewerOptimization.is_okay == True).all()

        if len(db_keep_version) > max_votes:
            add_reputation_and_send_popup(db_user_created_flag, get_reason_by_action(ReputationReasons.bad_flag),
                                          main_page, translator)

            db_review.set_executed(True)
            db_review.update_timestamp()
            DBDiscussionSession.add(db_review)
            DBDiscussionSession.flush()
            transaction.commit()

    def __proposal_for_the_element(self, db_review: ReviewOptimization, data: dict, db_user: User):
        """
        Adds proposal for the ReviewEdit

        :param db_review: ReviewEdit
        :param data: dict
        :param db_user: User
        :return: None
        """
        # sort the new edits by argument uid
        argument_dict, statement_dict = self.__prepare_dicts_for_proposals(data)

        LOG.debug("Detector %s, statements %s, arguments %s", db_user.uid, statement_dict, argument_dict)

        # add reviews
        new_edits = list()
        for argument_uid in argument_dict:
            DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, argument=argument_uid))
            DBDiscussionSession.flush()
            transaction.commit()
            db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(
                ReviewEdit.detector_uid == db_user.uid,
                ReviewEdit.argument_uid == argument_uid).order_by(ReviewEdit.uid.desc()).first()
            LOG.debug("New ReviewEdit with uid %s (argument)", db_review_edit.uid)

            for edit in argument_dict[argument_uid]:
                new_edits.append(ReviewEditValue(review_edit=db_review_edit.uid,
                                                 statement=edit['uid'],
                                                 typeof=edit['type'],
                                                 content=edit['val']))

        for statement_uid in statement_dict:
            DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, statement=statement_uid))
            DBDiscussionSession.flush()
            transaction.commit()
            db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(
                ReviewEdit.detector_uid == db_user.uid,
                ReviewEdit.statement_uid == statement_uid).order_by(ReviewEdit.uid.desc()).first()
            LOG.debug("New ReviewEdit with uid %s (statement)", db_review_edit.uid)

            for edit in statement_dict[statement_uid]:
                new_edits.append(ReviewEditValue(review_edit=db_review_edit.uid,
                                                 statement=statement_uid,
                                                 typeof=edit['type'],
                                                 content=edit['val']))

        if len(new_edits) > 0:
            DBDiscussionSession.add_all(new_edits)

        # edit given, so this review is executed
        db_review.set_executed(True)
        db_review.update_timestamp()
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

    @staticmethod
    def __prepare_dicts_for_proposals(data):
        """

        :param data:
        :return:
        """
        argument_dict = {}
        statement_dict = {}
        for d in data:
            is_argument = d['argument'] > 0
            if is_argument:
                if d['argument'] in argument_dict:
                    argument_dict[d['argument']].append(d)
                else:
                    argument_dict[d['argument']] = [d]
            else:
                if d['statement'] in statement_dict:
                    statement_dict[d['statement']].append(d)
                else:
                    statement_dict[d['statement']] = [d]
        return argument_dict, statement_dict
