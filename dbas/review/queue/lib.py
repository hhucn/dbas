from typing import Union

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import LastReviewerSplit, LastReviewerMerge, LastReviewerDelete, \
    LastReviewerDuplicate, LastReviewerEdit, LastReviewerOptimization, User, ReviewDelete, ReviewEdit, ReviewMerge, \
    ReviewOptimization, ReviewSplit, ReviewDuplicate
from dbas.logger import logger
from dbas.review.reputation import add_reputation_for, has_access_to_review_system
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio


def add_vote_for(db_user: User, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge,
                                                 ReviewOptimization, ReviewSplit], is_okay: bool,
                 db_reviewer_type: Union[LastReviewerDelete, LastReviewerDuplicate, LastReviewerEdit, LastReviewerMerge,
                                         LastReviewerOptimization, LastReviewerSplit]):
    """
    Add vote for a specific review

    :param db_user: User
    :param db_review: one table ouf of the Reviews
    :param is_okay: Boolean
    :param db_reviewer_type: one table out of the LastReviews
    :return: None
    """
    logger('review.lib', f'{db_reviewer_type}, user {db_user.uid}, db_review {db_review}, is_okay {is_okay}')
    already_voted = DBDiscussionSession.query(db_reviewer_type).filter(db_reviewer_type.reviewer_uid == db_user.uid,
                                                                       db_reviewer_type.review_uid == db_review.uid).first()
    if not already_voted:
        db_new_review = db_reviewer_type(db_user.uid, db_review.uid, is_okay)
        DBDiscussionSession.add(db_new_review)
        DBDiscussionSession.flush()
        transaction.commit()
        logger('review.lib', 'vote added')
    else:
        logger('review.lib', 'already voted')


def add_reputation_and_check_review_access(db_user: User, rep_reason: str, main_page: str, translator: Translator):
    """
    Adds reputation to a specific user and checks (send info popup) to this user

    :param db_user: user, which should get reputation
    :param rep_reason: Any reputation reason as string
    :param main_page: URL of the app
    :param translator: Instance of a translator
    :return:
    """
    if not rep_reason:
        return

    add_reputation_for(db_user, rep_reason)

    if has_access_to_review_system(db_user):
        send_request_for_info_popup_to_socketio(db_user.nickname, translator.get(_.youAreAbleToReviewNow),
                                                main_page + '/review')
