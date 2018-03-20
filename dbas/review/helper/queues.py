"""
Provides helping function for displaying the review queues and locking entries.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from enum import Enum, auto

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, ReviewOptimization, TextVersion, \
    LastReviewerOptimization, ReviewEdit, LastReviewerEdit, OptimizationReviewLocks, ReviewEditValue, get_now, \
    Statement, ReviewDuplicate, LastReviewerDuplicate, Argument, Premise, ReviewMerge, ReviewSplit, \
    LastReviewerMerge, LastReviewerSplit
from dbas.lib import get_profile_picture
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of, reputation_icons, reputation_borders
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

max_lock_time_in_sec = 180

key_deletes = 'deletes'
key_optimizations = 'optimizations'
key_edits = 'edits'
key_duplicates = 'duplicates'
key_merge = 'merges'
key_split = 'splits'
key_history = 'history'
key_ongoing = 'ongoing'

review_queues = [
    key_deletes,
    key_optimizations,
    key_edits,
    key_duplicates,
    key_merge,
    key_split
]

title_mapping = {
    key_deletes: _.queueDelete,
    key_optimizations: _.queueOptimization,
    key_edits: _.queueEdit,
    key_duplicates: _.queueDuplicates,
    key_split: _.queueSplit,
    key_merge: _.queueMerge
}

model_mapping = {
    key_deletes: ReviewDelete,
    key_optimizations: ReviewOptimization,
    key_edits: ReviewEdit,
    key_duplicates: ReviewDuplicate,
    key_split: ReviewSplit,
    key_merge: ReviewMerge
}


class _Code(Enum):
    DOESNT_EXISTS = auto()
    DUPLICATE = auto()
    SUCCESS = auto()
    ERROR = auto()


def get_review_queues_as_lists(main_page, translator, nickname):
    """
    Prepares dictionary for the edit section.

    :param main_page: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Array
    """
    logger('ReviewQueues', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None
    count, all_rights = get_reputation_of(nickname)

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


def get_count_of_all():
    reviews = [ReviewDelete, ReviewOptimization, ReviewEdit, ReviewDuplicate, ReviewSplit, ReviewMerge]
    count = [DBDiscussionSession.query(r).count() for r in reviews]
    return sum(count)


def get_complete_review_count(db_user: User) -> int:
    """
    Sums up the review points of the user

    :param db_user: User
    :return: int
    """
    count, all_rights = get_reputation_of(db_user)

    rights1 = count >= reputation_borders[key_deletes] or all_rights
    rights2 = count >= reputation_borders[key_optimizations] or all_rights
    rights3 = count >= reputation_borders[key_edits] or all_rights
    rights4 = count >= reputation_borders[key_duplicates] or all_rights
    rights5 = count >= reputation_borders[key_split] or all_rights
    rights6 = count >= reputation_borders[key_merge] or all_rights

    count = [
        __get_review_count_for(ReviewDelete, LastReviewerDelete, db_user) if rights1 else 0,
        __get_review_count_for(ReviewOptimization, LastReviewerOptimization, db_user) if rights2 else 0,
        __get_review_count_for(ReviewEdit, LastReviewerEdit, db_user) if rights3 else 0,
        __get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, db_user) if rights4 else 0,
        __get_review_count_for(ReviewSplit, LastReviewerSplit, db_user) if rights5 else 0,
        __get_review_count_for(ReviewMerge, LastReviewerMerge, db_user) if rights6 else 0,
    ]

    return sum(count)


def __get_delete_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section.

    :param main_page: URL
    :param translator: Translator
    :param db_user: Users
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_delete_dict', 'main')
    task_count = __get_review_count_for(ReviewDelete, LastReviewerDelete, db_user)

    tmp_dict = {'task_name': translator.get(_.queueDelete),
                'id': 'deletes',
                'url': main_page + '/review/' + key_deletes,
                'icon': reputation_icons[key_deletes],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_deletes] or all_rights,
                'is_allowed_text': translator.get(_.visitDeleteQueue),
                'is_not_allowed_text': translator.get(_.visitDeleteQueueLimitation).format(str(reputation_borders[key_deletes])),
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
    task_count = __get_review_count_for(ReviewOptimization, LastReviewerOptimization, db_user)

    tmp_dict = {'task_name': translator.get(_.queueOptimization),
                'id': 'optimizations',
                'url': main_page + '/review/' + key_optimizations,
                'icon': reputation_icons[key_optimizations],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_optimizations] or all_rights,
                'is_allowed_text': translator.get(_.visitOptimizationQueue),
                'is_not_allowed_text': translator.get(_.visitOptimizationQueueLimitation).format(str(reputation_borders[key_optimizations])),
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
    task_count = __get_review_count_for(ReviewEdit, LastReviewerEdit, db_user)

    tmp_dict = {'task_name': translator.get(_.queueEdit),
                'id': 'edits',
                'url': main_page + '/review/' + key_edits,
                'icon': reputation_icons[key_edits],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_edits] or all_rights,
                'is_allowed_text': translator.get(_.visitEditQueue),
                'is_not_allowed_text': translator.get(_.visitEditQueueLimitation).format(str(reputation_borders[key_edits])),
                'last_reviews': __get_last_reviewer_of(LastReviewerEdit, main_page)
                }
    return tmp_dict


def __get_duplicates_dict(main_page, translator, db_user, count, all_rights):
    """
    Prepares dictionary for the a section. Queue should be added iff the user is author!

    :param main_page: URL
    :param translator: Translator
    :param db_user: User
    :return: Dict()
    """
    #  logger('ReviewQueues', '__get_duplicates_dict', 'main')
    task_count = __get_review_count_for(ReviewDuplicate, LastReviewerDuplicate, db_user)

    tmp_dict = {'task_name': translator.get(_.queueDuplicates),
                'id': 'duplicates',
                'url': main_page + '/review/' + key_duplicates,
                'icon': reputation_icons[key_duplicates],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_duplicates] or all_rights,
                'is_allowed_text': translator.get(_.visitDuplicateQueue),
                'is_not_allowed_text': translator.get(_.visitDuplicateQueueLimitation).format(str(reputation_borders[key_duplicates])),
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
    task_count = __get_review_count_for(ReviewSplit, LastReviewerSplit, db_user)

    tmp_dict = {'task_name': translator.get(_.queueSplit),
                'id': 'splits',
                'url': main_page + '/review/' + key_split,
                'icon': reputation_icons[key_split],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_split] or all_rights,
                'is_allowed_text': translator.get(_.visitSplitQueue),
                'is_not_allowed_text': translator.get(_.visitSplitQueueLimitation).format(str(reputation_borders[key_split])),
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
    task_count = __get_review_count_for(ReviewMerge, LastReviewerMerge, db_user)

    tmp_dict = {'task_name': translator.get(_.queueMerge),
                'id': 'merges',
                'url': main_page + '/review/' + key_merge,
                'icon': reputation_icons[key_merge],
                'task_count': task_count,
                'is_allowed': count >= reputation_borders[key_merge] or all_rights,
                'is_allowed_text': translator.get(_.visitMergeQueue),
                'is_not_allowed_text': translator.get(_.visitMergeQueueLimitation).format(str(reputation_borders[key_merge])),
                'last_reviews': __get_last_reviewer_of(LastReviewerMerge, main_page)
                }
    return tmp_dict


def __get_history_dict(main_page, translator, count, all_rights):
    """
    Prepares dictionary for the a section. Queue should be added iff the user is author!

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
                'is_not_allowed_text': translator.get(_.visitHistoryQueueLimitation).format(str(reputation_borders[key_history])),
                'last_reviews': list()
                }
    return tmp_dict


