import transaction

from admin.views import main_table, main_admin
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig


class AdminViewTest(TestCaseWithConfig):
    def __update_user(self, nickname):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
        db_user.update_last_login()
        db_user.update_last_action()
        transaction.commit()

    def test_main_admin_no_author(self):
        request = construct_dummy_request()
        response = main_admin(request)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('dashboard', response)

    def test_main_admin(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        self.__update_user('Tobias')
        request = construct_dummy_request()
        response = main_admin(request)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIn('dashboard', response)

    def test_main_table_no_author(self):
        request = construct_dummy_request()
        response = main_table(request)
        self.assertEqual(400, response.status_code)

    def test_main_table_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(matchdict={'table': 'fu'})
        response = main_table(request)
        self.assertEqual(400, response.status_code)

    def test_main_table(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(matchdict={'table': 'User'})
        response = main_table(request)
        self.assertIn('title', response)
        self.assertIn('project', response)
        self.assertIn('extras', response)
        self.assertIsNotNone(response['table'].get('name'))
        self.assertIsNotNone(response['table'].get('has_elements'))
        self.assertIsNotNone(response['table'].get('count'))
        self.assertIsNotNone(response['table'].get('head'))
        self.assertIsNotNone(response['table'].get('row'))
