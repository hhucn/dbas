"""
Provides helping function for the managing reputation.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import dbas.user_management as _user_manager
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, ReviewDelete, LastReviewerDelete, ReviewOptimization, \
    LastReviewerOptimization
from dbas.review.helper.reputation import get_reputation_of
from dbas.review.helper.subpage import reputation_borders
from sqlalchemy import and_


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
                'is_allowed': count >= reputation_borders[key] or all_rights,
                'is_allowed_text': translator.get(translator.visitDeleteQueue),
                'is_not_allowed_text': translator.get(translator.visitDeleteQueueLimitation).replace('XX', str(reputation_borders[key])),
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
                'is_allowed': count >= reputation_borders[key] or all_rights,
                'is_allowed_text': translator.get(translator.visitOptimizationQueue),
                'is_not_allowed_text': translator.get(translator.visitOptimizationQueueLimitation).replace('XX', str(reputation_borders[key])),
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
                'is_allowed': count >= reputation_borders[key] or all_rights,
                'is_allowed_text': translator.get(translator.visitHistoryQueue),
                'is_not_allowed_text': translator.get(translator.visitHistoryQueueLimitation).replace('XX', str(reputation_borders[key])),
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