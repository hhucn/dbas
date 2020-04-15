"""
Provides helping function for flagging arguments.
"""

import logging
from typing import Union, Optional

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDeleteReason, ReviewDelete, ReviewOptimization, \
    User, ReviewDuplicate, ReviewSplit, ReviewMerge, ReviewMergeValues, ReviewSplitValues, \
    PremiseGroup, Statement, Argument
from dbas.review import FlaggedBy, ReviewDeleteReasons
from dbas.review.queue import key_merge, key_split, key_duplicate, key_optimization
from dbas.review.queue.adapter import QueueAdapter
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


def flag_element(argument_or_statement: Union[Argument, Statement],
                 reason: Union[key_duplicate, key_optimization, ReviewDeleteReasons], user: User,
                 is_argument: bool, ui_locales: str, extra_uid: Statement = None) -> dict:
    """
    Flags an given argument based on the reason which was sent by the author. This argument will be enqueued
    for a review process.

    :param argument_or_statement: argument/statement, which should be flagged
    :param reason: String which describes the reason
    :param user: User
    :param is_argument: Boolean
    :param ui_locales: ui_locales
    :param extra_uid: Uid of the argument/statement, which should be flagged
    :return: success, info, error
    """
    tn = Translator(ui_locales)

    # was this already flagged?
    flag_status = QueueAdapter(db_user=user).element_in_queue(
        argument_uid=argument_or_statement.argument_uid if is_argument else None,
        statement_uid=argument_or_statement.uid if not is_argument else None,
        premisegroup_uid=None)
    if flag_status:
        LOG.debug("Already flagged by %s", flag_status)
        if flag_status == FlaggedBy.user:
            info = tn.get(_.alreadyFlaggedByYou)
        else:
            info = tn.get(_.alreadyFlaggedByOthers)
        return {'success': '', 'info': info}

    if is_argument:
        return _add_flag(reason, argument_or_statement, None, extra_uid, user, tn)

    return _add_flag(reason, None, argument_or_statement, extra_uid, user, tn)


def _add_flag(reason: Union[key_duplicate, key_optimization, ReviewDeleteReasons], argument: Optional[Argument],
              statement: Optional[Statement], extra_uid: Optional[Statement], user: User, tn: Translator) -> dict:
    """

    :param reason:
    :param argument:
    :param statement:
    :param extra_uid:
    :param user:
    :param tn:
    :return:
    """
    reason_val = reason.value if isinstance(reason, ReviewDeleteReasons) else reason
    db_del_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason_val).first()

    if db_del_reason:
        _add_delete_review(argument if argument else None, statement.uid if statement else None, user,
                           db_del_reason.uid)

    elif reason_val == key_optimization:
        _add_optimization_review(argument.argument_uid if argument else None, statement.uid if statement else None,
                                 user.uid)

    elif reason_val == key_duplicate:
        if statement.uid == extra_uid.uid:
            LOG.debug("uid Error")
            return {'success': '', 'info': tn.get(_.internalKeyError)}
        _add_duplication_review(statement, extra_uid, user.uid)

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
        _add_merge_review(pgroup.uid, db_user.uid, text_values)
    elif key == key_split:
        _add_split_review(pgroup.uid, db_user.uid, text_values)

    success = tn.get(_.thxForFlagText)
    return {'success': success, 'info': ''}


def flag_pgroup_for_merge_or_split(key: str, pgroup: PremiseGroup, db_user: User, tn: Translator) -> dict:
    """
    Flags a premisegroup for a merge or split event. On split the premisegroup will be divided into independent groups.
    On merge the statements of this group will be one statement.

    :param key: either 'split' or 'merge'
    :param pgroup: ID of the selected PremiseGroup
    :param db_user: current user
    :param tn: The translator used
    :return: success, info
    """
    LOG.debug("Flag pgroup %s for a %s", pgroup.uid, key)
    return flag_statement_for_merge_or_split(key, pgroup, [], db_user, tn)


def _add_delete_review(argument: Optional[Argument], statement_uid, user: User, reason_uid):
    """
    Adds a ReviewDelete row

    :param argument: Argument.uid
    :param statement_uid: Statement.uid
    :param user: User.uid
    :param reason_uid: ReviewDeleteReason.uid
    :return: None
    """
    LOG.debug("Flag argument/statement %s/%s by user %s for delete", argument.argument_uid if argument else None,
              statement_uid, user)
    review_delete = ReviewDelete(detector=user, argument=argument, statement=statement_uid, reason=reason_uid)
    DBDiscussionSession.add(review_delete)
    DBDiscussionSession.flush()
    transaction.commit()


def _add_optimization_review(argument_uid, statement_uid, user_uid):
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


def _add_duplication_review(duplicate_statement: Statement, original_statement: Statement, user_uid):
    """
    Adds a ReviewDuplicate row

    :param duplicate_statement: Statement
    :param original_statement: Statement
    :param user_uid: User.uid
    :return: None
    """
    LOG.debug("Flag statement %s by user %s as duplicate of %s", duplicate_statement, user_uid,
              original_statement)
    review_duplication = ReviewDuplicate(detector=user_uid, duplicate_statement=duplicate_statement,
                                         original_statement=original_statement)
    DBDiscussionSession.add(review_duplication)
    DBDiscussionSession.flush()  # vorsicht
    transaction.commit()  # vorsicht


def _add_split_review(pgroup_uid, user_uid, text_values):
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


def _add_merge_review(pgroup_uid, user_uid, text_values):
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
