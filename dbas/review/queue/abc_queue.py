# Source interface for the review queues

from abc import ABCMeta, abstractmethod
from typing import Union

from requests import Session

from dbas.database.discussion_model import User, ReviewDelete, ReviewEdit, ReviewMerge, ReviewOptimization, \
    ReviewSplit, ReviewDuplicate
from dbas.strings.translator import Translator


def subclass_by_name(key: str):
    """
    Evaluates the subclasses of the abstract base class Queue and returns the subclass with key in its name

    :param key:
    :return:
    """
    for cls in eval('QueueABC').__subclasses__():
        if key.lower() in cls.__name__.lower():
            return cls


class QueueABC(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self.key = 'key'

    @abstractmethod
    def key(self, key=None):
        pass

    @abstractmethod
    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        """
        Setup the subpage for the any queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return:
        """
        pass

    @abstractmethod
    def add_vote(self, db_user: User, db_review: Union[ReviewDelete, ReviewEdit, ReviewDuplicate, ReviewMerge,
                                                       ReviewOptimization, ReviewSplit], is_okay: bool, main_page: str,
                 translator: Translator, **kwargs):
        """

        :param db_user:
        :param db_review:
        :param is_okay:
        :param main_page:
        :param translator:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def add_review(self, db_user: User):
        """

        :return:
        """
        pass

    @abstractmethod
    def get_review_count(self, review_uid: int):
        """

        :return:
        """
        pass

    @abstractmethod
    def cancel_ballot(self, db_user: User, db_review: Union[ReviewDelete, ReviewEdit, ReviewDuplicate, ReviewMerge, ReviewOptimization, ReviewSplit]):
        """

        :return:
        """
        pass

    @abstractmethod
    def revoke_ballot(self, db_user: User, db_review: Union[ReviewDelete, ReviewEdit, ReviewDuplicate, ReviewMerge, ReviewOptimization, ReviewSplit]):
        """

        :return:
        """
        pass
