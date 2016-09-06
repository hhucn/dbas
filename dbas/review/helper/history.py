"""
Provides helping function for the managing reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import ReviewDelete, LastReviewerDelete, ReviewOptimization, LastReviewerOptimization, \
    User, ReputationHistory, ReputationReason, ReviewDeleteReason
from dbas.lib import sql_timestamp_pretty_print, get_public_nickname_based_on_settings, get_text_for_argument_uid, get_profile_picture, is_user_author
from dbas.review.helper.reputation import get_reputation_of, reputation_borders, reputation_icons
from dbas.review.helper.main import en_or_disable_arguments_and_premise_of_review
from sqlalchemy import and_
from dbas.strings.translator import Translator


def get_complete_review_history(mainpage, nickname, translator, is_not_executed=False):
    """

    :param mainpage:
    :param nickname:
    :param translator:
    :param is_not_executed:
    :return:
    """
    ret_dict = dict()
    if is_not_executed:
        ret_dict['has_access'] = is_user_author(nickname)
    else:
        ret_dict['has_access'] = __has_access_to_history(nickname)
    ret_dict['is_history'] = not is_not_executed

    deletes_list = __get_executed_reviews_of('deletes', mainpage, ReviewDelete, LastReviewerDelete, translator, is_not_executed)
    optimizations_list = __get_executed_reviews_of('optimizations', mainpage, ReviewOptimization, LastReviewerOptimization, translator, is_not_executed)

    past_decision = [{
        'title': 'Delete Queue',
        'icon': reputation_icons['deletes'],
        'queue': 'deletes',
        'content': deletes_list,
        'has_reason': True
    }, {
        'title': 'Optimization Queue',
        'queue': reputation_icons['optimizations'],
        'icon': 'fa fa-flag',
        'content': optimizations_list,
        'has_reason': False
    }]
    ret_dict['past_decision'] = past_decision

    return ret_dict


def get_reputation_history_of(nickname, translator):
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
        .order_by(ReputationHistory.uid.asc())\
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


def __get_executed_reviews_of(table, mainpage, table_type, last_review_type, translator, is_not_executed=False):
    """
    Returns array with all relevant information about the last reviews of the given table.

    :param table: Shortcut for the table
    :param mainpage: Mainpage of D-BAS
    :param table_type: Type of the review table
    :param last_review_type: Type of the last reviewer of the table
    :param translator: current ui_locales
    :param is_not_executed
    :return: Array with all decision per table
    """
    some_list = list()
    db_reviews = DBDiscussionSession.query(table_type).filter(table_type.is_executed != is_not_executed).order_by(table_type.uid.desc()).all()

    for review in db_reviews:
        fulltext = get_text_for_argument_uid(review.argument_uid)
        shorttext = '<span class="text-primary">'
        intro = translator.get(translator.otherUsersSaidThat) + ' '
        if fulltext.startswith(intro):
            shorttext += fulltext[len(intro):len(intro) + 1].upper() + fulltext[len(intro) + 1:len(intro) + 15]
        else:
            shorttext += fulltext[0:15]
        shorttext += '...' + '<span>'

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
        entry['entry_id'] = review.uid
        if table == 'deletes':
            db_reason = DBDiscussionSession.query(ReviewDeleteReason).filter_by(uid=review.reason_uid).first()
            entry['reason'] = db_reason.reason
        entry['row_id'] = table + str(review.uid)
        entry['argument_shorttext'] = shorttext
        entry['argument_fulltext'] = fulltext
        entry['pro'] = pro_list
        entry['con'] = con_list
        entry['timestamp'] = sql_timestamp_pretty_print(review.timestamp, translator.get_lang())
        entry['votes_pro'] = pro_list
        entry['votes_con'] = con_list
        some_list.append(entry)

    return some_list


def __get_user_dict_for_review(user_id, mainpage):
    """
    Fetches some data of the given user.

    :param mainpage: Mainpage of D-BAS
    :return: dcit with gravatar, uerpage and nickname
    """
    db_user = DBDiscussionSession.query(User).filter_by(uid=user_id).first()
    image_url = get_profile_picture(db_user, 20)
    return {
        'gravatar_url': image_url,
        'nickname': get_public_nickname_based_on_settings(db_user),
        'userpage_url': mainpage + '/user/' + get_public_nickname_based_on_settings(db_user)
    }


def __has_access_to_history(nickname):
    """

    :param nickname:
    :return:
    """
    reputation_count, is_user_author = get_reputation_of(nickname)
    return is_user_author or reputation_count > reputation_borders['history']


def revoke_decision(queue, uid, lang, transaction):
    """

    :param queue:
    :param uid:
    :param lang:
    :param transaction:
    :return:
    """
    success = ''
    error = ''
    _t = Translator(lang)
    if queue == 'deletes':
        __revoke_decision_and_implications(ReviewDelete, LastReviewerDelete, uid, transaction)

        success = _t.get(_t.dataRemoved)
    elif queue == 'optimizations':
        __revoke_decision_and_implications(ReviewOptimization, LastReviewerOptimization, uid, transaction)
        success = _t.get(_t.dataRemoved)

    else:
        error = _t.get(_t.internalKeyError)

    return success, error


def cancel_decision(queue, uid, lang, transaction):
    """

    :param queue:
    :param uid:
    :param lang:
    :param transaction:
    :return:
    """
    success = ''
    error = ''
    _t = Translator(lang)
    if queue == 'deletes':
        __revoke_decision_and_implications(ReviewDelete, LastReviewerDelete, uid, transaction)

        success = _t.get(_t.dataRemoved)
    elif queue == 'optimizations':
        __revoke_decision_and_implications(ReviewOptimization, LastReviewerOptimization, uid, transaction)
        success = _t.get(_t.dataRemoved)

    else:
        error = _t.get(_t.internalKeyError)

    return success, error


def __revoke_decision_and_implications(type, reviewer_type, uid, transaction):
    """

    :param type:
    :param reviewer_type:
    :param uid:
    :param transaction:
    :return:
    """
    DBDiscussionSession.query(reviewer_type).filter_by(review_uid=uid).delete()

    db_review = DBDiscussionSession.query(type).filter_by(uid=uid).first()
    en_or_disable_arguments_and_premise_of_review(db_review, False)

    DBDiscussionSession.query(type).filter_by(uid=uid).delete()
    transaction.commit()
