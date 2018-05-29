from abc import ABCMeta, abstractmethod

from dbas.database.discussion_model import User


class Base(metaclass=ABCMeta):
    @abstractmethod
    def get_queue_information(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def add_vote(self, db_user: User):
        """

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
    def get_review_count(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def cancel_vote(self, db_user: User):
        """

        :return:
        """
        pass

    @abstractmethod
    def revoke_vote(self, db_user: User):
        """

        :return:
        """
        pass
