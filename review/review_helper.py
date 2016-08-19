"""
Provides helping function for the review page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User

import dbas.user_management as UserManager

pages = ['edits', 'deletes', 'flags', 'random', 'duplicates', 'freshest']
reputation = {'edits': 100,
              'deletes': 200,
              'flags': 150,
              'random': 50,
              'duplicates': 10,
              'freshest': 75}


def get_review_array(mainpage, issue, translator):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Array
    """
    review_list = list()
    review_list.append(__get_edit_dict(mainpage, issue, translator))
    review_list.append(__get_delete_dict(mainpage, issue, translator))
    review_list.append(__get_flag_dict(mainpage, issue, translator))
    review_list.append(__get_random_dict(mainpage, issue, translator))
    review_list.append(__get_duplicate_dict(mainpage, issue, translator))
    review_list.append(__get_freshest_dict(mainpage, issue, translator))

    return review_list


def get_subpage_for(subpage_name, nickname):
    """

    :param subpage_name:
    :param nickname:
    :return:
    """
    logger('ReviewHelper', 'get_subpage_for', subpage_name)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    if subpage_name in pages and subpage_name not in ['deletes', 'flags']:
        return subpage_name

    return None


def __get_edit_dict(mainpage, issue, translator):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Dict()
    """
    key = 'edits'
    tmp_dict = {'task_name': 'Edits',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-eraser',
                'task_count': 2,
                'is_allowed': True,
                'is_allowed_text': 'Visit the edit queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review edits.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_delete_dict(mainpage, issue, translator):
    """
    Prepares dictionary for the delete section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Dict()
    """
    key = 'deletes'
    tmp_dict = {'task_name': 'Deletes',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-trash-o',
                'task_count': 4,
                'is_allowed': False,
                'is_allowed_text': 'Visit the delete queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review deletes.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_flag_dict(mainpage, issue, translator):
    """
    Prepares dictionary for the flag section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Dict()
    """
    key = 'flags'
    tmp_dict = {'task_name': 'Flags',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-flag',
                'task_count': 8,
                'is_allowed': False,
                'is_allowed_text': 'Visit the review queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review edits.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_random_dict(mainpage, issue, translator):
    """
    Prepares dictionary for the random section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Dict()
    """
    key = 'random'
    tmp_dict = {'task_name': 'Random',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-random',
                'task_count': '-',
                'is_allowed': True,
                'is_allowed_text': 'Visit the random queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review random statements.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_duplicate_dict(mainpage, issue, translator):
    """
    Prepares dictionary for the duplicate section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Dict()
    """
    key = 'duplicates'
    tmp_dict = {'task_name': 'Duplicates',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-files-o',
                'task_count': '-',
                'is_allowed': True,
                'is_allowed_text': 'Visit the duplicate queue for D-BAS.',
                'is_not_allowed_text': 'You need at least ' + str(reputation[key]) + ' reputation to review duplicated statements.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_freshest_dict(mainpage, issue, translator):
    """
    Prepares dictionary for the freshest section.

    :param mainpage: URL
    :param issue: current issue
    :param translator: Translator
    :return: Dict()
    """
    key = 'freshest'
    tmp_dict = {'task_name': 'First Posts',
                'url': mainpage + '/review/' + key + '/' + issue,
                'icon': 'fa fa-level-up',
                'task_count': '3',
                'is_allowed': False,
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
        tmp_dict['img_src'] = UserManager.get_public_profile_picture(db_user, 40)
        tmp_dict['url'] = mainpage + '/user/' + db_user.public_nickname
        tmp_dict['name'] = db_user.public_nickname
        users_array.append(tmp_dict)
    return users_array
