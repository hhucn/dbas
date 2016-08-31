"""
Provides helping function for the review page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
from sqlalchemy import and_

from dbas.lib import get_user_by_private_or_public_nickname, get_text_for_argument_uid, sql_timestamp_pretty_print, get_public_nickname_based_on_settings
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, ReviewOptimization, LastReviewerOptimization, LastReviewerDelete, \
    ReviewDeleteReason, Argument, ArgumentSeenBy, ReputationReason, ReputationHistory
from dbas.helper.relation import RelationHelper
from dbas import user_management as _user_manager

pages = ['deletes', 'optimizations']
reputation = {'deletes': 15,
              'optimizations': 15,
              'history': 100}


def get_review_queues_array(mainpage, translator, nickname):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Array
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None

    review_list = list()
    review_list.append(__get_delete_dict(mainpage, translator, nickname))
    review_list.append(__get_optimization_dict(mainpage, translator, nickname))
    review_list.append(__get_history_dict(mainpage, translator, nickname))

    return review_list


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
    user_has_access = rep_count >= reputation[subpage_name] or all_rights
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


def __get_delete_dict(mainpage, translator, nickname):
    """
    Prepares dictionary for the a section.

    :param mainpage: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    task_count = __get_review_count_for(ReviewDelete, nickname)

    key = 'deletes'
    count, all_rights = get_reputation_of(nickname)
    tmp_dict = {'task_name': 'Deletes',
                'id': 'deletes',
                'url': mainpage + '/review/' + key,
                'icon': 'fa fa-trash-o',
                'task_count': task_count,
                'is_allowed': count >= reputation[key] or all_rights,
                'is_allowed_text': translator.get(translator.visitDeleteQueue),
                'is_not_allowed_text': translator.get(translator.visitDeleteQueueLimitation).replace('XX', str(reputation[key])),
                'last_reviews': __get_last_reviewer_of(LastReviewerDelete, mainpage)
                }
    return tmp_dict


def __get_optimization_dict(mainpage, translator, nickname):
    """
    Prepares dictionary for the a section.

    :param mainpage: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    task_count = __get_review_count_for(ReviewOptimization, nickname)

    key = 'optimizations'
    count, all_rights = get_reputation_of(nickname)
    tmp_dict = {'task_name': 'Optimizations',
                'id': 'flags',
                'url': mainpage + '/review/' + key,
                'icon': 'fa fa-flag',
                'task_count': task_count,
                'is_allowed': count >= reputation[key] or all_rights,
                'is_allowed_text': translator.get(translator.visitOptimizationQueue),
                'is_not_allowed_text': translator.get(translator.visitOptimizationQueueLimitation).replace('XX', str(reputation[key])),
                'last_reviews': __get_last_reviewer_of(LastReviewerOptimization, mainpage)
                }
    return tmp_dict


def __get_history_dict(mainpage, translator, nickname):
    """
    Prepares dictionary for the a section.

    :param mainpage: URL
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'history'
    count, all_rights = get_reputation_of(nickname)
    tmp_dict = {'task_name': 'History',
                'id': 'flags',
                'url': mainpage + '/review/' + key,
                'icon': 'fa fa-history',
                'task_count': '-',
                'is_allowed': count >= reputation[key] or all_rights,
                'is_allowed_text': translator.get(translator.visitHistoryQueue),
                'is_not_allowed_text': translator.get(translator.visitHistoryQueueLimitation).replace('XX', str(reputation[key])),
                'last_reviews': list()
                }
    return tmp_dict


