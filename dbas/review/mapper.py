from dbas.database import DiscussionBase
from dbas.review.queue import review_queues
from dbas.review.queue.abc_queue import subclass_by_name
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital


def __get_table_by_key(prefix: str, key: str):
    """
    Iterates through all tables of the base and returns the first one which matches with the pattern {prefix}{key}[s?]

    :param prefix:
    :param key:
    :return:
    """
    for c in DiscussionBase._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ in [f'{prefix}{key}', f'{prefix}{key}s']:
            return c


# key value pairs of the queue key and a title string

def get_title_by_key(key: str):
    """

    :param key:
    :return:
    """
    # title_mapping = {key: _.get_key_by_string(_.queue.value + start_with_capital(key)) for key in review_queues}
    return _.get_key_by_string(_.queue.value + start_with_capital(key))


# key value pairs of the queue key and the table object
def get_review_model_by_key(key: str):
    """
    Get the review table by key, because all tables are named by review_{key}

    :param key: suffix of the table
    :return:
    """
    return __get_table_by_key('review_', key)


def get_review_modal_mapping():
    """
    Get the all review tables as mapping key: table

    :return:
    """
    return {key: __get_table_by_key('review_', key) for key in review_queues}


# key value pairs of the queue key and the queue object
def get_queue_by_key(key):
    """
    Returns any queue with given key in its name, derivated from the abc_queue

    :param key: infix of the queue
    :return:
    """
    return subclass_by_name(key)


# key value pairs of the queue key and the last reviewer object
def get_last_reviewer_by_key(key):
    """
    Get the last reviewer  table by key, because all tables are named by last_reviewers_{key}

    :param key: suffix of the table
    :return:
    """
    # reviewer_mapping = {key: __get_table_by_key('last_reviewers_', key) for key in review_queues}
    return __get_table_by_key('last_reviewers_', key)
