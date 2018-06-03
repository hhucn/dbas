from typing import Union

from beaker.session import Session

from dbas.database.discussion_model import User, ReviewSplit, ReviewOptimization, ReviewMerge, ReviewEdit, ReviewDelete, \
    ReviewDuplicate
from dbas.review.queue import review_queues
from dbas.review.queue.delete import DeleteQueue
from dbas.review.queue.duplicate import DuplicateQueue
from dbas.review.queue.edit import EditQueue
from dbas.review.queue.merge import MergeQueue
from dbas.review.queue.optimization import OptimizationQueue
from dbas.review.queue.split import SplitQueue
from dbas.strings.translator import Translator


class QueueAdapter():
    """
    Adapter for the different queue adaptees
    """

    def __init__(self,
                 queue: Union[DeleteQueue, DuplicateQueue, EditQueue, MergeQueue, OptimizationQueue, SplitQueue] = None,
                 db_user: User = None,
                 application_url: str = '',
                 translator: Translator = '',
                 **kwargs):
        """

        :param queue:
        :param db_user:
        :param application_url:
        :param translator:
        """
        self.queue = queue
        self.db_user: User = db_user
        self.application_url = application_url
        self.translator = translator
        self.kwargs = kwargs

    def get_queue_information(self, session: Session, queue_name: str):
        """

        :return:
        """
        button_set = {f'is_{key}': False for key in review_queues}
        button_set[f'is_{queue_name}'] = True
        subpage_dict = self.queue.get_queue_information(self.db_user, session, self.application_url, self.translator)

        ret_dict = {
            'page_name': queue_name,
            'reviewed_element': subpage_dict,
            'session': subpage_dict['session']
        }
        if subpage_dict['text'] is None and subpage_dict['reason'] is None and subpage_dict['stats'] is None:
            return self.__wrap_subpage_dict({}, button_set)

        return self.__wrap_subpage_dict(ret_dict, button_set)

    @staticmethod
    def __wrap_subpage_dict(ret_dict, button_set):
        """
        Set up dict()

        :param ret_dict: dict()
        :param button_set: dict()
        :return: dict()
        """
        session = {}
        if ret_dict and 'session' in ret_dict:
            session = ret_dict['session']
            ret_dict.pop('session')

        return {
            'elements': ret_dict,
            'no_arguments_to_review': len(ret_dict) is 0,
            'button_set': button_set,
            'session': session
        }

    def add_vote(self, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge, ReviewOptimization,
                                        ReviewSplit], is_okay: bool):
        """

        :param db_review:
        :param is_okay:
        :return:
        """
        return self.queue.add_vote(db_user=self.db_user, db_review=db_review, is_okay=is_okay,
                                   application_url=self.application_url,
                                   translator=self.translator, **self.kwargs)

    def add_review(self):
        """

        :return:
        """
        return self.queue.add_review(self.db_user)

    def get_review_count(self, review_uid: int):
        """

        :return:
        """
        return self.queue.get_review_count(review_uid)

    def cancel_ballot(self, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge, ReviewOptimization, ReviewSplit]):
        """

        :return:
        """
        return self.queue.cancel_ballot(self.db_user, db_review)

    def revoke_ballot(self, db_review: Union[ReviewDelete, ReviewDuplicate, ReviewEdit, ReviewMerge, ReviewOptimization, ReviewSplit]):
        """

        :param db_review:
        :return:
        """
        return self.queue.revoke_ballot(self.db_user, db_review)
