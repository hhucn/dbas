"""
Provides helping function for the review page.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User

import dbas.user_management as UserManager


def get_review_array(mainpage, translator):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param translator: Translator
    :return: Array
    """
    review_dict = []

    review_dict.append(__get_edit_dict(mainpage, translator))
    review_dict.append(__get_delete_dict(mainpage, translator))
    review_dict.append(__get_flag_dict(mainpage, translator))
    review_dict.append(__get_random_dict(mainpage, translator))
    review_dict.append(__get_duplicate_dict(mainpage, translator))

    return review_dict


def __get_edit_dict(mainpage, translator):
    """
    Prepares dictionary for the edit section.

    :param mainpage: URL
    :param translator: Translator
    :return: Dict()
    """
    tmp_dict = {'task_name': 'Edits',
                'url': mainpage + '/review/edits',
                'icon': 'fa fa-eraser',
                'task_count': 2,
                'is_allowed': True,
                'is_allowed_text': 'Visit the edit queue for D-BAS.',
                'is_not_allowed_text': 'You need at least 100 reputation to review edits.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_delete_dict(mainpage, translator):
    """
    Prepares dictionary for the delete section.

    :param mainpage: URL
    :param translator: Translator
    :return: Dict()
    """
    tmp_dict = {'task_name': 'Deletes',
                'url': mainpage + '/review/deletes',
                'icon': 'fa fa-trash-o',
                'task_count': 4,
                'is_allowed': False,
                'is_allowed_text': 'Visit the delete queue for D-BAS.',
                'is_not_allowed_text': 'You need at least 200 reputation to review deletes.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_flag_dict(mainpage, translator):
    """
    Prepares dictionary for the flag section.

    :param mainpage: URL
    :param translator: Translator
    :return: Dict()
    """
    tmp_dict = {'task_name': 'Flags',
                'url': mainpage + '/review/flags',
                'icon': 'fa fa-flag',
                'task_count': 8,
                'is_allowed': False,
                'is_allowed_text': 'Visit the review queue for D-BAS.',
                'is_not_allowed_text': 'You need at least 150 reputation to review edits.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_random_dict(mainpage, translator):
    """
    Prepares dictionary for the random section.

    :param mainpage: URL
    :param translator: Translator
    :return: Dict()
    """
    tmp_dict = {'task_name': 'Random',
                'url': mainpage + '/review/random',
                'icon': 'fa fa-random',
                'task_count': '-',
                'is_allowed': True,
                'is_allowed_text': 'Visit the random queue for D-BAS.',
                'is_not_allowed_text': 'You need at least 50 reputation to review random statements.',
                'last_reviews': __get_users_array(mainpage)
                }
    return tmp_dict


def __get_duplicate_dict(mainpage, translator):
    """
    Prepares dictionary for the duplicate section.

    :param mainpage: URL
    :param translator: Translator
    :return: Dict()
    """
    tmp_dict = {'task_name': 'Duplicates',
                'url': mainpage + '/review/duplicate',
                'icon': 'fa fa-files-o',
                'task_count': '-',
                'is_allowed': True,
                'is_allowed_text': 'Visit the duplicate queue for D-BAS.',
                'is_not_allowed_text': 'You need at least 10 reputation to review duplicated statements.',
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