def __get_ongoing_dict(main_page, translator):
    """
    Prepares dictionary for the a section. Queue should be added iff the user is author!

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


def __get_review_count_for(review_type, last_reviewer_type, db_user):
    """
    Returns the count of reviews of *review_type* for the user with *nickname*, whereby all reviewed data
    of *last_reviewer_type* are not observed

    :param review_type: ReviewEdit, ReviewOptimization or ...
    :param last_reviewer_type: LastReviewerEdit, LastReviewer...
    :param db_user: User
    :return: Integer
    """
    #  logger('ReviewQueues', '__get_review_count_for', 'main')
    if not db_user:
        db_reviews = DBDiscussionSession.query(review_type).filter_by(is_executed=False).all()
        return len(db_reviews)

    # get all reviews but filter reviews, which
    # - the user has detected
    # - the user has reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = []
    for last_review in db_last_reviews_of_user:
        already_reviewed.append(last_review.review_uid)
    db_reviews = DBDiscussionSession.query(review_type).filter(review_type.is_executed == False,
                                                               review_type.detector_uid != db_user.uid)

    if len(already_reviewed) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_reviewed))
    db_reviews = db_reviews.all()

    return len(db_reviews)


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


def add_proposals_for_statement_corrections(elements, db_user, _tn):
    """
    Add a proposal to correct a statement

    :param elements: [Strings]
    :param db_user: User
    :param _tn: Translator
    :return: String, Boolean for Error
    """
    logger('ReviewQueues', 'main')

    review_count = len(elements)
    added_reviews = [__add_edit_reviews(el, db_user) for el in elements]

    if added_reviews.count(_Code.SUCCESS) == 0:  # no edits set
        if added_reviews.count(_Code.DOESNT_EXISTS) > 0:
            logger('ReviewQueues', 'internal key error')
            return _tn.get(_.internalKeyError), True
        if added_reviews.count(_Code.DUPLICATE) > 0:
            logger('ReviewQueues', 'already edit proposals')
            return _tn.get(_.alreadyEditProposals), True
        logger('ReviewQueues', 'no corrections given')
        return _tn.get(_.noCorrections), True

    DBDiscussionSession.flush()
    transaction.commit()

    added_values = [__add_edit_values_review(element, db_user) for element in elements]
    if added_values == 0:
        return _tn.get(_.alreadyEditProposals), True
    DBDiscussionSession.flush()
    transaction.commit()

    msg = ''
    if review_count > added_values.count(1) or added_reviews.count(1) != added_values.count(1):
        msg = _tn.get(_.alreadyEditProposals)

    return msg, False


def __add_edit_reviews(element, db_user):
    """
    Setup a new ReviewEdit row

    :param element: String
    :param db_user: User
    :return: -1 if the statement of the element does not exists, -2 if this edit already exists, 1 on success, 0 otherwise
    """
    logger('ReviewQueues', 'current element: {}'.format(element))
    db_statement = DBDiscussionSession.query(Statement).get(element['uid'])
    if not db_statement:
        logger('ReviewQueues', 'statement {} not found (return -1)'.format(element['uid']))
        return _Code.DOESNT_EXISTS

    # already set an correction for this?
    if is_statement_in_edit_queue(element['uid']):  # if we already have an edit, skip this
        logger('ReviewQueues', '{} already got an edit (return -2)'.format(element['uid']))
        return _Code.DUPLICATE

    # is text different?
    db_tv = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)
    if len(element['text']) > 0 and db_tv.content.lower().strip() != element['text'].lower().strip():
        logger('ReviewQueues', 'added review element for {}  (return 1)'.format(element['uid']))
        DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, statement=element['uid']))
        return _Code.SUCCESS

    return _Code.ERROR


def is_statement_in_edit_queue(uid: int, is_executed: bool = False) -> bool:
    """
    Returns true if the statement is not in the edit queue

    :param uid: Statement.uid
    :param is_executed: Bool
    :return: Boolean
    """
    logger('ReviewQueues', 'current element: {}'.format(uid))
    db_already_edit_count = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.statement_uid == uid,
                                                                         ReviewEdit.is_executed == is_executed).count()
    return db_already_edit_count > 0


def is_arguments_premise_in_edit_queue(db_argument: Argument, is_executed: bool = False) -> bool:
    """
    Returns true if the premises of an argument are not in the edit queue

    :param db_argument: Argument
    :param is_executed: Bool
    :return: Boolean
    """
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    dbp_uid = [p.uid for p in db_premises]
    db_already_edit_count = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.statement_uid.in_(dbp_uid),
                                                                         ReviewEdit.is_executed == is_executed).count()
    return db_already_edit_count > 0


def __add_edit_values_review(element, db_user):
    """
    Setup a new ReviewEditValue row

    :param element: String
    :param db_user: User
    :return: 1 on success, 0 otherwise
    """
    logger('ReviewQueues', 'current element: ' + str(element))
    db_statement = DBDiscussionSession.query(Statement).get(element['uid'])
    if not db_statement:
        logger('ReviewQueues', str(element['uid']) + ' not found')
        return 0

    db_textversion = DBDiscussionSession.query(TextVersion).get(db_statement.textversion_uid)

    if len(element['text']) > 0 and db_textversion.content.lower().strip() != element['text'].lower().strip():
        db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(ReviewEdit.detector_uid == db_user.uid,
                                                                      ReviewEdit.statement_uid == element['uid']).order_by(ReviewEdit.uid.desc()).first()
        DBDiscussionSession.add(ReviewEditValue(db_review_edit.uid, element['uid'], 'statement', element['text']))
        logger('ReviewQueues', '{} - \'{}\' accepted'.format(element['uid'], element['text']))
        return 1
    else:
        logger('ReviewQueues', '{} - \'{}\' malicious edit'.format(element['uid'], element['text']))
        return 0


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
        'is_locked':  False,
        'success':  translator.get(_.dataUnlocked),
        'info':  ''
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
            DBDiscussionSession.query(OptimizationReviewLocks).filter_by(review_optimization_uid=lock.review_optimization_uid).delete()
