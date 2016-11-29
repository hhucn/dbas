"""
Provides helping function for displaying subpages like the edit queue.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, ReviewOptimization, ReviewDeleteReason, Argument,\
    Issue, LastReviewerDelete, LastReviewerOptimization, ReviewEdit, LastReviewerEdit, ReviewEditValue, Statement, \
    sql_timestamp_pretty_print
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid,\
    get_text_for_premisesgroup_uid, get_profile_picture
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of, reputation_borders
from dbas.strings.keywords import Keywords as _
from sqlalchemy import and_

pages = ['deletes', 'optimizations', 'edits']


def get_subpage_elements_for(request, subpage_name, nickname, translator):
    """

    :param request:
    :param subpage_name:
    :param nickname:
    :param translator:
    :return:
    """
    logger('ReviewSubpagerHelper', 'get_subpage_elements_for', subpage_name)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    user_has_access = False
    no_arguments_to_review = False
    button_set = {'is_delete': False, 'is_optimize': False, 'is_edit': False}

    # does the subpage exists
    if subpage_name not in pages and subpage_name != 'history':
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    rep_count, all_rights = get_reputation_of(nickname)
    user_has_access = rep_count >= reputation_borders[subpage_name] or all_rights
    # does the user exists and does he has the rights for this queue?
    if not db_user or not user_has_access:
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    ret_dict = dict()
    ret_dict['page_name'] = subpage_name

    # get a random argument for reviewing
    text = translator.get(_.internalError)
    reason = ''
    stats = ''
    issue = translator.get(_.internalError)

    if subpage_name == 'deletes':
        subpage_dict = __get_subpage_dict_for_deletes(request, db_user, translator, request.application_url)
        button_set['is_delete'] = True
        button_set['is_optimize'] = False
        button_set['is_edit'] = False

    elif subpage_name == 'optimizations':
        subpage_dict = __get_subpage_dict_for_optimization(request, db_user, translator, request.application_url)
        button_set['is_delete'] = False
        button_set['is_optimize'] = True
        button_set['is_edit'] = False

    elif subpage_name == 'edits':
        subpage_dict = __get_subpage_dict_for_edits(request, db_user, translator, request.application_url)
        button_set['is_delete'] = False
        button_set['is_optimize'] = False
        button_set['is_edit'] = True

    else:
        subpage_dict = {'stats': stats, 'text': text, 'reason': reason, 'issue': issue}

    ret_dict['reviewed_argument'] = subpage_dict
    if subpage_dict['text'] is None and subpage_dict['reason'] is None and subpage_dict['stats'] is None:
        no_arguments_to_review = True
        return __get_subpage_dict(None, user_has_access, no_arguments_to_review, button_set)

    return __get_subpage_dict(ret_dict, True, no_arguments_to_review, button_set)


def __get_subpage_dict(ret_dict, has_access, no_arguments_to_review, button_set):
    """

    :param ret_dict:
    :param has_access:
    :param no_arguments_to_review:
    :param button_set:
    :return:
    """
    return {'elements': ret_dict,
            'has_access': has_access,
            'no_arguments_to_review': no_arguments_to_review,
            'button_set': button_set}


def __get_all_allowed_reviews_for_user(request, session_keyword, db_user, review_type, last_reviewer_type):
    """
    Returns all reviews from given type, whereby already seen and reviewed reviews are restricted.

    :param request: current request
    :param session_keyword: keyword of 'already_seen' element in request.session
    :param db_user: current user
    :param review_type: data table of reviews
    :param last_reviewer_type: data table of last reviewers
    :return: all revies, list of already seen reviews as uids, list of already reviewed reviews as uids, boolean if the user reviews for the first time in this session
    """
    # only get arguments, which the user has not seen yet
    logger('ReviewSubpagerHelper', '__get_all_allowed_reviews_for_user', 'main')
    already_seen, first_time = (request.session[session_keyword], False) if session_keyword in request.session else (list(), True)

    # and not reviewed
    db_last_reviews_of_user = DBDiscussionSession.query(last_reviewer_type).filter_by(reviewer_uid=db_user.uid).all()
    already_reviewed = []
    for last_review in db_last_reviews_of_user:
        already_reviewed.append(last_review.review_uid)

    # get all reviews
    db_reviews = DBDiscussionSession.query(review_type).filter(and_(review_type.is_executed == False,
                                                                    review_type.detector_uid != db_user.uid))

    # filter the ones, we have already seen
    if len(already_seen) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_seen))

    # filter the ones, we have already reviewed
    if len(already_reviewed) > 0:
        db_reviews = db_reviews.filter(~review_type.uid.in_(already_reviewed))

    return db_reviews.all(), already_seen, already_reviewed, first_time


def __get_subpage_dict_for_deletes(request, db_user, translator, main_page):
    """

    :param request:
    :param db_user:
    :param translator:
    :param main_page:
    :return:
    """
    logger('ReviewSubpagerHelper', '__get_subpage_dict_for_deletes', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(request, 'already_seen_deletes', db_user, ReviewDelete, LastReviewerDelete)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.is_executed == False,
                                                                         ReviewDelete.detector_uid != db_user.uid))
        if len(already_reviewed) > 0:
            db_reviews = db_reviews.filter(~ReviewDelete.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()
    if not db_reviews:
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
        text = get_text_for_argument_uid(db_argument.uid)
        issue = DBDiscussionSession.query(Issue).filter_by(uid=db_argument.issue_uid).first().title
    else:
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=rnd_review.statement_uid).first()
        text = get_text_for_statement_uid(db_statement.uid)
        issue = DBDiscussionSession.query(Issue).filter_by(uid=db_statement.issue_uid).first().title

    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(uid=rnd_review.reason_uid).first()
    stats = __get_stats_for_review(rnd_review, translator.get_lang(), main_page)

    reason = ''
    if db_reason.reason == 'offtopic':
        reason = translator.get(_.argumentFlaggedBecauseOfftopic)
    if db_reason.reason == 'spam':
        reason = translator.get(_.argumentFlaggedBecauseSpam)
    if db_reason.reason == 'harmful':
        reason = translator.get(_.argumentFlaggedBecauseHarmful)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_deletes'] = already_seen

    return {'stats': stats,
            'text': text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info}


def __get_subpage_dict_for_optimization(request, db_user, translator, main_page):
    """

    :param request:
    :param db_user:
    :param translator:
    :param main_page:
    :return:
    """
    logger('ReviewSubpagerHelper', '__get_subpage_dict_for_optimization', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(request,
                                                                                                'already_seen_optimization',
                                                                                                db_user, ReviewOptimization,
                                                                                                LastReviewerOptimization)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.is_executed == False,
                                                                               ReviewOptimization.detector_uid != db_user.uid))
        if len(already_reviewed) > 0:
            db_reviews = db_reviews.filter(~ReviewOptimization.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
        text = get_text_for_argument_uid(db_argument.uid)
        issue = DBDiscussionSession.query(Issue).filter_by(uid=db_argument.issue_uid).first().title
        parts = __get_text_parts_of_argument(db_argument)
    else:
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=rnd_review.statement_uid).first()
        text = get_text_for_statement_uid(db_statement.uid)
        issue = DBDiscussionSession.query(Issue).filter_by(uid=db_statement.issue_uid).first().title
        parts = [__get_part_dict('statement', text, 0, rnd_review.statement_uid)]

    reason = translator.get(_.argumentFlaggedBecauseOptimization)

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), main_page)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_optimization'] = already_seen

    return {'stats': stats,
            'text': text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'parts': parts}


def __get_subpage_dict_for_edits(request, db_user, translator, main_page):
    """

    :param request:
    :param db_user:
    :param translator:
    :param main_page:
    :return:
    """
    logger('ReviewSubpagerHelper', '__get_subpage_dict_for_edits', 'main')
    db_reviews, already_seen, already_reviewed, first_time = __get_all_allowed_reviews_for_user(request,
                                                                                                'already_seen_edit',
                                                                                                db_user,
                                                                                                ReviewEdit,
                                                                                                LastReviewerEdit)

    extra_info = ''
    # if we have no reviews, try again with fewer restrictions
    if not db_reviews:
        already_seen = list()
        extra_info = 'already_seen' if not first_time else ''
        db_reviews = DBDiscussionSession.query(ReviewEdit).filter(and_(ReviewEdit.is_executed == False,
                                                                       ReviewEdit.detector_uid != db_user.uid))
        if len(already_reviewed) > 0:
            db_reviews = db_reviews.filter(~ReviewEdit.uid.in_(already_reviewed))
        db_reviews = db_reviews.all()

    if not db_reviews:
        return {'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None}

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    if rnd_review.statement_uid is None:
        db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
        text = get_text_for_argument_uid(db_argument.uid)
        issue = DBDiscussionSession.query(Issue).filter_by(uid=db_argument.issue_uid).first().title
    else:
        db_statement = DBDiscussionSession.query(Statement).filter_by(uid=rnd_review.statement_uid).first()
        text = get_text_for_statement_uid(db_statement.uid)
        issue = DBDiscussionSession.query(Issue).filter_by(uid=db_statement.issue_uid).first().title
    reason = translator.get(_.argumentFlaggedBecauseEdit)

    # build correction
    correction = '<span class="text-muted">' + text + '</span>'
    db_values = DBDiscussionSession.query(ReviewEditValue).filter_by(review_edit_uid=rnd_review.uid).all()
    if not db_values:
        correction = translator.get(_.internalKeyError)
    for value in db_values:
        oem_text = get_text_for_statement_uid(value.statement_uid)
        pos = correction.lower().find(oem_text.lower())
        correction = correction[0:pos] + '<span class="text-warning">' + value.content + '</span>' + correction[pos + len(oem_text):]

        pos = text.lower().find(oem_text.lower())
        text = text[0:pos] + '<span class="text-warning">' + text[pos:pos + len(oem_text)] + '</span>' + text[pos + len(oem_text):]

    stats = __get_stats_for_review(rnd_review, translator.get_lang(), main_page)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_edit'] = already_seen

    return {'stats': stats,
            'text': text,
            'correction': correction,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info}


def __get_stats_for_review(review, ui_locales, main_page):
    """

    :param argument_uid:
    :param review:
    :param ui_locales:
    :return:
    """
    logger('ReviewSubpagerHelper', '__get_stats_for_review', 'main')
    # viewed = len(DBDiscussionSession.query(ArgumentSeenBy).filter_by(argument_uid=argument_uid).all())

    # _rh = RelationHelper(argument_uid)
    # undermines = _rh.get_undermines_for_argument_uid()
    # undercuts = _rh.get_undercuts_for_argument_uid()
    # rebuts = _rh.get_rebuts_for_argument_uid()
    # supports = _rh.get_supports_for_argument_uid()

    # len_undermines = len(undermines) if undermines else 0
    # len_undercuts = len(undercuts) if undercuts else 0
    # len_rebuts = len(rebuts) if rebuts else 0
    # len_supports = len(supports) if supports else 0
    # attacks = len_undermines + len_undercuts + len_rebuts

    db_reporter = DBDiscussionSession.query(User).filter_by(uid=review.detector_uid).first()

    stats = dict()
    stats['reported'] = sql_timestamp_pretty_print(review.timestamp, ui_locales)
    stats['reporter'] = db_reporter.get_global_nickname()
    stats['reporter_gravatar'] = get_profile_picture(db_reporter, 20)
    stats['reporter_url'] = main_page + '/user/' + stats['reporter']
    stats['id'] = str(review.uid)
    # stats['viewed'] = viewed
    # stats['attacks'] = attacks
    # stats['supports'] = len_supports

    return stats


def __get_text_parts_of_argument(argument):
    """

    :param argument:
    :return:
    """
    logger('ReviewSubpagerHelper', '__get_text_parts_of_argument', 'main')
    ret_list = list()

    # get premise of current argument
    premisegroup, premises_uid = get_text_for_premisesgroup_uid(argument.premisesgroup_uid)
    for uid in premises_uid:
        logger('ReviewSubpagerHelper', '__get_text_parts_of_argument', 'add premise of argument ' + str(argument.uid))
        text = get_text_for_statement_uid(uid)
        ret_list.append(__get_part_dict('premise', text, argument.uid, uid))

    if argument.argument_uid is None:  # get conlusion of current argument
        conclusion = get_text_for_statement_uid(argument.conclusion_uid)
        logger('ReviewSubpagerHelper', '__get_text_parts_of_argument', 'add statement of argument ' + str(argument.uid))
        ret_list.append(__get_part_dict('conclusion', conclusion, argument.uid, argument.conclusion_uid))
    else:  # or get the conclusions argument
        db_conclusions_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument.argument_uid).first()

        while db_conclusions_argument.argument_uid is not None:  # get further conclusions arguments

            # get premise of conclusions arguments
            premisegroup, premises_uid = get_text_for_premisesgroup_uid(db_conclusions_argument.premisesgroup_uid)
            for uid in premises_uid:
                text = get_text_for_statement_uid(uid)
                logger('ReviewSubpagerHelper', '__get_text_parts_of_argument', 'add premise of argument ' + str(db_conclusions_argument.uid))
                ret_list.append(__get_part_dict('premise', text, db_conclusions_argument.uid, uid))

            db_conclusions_argument = DBDiscussionSession.query(Argument).filter_by(uid=db_conclusions_argument.argument_uid).first()

        # get the last conclusion of the chain
        conclusion = get_text_for_statement_uid(db_conclusions_argument.conclusion_uid)
        logger('ReviewSubpagerHelper', '__get_text_parts_of_argument', 'add statement of argument ' + str(db_conclusions_argument.uid))
        ret_list.append(__get_part_dict('conclusion', conclusion, db_conclusions_argument.uid, db_conclusions_argument.conclusion_uid))

    return ret_list[::-1]


def __get_part_dict(typeof, text, argument, uid):
    """

    :param typeof:
    :param text:
    :param argument:
    :param uid:
    :return:
    """
    logger('ReviewSubpagerHelper', '__get_part_dict', 'type: ' + str(typeof) + ', text: ' + str(text) + ', arg: ' + str(argument) + ', uid: ' + str(uid))
    logger('ReviewSubpagerHelper', '__get_part_dict', 'type: ' + str(typeof) + ', text: ' + str(text) + ', arg: ' + str(argument) + ', uid: ' + str(uid))
    logger('ReviewSubpagerHelper', '__get_part_dict', 'type: ' + str(typeof) + ', text: ' + str(text) + ', arg: ' + str(argument) + ', uid: ' + str(uid))
    return {'type': typeof,
            'text': text,
            'argument_uid': argument,
            'statement_uid': uid}
