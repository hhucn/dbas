"""
Provides helping function for the adding task in the review queuees or en-/disabling statemetns & arguments.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, Argument, Premise, Statement, \
    LastReviewerOptimization, ReviewOptimization, ReviewEdit, ReviewEditValue, LastReviewerEdit, LastReviewerDuplicate,\
    ReviewDuplicate, RevokedDuplicate, LastReviewerSplit, LastReviewerMerge, ReviewMerge, ReviewSplit,\
    ReviewMergeValues, ReviewSplitValues, PremiseGroup, PremiseGroupMerged, PremiseGroupSplitted, \
    StatementReplacementsByPremiseGroupMerge, StatementReplacementsByPremiseGroupSplit
from dbas.handler.statements import correct_statement
from dbas.lib import get_all_arguments_by_statement, get_text_for_premisesgroup_uid
from dbas.logger import logger
from dbas.review.helper.reputation import add_reputation_for, rep_reason_success_flag, rep_reason_bad_flag, \
    rep_reason_success_duplicate, rep_reason_bad_duplicate, rep_reason_success_edit, rep_reason_bad_edit
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from webhook.lib import send_request_for_info_popup_to_socketio, get_port
from dbas.handler.statements import set_statement

max_votes = 5
min_difference = 3


def __add_vote_for(user, review, is_okay, review_type):
    """
    Add vote for a specific review

    :param user: User
    :param review: one table ouf of the Reviews
    :param is_okay: Boolean
    :param review_type: one table out of the LastReviews
    :return: None
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
    if review_type == LastReviewerSplit:
        msg = 'LastReviewerSplit'
    if review_type == LastReviewerMerge:
        msg = 'LastReviewerMerge'

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
    Get review count of specific review

    :param review_type: Table of Review
    :param review_uid: uid of review
    :return: count of okay, count fo not okay
    """
    db_reviews = DBDiscussionSession.query(review_type).filter_by(review_uid=review_uid)
    count_of_okay = len(db_reviews.filter_by(is_okay=True).all())
    count_of_not_okay = len(db_reviews.filter_by(is_okay=False).all())
    return count_of_okay, count_of_not_okay


def add_review_opinion_for_delete(request, review_uid, _t):
    """
    Adds row the delete review

    :param request: Pyramids request object
    :param review_uid: ReviewDelete.uid
    :param _t: Translator
    :return: String
    """
    logger('review_main_helper', 'add_review_opinion_for_delete', 'main')
    should_delete = True if str(request.params['should_delete']) == 'true' else False
    nickname = request.authenticated_userid

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
            logger('review_main_helper', 'add_review_opinion_for_delete', 'max reached / delete for review {}'.format(review_uid))
            en_or_disable_object_of_review(db_review, True)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        else:  # just close the review
            logger('review_main_helper', 'add_review_opinion_for_delete', 'max reached / keep for review {}'.format(review_uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_keep - count_of_delete >= min_difference:  # just close the review
        logger('review_main_helper', 'add_review_opinion_for_delete', 'vote says keep for review {}'.format(review_uid))
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_delete - count_of_keep >= min_difference:  # disable the flagged part
        logger('review_main_helper', 'add_review_opinion_for_delete', 'vote says delete for review {}'.format(review_uid))
        en_or_disable_object_of_review(db_review, True)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        port = get_port(request)
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                request.application_url + '/review')

    return ''


def add_review_opinion_for_edit(request, is_edit_okay, review_uid, _t):
    """
    Adds row the edit review

    :param request: Pyramids request object
    :param is_edit_okay: Boolean
    :param review_uid: ReviewEdit.uid
    :param _t: Translator
    :return: String
    """
    logger('review_main_helper', 'add_review_opinion_for_edit', 'main')
    nickname = request.authenticated_userid
    application_url = request.application_url

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
            __accept_edit_review(db_review)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_edit)
        else:  # just close the review
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_edit)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_edit - count_of_dont_edit >= min_difference:  # accept the edit
        __accept_edit_review(db_review)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_edit)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_dont_edit - count_of_edit >= min_difference:  # decline edit
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_edit)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        port = get_port(request)
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def add_review_opinion_for_optimization(request, should_optimized, review_uid, data, _t):
    """
    Adds row the optimization review

    :param request: Pyramids request object
    :param should_optimized: Boolean
    :param review_uid: ReviewOptimization
    :param data: String
    :param _t: Translator
    :return: String
    """
    nickname = request.authenticated_userid
    application_url = request.application_url

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
        __keep_the_element_of_optimization_review(request, db_review, application_url, _t)
    else:
        __proposal_for_the_element(db_review, data, db_user)

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    return ''


def add_review_opinion_for_duplicate(request, is_duplicate, review_uid, _t):
    """
    Adds row to the duplicate review

    :param request: Pyramids request object
    :param is_duplicate: Boolean
    :param review_uid: ReviewDuplicate.uid
    :param _t: Translator
    :return: String
    """
    logger('review_main_helper', 'add_review_opinion_for_duplicate', 'main {}, duplicate {}'.format(review_uid, is_duplicate))
    nickname = request.authenticated_userid
    application_url = request.application_url

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
            logger('review_main_helper', 'add_review_opinion_for_duplicate', 'max reached / bend for review {}'.format(review_uid))
            __bend_objects_of_duplicate_review(db_review)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_duplicate)
        else:  # just close the review
            logger('review_main_helper', 'add_review_opinion_for_duplicate', 'max reached / forget about review {}'.format(review_uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_duplicate)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_keep - count_of_reset >= min_difference:  # just close the review
        logger('review_main_helper', 'add_review_opinion_for_duplicate', 'vote says forget about review {}'.format(review_uid))
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_duplicate)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_reset - count_of_keep >= min_difference:  # disable the flagged part
        logger('review_main_helper', 'add_review_opinion_for_duplicate', 'vote says bend for review {}'.format(review_uid))
        __bend_objects_of_duplicate_review(db_review)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_duplicate)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        port = get_port(request)
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def add_review_opinion_for_split(request, review_uid, should_split, _t):
    """
    Adds row to the split review

    :param request: Pyramids request object
    :param review_uid: ReviewSplit
    :param should_split: True, if it should be merged
    :param _t: Translator
    :return: String
    """
    logger('review_main_helper', 'add_review_opinion_for_split', 'main {}'.format(review_uid))
    nickname = request.authenticated_userid
    application_url = request.application_url

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewSplit).get(review_uid)
    if db_review.is_executed:
        logger('review_main_helper', 'add_review_opinion_for_split', 'already executed')
        return _t.get(_.alreadyExecuted)

    if not db_user:
        logger('review_main_helper', 'add_review_opinion_for_split', 'no user')
        return _t.get(_.justLookDontTouch)

    db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
    # add new vote
    __add_vote_for(db_user, db_review, should_split, LastReviewerSplit)
    broke_limit = False

    # get all keep and delete votes
    count_of_keep, count_of_reset = __get_review_count(LastReviewerSplit, review_uid)
    logger('review_main_helper', 'add_review_opinion_for_split', 'result ' + str(count_of_keep) + ':' + str(count_of_reset))

    # do we reached any limit?
    reached_max = max(count_of_keep, count_of_reset) >= max_votes
    if reached_max:
        if count_of_reset > count_of_keep:  # disable the flagged part
            logger('review_main_helper', 'add_review_opinion_for_split', 'max reached / bend for review {}'.format(review_uid))
            __split_premisegroup(db_review)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        else:  # just close the review
            logger('review_main_helper', 'add_review_opinion_for_split', 'max reached / forget about review {}'.format(review_uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_keep - count_of_reset >= min_difference:  # just close the review
        logger('review_main_helper', 'add_review_opinion_for_split', 'vote says forget about review {}'.format(review_uid))
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_reset - count_of_keep >= min_difference:  # disable the flagged part
        logger('review_main_helper', 'add_review_opinion_for_split', 'vote says bend for review {}'.format(review_uid))
        __split_premisegroup(db_review)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        port = get_port(request)
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def add_review_opinion_for_merge(request, review_uid, should_merge, _t):
    """
    Adds row to the merge review

    :param request: Pyramids request object
    :param review_uid: ReviewMerge
    :param should_merge: True, if it should be merged
    :param _t: Translator
    :return: String
    """
    logger('review_main_helper', 'add_review_opinion_for_merge', 'main {}'.format(review_uid))
    nickname = request.authenticated_userid
    application_url = request.application_url

    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    db_review = DBDiscussionSession.query(ReviewMerge).get(review_uid)
    if db_review.is_executed:
        logger('review_main_helper', 'add_review_opinion_for_merge', 'already executed')
        return _t.get(_.alreadyExecuted)

    if not db_user:
        logger('review_main_helper', 'add_review_opinion_for_merge', 'no user')
        return _t.get(_.justLookDontTouch)

    db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
    # add new vote
    __add_vote_for(db_user, db_review, should_merge, LastReviewerMerge)
    broke_limit = False

    # get all keep and delete votes
    count_of_keep, count_of_reset = __get_review_count(LastReviewerMerge, review_uid)
    logger('review_main_helper', 'add_review_opinion_for_merge', 'result ' + str(count_of_keep) + ':' + str(count_of_reset))

    # do we reached any limit?
    reached_max = max(count_of_keep, count_of_reset) >= max_votes
    if reached_max:
        if count_of_reset > count_of_keep:  # disable the flagged part
            logger('review_main_helper', 'add_review_opinion_for_merge', 'max reached / bend for review {}'.format(review_uid))
            __merge_premisegroup(db_review)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        else:  # just close the review
            logger('review_main_helper', 'add_review_opinion_for_merge', 'max reached / forget about review {}'.format(review_uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_keep - count_of_reset >= min_difference:  # just close the review
        logger('review_main_helper', 'add_review_opinion_for_merge', 'vote says forget about review {}'.format(review_uid))
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    elif count_of_reset - count_of_keep >= min_difference:  # disable the flagged part
        logger('review_main_helper', 'add_review_opinion_for_merge', 'vote says bend for review {}'.format(review_uid))
        __merge_premisegroup(db_review)
        add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
        db_review.set_executed(True)
        db_review.update_timestamp()

    DBDiscussionSession.add(db_review)
    DBDiscussionSession.flush()
    transaction.commit()

    if broke_limit:
        port = get_port(request)
        send_request_for_info_popup_to_socketio(db_user_created_flag.nickname, port, _t.get(_.youAreAbleToReviewNow),
                                                application_url + '/review')

    return ''


def __keep_the_element_of_optimization_review(request, db_review, application_url, _t):
    """
    Adds row for LastReviewerOptimization

    :param db_review: ReviewOptimization
    :param application_url: URL
    :param _t: Translator
    :return: None
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
            port = get_port(request)
            send_request_for_info_popup_to_socketio(db_user_who_created_flag.nickname, port,
                                                    _t.get(_.youAreAbleToReviewNow), application_url + '/review')

        db_review.set_executed(True)
        db_review.update_timestamp()
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()


