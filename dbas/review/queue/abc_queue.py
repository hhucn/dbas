# Source interface for the review queues

from abc import ABCMeta, abstractmethod
from typing import Union

from requests import Session

from dbas.database.discussion_model import User, ReviewDelete, ReviewEdit, ReviewMerge, ReviewOptimization, \
    ReviewSplit, ReviewDuplicate
from dbas.strings.translator import Translator


class QueueABC(metaclass=ABCMeta):
    @abstractmethod
    def get_queue_information(self, db_user: User, session: Session, application_url: str, queue_name: str, translator: Translator):
        """

        :param db_user:
        :param session:
        :param application_url:
        :param queue_name:
        :param translator:
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
    def cancel_ballot(self, db_user: User):
        """

        :return:
        """
        pass

    @abstractmethod
    def revoke_ballot(self, db_user: User):
        """

        :return:
        """
        pass
