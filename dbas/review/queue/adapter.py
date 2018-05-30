from typing import Union

from dbas.database.discussion_model import User, ReviewSplit, ReviewOptimization, ReviewMerge, ReviewEdit, ReviewDelete
from dbas.review.queue.delete import DeleteQueue
from dbas.review.queue.edit import EditQueue
from dbas.review.queue.merge import MergeQueue
from dbas.review.queue.optimization import OptimizationQueue
from dbas.review.queue.split import SplitQueue
from dbas.strings.translator import Translator


class Queue():
    """
    Adapter for the different queue adaptees
    """

    def __init__(self, queue: Union[DeleteQueue, EditQueue, MergeQueue, OptimizationQueue, SplitQueue], db_user: User, main_page: str, translator: Translator):
        """

        :param queue:
        :param db_user:
        :param main_page:
        :param translator:
        """
        self.queue: Union[DeleteQueue, EditQueue, MergeQueue, OptimizationQueue, SplitQueue] = queue
        self.db_user: User = db_user
        self.main_page = main_page
        self.translator = translator

    def get_queue_information(self, _t):
        """

        :return:
        """
        self.queue.get_queue_information()

    def add_vote(self, db_review: Union[ReviewDelete, ReviewEdit, ReviewMerge, ReviewOptimization, ReviewSplit], is_okay: bool):
        """

        :param db_review:
        :param is_okay:
        :return:
        """
        self.queue.add_vote(self.db_user, db_review, is_okay, self.main_page, self.translator)

    def add_review(self):
        """

        :return:
        """
        self.queue.add_review(self.db_user)

    def get_review_count(self, review_uid: int):
        """

        :return:
        """
        return self.queue.get_review_count(review_uid)

    def cancel_ballot(self):
        """

        :return:
        """
        self.queue.cancel_ballot(self.db_user)

    def revoke_ballot(self):
        """

        :return:
        """
        self.queue.revoke_ballot(self.db_user)
