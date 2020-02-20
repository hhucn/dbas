import unittest

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument
# copy/paste from https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/tests.html
from dbas.tests.utils import test_app


class RoutingTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.testapp = test_app()

        for db_arg in DBDiscussionSession.query(Argument).filter(Argument.uid != 1,
                                                                 Argument.is_disabled == True).all():
            db_arg.set_disabled(False)
        transaction.commit()

    def test_page(self):
        self.testapp.get('/', status=200)

    def test_settings(self):
        self.testapp.get('/settings', status=200)

    def test_notification(self):
        self.testapp.get('/notifications', status=200)

    def test_news(self):
        self.testapp.get('/news', status=200)

    def test_imprint(self):
        self.testapp.get('/imprint', status=200)

    def test_faq(self):
        self.testapp.get('/faq', status=200)

    def test_docs(self):
        self.testapp.get('/docs', status=200)

    def test_user(self):
        self.testapp.get('/user', status=404)
        self.testapp.get('/user/0', status=404)
        self.testapp.get('/user/9000', status=404)
        self.testapp.get('/user/2', status=200)

    def test_discussion_start(self):
        self.testapp.get('/discuss', status=200)
        self.testapp.get('/discuss/', status=200)

    def test_discussion_overview(self):
        self.testapp.get('/discuss/mydiscussions', status=404)  # not logged in

    def test_discussion_support(self):
        self.testapp.get('/discuss/cat-or-dog/support/11/12', status=200)

    def test_discussion_reaction(self):
        self.testapp.get('/discuss/cat-or-dog/reaction/12/undercut/13', status=200)
        self.testapp.get('/discuss/cat-or-dog/reaction/12/undercut/-1', status=404)
        self.testapp.get('/discuss/cat-or-dog/reaction/-1/undercut/13', status=404)

    def test_discussion_justify(self):
        self.testapp.get('/discuss/cat-or-dog/justify/2/agree', status=200)
        self.testapp.get('/discuss/cat-or-dog/justify/13/agree/undercut', status=200)

    def test_discussion_attitude(self):
        self.testapp.get('/discuss/cat-or-dog/attitude/1', status=410)
        self.testapp.get('/discuss/cat-or-dog/attitude/2', status=200)

    def test_discussion_choose(self):
        self.testapp.get('/discuss/cat-or-dog/choose/6', status=200)

    def test_discussion_jump(self):
        self.testapp.get('/discuss/cat-or-dog/jump/12', status=200)

    def test_discussion_exit(self):
        self.testapp.get('/discuss/exit', status=200)

    def test_discussion_finish(self):
        self.testapp.get('/discuss/cat-or-dog/finish/10', status=200)

    def test_discussion_init(self):
        self.testapp.get('/discuss', status=200)
        self.testapp.get('/discuss/', status=200)
        self.testapp.get('/discuss/cat-or-dog', status=200)
        self.testapp.get('/discuss/cat-or-dogg', status=404)

    def test_review_index(self):
        self.testapp.get('/review', status=200)

    def test_review_reputation(self):
        self.testapp.get('/review/reputation', status=200)

    def test_review_history(self):
        self.testapp.get('/review/history', status=200)

    def test_review_ongoing(self):
        self.testapp.get('/review/ongoing', status=200)

    def test_review_content(self):
        self.testapp.get('/review/', status=404)
        from dbas.review.queue import review_queues
        for queue in review_queues:
            self.testapp.get('/review/' + queue, status=200)
