import unittest
import webtest
import dbas
import os
from dbas.helper.tests import add_settings_to_appconfig

# copy/paste from https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/tests.html

class FunctionalTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        settings = add_settings_to_appconfig()
        file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'development.ini'))
        app = dbas.main({'__file__': file}, **settings)
        self.testapp = webtest.TestApp(app)

    def test_page(self):
        self.testapp.get('/', status=200)

    def test_contact(self):
        self.testapp.get('/contact', status=200)
        self.testapp.get('/contact&bug=true', status=200)
        self.testapp.get('/contact&bug=false', status=404)
        self.testapp.get('/contact&bug=f', status=404)
        self.testapp.get('/contact&gadse', status=404)

    def test_settings(self):
        self.testapp.get('/settings', status=200)

    def test_notification(self):
        self.testapp.get('/notifications', status=200)

    def test_news(self):
        self.testapp.get('/news', status=200)

    def test_imprint(self):
        self.testapp.get('/imprint', status=200)

    def test_publications(self):
        self.testapp.get('/publications', status=200)

    def test_rss(self):
        self.testapp.get('/rss', status=200)

    def test_faq(self):
        self.testapp.get('/faq', status=200)

    def test_docs(self):
        self.testapp.get('/docs', status=200)

    def test_user(self):
        self.testapp.get('/user', status=404)
        self.testapp.get('/user/0', status=404)
        self.testapp.get('/user/1', status=404)
        self.testapp.get('/user/2', status=200)

    def test_discussion_support(self):
        self.testapp.get('/discuss/cat-or-dog/support/11/12', status=200)

    def test_discussion_reaction(self):
        self.testapp.get('/discuss/cat-or-dog/reaction/12/undercut/13', status=200)
        self.testapp.get('/discuss/cat-or-dog/reaction/13/end/0', status=200)

    def test_discussion_justify(self):
        self.testapp.get('/discuss/cat-or-dog/justify/2/t', status=200)
        self.testapp.get('/discuss/cat-or-dog/justify/13/t/undercut', status=200)

    def test_discussion_attitude(self):
        self.testapp.get('/discuss/cat-or-dog/attitude/1', status=404)
        self.testapp.get('/discuss/cat-or-dog/attitude/2', status=200)

    def test_discussion_choose(self):
        self.testapp.get('/discuss/cat-or-dog/choose/t/f/4/6', status=200)

    def test_discussion_jump(self):
        self.testapp.get('/discuss/cat-or-dog/jump/12', status=200)

    def test_discussion_finish(self):
        self.testapp.get('/discuss/finish', status=200)

    def test_discussion_init(self):
        self.testapp.get('/discuss', status=200)
        self.testapp.get('/discuss/', status=200)
        self.testapp.get('/discuss/cat-or-dog', status=200)
        self.testapp.get('/discuss/cat-or-dogg', status=200)

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
        from dbas.review.helper.subpage import pages
        for page in pages:
            self.testapp.get('/review/' + page, status=200)
