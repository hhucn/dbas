"""
Provides helping function for the adding task in the review queuees or en-/disabling statemetns & arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction

from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, Argument, Premise, Statement, \
    LastReviewerOptimization, ReviewOptimization, ReviewEdit, ReviewEditValue, LastReviewerEdit, LastReviewerDuplicate,\
    ReviewDuplicate, RevokedDuplicate
from dbas.review.helper.reputation import add_reputation_for, rep_reason_success_flag, rep_reason_bad_flag, \
    rep_reason_success_duplicate, rep_reason_bad_duplicate, rep_reason_success_edit, rep_reason_bad_edit
from dbas.helper.query import correct_statement
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from websocket.lib import send_request_for_info_popup_to_socketio
from dbas.lib import get_all_arguments_by_statement

max_votes = 5
min_difference = 3


def __add_vote_for(user, review, is_okay, review_type):
    """

    :param user:
    :param review:
    :param is_okay:
    :param review_type:
    :return:
    """
    msg = '...'
    if review_type == LastReviewerDelete:
        msg = 'LastReviewerDelete'
    if review_type == LastReviewerEdit:
        msg = 'LastReviewerEdit'
    if review_type == LastReviewerOptimization:
        msg = 'LastReviewerOptimization'
    if review_type == LastReviewerDuplicate:
        msg = 'LastReviewerDuplicate'

    logger('review_main_helper', '__add_vote_for', '{}, user {}'.format(msg, user.uid))
    already_voted = DBDiscussionSession.query(review_type).filter(and_(review_type.reviewer_uid == user.uid,
                                                                       review_type.review_uid == review.uid)).first()
    if not already_voted:
        db_new_review = review_type(user.uid, review.uid, is_okay)
        DBDiscussionSession.add(db_new_review)
        DBDiscussionSession.flush()
        transaction.commit()
        logger('review_main_helper', '__add_vote_for', 'vote added')
    else:
        logger('review_main_helper', '__add_vote_for', 'already voted')


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


def add_review_opinion_for_delete(nickname, should_delete, review_uid, _t, application_url):
    """

    :param nickname:
    :param should_delete:
    :param review_uid:
    :param _t:
    :param application_url:
    :return:
    """
    logger('review_main_helper', 'add_review_opinion_for_delete', 'main')

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewDelete).get(review_uid)
    if db_review.is_executed:
        logger('review_main_helper', 'add_review_opinion_for_delete', 'already executed')
        return _t.get(_.alreadyExecuted)

    if not db_user:
        logger('review_main_helper', 'add_review_opinion_for_delete', 'no user')
        return _t.get(_.justLookDontTouch)

    db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
    # add new vote
    __add_vote_for(db_user, db_review, not should_delete, LastReviewerDelete)
    broke_limit = False

    # get all keep and delete votes
    count_of_keep, count_of_delete = __get_review_count(LastReviewerDelete, review_uid)
    logger('review_main_helper', 'add_review_opinion_for_delete', 'result ' + str(count_of_keep) + ':' + str(count_of_delete))

    # do we reached any limit?
    reached_max = max(count_of_keep, count_of_delete) >= max_votes
    if reached_max:
        if count_of_delete > count_of_keep:  # disable the flagged part
            logger('review_main_helper', 'add_review_opinion_for_delete', 'max reached / delete for review ' + str(review_uid))
            en_or_disable_object_of_review(db_review, True)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        else:  # just close the review
            logger('review_main_helper', 'add_review_opinion_for_delete', 'max reached / keep for review ' + str(review_uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_keep - count_of_delete >= min_difference:  # just close the review
        logger('review_main_helper', 'add_review_opinion_for_delete', 'vote says keep for review ' + str(review_uid))
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_delete - count_of_keep >= min_difference:  # disable the flagged part
        logger('review_main_helper', 'add_review_opinion_for_delete', 'vote says delete for review ' + str(review_uid))
        en_or_disable_object_of_review(db_review, True)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def add_review_opinion_for_edit(nickname, is_edit_okay, review_uid, _t, application_url):
    """

    :param nickname:
    :param is_edit_okay:
    :param review_uid:
    :param _t:
    :param application_url:
    :return:
    """
    logger('review_main_helper', 'add_review_opinion_for_edit', 'main')

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewEdit).get(review_uid)
    if db_review.is_executed:
        logger('review_main_helper', 'add_review_opinion_for_edit', 'already executed')
        return _t.get(_.alreadyExecuted)

    if not db_user:
        logger('review_main_helper', 'add_review_opinion_for_edit', 'no user')
        return _t.get(_.justLookDontTouch)

    db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
    broke_limit = False

    # add new vote
    __add_vote_for(db_user, db_review, is_edit_okay, LastReviewerEdit)

    # get all keep and delete votes
    count_of_edit, count_of_dont_edit = __get_review_count(LastReviewerEdit, review_uid)

    # do we reached any limit?
    reached_max = max(count_of_edit, count_of_dont_edit) >= max_votes
    if reached_max:
        if count_of_dont_edit < count_of_edit:  # accept the edit
            __accept_edit_review(db_review, db_user_created_flag)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_edit)
        else:  # just close the review
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_edit)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_edit - count_of_dont_edit >= min_difference:  # accept the edit
        __accept_edit_review(db_review, db_user_created_flag)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_edit)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_dont_edit - count_of_dont_edit >= min_difference:  # decline edit
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_edit)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def add_review_opinion_for_optimization(nickname, should_optimized, review_uid, data, _t, application_url):
    """

    :param nickname:
    :param should_optimized:
    :param review_uid:
    :param data:
    :param _t:
    :param application_url:
    :return:
    """
    logger('review_main_helper', 'add_review_opinion_for_optimization',
           'main ' + str(review_uid) + ', optimize ' + str(should_optimized))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewOptimization).get(review_uid)
    if not db_review or db_review.is_executed:
        logger('review_main_helper', 'add_review_opinion_for_optimization', 'not found / already executed')
        return _t.get(_.alreadyExecuted)

    if not db_user:
        logger('review_main_helper', 'add_review_opinion_for_optimization', 'no use found')
        return _t.get(_.justLookDontTouch)

    # add new review
    db_new_review = LastReviewerOptimization(db_user.uid, db_review.uid, not should_optimized)
    DBDiscussionSession.add(db_new_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if not should_optimized:
        __keep_the_element(db_review, application_url, _t)
    else:
        __proposal_for_the_element(db_review, data, db_user)

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    return ''


def add_review_opinion_for_duplicate(nickname, is_duplicate, review_uid, _t, application_url):
    """

    :param nickname:
    :param is_duplicate:
    :param review_uid:
    :param _t:
    :param application_url:
    :return:
    """
    logger('review_main_helper', 'add_review_opinion_for_duplicate', 'main ' + str(review_uid) + ', duplicate ' + str(is_duplicate))

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewDuplicate).get(review_uid)
    if db_review.is_executed:
        logger('review_main_helper', 'add_review_opinion_for_duplicate', 'already executed')
        return _t.get(_.alreadyExecuted)

    if not db_user:
        logger('review_main_helper', 'add_review_opinion_for_duplicate', 'no user')
        return _t.get(_.justLookDontTouch)

    db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
    # add new vote
    __add_vote_for(db_user, db_review, not is_duplicate, LastReviewerDuplicate)
    broke_limit = False

    # get all keep and delete votes
    count_of_keep, count_of_reset = __get_review_count(LastReviewerDuplicate, review_uid)
    logger('review_main_helper', 'add_review_opinion_for_duplicate', 'result ' + str(count_of_keep) + ':' + str(count_of_reset))

    # do we reached any limit?
    reached_max = max(count_of_keep, count_of_reset) >= max_votes
    if reached_max:
        if count_of_reset > count_of_keep:  # disable the flagged part
            logger('review_main_helper', 'add_review_opinion_for_duplicate', 'max reached / bend for review ' + str(review_uid))
            __bend_objects_of_duplicate_review(db_review, db_user)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_duplicate)
        else:  # just close the review
            logger('review_main_helper', 'add_review_opinion_for_duplicate', 'max reached / forget about review ' + str(review_uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_duplicate)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_keep - count_of_reset >= min_difference:  # just close the review
        logger('review_main_helper', 'add_review_opinion_for_duplicate', 'vote says forget about review ' + str(review_uid))
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_duplicate)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_reset - count_of_keep >= min_difference:  # disable the flagged part
        logger('review_main_helper', 'add_review_opinion_for_duplicate', 'vote says bend for review ' + str(review_uid))
        __bend_objects_of_duplicate_review(db_review, db_user)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_duplicate)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def __keep_the_element(db_review, application_url, _t):
    """

    :param db_review:
    :param application_url:
    :param _t:
    :return:
    """
    # add new vote
    db_user_who_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)

    # get all keep and delete votes
    db_keep_version = DBDiscussionSession.query(LastReviewerOptimization).filter(
        and_(LastReviewerOptimization.review_uid == db_review.uid,
             LastReviewerOptimization.is_okay == True)).all()

    if len(db_keep_version) > max_votes:
        add_rep, broke_limit = add_reputation_for(db_user_who_created_flag, rep_reason_bad_flag)
        if broke_limit:
            send_request_for_info_popup_to_socketio(db_user_who_created_flag.nickname, _t.get(_.youAreAbleToReviewNow),
                                                    application_url + '/review')

        db_review.set_executed(True)
        db_review.update_timestamp()
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()


def __proposal_for_the_element(db_review, data, db_user):
    """

    :param db_review:
    :param data:
    :param db_user:
    :return:
    """
    # add new edit
    argument_dict = {}
    statement_dict = {}

    # sort the new edits by argument uid
    for d in data:
        is_argument = d['argument'] > 0
        if is_argument:
            if d['argument'] in argument_dict:
                argument_dict[d['argument']].append(d)
            else:
                argument_dict[d['argument']] = [d]
        else:
            if d['statement'] in statement_dict:
                statement_dict[d['statement']].append(d)
            else:
                statement_dict[d['statement']] = [d]

    logger('review_main_helper', 'add_review_opinion_for_optimization',
           'statements ' + str(statement_dict) + ', argument ' + str(argument_dict))

    # add reviews
    new_edits = list()
    for argument_uid in argument_dict:
        DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, argument=argument_uid))
        DBDiscussionSession.flush()
        transaction.commit()
        db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(
            and_(ReviewEdit.detector_uid == db_user.uid,
                 ReviewEdit.argument_uid == argument_uid)).order_by(ReviewEdit.uid.desc()).first()
        logger('review_main_helper', 'add_review_opinion_for_optimization',
               'New ReviewEdit with uid ' + str(db_review_edit.uid) + ' (argument)')

        for edit in argument_dict[argument_uid]:
            new_edits.append(ReviewEditValue(review_edit=db_review_edit.uid,
                                             statement=edit['uid'],
                                             typeof=edit['type'],
                                             content=edit['val']))

    for statement_uid in statement_dict:
        DBDiscussionSession.add(ReviewEdit(detector=db_user.uid, statement=statement_uid))
        DBDiscussionSession.flush()
        transaction.commit()
        db_review_edit = DBDiscussionSession.query(ReviewEdit).filter(
            and_(ReviewEdit.detector_uid == db_user.uid,
                 ReviewEdit.statement_uid == statement_uid)).order_by(ReviewEdit.uid.desc()).first()
        logger('review_main_helper', 'add_review_opinion_for_optimization',
               'New ReviewEdit with uid ' + str(db_review_edit.uid) + ' (statement)')

        for edit in statement_dict[statement_uid]:
            new_edits.append(ReviewEditValue(review_edit=db_review_edit.uid,
                                             statement=statement_uid,
                                             typeof=edit['type'],
                                             content=edit['val']))

    if len(new_edits) > 0:
        DBDiscussionSession.add_all(new_edits)

    # edit given, so this review is executed
    db_review.set_executed(True)
    db_review.update_timestamp()
    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()


def en_or_disable_object_of_review(review, is_disabled):
    """

    :param review:
    :param is_disabled:
    :return:
    """
    logger('review_main_helper', 'en_or_disable_object_of_review', str(review.uid) + ' ' + str(is_disabled))
    if review.statement_uid is not None:
        __en_or_disable_statement_and_premise_of_review(review, is_disabled)
    else:
        __en_or_disable_arguments_and_premise_of_review(review, is_disabled)


def __en_or_disable_statement_and_premise_of_review(review, is_disabled):
    """

    :param review:
    :param is_disabled:
    :return:
    """
    logger('review_main_helper', '__en_or_disable_statement_and_premise_of_review', str(review.uid) + ' ' + str(is_disabled))
    db_statement = DBDiscussionSession.query(Statement).get(review.statement_uid)
    db_statement.set_disable(is_disabled)
    DBDiscussionSession.add(db_statement)
    db_premises = DBDiscussionSession.query(Premise).filter_by(statement_uid=review.statement_uid).all()

    for premise in db_premises:
        premise.set_disable(is_disabled)
        DBDiscussionSession.add(premise)

    DBDiscussionSession.flush()
    transaction.commit()


def __en_or_disable_arguments_and_premise_of_review(review, is_disabled):
    """

    :param review:
    :param is_disabled:
    :return:
    """
    logger('review_main_helper', '__en_or_disable_arguments_and_premise_of_review', str(review.uid) + ' ' + str(is_disabled))
    db_argument = DBDiscussionSession.query(Argument).get(review.argument_uid)
    db_argument.set_disable(is_disabled)
    DBDiscussionSession.add(db_argument)
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()

    for premise in db_premises:
        db_statement = DBDiscussionSession.query(Statement).get(premise.statement_uid)
        db_statement.set_disable(is_disabled)
        premise.set_disable(is_disabled)
        DBDiscussionSession.add(premise)

    if db_argument.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).get(db_argument.conclusion_uid)
        db_statement.set_disable(is_disabled)
        DBDiscussionSession.add(db_statement)

    DBDiscussionSession.flush()
    transaction.commit()


def __bend_objects_of_duplicate_review(db_review, db_user):
    """

    :param db_review:
    :param db_user:
    :return:
    """
    logger('review_main_helper', '__bend_objects_of_duplicate_review', 'Review {} with dupl {} and oem {}'.format(db_review.uid, db_review.duplicate_statement_uid, db_review.original_statement_uid))
    db_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
    db_statement.set_disable(True)
    DBDiscussionSession.add(db_statement)

    # TODO   Wrong UID, POSITION, SINGLE STATEMENT

    # getting all argument where the duplicated statement is used
    all_arguments = get_all_arguments_by_statement(db_review.duplicate_statement_uid, True)
    for argument in all_arguments:
        text = 'Statement {} was used in argument {}'.format(db_review.duplicate_statement_uid, argument.uid)
        used = False

        # recalibrate conclusion
        if argument.conclusion_uid == db_review.duplicate_statement_uid:
            tmp = '{}, bend conclusion from {} to {}' .format(text, argument.conclusion_uid, db_review.original_statement_uid)
            logger('review_main_helper', '__bend_objects_of_duplicate_review', tmp)
            argument.set_conclusion(db_review.original_statement_uid)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.add(RevokedDuplicate(review=db_review.uid, author=db_user.uid, in_argument_as_conclusion=argument.uid))
            used = True

        # recalibrate premises
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
        for premise in db_premises:
            if premise.statement_uid == db_review.duplicate_statement_uid:
                tmp = '{}, bend premise from {} to {}' .format(text, premise.statement_uid, db_review.original_statement_uid)
                logger('review_main_helper', '__bend_objects_of_duplicate_review', tmp)
                premise.set_statement(db_review.original_statement_uid)
                DBDiscussionSession.add(premise)
                DBDiscussionSession.add(RevokedDuplicate(author=db_user.uid,
                                                         review=db_review.uid,
                                                         in_premise_as_statement=premise.statement_uid,
                                                         premise_in_group=premise.premisesgroup_uid))
                used = True

        if not used:
            logger('review_main_helper', '__bend_objects_of_duplicate_review', 'Nothing was bend - undercut from {} to {}'.format(argument.uid, argument.argument_uid), error=True)

    DBDiscussionSession.flush()
    transaction.commit()


def __accept_edit_review(review, db_user_created_flag):
    """

    :param review:
    :param db_user_created_flag:
    :return:
    """
    db_values = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=review.uid).all()
    db_user = DBDiscussionSession.query(User).get(review.detector_uid)
    for value in db_values:
        correct_statement(db_user.nickname, value.statement_uid, value.content)
        # val = QueryHelper.correct_statement(transaction, db_user.nickname, value.statement_uid, value.content)
        # db_textversion = DBDiscussionSession.query(TextVersion).filter_by(content=val['text']).order_by(TextVersion.uid.desc()).first()
        # send_edit_text_notification(db_user_created_flag, db_textversion, None, None)