def __get_review_count_for(review_type, nickname):
    """

    :param review_type:
    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if db_user:
        db_reviews = DBDiscussionSession.query(review_type).filter(and_(review_type.is_executed == False,
                                                                        review_type.detector_uid != db_user.uid)).all()
    else:
        db_reviews = DBDiscussionSession.query(review_type).filter_by(is_executed=False).all()
    return len(db_reviews)


def __get_last_reviewer_of(reviewer_type, mainpage):
    """

    :param reviewer_type:
    :param mainpage:
    :return:
    """
    users_array = list()
    db_reviews = DBDiscussionSession.query(reviewer_type).order_by(reviewer_type.uid.desc()).all()
    limit = 5 if len(db_reviews) > 5 else len(db_reviews)
    for x in range(limit):
        db_review = db_reviews[x]
        db_user = DBDiscussionSession.query(User).filter_by(uid=db_review.reviewer_uid).first()
        if db_user:
            tmp_dict = dict()
            tmp_dict['img_src'] = _user_manager.get_profile_picture(db_user, 40)
            tmp_dict['url'] = mainpage + '/user/' + db_user.get_global_nickname()
            tmp_dict['name'] = db_user.get_global_nickname()
            users_array.append(tmp_dict)
        else:
            limit += 1 if len(db_reviews) > limit else 0
    return users_array


def __get_users_array(mainpage):
    users_array = []
    for x in range(5):
        tmp_dict = {}
        db_user = DBDiscussionSession.query(User).filter_by(uid=random.randint(3, 38)).first()
        tmp_dict['img_src'] = _user_manager.get_profile_picture(db_user, 40)
        tmp_dict['url'] = mainpage + '/user/' + db_user.get_global_nickname()
        tmp_dict['name'] = db_user.get_global_nickname()
        users_array.append(tmp_dict)
    return users_array


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

    rnd_review = db_reviews[random.randint(0, len(db_reviews)-1)]
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

    rnd_review = db_reviews[random.randint(0, len(db_reviews)-1)]
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


def get_reputation_history(nickname, translator):
    """

    :param nickname:
    :param translator:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return dict()

    ret_dict = dict()
    count, all_rights = get_reputation_of(nickname)
    ret_dict['count'] = count
    ret_dict['all_rights'] = all_rights

    db_reputation = DBDiscussionSession.query(ReputationHistory) \
        .filter_by(reputator_uid=db_user.uid) \
        .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid) \
        .all()

    rep_list = list()
    for rep in db_reputation:
        date = sql_timestamp_pretty_print(rep.timestamp, translator.get_lang(), humanize=False)
        points_data = '<span class="success-description points">+' if rep.reputations.points > 0 else '<span class="error-description points">'
        points_data += str(rep.reputations.points) + '</span'
        points = rep.reputations.points
        action = translator.get(rep.reputations.reason)
        rep_list.append({'date': date, 'points_data': points_data, 'action': action, 'points': points})

    ret_dict['history'] = rep_list

    return ret_dict


def get_privilege_list(translator):
    """

    :param translator:
    :return:
    """

    reputations = list()
    # reputations.append({'points': 1000, 'icon': 'fa fa-arrow-down', 'text': 'Some text'})
    # reputations.append({'points': 750, 'icon': 'fa fa-arrow-up', 'text': 'Some text'})
    # reputations.append({'points': 500, 'icon': 'fa fa-hand-o-up', 'text': 'Some text'})
    # reputations.append({'points': 250, 'icon': 'fa fa-hand-o-down', 'text': 'Review a statement with many contra-arguments'})
    # reputations.append({'points': 200, 'icon': 'fa fa-times', 'text': 'Decide, whether it is spam or not'})
    # reputations.append({'points': 100, 'icon': 'fa fa-trash', 'text': 'Decision about statement, which should be deleted'})
    reputations.append({'points': reputation['history'], 'icon': 'fa fa-history', 'text': translator.get(translator.priv_history_queue)})
    reputations.append({'points': reputation['deletes'], 'icon': 'fa fa-pencil-square-o', 'text': translator.get(translator.priv_access_opti_queue)})
    reputations.append({'points': reputation['optimizations'], 'icon': 'fa fa-flag', 'text': translator.get(translator.priv_access_del_queue)})
    return reputations


