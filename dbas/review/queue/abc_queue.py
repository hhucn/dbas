# Source interface for the review queues

from abc import ABCMeta, abstractmethod
from typing import Tuple, Optional

from requests import Session

from dbas.database.discussion_model import User, AbstractReviewCase
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
    def add_vote(self, db_user: User, db_review: AbstractReviewCase, is_okay: bool, main_page: str,
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

        :param db_user:
        :return:
        """
        pass

    @abstractmethod
    def get_review_count(self, review_uid: int) -> Tuple[int, int]:
        """
        Returns total pro and con count for the given review.uid

        :param review_uid: Review.uid
        :return:
        """
        pass

    @abstractmethod
    def cancel_ballot(self, db_user: User, db_review: AbstractReviewCase):
        """

        :param db_user:
        :param db_review:
        :return:
        """
        pass

    @abstractmethod
    def revoke_ballot(self, db_user: User, db_review: AbstractReviewCase):
        """

        :param db_user:
        :param db_review:
        :return:
        """
        pass

    @abstractmethod
    def element_in_queue(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def get_history_table_row(self, db_review: AbstractReviewCase, entry, **kwargs) -> Optional[dict]:
        """

        :param db_review:
        :param entry:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def get_text_of_element(self, db_review: AbstractReviewCase) -> str:
        """

        :param db_review:
        :return:
        """
        pass

    @abstractmethod
    def get_all_votes_for(self, db_review: AbstractReviewCase,
                          application_url: str) -> Tuple[list, list]:
        """

        :param db_review:
        :param application_url:
        :return:
        """
        pass
