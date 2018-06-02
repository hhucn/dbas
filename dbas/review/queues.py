"""
Provides helping function for displaying the review queues and locking entries.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from typing import Union

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, ReviewOptimization, \
    LastReviewerOptimization, ReviewEdit, LastReviewerEdit, OptimizationReviewLocks, get_now, \
    ReviewDuplicate, LastReviewerDuplicate, ReviewMerge, ReviewSplit, LastReviewerMerge, LastReviewerSplit
from dbas.lib import get_profile_picture
from dbas.logger import logger
from dbas.review.queue import max_lock_time_in_sec, key_edit, key_delete, key_duplicate, key_optimization, key_merge, \
    key_split, key_history, key_ongoing
from dbas.review.queue.lib import get_review_count_for
from dbas.review.reputation import get_reputation_of, reputation_borders, reputation_icons
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


def get_review_queues_as_lists(main_page: str, translator: Translator, db_user: User):
    """
    Prepares dictionary for the edit section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: Users nickname
    :return: Array
    """
    logger('ReviewQueues', 'main')
    count, all_rights = get_reputation_of(db_user)

    review_list = list()
    review_list.append(__get_delete_dict(main_page, translator, db_user, count, all_rights))
    review_list.append(__get_optimization_dict(main_page, translator, db_user, count, all_rights))
    review_list.append(__get_edit_dict(main_page, translator, db_user, count, all_rights))
    review_list.append(__get_duplicates_dict(main_page, translator, db_user, count, all_rights))
    review_list.append(__get_split_dict(main_page, translator, db_user, count, all_rights))
    review_list.append(__get_merge_dict(main_page, translator, db_user, count, all_rights))
    review_list.append(__get_history_dict(main_page, translator, count, all_rights))

    if db_user.is_author() or db_user.is_admin():
        review_list.append(__get_ongoing_dict(main_page, translator))

    return review_list


def __get_delete_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: Users
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = get_review_count_for(ReviewDelete, LastReviewerDelete, db_user)

    tmp_dict = {'task_name': translator.get(_.queueDelete),
                'id': 'deletes',
                'url': main_page + '/review/' + key_delete,
                'icon': reputation_icons[key_delete],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_delete] or all_rights,
                'is_allowed_text': translator.get(_.visitDeleteQueue),
                'is_not_allowed_text': translator.get(_.visitDeleteQueueLimitation).format(
                    str(reputation_borders[key_delete])),
                'last_reviews': __get_last_reviewer_of(LastReviewerDelete, main_page)
                }
    return tmp_dict


def __get_optimization_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: User
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_optimization_dict', 'main')
    task_count = get_review_count_for(ReviewOptimization, LastReviewerOptimization, db_user)

    tmp_dict = {'task_name': translator.get(_.queueOptimization),
                'id': 'optimizations',
                'url': main_page + '/review/' + key_optimization,
                'icon': reputation_icons[key_optimization],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_optimization] or all_rights,
                'is_allowed_text': translator.get(_.visitOptimizationQueue),
                'is_not_allowed_text': translator.get(_.visitOptimizationQueueLimitation).format(
                    str(reputation_borders[key_optimization])),
                'last_reviews': __get_last_reviewer_of(LastReviewerOptimization, main_page)
                }
    return tmp_dict


def __get_edit_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: User
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_edit_dict', 'main')
    task_count = get_review_count_for(ReviewEdit, LastReviewerEdit, db_user)

    tmp_dict = {'task_name': translator.get(_.queueEdit),
                'id': 'edits',
                'url': main_page + '/review/' + key_edit,
                'icon': reputation_icons[key_edit],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_edit] or all_rights,
                'is_allowed_text': translator.get(_.visitEditQueue),
                'is_not_allowed_text': translator.get(_.visitEditQueueLimitation).format(
                    str(reputation_borders[key_edit])),
                'last_reviews': __get_last_reviewer_of(LastReviewerEdit, main_page)
                }
    return tmp_dict


def __get_duplicates_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section. QueueAdapter should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :param db_user: User
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_duplicates_dict', 'main')
    task_count = get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, db_user)

    tmp_dict = {'task_name': translator.get(_.queueDuplicate),
                'id': 'duplicates',
                'url': main_page + '/review/' + key_duplicate,
                'icon': reputation_icons[key_duplicate],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_duplicate] or all_rights,
                'is_allowed_text': translator.get(_.visitDuplicateQueue),
                'is_not_allowed_text': translator.get(_.visitDuplicateQueueLimitation).format(
                    str(reputation_borders[key_duplicate])),
                'last_reviews': __get_last_reviewer_of(LastReviewerDuplicate, main_page)
                }
    return tmp_dict


def __get_split_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: User
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = get_review_count_for(ReviewSplit, LastReviewerSplit, db_user)

    tmp_dict = {'task_name': translator.get(_.queueSplit),
                'id': 'splits',
                'url': main_page + '/review/' + key_split,
                'icon': reputation_icons[key_split],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_split] or all_rights,
                'is_allowed_text': translator.get(_.visitSplitQueue),
                'is_not_allowed_text': translator.get(_.visitSplitQueueLimitation).format(
                    str(reputation_borders[key_split])),
                'last_reviews': __get_last_reviewer_of(LastReviewerSplit, main_page)
                }
    return tmp_dict


def __get_merge_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: User
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = get_review_count_for(ReviewMerge, LastReviewerMerge, db_user)

    tmp_dict = {'task_name': translator.get(_.queueMerge),
                'id': 'merges',
                'url': main_page + '/review/' + key_merge,
                'icon': reputation_icons[key_merge],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_merge] or all_rights,
                'is_allowed_text': translator.get(_.visitMergeQueue),
                'is_not_allowed_text': translator.get(_.visitMergeQueueLimitation).format(
                    str(reputation_borders[key_merge])),
                'last_reviews': __get_last_reviewer_of(LastReviewerMerge, main_page)
                }
    return tmp_dict


def __get_history_dict(main_page, translator, count, all_rights):
    """
    Prepares dictionary for the a section. QueueAdapter should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_history_dict', 'main')
    tmp_dict = {'task_name': translator.get(_.queueHistory),
                'id': 'flags',
                'url': main_page + '/review/' + key_history,
                'icon': reputation_icons[key_history],
                'task_count': __get_review_count_for_history(True),
                'is_allowed': count >= reputation_borders[key_history] or all_rights,
                'is_allowed_text': translator.get(_.visitHistoryQueue),
                'is_not_allowed_text': translator.get(_.visitHistoryQueueLimitation).format(
                    str(reputation_borders[key_history])),
                'last_reviews': list()
                }
    return tmp_dict


