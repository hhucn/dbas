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
        argument_uid=argument_or_statement.uid if is_argument else None,
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
    del_reason: ReviewDeleteReasons = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason_val).first()

    if del_reason:
        _add_delete_review(argument if argument else None, statement if statement else None, user, del_reason)

    elif reason_val == key_optimization:
        _add_optimization_review(argument if argument else None, statement if statement else None, user)

    elif reason_val == key_duplicate:
        if statement.uid == extra_uid.uid:
            LOG.debug("uid Error")
            return {'success': '', 'info': tn.get(_.internalKeyError)}
        _add_duplication_review(statement, extra_uid, user)

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
        _add_merge_review(pgroup, db_user, text_values)
    elif key == key_split:
        _add_split_review(pgroup, db_user, text_values)

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


def _add_delete_review(argument: Optional[Argument], statement: Optional[Statement], user: User,
                       reason: Optional[ReviewDeleteReasons]):
    """
    Adds a ReviewDelete row

    :param argument: Argument to be deleted
    :param statement: Statement to be deleted
    :param user: User who wants to delete the argument or statement
    :param reason: The reason for the deletion
    :return: None
    """
    LOG.debug("Flag argument/statement %s/%s by user %s for delete", argument.argument_uid if argument else None,
              statement.uid if statement else None, user)
    review_delete = ReviewDelete(detector=user, argument=argument, statement=statement, reason=reason)
    DBDiscussionSession.add(review_delete)
    DBDiscussionSession.flush()
    transaction.commit()


def _add_optimization_review(argument: Optional[Argument], statement: Optional[Statement], user: User):
    """
    Adds a ReviewOptimization row

    :param argument: Argument.uid
    :param statement: Statement.uid
    :param user_uid: User.uid
    :return: None
    """
    LOG.debug("Flag argument/statement %s/%s by user %s for optimization", argument, statement, user.uid)
    review_optimization = ReviewOptimization(detector=user, argument=argument, statement=statement)
    DBDiscussionSession.add(review_optimization)
    DBDiscussionSession.flush()
    transaction.commit()


def _add_duplication_review(duplicate_statement: Statement, original_statement: Statement, user: User):
    """
    Adds a ReviewDuplicate row

    :param duplicate_statement: Statement
    :param original_statement: Statement
    :param user: User.uid
    :return: None
    """
    LOG.debug("Flag statement %s by user %s as duplicate of %s", duplicate_statement, user.uid, original_statement)
    review_duplication = ReviewDuplicate(detector=user, duplicate_statement=duplicate_statement,
                                         original_statement=original_statement)
    DBDiscussionSession.add(review_duplication)
    DBDiscussionSession.flush()  # vorsicht
    transaction.commit()  # vorsicht


def _add_split_review(premisegroup: PremiseGroup, detector: User, text_values: list):
    """
    Adds a row in the ReviewSplit table as well as the values, if not none

    :param premisegroup: Selected PremiseGroup
    :param detector: User object
    :param text_values: text values or None, if you want to split the premisegroup itself
    :return: None
    """
    LOG.debug("Flag pgroup %s by user %s for merging with additional values %s", premisegroup.uid, detector.uid,
              text_values)
    review_split = ReviewSplit(detector=detector, premisegroup=premisegroup)
    DBDiscussionSession.add(review_split)
    DBDiscussionSession.flush()

    if text_values:
        DBDiscussionSession.add_all(
            [ReviewSplitValues(review=review_split, content=value) for value in text_values])
        DBDiscussionSession.flush()

    transaction.commit()


def _add_merge_review(premisegroup: PremiseGroup, detector: User, text_values: list):
    """
    Adds a row in the ReviewMerge table as well as the values, if not none

    :param premisegroup: Selected PremiseGroup
    :param detector: User object
    :param text_values: text values or None, if you want to merge the premisegroup itself
    :return: None
    """
    LOG.debug("Flag pgroup %s by user %s for merging with additional values %s", premisegroup.uid, detector.uid,
              text_values)
    review_merge = ReviewMerge(detector=detector, premisegroup=premisegroup)
    DBDiscussionSession.add(review_merge)
    DBDiscussionSession.flush()

    if text_values:
        DBDiscussionSession.add_all(
            [ReviewMergeValues(review=review_merge, content=value) for value in text_values])
        DBDiscussionSession.flush()

    transaction.commit()
