"""
Provides helping function for the managing reviews.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, Argument, Premise, Statement, \
    LastReviewerOptimization, ReviewOptimization, ReviewEdit, ReviewEditValue, LastReviewerEdit, TextVersion
from dbas.review.helper.reputation import add_reputation_for, rep_reason_success_flag, rep_reason_bad_flag
from dbas.helper.query import QueryHelper
from dbas.logger import logger
from dbas.helper.notification import send_edit_text_notification

max_votes = 5
min_difference = 3


def __add_vote_for(user, review, is_okay, review_type, transaction):
    """

    :param user:
    :param review:
    :param is_okay:
    :param transaction:
    :return:
    """
    db_new_review = review_type(user.uid, review.uid, is_okay)
    DBDiscussionSession.add(db_new_review)
    DBDiscussionSession.flush()
    transaction.commit()


def __get_review_count(review_type, review_uid):
    """

    :param review_type:
    :param review_uid:
    :return:
    """
    db_reviews = DBDiscussionSession.query(review_type).filter_by(review_uid=review_uid)
    count_of_okay = len(db_reviews.filter_by(is_okay=True).all())
    count_of_not_okay = len(db_reviews.filter_by(is_okay=False).all())
    return count_of_okay, count_of_not_okay


def add_review_opinion_for_delete(nickname, should_delete, review_uid, translator, transaction):
    """

    :param nickname:
    :param should_delete:
    :param review_uid:
    :param translator:
    :param transaction:
    :return:
    """
    logger('ReviewMainHelper', 'add_review_opinion_for_delete', 'main')

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewDelete).filter_by(uid=review_uid).first()
    if db_review.is_executed or not db_user:
        return translator.get(translator.internalKeyError)

    db_user_created_flag = DBDiscussionSession.query(User).filter_by(uid=db_review.detector_uid).first()
    # add new vote
    __add_vote_for(db_user, db_review, not should_delete, LastReviewerDelete, transaction)

    # get all keep and delete votes
    count_of_keep, count_of_delete = __get_review_count(LastReviewerDelete, review_uid)

    # do we reached any limit?
    reached_max = max(count_of_keep, count_of_delete) >= max_votes
    if reached_max:
        db_review.set_executed(True)
        db_review.is_executed = True
        if count_of_delete > count_of_keep:  # disable the flagged part
            en_or_disable_arguments_and_premise_of_review(db_review, True)
            add_reputation_for(db_user_created_flag, rep_reason_success_flag, transaction)
        else:  # just close the review
            add_reputation_for(db_user_created_flag, rep_reason_bad_flag, transaction)

    if count_of_keep - count_of_delete >= min_difference:  # just close the review
        db_review.set_executed(True)
        add_reputation_for(db_user_created_flag, rep_reason_bad_flag, transaction)

    if count_of_delete - count_of_keep >= min_difference:  # disable the flagged part
        db_review.set_executed(True)
        en_or_disable_arguments_and_premise_of_review(db_review, True)
        add_reputation_for(db_user_created_flag, rep_reason_success_flag, transaction)

    return ''


def add_review_opinion_for_edit(nickname, is_edit_okay, review_uid, translator, transaction):
    """

    :param nickname:
    :param is_edit_okay:
    :param review_uid:
    :param translator:
    :param transaction:
    :return:
    """
    logger('ReviewMainHelper', 'add_review_opinion_for_edit', 'main')

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewEdit).filter_by(uid=review_uid).first()
    if db_review.is_executed or not db_user:
        return translator.get(translator.internalKeyError)

    db_user_created_flag = DBDiscussionSession.query(User).filter_by(uid=db_review.detector_uid).first()

    # add new vote
    __add_vote_for(db_user, db_review, is_edit_okay, LastReviewerEdit, transaction)

    # get all keep and delete votes
    count_of_edit, count_of_dont_edit = __get_review_count(LastReviewerEdit, review_uid)

    # do we reached any limit?
    reached_max = max(count_of_edit, count_of_dont_edit) >= max_votes
    if reached_max:
        db_review.set_executed(True)
        db_review.is_executed = True
        if count_of_dont_edit < count_of_edit:  # accept the edit
            accept_edit_review(db_review, transaction, db_user_created_flag)
            add_reputation_for(db_user_created_flag, rep_reason_success_flag, transaction)
        else:  # just close the review
            add_reputation_for(db_user_created_flag, rep_reason_bad_flag, transaction)

    if count_of_edit - count_of_dont_edit >= min_difference:  # accept the edit
        db_review.set_executed(True)
        db_review.is_executed = True
        accept_edit_review(db_review, transaction, db_user_created_flag)
        add_reputation_for(db_user_created_flag, rep_reason_success_flag, transaction)

    if count_of_dont_edit - count_of_dont_edit >= min_difference:  # decline edit
        db_review.set_executed(True)
        db_review.is_executed = True
        add_reputation_for(db_user_created_flag, rep_reason_bad_flag, transaction)

    return ''


def add_review_opinion_for_optimization(nickname, should_optimized, review_uid, data, translator, transaction):
    """

    :param nickname:
    :param should_optimized:
    :param review_uid:
    :param data:
    :param translator:
    :param transaction:
    :return:
    """
    logger('ReviewMainHelper', 'add_review_opinion_for_optimization', 'main ' + str(review_uid) + ', optimize ' + str(should_optimized))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewOptimization).filter_by(uid=review_uid).first()
    if not db_review or db_review.is_executed or not db_user:
        return translator.get(translator.internalKeyError)

    db_new_review = LastReviewerOptimization(db_user.uid, db_review.uid, not should_optimized)
    DBDiscussionSession.add(db_new_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if not should_optimized:
        # add new vote
        db_user_who_created_flag = DBDiscussionSession.query(User).filter_by(uid=db_review.detector_uid).first()

        # get all keep and delete votes
        db_keep_version = DBDiscussionSession.query(LastReviewerOptimization).filter(and_(LastReviewerOptimization.review_uid == review_uid,
                                                                                          LastReviewerOptimization.is_okay == True)).all()

        if len(db_keep_version) > max_votes:
            db_review.set_executed(True)
            db_review.is_executed = True
            add_reputation_for(db_user_who_created_flag, rep_reason_bad_flag, transaction)
    else:
        logger('ReviewMainHelper', 'add_review_opinion_for_optimization', 'new edit')
        # add new edit
        argument_dict = {}
        # sort the new edits by argument uid
        for d in data:
            if d['argument'] in argument_dict:
                argument_dict[d['argument']].append(d)
            else:
                argument_dict[d['argument']] = [d]

        # add reviews
        new_edits = list()
        for argument_uid in argument_dict:
            DBDiscussionSession.add(ReviewEdit(db_user.uid, argument_uid))
            DBDiscussionSession.flush()
            transaction.commit()
            db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(and_(ReviewEdit.detector_uid == db_user.uid,
                                                                               ReviewEdit.argument_uid == argument_uid)).order_by(ReviewEdit.uid.desc()).first()
            logger('ReviewMainHelper', 'add_review_opinion_for_optimization', 'new ReviewEdit with uid ' + str(db_review_edit.uid))
            for edit in argument_dict[argument_uid]:
                new_edits.append(ReviewEditValue(db_review_edit.uid, argument_uid, edit['uid'], edit['type'], edit['val']))

        if len(new_edits) > 0:
            DBDiscussionSession.add_all(new_edits)

        # edit given, so this review is executed
        logger('ReviewMainHelper', 'add_review_opinion_for_optimization', 'set executed')
        db_review.set_executed(True)
        db_review.is_executed = True

        DBDiscussionSession.flush()
        transaction.commit()

    return ''


def en_or_disable_arguments_and_premise_of_review(review, is_disabled):
    """

    :param review:
    :param is_disabled:
    :return:
    """
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=review.argument_uid).first()
    db_argument.set_disable(is_disabled)
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()

    for premise in db_premises:
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=premise.statement_uid).first()
        db_statement.set_disable(is_disabled)

    if db_argument.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid.statement_uid).first()
        db_statement.set_disable(is_disabled)


def accept_edit_review(review, transaction, db_user_created_flag):
    """

    :param review:
    :param transaction:
    :param db_user_created_flag:
    :return:
    """
    db_values = DBDiscussionSession.query(ReviewEditValue).filter_by(reviewedit_uid=review.uid).all()
    db_user = DBDiscussionSession.query(User).filter_by(uid=review.detector_uid).first()
    for value in db_values:
        val = QueryHelper.correct_statement(transaction, db_user.nickname, value.statement_uid, value.content)
        db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=val['text']).order_by(TextVersion.uid.desc()).first()
        send_edit_text_notification(db_user_created_flag, db_textversion, None, None)
