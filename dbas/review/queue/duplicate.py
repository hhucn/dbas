# Adaptee for the duplicate queue.
import random

import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerDuplicate, ReviewDuplicate, Statement, RevokedDuplicate, \
    Premise, ReviewCanceled, Argument, LastReviewerDelete
from dbas.lib import get_all_arguments_by_statement, get_text_for_statement_uid
from dbas.logger import logger
from dbas.review import FlaggedBy, txt_len_history_page
from dbas.review.queue import min_difference, max_votes, key_duplicate
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import get_all_allowed_reviews_for_user, get_reporter_stats_for_review, \
    get_issues_for_statement_uids, add_vote_for
from dbas.review.reputation import get_reason_by_action, add_reputation_and_check_review_access, ReputationReasons
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class DuplicateQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_duplicate

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
        Setup the subpage for the duplicate queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        logger('DuplicateQueue', 'main')
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{self.key}', db_user,
                                                        ReviewDuplicate,
                                                        LastReviewerDuplicate)

        extra_info = ''
        # if we have no reviews, try again with fewer restrictions
        if not all_rev_dict['reviews']:
            logger('DuplicateQueue', 'no unseen reviews')
            all_rev_dict['already_seen_reviews'] = list()
            extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
            all_rev_dict['reviews'] = DBDiscussionSession.query(ReviewDuplicate).filter(
                ReviewDuplicate.is_executed == False,
                ReviewDuplicate.detector_uid != db_user.uid)
            if len(all_rev_dict['already_voted_reviews']) > 0:
                logger('DuplicateQueue', 'everything was seen')
                all_rev_dict['reviews'] = all_rev_dict['reviews'].filter(
                    ~ReviewDuplicate.uid.in_(all_rev_dict['already_voted_reviews'])).all()

        if not all_rev_dict['reviews']:
            logger('DuplicateQueue', 'no reviews')
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue_titles': None,
                'extra_info': None,
                'session': session
            }

        rnd_review = random.choice(all_rev_dict['reviews'])
        db_statement = DBDiscussionSession.query(Statement).get(rnd_review.duplicate_statement_uid)
        text = db_statement.get_text()

        issue_titles = [issue.title for issue in get_issues_for_statement_uids([rnd_review.duplicate_statement_uid])]
        reason = translator.get(_.argumentFlaggedBecauseDuplicate)
        duplicate_of_text = get_text_for_statement_uid(rnd_review.original_statement_uid)
        stats = get_reporter_stats_for_review(rnd_review, translator.get_lang(), application_url)

        all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
        session['already_seen_duplicate'] = all_rev_dict['already_seen_reviews']

        return {
            'stats': stats,
            'text': text,
            'duplicate_of': duplicate_of_text,
            'reason': reason,
            'issue_titles': issue_titles,
            'extra_info': extra_info,
            'session': session
        }

    def add_vote(self, db_user: User, db_review: ReviewDuplicate, is_okay: bool, application_url: str,
                 translator: Translator,
                 **kwargs):
        """
        Adds an vote for this queue. If any (positive or negative) limit is reached, the flagged element will disabled
        and the origin will be set as root for any relative

        :param db_user: current user who votes
        :param db_review: the review, which is voted vor
        :param is_okay: True, if the element is rightly flagged
        :param application_url: the app url
        :param translator: a instance of a translator
        :param kwargs: optional, keyworded arguments
        :return:
        """
        logger('DuplicateQueue', 'main {}, duplicate {}'.format(db_review.uid, is_okay))
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        rep_reason = None

        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerDuplicate)

        # get all keep and delete votes
        count_of_reset, count_of_keep = self.get_review_count(db_review.uid)

        # do we reached any limit?
        reached_max = max(count_of_keep, count_of_reset) >= max_votes
        if reached_max:
            if count_of_reset > count_of_keep:  # disable the flagged part
                self.__bend_objects_of_review(db_review)
                rep_reason = get_reason_by_action(ReputationReasons.success_duplicate)
            else:  # just close the review
                rep_reason = get_reason_by_action(ReputationReasons.bad_duplicate)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_reset >= min_difference:  # just close the review
            rep_reason = get_reason_by_action(ReputationReasons.bad_duplicate)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_reset - count_of_keep >= min_difference:  # disable the flagged part
            self.__bend_objects_of_review(db_review)
            rep_reason = get_reason_by_action(ReputationReasons.success_duplicate)
            db_review.set_executed(True)
            db_review.update_timestamp()

        if rep_reason:
            add_reputation_and_check_review_access(db_user_created_flag, rep_reason, application_url, translator)
            DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    def add_review(self, db_user: User):
        """
        Just adds a new element

        :param db_user:
        :return:
        """
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User, db_review: ReviewDuplicate):
        """

        :param db_user:
        :param db_review:
        :return:
        """
        DBDiscussionSession.query(ReviewDuplicate).get(db_review.uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_duplicate: db_review.uid},
                                            was_ongoing=True)

        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def revoke_ballot(self, db_user: User, db_review: ReviewDuplicate):
        """

        :param db_user:
        :param db_review:
        :return:
        """
        db_review = DBDiscussionSession.query(ReviewDuplicate).get(db_review.uid)
        db_review.set_revoked(True)
        self.__rebend_objects_of_review(db_review)
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_duplicate: db_review.uid})
        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def element_in_queue(self, db_user: User, **kwargs):
        """

        :param db_user:
        :param kwargs:
        :return:
        """
        db_review = DBDiscussionSession.query(ReviewDuplicate).filter_by(
            duplicate_statement_uid=kwargs.get('statement_uid'),
            is_executed=False,
            is_revoked=False)
        if db_review.filter_by(detector_uid=db_user.uid).count() > 0:
            return FlaggedBy.user
        if db_review.count() > 0:
            return FlaggedBy.other
        return None

    def get_history_table_row(self, db_review: ReviewDuplicate, entry, **kwargs):
        """

        :param db_review:
        :param entry:
        :param kwargs:
        :return:
        """
        text = get_text_for_statement_uid(db_review.original_statement_uid)
        if text is None:
            text = '...'
        entry['statement_duplicate_shorttext'] = text[0:txt_len_history_page] + ('...' if len(text) > txt_len_history_page else '')
        entry['statement_duplicate_fulltext'] = text
        return entry

    @staticmethod
    def __bend_objects_of_review(db_review):
        """
        If an argument is a duplicate, we have to bend the objects of argument, which are no duplicates

        :param db_review: Review
        :return: None
        """
        msg = 'Review {} with dupl {} and oem {}'.format(db_review.uid,
                                                         db_review.duplicate_statement_uid,
                                                         db_review.original_statement_uid)
        logger('DuplicateQueue', msg)
        db_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
        db_statement.set_disabled(True)
        DBDiscussionSession.add(db_statement)

        # do we need a new position
        db_dupl_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
        db_orig_statement = DBDiscussionSession.query(Statement).get(db_review.original_statement_uid)
        if db_dupl_statement.is_position and not db_orig_statement.is_position:
            logger('DuplicateQueue', 'Duplicate is startpoint, but original one is not')
            DBDiscussionSession.add(
                RevokedDuplicate(review=db_review.uid, bend_position=True, statement=db_orig_statement.uid))
            db_orig_statement.set_position(True)

        # getting all argument where the duplicated statement is used
        all_arguments = get_all_arguments_by_statement(db_review.duplicate_statement_uid, True)
        for argument in all_arguments:
            text = 'Statement {db_review.duplicate_statement_uid} was used in argument {argument.uid}'
            used = False

            # recalibrate conclusion
            if argument.conclusion_uid == db_review.duplicate_statement_uid:
                tmp = '{text}, bend conclusion from {argument.conclusion_ui} to {db_review.original_statement_uid}'
                logger('DuplicateQueue', tmp)
                argument.set_conclusion(db_review.original_statement_uid)
                DBDiscussionSession.add(argument)
                DBDiscussionSession.add(RevokedDuplicate(review=db_review.uid, conclusion_of_argument=argument.uid))
                used = True

            # recalibrate premises
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=argument.premisegroup_uid).all()
            for premise in db_premises:
                if premise.statement_uid == db_review.duplicate_statement_uid:
                    tmp = f'{text}, bend premise {premise.uid} from {premise.statement_uid} to {db_review.original_statement_uid}'
                    logger('DuplicateQueue', tmp)
                    premise.set_statement(db_review.original_statement_uid)
                    DBDiscussionSession.add(premise)
                    DBDiscussionSession.add(RevokedDuplicate(review=db_review.uid, premise=premise.uid))
                    used = True

            if not used:
                logger('DuplicateQueue', f'Nothing was bend - undercut from {argument.uid} to {argument.argument_uid}',
                       error=True)

        DBDiscussionSession.flush()
        transaction.commit()

    @staticmethod
    def __rebend_objects_of_review(db_review):
        """
        If something was bend (due to duplicates), lets rebend this

        :param db_review: Review
        :return: None
        """
        logger('review_history_helper', f'review: {db_review.uid}')

        db_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
        db_statement.set_disabled(False)
        DBDiscussionSession.add(db_statement)

        db_revoked_elements = DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=db_review.uid).all()
        for revoke in db_revoked_elements:
            if revoke.bend_position:
                db_statement = DBDiscussionSession.query(Statement).get(revoke.statement_uid)
                db_statement.set_position(False)
                DBDiscussionSession.add(db_statement)

            if revoke.argument_uid is not None:
                db_argument = DBDiscussionSession.query(Argument).get(revoke.argument_uid)
                text = f'Rebend conclusion of argument {revoke.argument_uid} from {db_argument.conclusion_uid} to {db_review.duplicate_statement_uid}'
                logger('review_history_helper', text)
                db_argument.conclusion_uid = db_review.duplicate_statement_uid
                DBDiscussionSession.add(db_argument)

            if revoke.premise_uid is not None:
                db_premise = DBDiscussionSession.query(Premise).get(revoke.premise_uid)
                text = f'Rebend premise {revoke.premise_uid} from {db_premise.statement_uid} to {db_review.duplicate_statement_uid}'
                logger('review_history_helper', text)
                db_premise.statement_uid = db_review.duplicate_statement_uid
                DBDiscussionSession.add(db_premise)
        DBDiscussionSession.query(RevokedDuplicate).filter_by(review_uid=db_review.uid).delete()

        DBDiscussionSession.flush()
        transaction.commit()
