"""
Provides helping function for the review page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
from slugify import slugify

from dbas.lib import get_user_by_private_or_public_nickname
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Issue, Argument
from dbas import user_management as UserManager

pages = ['edits', 'deletes', 'flags', 'random', 'duplicates', 'freshest']
reputation = {'deletes': 200,
              'flags': 150,
              'freshest': 75,
              'random': 50,
              'edits': 25,
              'duplicates': 10}


def get_review_array(mainpage, slug, translator, nickname):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param slug: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Array
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None

    db_issues = DBDiscussionSession.query(Issue).all()
    slugs = list()
    for issue in db_issues:
        slugs.append(str(slugify(issue.title)))
    if slug not in slugs:
        return None

    review_list = list()
    review_list.append(__get_edit_dict(mainpage, slug, translator, nickname))
    review_list.append(__get_delete_dict(mainpage, slug, translator, nickname))
    review_list.append(__get_flag_dict(mainpage, slug, translator, nickname))
    review_list.append(__get_random_dict(mainpage, slug, translator, nickname))
    review_list.append(__get_duplicate_dict(mainpage, slug, translator, nickname))
    review_list.append(__get_freshest_dict(mainpage, slug, translator, nickname))

    return review_list


def get_subpage_for(subpage_name, nickname):
    """

    :param subpage_name:
    :param nickname:
    :return:
    """
    logger('ReviewHelper', 'get_subpage_for', subpage_name)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return None

    if subpage_name in pages and subpage_name not in ['deletes', 'flags']:
        return subpage_name

    return None


def __get_edit_dict(mainpage, issue, translator, nickname):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'edits'
    tmp_dict = {'task_name': 'Edits',
                'id': 'edits',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-eraser',
                'task_count': 2,
                'is_allowed': get_reputation_of(nickname) >= reputation[key],
                'is_allowed_text': 'Visit the edit queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review edits.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_delete_dict(mainpage, issue, translator, nickname):
    """
    Prepares dictionary for the delete section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'deletes'
    tmp_dict = {'task_name': 'Deletes',
                'id': 'deletes',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-trash-o',
                'task_count': 4,
                'is_allowed': get_reputation_of(nickname) >= reputation[key],
                'is_allowed_text': 'Visit the delete queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review deletes.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_flag_dict(mainpage, issue, translator, nickname):
    """
    Prepares dictionary for the flag section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'flags'
    tmp_dict = {'task_name': 'Flags',
                'id': 'flags',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-flag',
                'task_count': 8,
                'is_allowed': get_reputation_of(nickname) >= reputation[key],
                'is_allowed_text': 'Visit the review queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review edits.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_random_dict(mainpage, issue, translator, nickname):
    """
    Prepares dictionary for the random section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'random'
    tmp_dict = {'task_name': 'Random',
                'id': 'random',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-random',
                'task_count': '-',
                'is_allowed': get_reputation_of(nickname) >= reputation[key],
                'is_allowed_text': 'Visit the random queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review random statements.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_duplicate_dict(mainpage, issue, translator, nickname):
    """
    Prepares dictionary for the duplicate section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'duplicates'
    tmp_dict = {'task_name': 'Duplicates',
                'id': 'duplicates',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-files-o',
                'task_count': '-',
                'is_allowed': get_reputation_of(nickname) >= reputation[key],
                'is_allowed_text': 'Visit the duplicate queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review duplicated statements.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_freshest_dict(mainpage, issue, translator, nickname):
    """
    Prepares dictionary for the freshest section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :param nickname: Users nickname
    :return: Dict()
    """
    key = 'freshest'
    tmp_dict = {'task_name': 'First Posts',
                'id': 'firstposts',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-level-up',
                'task_count': '3',
                'is_allowed': get_reputation_of(nickname) >= reputation[key],
                'is_allowed_text': 'Visit the newest statements queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review freshest statements.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_users_array(mainpage):
    users_array = []
    for x in range(5):
        tmp_dict = {}
        db_user = DBDiscussionSession.query(User).filter_by(uid=random.randint(3, 38)).first()
        tmp_dict['img_src'] = UserManager.get_profile_picture(db_user, 40)
        tmp_dict['url'] = mainpage + '/user/' + db_user.get_global_nickname()
        tmp_dict['name'] = db_user.get_global_nickname()
        users_array.append(tmp_dict)
    return users_array


def get_reputation_history(nickname):
    """

    :return:
    """
    current_user = get_user_by_private_or_public_nickname(nickname)
    if not current_user:
        return dict()

    ret_dict = dict()
    ret_dict['count'] = get_reputation_of(nickname)

    rep_list = list()
    rep_list.append({'date': '20.08.2016', 'points_data': '<span class="success-description points">1</span>', 'action': 'first click in a discussion', 'points': 1})
    rep_list.append({'date': '21.08.2016', 'points_data': '<span class="success-description points">1</span>', 'action': 'first switch of the discussions topic', 'points': 1})
    rep_list.append({'date': '21.08.2016', 'points_data': '<span class="success-description points">3</span>', 'action': 'edited a statement successfully', 'points': 3})
    rep_list.append({'date': '22.08.2016', 'points_data': '<span class="error-description points">-1</span>',  'action': 'edited a statement vainly',  'points': -1})
    rep_list.append({'date': '22.08.2016', 'points_data': '<span class="error-description points">-1</span>',  'action': 'edited a statement vainly',  'points': -1})
    rep_list.append({'date': '22.08.2016', 'points_data': '<span class="success-description points">3</span>', 'action': 'mark a statement as spam successfully', 'points': 3})
    rep_list.append({'date': '23.08.2016', 'points_data': '<span class="success-description points">2</span>', 'action': 'voted for a deletion successfully', 'points': 2})
    rep_list.append({'date': '23.08.2016', 'points_data': '<span class="error-description points">-1</span>',  'action': 'voted for a deletion vainly',  'points': -1})

    ret_dict['history'] = rep_list

    return ret_dict


def get_reputation_list():
    """

    :return:
    """
    reputations = list()
    reputations.append({'points': 1000, 'icon': 'fa fa-arrow-down', 'text': 'Some text'})
    reputations.append({'points': 750, 'icon': 'fa fa-arrow-up', 'text': 'Some text'})
    reputations.append({'points': 500, 'icon': 'fa fa-hand-o-up', 'text': 'Some text'})
    reputations.append({'points': 250, 'icon': 'fa fa-hand-o-down', 'text': 'Review a statement with many contra-arguments'})
    reputations.append({'points': 200, 'icon': 'fa fa-times', 'text': 'Decide, whether it is spam or not'})
    reputations.append({'points': 100, 'icon': 'fa fa-trash', 'text': 'Decision about statement, which should be deleted'})
    reputations.append({'points': 50, 'icon': 'fa fa-pencil-square-o', 'text': 'Review edited statements'})
    reputations.append({'points': 15, 'icon': '', 'text': 'Stackoverflow: Users with 15 rep can flag posts.'})
    reputations.append({'points': 500, 'icon': '', 'text': 'Stackoverflow: Users with 500 rep can review posts from new users.'})
    reputations.append({'points': 2000, 'icon': '', 'text': 'Stackoverflow: Users with 2000 rep can edit any question or answer in the system.'})
    reputations.append({'points': 3000, 'icon': '', 'text': 'Stackoverflow: Users with 3000 rep can cast close and open votes.'})
    reputations.append({'points': 10000, 'icon': '', 'text': 'Stackoverflow: Users with 10000 rep can cast delete and undelete votes on questions, and have access to a moderation dashboard.'})
    reputations.append({'points': 15000, 'icon': '', 'text': 'Stackoverflow: Users with 15000 rep can protect posts.'})
    reputations.append({'points': 20000, 'icon': '', 'text': 'Stackoverflow: Users with 20000 rep can cast delete votes on negatively voted answers.'})
    return reputations


def get_reputation_of(nickname):
    """

    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        return 0

    return 70


def flag_argument(uid, reason, nickname, translator):
    """

    :param uid:
    :param reason:
    :param nickname:
    :param translator:
    :return:
    """
    db_argument = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_argument or not db_user:
        return -1, translator.get(translator.internalKeyError)

    ret_success = ''
    ret_info = ''
    ret_error = ''

    # error if user reports an argument twice
    # notification to the author of the flagged argument

    if reason == 'offtopic':
        ret_value = 1
        ret_success = translator.get(translator.thxForFlagText)

    elif reason == 'spam':
        ret_value = 2
        ret_info = translator.get(translator.alreadyFlagged)
        ret_success = translator.get(translator.thxForFlagText)

    elif reason == 'harmful':
        ret_value = 3
        ret_error = translator.get(translator.internalKeyError)
        ret_success = translator.get(translator.thxForFlagText)

    elif reason == 'optimization':
        ret_value = 4
        ret_success = translator.get(translator.thxForFlagText)

    else:
        ret_value = -1
        ret_error = translator.get(translator.internalKeyError)

    return ret_value, ret_success, ret_info, ret_error
