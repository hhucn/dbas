from dbas.database.discussion_model import User
from dbas.review.queue.base import Base


class EditQueue(Base):
    def get_queue_information(self):
        pass

    def add_vote(self, db_user: User):
        pass

    def add_review(self, db_user: User):
        pass

    def get_review_count(self):
        pass

    def cancel_vote(self, db_user: User):
        pass

    def revoke_vote(self, db_user: User):
        pass