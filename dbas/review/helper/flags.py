"""
Provides helping function for flagging arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from sqlalchemy import and_

from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, ReviewDeleteReason, ReviewDelete, ReviewOptimization, \
    Statement, User, ReviewDuplicate
from dbas.strings.keywords import Keywords as _


def flag_element(uid, reason, nickname, is_argument, extra_uid=None):
    """
    Flags an given argument based on the reason which was sent by the author. This argument will be enqueued
    for a review process.

    :param uid: Uid of the argument/statement, which should be flagged
    :param reason: String which describes the reason
    :param nickname: Users nickname
    :param is_argument: Boolean
    :param extra_uid: Uid of the argument/statement, which should be flagged
    :return: success, info, error
    """

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return '', '', _.noRights

    db_element = DBDiscussionSession.query(Argument if is_argument else Statement).get(uid)

    # we could have only one reason!
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).first()

    # sanity check
    if None in [db_element, db_user, db_reason] and reason not in ['optimization', 'duplicate']:
        logger('FlagingHelper', 'flag_element', 'Key error', error=True)
        return '', '', _.internalKeyError

    argument_uid = uid if is_argument else None
    statement_uid = uid if not is_argument else None

    # was this already flagged?
    flag_status = __get_flag_status(argument_uid, statement_uid, db_user.uid)
    if flag_status:
        logger('FlagingHelper', 'flag_element', 'already flagged')
        # who flagged this argument?
        return '', _.alreadyFlaggedByYou if flag_status == 'user' else _.alreadyFlaggedByOthers, ''

    # add flag
    else:
        if db_reason:
            # flagged for the first time
            __add_delete_review(argument_uid, statement_uid, db_user.uid, db_reason.uid)

        # and another reason for optimization
        elif reason == 'optimization':
            # flagged for the first time
            __add_optimization_review(argument_uid, statement_uid, db_user.uid)

        # and another reason for duplicates
        elif reason == 'duplicate':
            # flagged for the first time
            __add_duplication_review(statement_uid, extra_uid, db_user.uid)

        return _.thxForFlagText, '', ''


def __get_flag_status(argument_uid, statement_uid, user_uid):
    """
    Gets the status for a flag in of given argument/statement

    :param argument_uid: The uid of the argument to check.
    :param statement_uid: The uid of the statement to check
    :param user_uid: The uid of the user which may have flagged the argument/statement
    :return: 'user' if the user flagged the argument/statement, 'other' if someone else did, None if unflagged.
    """
    ret_val = None

    if any((__is_argument_flagged_for_delete_by_user(argument_uid, statement_uid, user_uid),
            __is_argument_flagged_for_optimization_by_user(argument_uid, statement_uid, user_uid),
            __is_argument_flagged_for_duplication_by_user(statement_uid, user_uid))):
        logger('FlagingHelper', '__get_flag_status', 'Already flagged by the user')
        return 'user'

    if any((__is_argument_flagged_for_delete(argument_uid, statement_uid),
            __is_argument_flagged_for_optimization(argument_uid, statement_uid),
            __is_argument_flagged_for_duplication(statement_uid))):
        logger('FlagingHelper', '__get_flag_status', 'Already flagged by others')
        return 'other'

    return ret_val


def __is_argument_flagged_for_delete(argument_uid, statement_uid, is_executed=False, is_revoked=False):
    """
    Check, if the argument is marked for delete by any user

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param is_executed: Boolean
    :param is_revoked: Boolean
    :return: Boolean
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
                                                                    ReviewDelete.statement_uid == statement_uid,
                                                                    ReviewDelete.is_executed == is_executed,
                                                                    ReviewDelete.is_revoked == is_revoked)).all()
    return len(db_review) > 0


