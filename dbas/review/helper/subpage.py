"""
Provides helping function for the review page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, ReviewOptimization, ReviewDeleteReason, Argument, ArgumentSeenBy
from dbas.helper.relation import RelationHelper
from dbas.lib import get_text_for_argument_uid, sql_timestamp_pretty_print
from dbas.logger import logger
from dbas.review.helper.reputation import get_reputation_of, reputation_borders
from sqlalchemy import and_

pages = ['deletes', 'optimizations']


def get_subpage_elements_for(request, subpage_name, nickname, translator):
    """

    :param request:
    :param subpage_name:
    :param nickname:
    :param translator:
    :return:
    """
    logger('ReviewPagerHelper', 'get_subpage_elements_for', subpage_name)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    user_has_access = False
    no_arguments_to_review = False
    button_set = {'is_delete': False, 'is_optimize': False}

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
    text = translator.get(translator.internalError)
    reason = ''
    stats = ''

    if subpage_name == 'deletes':
        text, reason, stats = __get_subpage_for_deletes(request, db_user, translator)
        button_set['is_delete'] = True

    elif subpage_name == 'optimizations':
        text, reason, stats = __get_subpage_for_optimization(request, db_user, translator)
        button_set['is_optimize'] = True

    ret_dict['reviewed_argument'] = {'stats': stats,
                                     'text': text,
                                     'reason': reason}

    if text is None and reason is None and stats is None:
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


def __get_subpage_for_deletes(request, db_user, translator):
    """

    :param request:
    :param db_user:
    :param translator:
    :return:
    """
    # only get arguments, which the user has not seen yet
    already_seen = request.session['already_seen_deletes'] if 'already_seen_deletes' in request.session else list()
    db_reviews = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.is_executed == False,
                                                                     ReviewDelete.detector_uid != db_user.uid,
                                                                     ReviewDelete.uid not in already_seen)).all()
    # maybe there are not argument or the user has seen everything, try again
    if not db_reviews:
        already_seen = list()
        db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.is_executed == False,
                                                                               ReviewOptimization.detector_uid != db_user.uid)).all()
    if not db_reviews:
        return None, None, None

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
    text = get_text_for_argument_uid(db_argument.uid)
    db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(uid=rnd_review.reason_uid).first()

    stats = __get_stats_for_argument(db_argument.uid)
    stats['reported'] = sql_timestamp_pretty_print(rnd_review.timestamp, translator.get_lang())
    stats['id'] = str(rnd_review.uid)

    reason = ''
    if db_reason.reason == 'offtopic':
        reason = translator.get(translator.argumentFlaggedBecauseOfftopic)
    if db_reason.reason == 'spam':
        reason = translator.get(translator.argumentFlaggedBecauseSpam)
    if db_reason.reason == 'harmful':
        reason = translator.get(translator.argumentFlaggedBecauseHarmful)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_deletes'] = already_seen

    return text, reason, stats


def __get_subpage_for_optimization(request, db_user, translator):
    """

    :param request:
    :param db_user:
    :param translator:
    :return:
    """
    # only get arguments, which the user has not seen yet
    already_seen = request.session['already_seen_optimization'] if 'already_seen_optimization' in request.session else list()
    db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.is_executed == False,
                                                                           ReviewOptimization.detector_uid != db_user.uid,
                                                                           ReviewOptimization.uid not in already_seen)).all()
    # maybe there are not argument or the user has seen everything, try again
    if not db_reviews:
        already_seen = list()
        db_reviews = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.is_executed == False,
                                                                               ReviewOptimization.detector_uid != db_user.uid)).all()

    if not db_reviews:
        return None, None, None

    rnd_review = db_reviews[random.randint(0, len(db_reviews) - 1)]
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=rnd_review.argument_uid).first()
    text = get_text_for_argument_uid(db_argument.uid)
    reason = translator.get(translator.argumentFlaggedBecauseOptimization)

    stats = __get_stats_for_argument(db_argument.uid)
    stats['reported'] = sql_timestamp_pretty_print(rnd_review.timestamp, translator.get_lang())
    stats['id'] = str(rnd_review.uid)

    already_seen.append(rnd_review.uid)
    request.session['already_seen_optimization'] = already_seen

    return text, reason, stats


def __get_stats_for_argument(argument_uid):
    """

    :param argument_uid:
    :return:
    """
    viewed = len(DBDiscussionSession.query(ArgumentSeenBy).filter_by(argument_uid=argument_uid).all())

    _rh = RelationHelper(argument_uid)
    undermines = _rh.get_undermines_for_argument_uid()
    undercuts = _rh.get_undercuts_for_argument_uid()
    rebuts = _rh.get_rebuts_for_argument_uid()
    supports = _rh.get_supports_for_argument_uid()

    len_undermines = len(undermines) if undermines else 0
    len_undercuts = len(undercuts) if undercuts else 0
    len_rebuts = len(rebuts) if rebuts else 0
    len_supports = len(supports) if supports else 0

    attacks = len_undermines + len_undercuts + len_rebuts

    return {'viewed': viewed, 'attacks': attacks, 'supports': len_supports}
