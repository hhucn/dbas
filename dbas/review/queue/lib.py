from typing import Union

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import LastReviewerSplit, LastReviewerMerge, LastReviewerDelete, \
    LastReviewerDuplicate, LastReviewerEdit, LastReviewerOptimization, User, ReviewDelete, ReviewEdit, ReviewMerge, \
    ReviewOptimization, ReviewSplit, ReviewDuplicate
from dbas.logger import logger

max_votes = 5
min_difference = 3


def add_vote_for(db_user: User, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge, ReviewOptimization, ReviewSplit],
                 is_okay: bool, db_reviewer_type: Union[LastReviewerDelete, LastReviewerDuplicate, LastReviewerEdit, LastReviewerMerge, LastReviewerOptimization, LastReviewerSplit]):
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


def get_review_count(review_type: Union[LastReviewerMerge, LastReviewerSplit, LastReviewerDelete, LastReviewerDuplicate,
                                        LastReviewerDuplicate, LastReviewerEdit, LastReviewerOptimization],
                     review_uid: int):
    """
    Get review count of specific review queue

    :param review_type: Table of Review
    :param review_uid: uid of review type
    :return: Tuple with counts of okay and not okay
    """
    db_reviews = DBDiscussionSession.query(review_type).filter_by(review_uid=review_uid)
    if review_type is LastReviewerMerge:
        count_of_okay = db_reviews.filter_by(should_merge=True).count()
        count_of_not_okay = db_reviews.filter_by(should_merge=False).count()
    elif review_type is LastReviewerSplit:
        count_of_okay = db_reviews.filter_by(should_split=True).count()
        count_of_not_okay = db_reviews.filter_by(should_split=False).count()
    else:
        count_of_okay = db_reviews.filter_by(is_okay=True).count()
        count_of_not_okay = db_reviews.filter_by(is_okay=False).count()

    return count_of_okay, count_of_not_okay