def __is_argument_flagged_for_delete_by_user(argument_uid, statement_uid, user_uid, is_executed=False,
                                             is_revoked=False):
    """
    Check, if the argument is marked for delete by current user

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param is_executed: Boolean
    :param is_revoked: Boolean
    :return: Boolean
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
                                                                    ReviewDelete.statement_uid == statement_uid,
                                                                    ReviewDelete.is_executed == is_executed,
                                                                    ReviewDelete.detector_uid == user_uid,
                                                                    ReviewDelete.is_revoked == is_revoked)).all()
    return len(db_review) > 0


def __is_argument_flagged_for_optimization(argument_uid, statement_uid, is_executed=False, is_revoked=False):
    """
    Check, if the argument is marked for optimization by any user

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param is_executed: Boolean
    :param is_revoked: Boolean
    :return: Boolean
    """
    db_review = DBDiscussionSession.query(ReviewOptimization).filter(
        and_(ReviewOptimization.argument_uid == argument_uid,
             ReviewOptimization.statement_uid == statement_uid,
             ReviewOptimization.is_executed == is_executed,
             ReviewOptimization.is_revoked == is_revoked)).all()
    return len(db_review) > 0


def __is_argument_flagged_for_optimization_by_user(argument_uid, statement_uid, user_uid, is_executed=False,
                                                   is_revoked=False):
    """
    Check, if the argument is marked for optimization by current user

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param is_executed: Boolean
    :param is_revoked: Boolean
    :return: Boolean
    """
    db_review = DBDiscussionSession.query(ReviewOptimization).filter(
        and_(ReviewOptimization.argument_uid == argument_uid,
             ReviewOptimization.statement_uid == statement_uid,
             ReviewOptimization.is_executed == is_executed,
             ReviewOptimization.detector_uid == user_uid,
             ReviewOptimization.is_revoked == is_revoked)).all()
    return len(db_review) > 0


def __is_argument_flagged_for_duplication(statement_uid, is_executed=False, is_revoked=False):
    """
    Check, if the argument is marked as duplicate by any user

    :param statement_uid: Statement.uid
    :param is_executed: Boolean
    :param is_revoked: Boolean
    :return: Boolean
    """
    db_review = DBDiscussionSession.query(ReviewDuplicate).filter(
        and_(ReviewDuplicate.duplicate_statement_uid == statement_uid,
             ReviewDuplicate.is_executed == is_executed,
             ReviewDuplicate.is_revoked == is_revoked)).all()
    return len(db_review) > 0


def __is_argument_flagged_for_duplication_by_user(statement_uid, user_uid, is_executed=False, is_revoked=False):
    """
    Check, if the argument is marked as duplicate by current user

    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param is_executed:
    :param is_revoked:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewDuplicate).filter(
        and_(ReviewDuplicate.duplicate_statement_uid == statement_uid,
             ReviewDuplicate.is_executed == is_executed,
             ReviewDuplicate.detector_uid == user_uid,
             ReviewDuplicate.is_revoked == is_revoked)).all()
    return len(db_review) > 0


def __add_delete_review(argument_uid, statement_uid, user_uid, reason_uid):
    """
    Adds a ReviewDelete row

    :param argument_uid: Argument.uid
    :param statement_uid: Statement.uid
    :param user_uid: User.uid
    :param reason_uid: ReviewDeleteReason.uid
    :return: None
    """
    logger('FlagingHelper', 'flag_element', 'Flag argument/statement {}/{} by user {} for delete'.format(argument_uid, statement_uid, user_uid))
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
    logger('FlagingHelper', 'flag_element', 'Flag argument/statement {}/{} by user {} for optimization'.format(argument_uid, statement_uid, user_uid))
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
    logger('FlagingHelper', 'flag_element', 'Flag statement {} by user {} as duplicate of'.format(duplicate_statement_uid, user_uid, original_statement_uid))
    review_duplication = ReviewDuplicate(detector=user_uid, duplicate_statement=duplicate_statement_uid, original_statement=original_statement_uid)
    DBDiscussionSession.add(review_duplication)
    DBDiscussionSession.flush()
    transaction.commit()
