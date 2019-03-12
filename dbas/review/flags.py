"""
Provides helping function for flagging arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
from typing import Union, Optional

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDeleteReason, ReviewDelete, ReviewOptimization, \
    User, ReviewDuplicate, ReviewSplit, ReviewMerge, ReviewMergeValues, ReviewSplitValues, \
    PremiseGroup
from dbas.review import FlaggedBy, ReviewDeleteReasons
from dbas.review.queue import key_merge, key_split, key_duplicate, key_optimization
from dbas.review.queue.adapter import QueueAdapter
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


def flag_element(uid: int, reason: Union[key_duplicate, key_optimization, ReviewDeleteReasons], db_user: User,
                 is_argument: bool, ui_locales: str, extra_uid=None) -> dict:
    """
    Flags an given argument based on the reason which was sent by the author. This argument will be enqueued
    for a review process.

    :param uid: Uid of the argument/statement, which should be flagged
    :param reason: String which describes the reason
    :param db_user: User
    :param is_argument: Boolean
    :param ui_locales: ui_locales
    :param extra_uid: Uid of the argument/statement, which should be flagged
    :return: success, info, error
    """
    tn = Translator(ui_locales)

    argument_uid = uid if is_argument else None
    statement_uid = uid if not is_argument else None

    # was this already flagged?
    flag_status = QueueAdapter(db_user=db_user).element_in_queue(argument_uid=argument_uid,
                                                                 statement_uid=statement_uid,
                                                                 premisegroup_uid=None)
    if flag_status:
        LOG.debug("Already flagged by %s", flag_status)
        if flag_status == FlaggedBy.user:
            info = tn.get(_.alreadyFlaggedByYou)
        else:
            info = tn.get(_.alreadyFlaggedByOthers)
        return {'success': '', 'info': info}

    return __add_flag(reason, argument_uid, statement_uid, extra_uid, db_user, tn)


def __add_flag(reason: Union[key_duplicate, key_optimization, ReviewDeleteReasons], argument_uid: Union[int, None],
               statement_uid: Optional[int], extra_uid: Optional[int], db_user: User, tn: Translator) -> dict:
    """

    :param reason:
    :param argument_uid:
    :param statement_uid:
    :param extra_uid:
    :param db_user:
    :param tn:
    :return:
    """
    reason_val = reason.value if isinstance(reason, ReviewDeleteReasons) else reason
    db_del_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason_val).first()
    if db_del_reason:
        __add_delete_review(argument_uid, statement_uid, db_user.uid, db_del_reason.uid)

    elif reason_val == key_optimization:
        __add_optimization_review(argument_uid, statement_uid, db_user.uid)

    elif reason_val == key_duplicate:
        if statement_uid == extra_uid:
            LOG.debug("uid Error")
            return {'success': '', 'info': tn.get(_.internalKeyError)}
        __add_duplication_review(statement_uid, extra_uid, db_user.uid)

    return {'success': tn.get(_.thxForFlagText), 'info': ''}


def flag_statement_for_merge_or_split(key: str, pgroup: PremiseGroup, text_values: list, db_user: User,
                                      tn: Translator) -> dict:
    """
    Flags a statement for a merge or split event. On split, the statement of the pgroup will be split into the
    given text_values. On merge the statements of the pgroup will be connected by an and.

    :param key: either 'split' or 'merge'
    :param pgroup: ID of the selected PremiseGroup
    :param text_values: text values
    :param db_user: current user
    :param tn: The translator used
    :return: success, info
    """
    LOG.debug("Flag statements in pgroup %s for a %s with values %s", pgroup.uid, key, text_values)
    # was this already flagged?
    flag_status = QueueAdapter(db_user=db_user).element_in_queue(argument_uid=None,
                                                                 statement_uid=None,
                                                                 premisegroup_uid=pgroup.uid)
    if flag_status:
        LOG.debug("Already flagged")
        if flag_status == FlaggedBy.user:
            info = tn.get(_.alreadyFlaggedByYou)
        else:
            info = tn.get(_.alreadyFlaggedByOthers)
        return {'success': '', 'info': info}

    if key == key_merge:
        __add_merge_review(pgroup.uid, db_user.uid, text_values)
    elif key == key_split:
        __add_split_review(pgroup.uid, db_user.uid, text_values)

    success = tn.get(_.thxForFlagText)
    return {'success': success, 'info': ''}


def flag_pgroup_for_merge_or_split(key: str, pgroup: PremiseGroup, db_user: User, tn: Translator) -> dict:
    """
    Flags a premisegroup for a merge or split event. On split the premisegroup will be divided into indepent groups.
    On merge the statements of this group will be one statement.

    :param key: either 'split' or 'merge'
    :param pgroup: ID of the selected PremiseGroup
    :param db_user: current user
    :param tn: The translator used
    :return: success, info
    """
    LOG.debug("Flag pgroup %s for a %s", pgroup.uid, key)
    return flag_statement_for_merge_or_split(key, pgroup, [], db_user, tn)


def __add_delete_review(argument_uid, statement_uid, user_uid, reason_uid):
    """
    Adds a ReviewDelete row

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param reason_uid: ReviewDeleteReason.uid
    :return: None
    """
    LOG.debug("Flag argument/statement %s/%s by user %s for delete", argument_uid, statement_uid, user_uid)
    review_delete = ReviewDelete(detector=user_uid, argument=argument_uid, statement=statement_uid, reason=reason_uid)
    DBDiscussionSession.add(review_delete)
    DBDiscussionSession.flush()
    transaction.commit()


def __add_optimization_review(argument_uid, statement_uid, user_uid):
    """
    Adds a ReviewOptimization row

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :return: None
    """
    LOG.debug("Flag argument/statement %s/%s by user %s for optimization", argument_uid, statement_uid, user_uid)
    review_optimization = ReviewOptimization(detector=user_uid, argument=argument_uid, statement=statement_uid)
    DBDiscussionSession.add(review_optimization)
    DBDiscussionSession.flush()
    transaction.commit()


def __add_duplication_review(duplicate_statement_uid, original_statement_uid, user_uid):
    """
    Adds a ReviewDuplicate row

    :param duplicate_statement_uid: Statement.uid
    :param original_statement_uid: Statement.uid
    :param user_uid: User.uid
    :return: None
    """
    LOG.debug("Flag statement %s by user %s as duplicate of %s", duplicate_statement_uid, user_uid,
              original_statement_uid)
    review_duplication = ReviewDuplicate(detector=user_uid, duplicate_statement=duplicate_statement_uid,
                                         original_statement=original_statement_uid)
    DBDiscussionSession.add(review_duplication)
    DBDiscussionSession.flush()
    transaction.commit()


def __add_split_review(pgroup_uid, user_uid, text_values):
    """
    Adds a row in the ReviewSplit table as well as the values, if not none

    :param pgroup_uid: ID of the selected PremiseGroup
    :param user_uid: ID of the user
    :param text_values: text values or None, if you want to split the premisegroup itself
    :return: None
    """
    LOG.debug("Flag pgroup %s by user %s for merging with additional values %s", pgroup_uid, user_uid, text_values)
    review_split = ReviewSplit(detector=user_uid, premisegroup=pgroup_uid)
    DBDiscussionSession.add(review_split)
    DBDiscussionSession.flush()

    if text_values:
        DBDiscussionSession.add_all(
            [ReviewSplitValues(review=review_split.uid, content=value) for value in text_values])
        DBDiscussionSession.flush()

    transaction.commit()


def __add_merge_review(pgroup_uid, user_uid, text_values):
    """
    Adds a row in the ReviewMerge table as well as the values, if not none

    :param pgroup_uid: ID of the selected PremiseGroup
    :param user_uid: ID of the user
    :param text_values: text values or None, if you want to merge the premisegroup itself
    :return: None
    """
    LOG.debug("Flag pgroup %s by user %s for merging with additional values %s", pgroup_uid, user_uid, text_values)
    review_merge = ReviewMerge(detector=user_uid, premisegroup=pgroup_uid)
    DBDiscussionSession.add(review_merge)
    DBDiscussionSession.flush()

    if text_values:
        DBDiscussionSession.add_all(
            [ReviewMergeValues(review=review_merge.uid, content=value) for value in text_values])
        DBDiscussionSession.flush()

    transaction.commit()
