"""
Provides helping function for flagging arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, ReviewDeleteReason, ReviewDelete, ReviewOptimization


def flag_argument(argument_uid, reason, nickname, translator, transaction):
    """

    :param argument_uid: Uid of the argument, which should be flagged
    :param reason:
    :param nickname:
    :param translator:
    :return:
    """
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).all()
    if not db_argument or not db_user or not (len(db_reason) > 0 or reason == 'optimization'):
        return translator.get(translator.internalKeyError)

    ret_success = ''
    ret_info = ''
    ret_error = ''

    # notification to the author of the flagged argument

    # was this argument flagged already?
    if __is_argument_flagged_for_delete(argument_uid, is_executed=False) or __is_argument_flagged_for_optimization(db_argument, is_executed=False):
        ret_info = translator.get(translator.alreadyFlaggedByOthers)
        return ret_success, ret_info, ret_error

    # get all reasons, why a statement could be flagged for delete
    if db_reason:
        # does the user has already flagged this argument?
        if __is_argument_flagged_for_delete_by_user(argument_uid, db_reason.uid, db_user.uid, is_executed=False):
            ret_info = translator.get(translator.alreadyFlaggedByYou)
            return ret_success, ret_info, ret_error

        # flagged for the first time
        __add_delete_review(db_user, db_argument, db_reason, transaction)
        ret_success = translator.get(translator.thxForFlagText)
        return ret_success, ret_info, ret_error

    # and another reason for optimization
    elif reason == 'optimization':
        if __is_argument_flagged_for_optimization_by_user(db_argument, db_user.uid, is_executed=False):
            ret_info = translator.get(translator.alreadyFlaggedByYou)
            return ret_success, ret_info, ret_error

        # flagged for the first time
        __add_optimization_review(db_user, db_argument, transaction)
        ret_success = translator.get(translator.thxForFlagText)
        return ret_success, ret_info, ret_error

    else:
        ret_error = translator.get(translator.internalKeyError)
        return ret_success, ret_info, ret_error


def __is_argument_flagged_for_delete(argument_uid, is_executed=False):
    """

    :param argument_uid:
    :param is_executed:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
                                                                    ReviewDelete.is_executed == is_executed)).all()
    return True if len(db_review) > 0 else False


def __is_argument_flagged_for_delete_by_user(argument_uid, reason_uid, user_uid, is_executed=False):
    """

    :param argument_uid:
    :param reason_uid:
    :param user_uid:
    :param is_executed:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
                                                                    ReviewDelete.reason_uid == reason_uid,
                                                                    ReviewDelete.is_executed == is_executed,
                                                                    ReviewDelete.detector_uid == user_uid)).all()
    return True if len(db_review) > 0 else False


def __is_argument_flagged_for_optimization(argument_uid, is_executed=False):
    """

    :param argument_uid:
    :param is_executed:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.argument_uid == argument_uid,
                                                                          ReviewOptimization.is_executed == is_executed)).all()
    return True if len(db_review) > 0 else False


def __is_argument_flagged_for_optimization_by_user(argument_uid, user_uid, is_executed=False):
    """

    :param argument_uid:
    :param user_uid:
    :param is_executed:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.argument_uid == argument_uid,
                                                                          ReviewOptimization.is_executed == is_executed,
                                                                          ReviewOptimization.detector_uid == user_uid)).all()
    return True if len(db_review) > 0 else False


def __add_delete_review(user, argument, reason, transaction):
    """

    :param user:
    :param argument:
    :param reason:
    :param transaction:
    :return:
    """
    review_delete = ReviewDelete(user.uid, argument.uid, reason.uid)
    DBDiscussionSession.add(review_delete)
    DBDiscussionSession.flush()
    transaction.commit()


def __add_optimization_review(user, argument, transaction):
    """

    :param user:
    :param argument:
    :param transaction:
    :return:
    """
    review_optimization = ReviewOptimization(user.uid, argument.uid)
    DBDiscussionSession.add(review_optimization)
    DBDiscussionSession.flush()
    transaction.commit()
