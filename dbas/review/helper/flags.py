"""
Provides helping function for flagging arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, ReviewDeleteReason, ReviewDelete, ReviewOptimization, Statement


def flag_argument(uid, reason, nickname, translator, is_argument, transaction):
    """
    Flags an given argument based on the reason which was sent by the author. This argument will be enqueued
    for a review process.

    :param uid: Uid of the argument/statement, which should be flagged
    :param reason: String which describes the reason
    :param nickname: Nickname of the requests sender
    :param translator: Class of String-Translator
    :param is_argument: Boolean whether the uid is for an argument
    :param transaction: current transaction
    :return:
    """
    if is_argument:
        db_element = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
    else:
        db_element = DBDiscussionSession.query(Statement).filter_by(uid=uid).first()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    # we could have only one reason!
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).first()

    # sanity check
    # if not db_element or not db_user or not (db_reason is not None or reason == 'optimization'):
    if not db_element or not db_user or db_reason is None and reason != 'optimization':
        return '', '', translator.get(translator.internalKeyError)

    ret_success = ''
    ret_info = ''
    ret_error = ''

    argument_uid = uid if is_argument else None
    statement_uid = None if is_argument else uid

    is_flagged_for_delete_by_user = __is_argument_flagged_for_delete_by_user(argument_uid, statement_uid, db_user.uid)
    is_flagged_for_delete_by_others = __is_argument_flagged_for_delete(argument_uid, statement_uid)
    is_flagged_for_optimization_by_user = __is_argument_flagged_for_optimization_by_user(argument_uid, statement_uid, db_user.uid)
    is_flagged_for_optimization_by_others = __is_argument_flagged_for_optimization(argument_uid, statement_uid)
    is_flagged_by_user = is_flagged_for_delete_by_user or is_flagged_for_optimization_by_user
    is_flagged_by_others = is_flagged_for_delete_by_others or is_flagged_for_optimization_by_others

    # was this already flagged?
    if db_reason or reason == 'optimization':
        # does the user has already flagged this argument?
        if is_flagged_by_user:
            ret_info = translator.get(translator.alreadyFlaggedByYou)
            return ret_success, ret_info, ret_error

        # was this argument flagged already?
        if is_flagged_by_others:
            ret_info = translator.get(translator.alreadyFlaggedByOthers)
            return ret_success, ret_info, ret_error

    # add flag
    if db_reason:
        # flagged for the first time
        __add_delete_review(argument_uid, statement_uid, db_user.uid, db_reason.uid, transaction)
        ret_success = translator.get(translator.thxForFlagText)

    # and another reason for optimization
    elif reason == 'optimization':
        # flagged for the first time
        __add_optimization_review(argument_uid, statement_uid, db_user.uid, transaction)
        ret_success = translator.get(translator.thxForFlagText)

    # or unknown reason
    else:
        ret_error = translator.get(translator.internalKeyError)

    return ret_success, ret_info, ret_error


def __is_argument_flagged_for_delete(argument_uid, statement_uid, is_executed=False, is_revoked=False):
    """

    :param argument_uid:
    :param statement_uid:
    :param is_executed:
    :param is_revoked:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
                                                                    ReviewDelete.statement_uid == statement_uid,
                                                                    ReviewDelete.is_executed == is_executed,
                                                                    ReviewDelete.is_revoked == is_revoked)).all()
    return True if len(db_review) > 0 else False


def __is_argument_flagged_for_delete_by_user(argument_uid, statement_uid, user_uid, is_executed=False, is_revoked=False):
    """

    :param argument_uid:
    :param statement_uid:
    :param user_uid:
    :param is_executed:
    :param is_revoked:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
                                                                    ReviewDelete.statement_uid == statement_uid,
                                                                    ReviewDelete.is_executed == is_executed,
                                                                    ReviewDelete.detector_uid == user_uid,
                                                                    ReviewDelete.is_revoked == is_revoked)).all()
    return True if len(db_review) > 0 else False


def __is_argument_flagged_for_optimization(argument_uid, statement_uid, is_executed=False, is_revoked=False):
    """

    :param argument_uid:
    :param statement_uid:
    :param is_executed:
    :param is_revoked:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.argument_uid == argument_uid,
                                                                          ReviewOptimization.statement_uid == statement_uid,
                                                                          ReviewOptimization.is_executed == is_executed,
                                                                          ReviewOptimization.is_revoked == is_revoked)).all()
    return True if len(db_review) > 0 else False


def __is_argument_flagged_for_optimization_by_user(argument_uid, statement_uid, user_uid, is_executed=False, is_revoked=False):
    """

    :param argument_uid:
    :param statement_uid:
    :param user_uid:
    :param is_executed:
    :param is_revoked:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.argument_uid == argument_uid,
                                                                          ReviewOptimization.statement_uid == statement_uid,
                                                                          ReviewOptimization.is_executed == is_executed,
                                                                          ReviewOptimization.detector_uid == user_uid,
                                                                          ReviewOptimization.is_revoked == is_revoked)).all()
    return True if len(db_review) > 0 else False


def __add_delete_review(argument_uid, statement_uid, user_uid, reason_uid, transaction):
    """

    :param argument_uid:
    :param statement_uid:
    :param user_uid:
    :param reason_uid:
    :param transaction:
    :return:
    """
    review_delete = ReviewDelete(detector=user_uid, argument=argument_uid, statement=statement_uid, reason=reason_uid)
    DBDiscussionSession.add(review_delete)
    DBDiscussionSession.flush()
    transaction.commit()


def __add_optimization_review(argument_uid, statement_uid, user_uid, transaction):
    """

    :param argument_uid:
    :param statement_uid:
    :param user_uid:
    :param transaction:
    :return:
    """
    review_optimization = ReviewOptimization(detector=user_uid, argument=argument_uid, statement=statement_uid)
    DBDiscussionSession.add(review_optimization)
    DBDiscussionSession.flush()
    transaction.commit()