def __proposal_for_the_element(db_review, data, db_user):
    """
    Adds proposal for the ReviewEdit

    :param db_review: ReviewEdit
    :param data: String
    :param db_user: User
    :return: None
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

    logger('review_main_helper', 'add_review_opinion_for_optimization', 'detector {}, statements {}, arguments {}'.format(db_user.uid, statement_dict, argument_dict))

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
    En- or -disable a specific review, this affects all the statements and arguments

    :param review: Review
    :param is_disabled: boolean
    :return: None
    """
    logger('review_main_helper', 'en_or_disable_object_of_review', str(review.uid) + ' ' + str(is_disabled))
    if review.statement_uid is not None:
        __en_or_disable_statement_and_premise_of_review(review, is_disabled)
    else:
        __en_or_disable_arguments_and_premise_of_review(review, is_disabled)


def __en_or_disable_statement_and_premise_of_review(review, is_disabled):
    """
    En- or -disable a specific review, this affects all the statements

    :param review: Review
    :param is_disabled: boolean
    :return: None
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
    En- or -disable a specific review, this affects all the arguments

    :param review: Review
    :param is_disabled: boolean
    :return: None
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


def __bend_objects_of_duplicate_review(db_review):
    """
    If an argument is a duplicate, we have to bend the objects of argument, which are no duplicates

    :param db_review: Review
    :return: None
    """
    msg = 'Review {} with dupl {} and oem {}'.format(db_review.uid,
                                                     db_review.duplicate_statement_uid,
                                                     db_review.original_statement_uid)
    logger('review_main_helper', '__bend_objects_of_duplicate_review', msg)
    db_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
    db_statement.set_disable(True)
    DBDiscussionSession.add(db_statement)

    # TODO   SINGLE STATEMENT SET DISABLE

    # do we need a new position
    db_dupl_statement = DBDiscussionSession.query(Statement).get(db_review.duplicate_statement_uid)
    db_orig_statement = DBDiscussionSession.query(Statement).get(db_review.original_statement_uid)
    if db_dupl_statement.is_startpoint and not db_orig_statement.is_startpoint:
        logger('review_main_helper', '__bend_objects_of_duplicate_review', 'Duplicate is startpoint, but original one is not')
        DBDiscussionSession.add(RevokedDuplicate(review=db_review.uid, bend_position=True, statement=db_orig_statement.uid))
        db_orig_statement.set_position(True)

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
            DBDiscussionSession.add(RevokedDuplicate(review=db_review.uid, conclusion_of_argument=argument.uid))
            used = True

        # recalibrate premises
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
        for premise in db_premises:
            if premise.statement_uid == db_review.duplicate_statement_uid:
                tmp = '{}, bend premise {} from {} to {}' .format(text, premise.uid, premise.statement_uid, db_review.original_statement_uid)
                logger('review_main_helper', '__bend_objects_of_duplicate_review', tmp)
                premise.set_statement(db_review.original_statement_uid)
                DBDiscussionSession.add(premise)
                DBDiscussionSession.add(RevokedDuplicate(review=db_review.uid, premise=premise.uid))
                used = True

        if not used:
            logger('review_main_helper', '__bend_objects_of_duplicate_review', 'Nothing was bend - undercut from {} to {}'.format(argument.uid, argument.argument_uid), error=True)

    DBDiscussionSession.flush()
    transaction.commit()


def __accept_edit_review(review):
    """
    Add correction for each value affected by the review

    :param review: Review
    :return: None
    """
    db_values = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=review.uid).all()
    db_user = DBDiscussionSession.query(User).get(review.detector_uid)
    for value in db_values:
        correct_statement(db_user.nickname, value.statement_uid, value.content)


def __merge_premisegroup(review):
    """
    Merges a premisegroup into the items, which are mapped with the given review

    :param review: ReviewSplit.uid
    :return: None
    """
    db_values = DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=review.uid).all()
    db_old_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=review.premisesgroup_uid).all()
    db_first_old_statement = DBDiscussionSession.query(Statement).get(db_old_premises[0].uid)
    discussion_lang = db_first_old_statement.lang
    db_user = DBDiscussionSession.query(User).get(review.detector_uid)

    if db_values:
        logger('review_main_helper', '__merge_premisegroup', 'merge given premisegroup with the mapped, new statements')
        texts = [values.content for values in db_values]
        translator_discussion = Translator(discussion_lang)
        new_text = ' {} '.format(translator_discussion.get(_.aand)).join(texts)
    else:
        logger('review_main_helper', '__merge_premisegroup', 'just merge the premisegroup')
        new_text, tmp = get_text_for_premisesgroup_uid(review.premisesgroup_uid)

    # now we have new text as a variable, let's set the statement
    new_statement, tmp = set_statement(new_text, db_user.uid, db_first_old_statement.is_startpoint, db_old_premises[0].issue_uid, discussion_lang)

    # new premisegroup for the statement
    db_new_premisegroup = PremiseGroup(author=db_user.uid)
    DBDiscussionSession.add(db_new_premisegroup)
    DBDiscussionSession.flush()

    # new premise
    db_new_premise = Premise(db_new_premisegroup.uid, new_statement.uid, False, db_user.uid, new_statement.issue_uid)
    DBDiscussionSession.add(db_new_premise)

    # swap the premisegroup occurence in every argument
    db_arguments = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=review.premisesgroup_uid).all()
    for argument in db_arguments:
        argument.set_premisegroup(db_new_premisegroup.uid)
        DBDiscussionSession.add(argument)

    # swap the conclusion in every argument as well as premise
    old_statement_ids = [p.statement_uid for p in db_old_premises]
    for old_statement_id in old_statement_ids:
        db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=old_statement_id).all()
        for argument in db_arguments:
            argument.set_conclusion(new_statement.uid)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.add(StatementReplacementsByPremiseGroupMerge(review.uid, old_statement_id, new_statement.uid))

    # add swap to database
    DBDiscussionSession.add(PremiseGroupMerged(review.uid, review.premisesgroup_uid, db_new_premisegroup.uid))

    # disable old statements and premises
    # db_old_statements = DBDiscussionSession.query(Statement).filter(Statement.uid.in_(old_statement_ids)).all()
    # for element in db_old_premises + db_old_statements:
    #    element.set_disable(True)
    #    DBDiscussionSession.add(element)

    # finish
    DBDiscussionSession.flush()
    transaction.commit()


def __split_premisegroup(review):
    """
    Splits a premisegroup into the items, which are mapped with the given review

    :param review: ReviewSplit.uid
    :return: None
    """
    db_values = DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=review.uid).all()
    db_old_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=review.premisesgroup_uid).all()
    db_old_statement_ids = [p.statement_uid for p in db_old_premises]
    db_first_old_statement = DBDiscussionSession.query(Statement).get(db_old_premises[0].uid)
    discussion_lang = db_first_old_statement.lang
    db_user = DBDiscussionSession.query(User).get(review.detector_uid)

    if db_values:
        logger('review_main_helper', '__split_premisegroup', 'split given premisegroup into the mapped, new statements')
        db_statements = []
        for value in db_values:
            new_statement, tmp = set_statement(value, db_user.uid, db_first_old_statement.is_startpoint, db_old_premises[0].issue_uid, discussion_lang)
            db_statements.append(new_statement)
    else:
        logger('review_main_helper', '__split_premisegroup', 'just split the premisegroup')
        db_statements = DBDiscussionSession.query(Statement).filter(Statement.uid.in_(db_old_statement_ids)).all()

    # new premisegroups, for each statement a new one
    db_new_premisegroup_ids = []
    db_new_premise_ids = []
    for statement in db_statements:
        db_new_premisegroup = PremiseGroup(author=db_user.uid)
        DBDiscussionSession.add(db_new_premisegroup)
        DBDiscussionSession.flush()
        db_new_premisegroup_ids.append(db_new_premisegroup.uid)

        db_new_premise = Premise(db_new_premisegroup.uid, statement.uid, False, db_user.uid, statement.issue_uid)
        DBDiscussionSession.add(db_new_premise)
        DBDiscussionSession.flush()
        db_new_premise_ids.append(db_new_premise.uid)

        DBDiscussionSession.add(PremiseGroupSplitted(review.uid, review.premisesgroup_uid, db_new_premisegroup.uid))

    # swap the premisegroup occurence in every argument
    for new_pgroup_uid in db_new_premisegroup_ids:
        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=new_pgroup_uid).all()
        for argument in db_arguments:
            argument.set_premisegroup(new_pgroup_uid)
            DBDiscussionSession.add(argument)

    # swap the conclusion in every argument
    new_statements_uids = [s.uid for s in db_statements]
    for old_statement_uid in db_old_statement_ids:
        db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=old_statement_uid).all()
        for argument in db_arguments:
            argument.set_conclusion(new_statements_uids[0])
            DBDiscussionSession.add(argument)
            DBDiscussionSession.add(StatementReplacementsByPremiseGroupSplit(review.uid, old_statement_uid, new_statements_uids[0]))

            for statement_uid in new_statements_uids[1:]:
                db_argument = Argument(argument.premisesgroup_uid, argument.is_supportive, argument.author_uid, argument.issue_uid, statement_uid, argument.argument_uid, argument.is_disabled)
                DBDiscussionSession.add(db_argument)
                DBDiscussionSession.add(StatementReplacementsByPremiseGroupSplit(review.uid, old_statement_uid, statement_uid))

    # disable old premises
    # for premise in db_old_premises:
    #     premise.set_disable(True)
    #     DBDiscussionSession.add(premise)

    # disable old statements and premises
    # db_old_statements = DBDiscussionSession.query(Statement).filter(Statement.uid.in_(db_old_statement_ids)).all()
    # for element in db_old_premises + db_old_statements:
    #     element.set_disable(True)
    #     DBDiscussionSession.add(element)

    # finish
    DBDiscussionSession.flush()
    transaction.commit()