def get_reputation_list(translator):
    """

    :param translator:
    :return:
    """
    gains = list()
    looses = list()

    db_gains = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points > 0).all()
    for gain in db_gains:
        gains.append({'text': translator.get(gain.reason),
                      'points': '+' + str(gain.points)})

    db_looses = DBDiscussionSession.query(ReputationReason).filter(ReputationReason.points < 0).all()
    for loose in db_looses:
        looses.append({'text': translator.get(loose.reason),
                       'points': loose.points})

    return {'gains': gains, 'looses': looses}


def get_reputation_of(nickname):
    """
    Return the total sum of reputation points for the given nickname

    :param nickname: Nickname of the user
    :return: Integer and Boolean, if the user is author
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    count = 0

    if db_user:
        db_reputation = DBDiscussionSession.query(ReputationHistory)\
            .filter_by(reputator_uid=db_user.uid)\
            .join(ReputationReason, ReputationReason.uid == ReputationHistory.reputation_uid)\
            .all()

        for reputation in db_reputation:
            count += reputation.reputations.points

    return count, _user_manager.is_user_author(nickname)


def __has_access_to_history(nickname):
    """

    :param nickname:
    :return:
    """
    return _user_manager.is_user_author(nickname) or get_reputation_of(nickname) > reputation['history']


def get_history(mainpage, nickname, translator):
    """

    :param nickname:
    :return:
    """
    ret_dict = dict()
    ret_dict['has_access'] = __has_access_to_history(nickname)

    deletes_list = __get_executed_reviews_of(mainpage, ReviewDelete, LastReviewerDelete, translator.get_lang())
    optimizations_list = __get_executed_reviews_of(mainpage, ReviewOptimization, LastReviewerOptimization, translator.get_lang())

    past_decision = [
        {
            'title': 'Delete Queue',
            'icon': 'fa fa-history',
            'queue': 'deletes',
            'content': deletes_list,
        },
        {
            'title': 'Optimization Queue',
            'queue': 'optimizations',
            'icon': 'fa fa-flag',
            'content': optimizations_list
         }
    ]
    ret_dict['past_decision'] = past_decision

    return ret_dict


def __get_executed_reviews_of(mainpage, table_type, last_review_type, lang):
    """
    Returns array with all relevant information about the last reviews of the given table.

    :param mainpage: Mainpage of D-BAS
    :param table_type: Type of the review table
    :param last_review_type: Type of the last reviewer of the table
    :param lang: current ui_locales
    :return: Array with all decision per table
    """
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed == True).order_by(table_type.uid.desc()).all()

    for review in db_reviews:
        # getting all pro and contra votes for this review
        pro_votes = DBDiscussionSession.query(last_review_type).filter(and_(last_review_type.review_uid == review.uid,
                                                                            last_review_type.is_okay == True)).all()
        con_votes = DBDiscussionSession.query(last_review_type).filter(and_(last_review_type.review_uid == review.uid,
                                                                            last_review_type.is_okay == False)).all()
        # getting the users which have voted
        pro_list = list()
        con_list = list()
        for pro in pro_votes:
            pro_list.append(__get_user_dict_for_review(pro.reviewer_uid, mainpage))
        for con in con_votes:
            con_list.append(__get_user_dict_for_review(con.reviewer_uid, mainpage))

        # and build up some dict
        entry = dict()
        entry['pro'] = pro_list
        entry['con'] = con_list
        entry['timestamp'] = sql_timestamp_pretty_print(review.timestamp, lang)
        entry['votes_pro'] = pro_list
        entry['votes_con'] = con_list
        some_list.append(entry)

    return some_list


def __get_user_dict_for_review(user_id, mainpage):
    """
    Fetches some data of the given user.

    :param reviewer_uid: User id of the reviewer
    :param mainpage: Mainpage of D-BAS
    :return: dcit with gravatar, uerpage and nickname
    """
    db_user = DBDiscussionSession.query(User).filter_by(uid=user_id).first()
    image_url = _user_manager.get_profile_picture(db_user, 20)
    return {
        'gravatar_url': image_url,
        'nickname': get_public_nickname_based_on_settings(db_user),
        'userpage_url': mainpage + '/user/' + get_public_nickname_based_on_settings(db_user)
    }
