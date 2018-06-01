# Adaptee for the optimizations queue. Every accepted optimization will be an edit.
import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerOptimization, ReviewOptimization, ReviewEdit, \
    ReviewEditValue
from dbas.logger import logger
from dbas.review import rep_reason_bad_flag, max_votes
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import add_reputation_and_check_review_access
from dbas.strings.translator import Translator


class OptimizationQueue(QueueABC):
    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        pass

    def add_vote(self, db_user: User, db_review: ReviewOptimization, is_okay: bool, application_url: str,
                 translator: Translator, **kwargs):
        """

        :param db_user:
        :param db_review:
        :param is_okay:
        :param application_url:
        :param translator:
        :param kwargs:
        :return:
        """
        logger('OptimizationQueue', 'main')
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
            add_reputation_and_check_review_access(db_user_created_flag, rep_reason_bad_flag, main_page, translator)

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

        logger('OptimizationQueue',
               'detector {}, statements {}, arguments {}'.format(db_user.uid, statement_dict, argument_dict))

        # add reviews
        new_edits = list()
        for argument_uid in argument_dict:
            DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, argument=argument_uid))
            DBDiscussionSession.flush()
            transaction.commit()
            db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(
                ReviewEdit.detector_uid == db_user.uid,
                ReviewEdit.argument_uid == argument_uid).order_by(ReviewEdit.uid.desc()).first()
            logger('OptimizationQueue', 'New ReviewEdit with uid ' + str(db_review_edit.uid) + ' (argument)')

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
            logger('OptimizationQueue', 'New ReviewEdit with uid ' + str(db_review_edit.uid) + ' (statement)')

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

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User):
        pass

    def revoke_ballot(self, db_user: User):
        pass