def __get_ongoing_dict(main_page, translator):
    """
    Prepares dictionary for the a section. QueueAdapter should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_ongoing_dict', 'main')
    key = 'ongoing'
    tmp_dict = {'task_name': translator.get(_.queueOngoing),
                'id': 'flags',
                'url': main_page + '/review/' + key,
                'icon': reputation_icons[key_ongoing],
                'task_count': __get_review_count_for_history(False),
                'is_allowed': True,
                'is_allowed_text': translator.get(_.visitOngoingQueue),
                'is_not_allowed_text': '',
                'last_reviews': list()
                }
    return tmp_dict


def __get_review_count_for_history(is_executed):
    """

    :param is_executed:
    :return:
    """
    db_optimizations = DBDiscussionSession.query(ReviewOptimization).filter_by(is_executed=is_executed).all()
    db_deletes = DBDiscussionSession.query(ReviewDelete).filter_by(is_executed=is_executed).all()
    db_edits = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=is_executed).all()
    return len(db_optimizations) + len(db_deletes) + len(db_edits)


def __get_last_reviewer_of(reviewer_type, main_page):
    """
    Returns a list with the last reviewers of the given type. Multiple reviewers are filtered

    :param reviewer_type:
    :param main_page:
    :return:
    """
    #  logger('ReviewQueues', '__get_last_reviewer_of', 'main')
    users_array = list()
    db_reviews = DBDiscussionSession.query(reviewer_type).order_by(reviewer_type.uid.desc()).all()
    limit = min(5, len(db_reviews))
    index = 0
    while index < limit:
        db_review = db_reviews[index]
        db_user = DBDiscussionSession.query(User).get(db_review.reviewer_uid)
        if db_user:
            tmp_dict = dict()
            tmp_dict['img_src'] = get_profile_picture(db_user, 40)
            tmp_dict['url'] = main_page + '/user/' + str(db_user.uid)
            tmp_dict['name'] = db_user.global_nickname
            # skip it, if it is already in
            if tmp_dict in users_array:
                limit += 1 if len(db_reviews) > limit else 0
            else:
                users_array.append(tmp_dict)
        else:
            limit += 1 if len(db_reviews) > limit else 0
        index += 1
    return users_array


def lock_optimization_review(db_user: User, db_review: ReviewOptimization, translator: Translator):
    """
    Locks a ReviewOptimization

    :param db_user:
    :param db_review:
    :param translator:
    :return:
    """
    logger('ReviewQueues', 'main')
    # check if author locked an item and maybe tidy up old locks
    db_locks = DBDiscussionSession.query(OptimizationReviewLocks).filter_by(author_uid=db_user.uid).first()
    if db_locks:
        if is_review_locked(db_locks.review_optimization_uid):
            logger('ReviewQueues', 'review already locked')
            return {
                'success': '',
                'info': translator.get(_.dataAlreadyLockedByYou),
                'is_locked': True
            }
        else:
            DBDiscussionSession.query(OptimizationReviewLocks).filter_by(author_uid=db_user.uid).delete()

    # is already locked?
    if is_review_locked(db_review.uid):
        logger('ReviewQueues', 'already locked', warning=True)
        return {
            'success': '',
            'info': translator.get(_.dataAlreadyLockedByOthers),
            'is_locked': True
        }

    DBDiscussionSession.add(OptimizationReviewLocks(db_user.uid, db_review.uid))
    DBDiscussionSession.flush()
    transaction.commit()
    success = translator.get(_.dataAlreadyLockedByYou)

    logger('ReviewQueues', 'review locked')
    return {
        'success': success,
        'info': '',
        'is_locked': True
    }


def unlock_optimization_review(db_review: ReviewOptimization, translator: Translator):
    """
    Unlock the OptimizationReviewLocks

    :param db_review:
    :param translator:
    :return:
    """
    tidy_up_optimization_locks()
    logger('ReviewQueues', 'main')
    DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=db_review.uid).delete()
    DBDiscussionSession.flush()
    transaction.commit()
    return {
        'is_locked': False,
        'success': translator.get(_.dataUnlocked),
        'info': ''
    }


def is_review_locked(review_uid):
    """
    Is the OptimizationReviewLocks set?

    :param review_uid: OptimizationReviewLocks.uid
    :return: Boolean
    """
    tidy_up_optimization_locks()
    logger('ReviewQueues', 'main')
    db_lock = DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=review_uid).first()
    if not db_lock:
        return False
    return (get_now() - db_lock.locked_since).seconds < max_lock_time_in_sec


def tidy_up_optimization_locks():
    """
    Tidy up all expired locks

    :return: None
    """
    logger('ReviewQueues', 'main')
    db_locks = DBDiscussionSession.query(OptimizationReviewLocks).all()
    for lock in db_locks:
        if (get_now() - lock.locked_since).seconds >= max_lock_time_in_sec:
            DBDiscussionSession.query(OptimizationReviewLocks).filter_by(
                review_optimization_uid=lock.review_optimization_uid).delete()


def add_vote_for(db_user: User, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge,
                                                 ReviewOptimization, ReviewSplit], is_okay: bool,
                 db_reviewer_type: Union[LastReviewerDelete, LastReviewerDuplicate, LastReviewerEdit, LastReviewerMerge,
                                         LastReviewerOptimization, LastReviewerSplit]) -> True:
    """
    Add vote for a specific review

    :param db_user: User
    :param db_review: one table ouf of the Reviews
    :param is_okay: Boolean
    :param db_reviewer_type: one table out of the LastReviews
    :return: True, if the cote can be added
    """
    logger('review.lib', f'{db_reviewer_type}, user {db_user.uid}, db_review {db_review}, is_okay {is_okay}')
    already_voted = DBDiscussionSession.query(db_reviewer_type).filter(db_reviewer_type.reviewer_uid == db_user.uid,
                                                                       db_reviewer_type.review_uid == db_review.uid).first()
    if already_voted:
        logger('review.lib', 'already voted')
        return False

    logger('review.lib', 'vote added')
    db_new_review = db_reviewer_type(db_user.uid, db_review.uid, is_okay)
    DBDiscussionSession.add(db_new_review)
    DBDiscussionSession.flush()
    transaction.commit()
    return True
