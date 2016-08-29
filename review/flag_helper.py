"""
Provides helping function for flagging arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Argument, ReviewDeleteReason, ReviewDelete, ReviewOptimization


def flag_argument(argument_uid, reason, nickname, translator, transaction):
    """
    Flags an given argument based on the reason which was sent by the author. This argument will be enqueued
    for a review process.

    :param argument_uid: Uid of the argument, which should be flagged
    :param reason: String which describes the reason
    :param nickname: Nickname of the requests sender
    :param translator: Class of String-Translator
    :param transaction: Le transactione
    :return:
    """
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    # we could have only one reason!
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(reason=reason).first()

    # sanity check
    if not db_argument or not db_user or not (db_reason is not None or reason == 'optimization'):
        return '', '', translator.get(translator.internalKeyError)

    ret_success = ''
    ret_info = ''
    ret_error = ''

    # notification to the author of the flagged argument

    # get all reasons, why a statement could be flagged for delete
    if db_reason:
        # does the user has already flagged this argument?
        if __is_argument_flagged_for_delete_by_user(argument_uid, db_user.uid, is_executed=False):
            ret_info = translator.get(translator.alreadyFlaggedByYou)
            return ret_success, ret_info, ret_error

        # was this argument flagged already?
        if __is_argument_flagged_for_delete(argument_uid, is_executed=False) or __is_argument_flagged_for_optimization(argument_uid, is_executed=False):
            ret_info = translator.get(translator.alreadyFlaggedByOthers)
            return ret_success, ret_info, ret_error

        # flagged for the first time
        __add_delete_review(argument_uid, db_user.uid, db_reason.uid, transaction)
        ret_success = translator.get(translator.thxForFlagText)
        return ret_success, ret_info, ret_error

    # and another reason for optimization
    elif reason == 'optimization':
        if __is_argument_flagged_for_optimization_by_user(argument_uid, db_user.uid, is_executed=False):
            ret_info = translator.get(translator.alreadyFlaggedByYou)
            return ret_success, ret_info, ret_error

        # flagged for the first time
        __add_optimization_review(argument_uid, db_user.uid, transaction)
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


def __is_argument_flagged_for_delete_by_user_and_reason(argument_uid, reason_uid, user_uid, is_executed=False):
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


def __is_argument_flagged_for_delete_by_user(argument_uid, user_uid, is_executed=False):
    """

    :param argument_uid:
    :param user_uid:
    :param is_executed:
    :return:
    """
    db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.argument_uid == argument_uid,
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


def __add_delete_review(argument_uid, user_uid, reason_uid, transaction):
    """

    :param argument_uid:
    :param user_uid:
    :param reason_uid:
    :param transaction:
    :return:
    """
    review_delete = ReviewDelete(user_uid, argument_uid, reason_uid)
    DBDiscussionSession.add(review_delete)
    DBDiscussionSession.flush()
    transaction.commit()


def __add_optimization_review(argument_uid, user_uid, transaction):
    """

    :param argument_uid:
    :param user_uid:
    :param transaction:
    :return:
    """
    review_optimization = ReviewOptimization(user_uid, argument_uid)
    DBDiscussionSession.add(review_optimization)
    DBDiscussionSession.flush()
    transaction.commit()
