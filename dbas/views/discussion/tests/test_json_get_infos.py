import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import History, StatementToIssue, User
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig
from dbas.views import get_infos_about_argument, get_arguments_by_statement_id, get_all_posted_statements, \
    get_all_edits_of_user, delete_statistics, delete_user_history, get_user_history, get_public_user_data, \
    get_users_with_opinion, get_shortened_url, get_logfile_for_some_statements, get_all_argument_clicks


class TestGetLogfileForSomeStatements(TestCaseWithConfig):
    def get_logfile_for_statements1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(params={
            'uids': [1, 2, 3],
            'issue': 1
        }, matchdict={})
        response = get_logfile_for_some_statements(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) == 3)
        self.assertTrue(len(response['error']) == 0)

    def get_logfile_for_statements2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(params={
            'uids': [1, 2, 300],
            'issue': 1
        }, matchdict={})
        response = get_logfile_for_some_statements(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) == 2)
        self.assertTrue(len(response['error']) == 0)

    def get_logfile_for_statements_failure(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(params={
            'uid': [1, 2],
            'issue': 1
        }, matchdict={})
        response = get_logfile_for_some_statements(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)


class TestGetShortenedUrl(TestCaseWithConfig):
    def test_get_shortened_url(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'url': 'https://dbas.cs.uni-duesseldorf.de'})
        response = get_shortened_url(request)
        self.assertIsNotNone(response)
        if Translator('en').get(_.serviceNotAvailable) == response['service_text']:
            self.assertEqual(0, len(response['url']))
        else:
            self.assertNotEqual(0, len(response['url']))

    def test_get_shortened_url_failure(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_shortened_url(request)
        self.assertEqual(response.status_code, 400)


class TestGetArgumentsByStatementId(TestCaseWithConfig):
    def test_get_arguments_by_statement_uid(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        issue_uid = DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=3).first().issue_uid
        request = construct_dummy_request(json_body={'issue': issue_uid}, matchdict={'statement_id': 3})
        response = get_arguments_by_statement_id(request)
        self.assertIsNotNone(response)
        self.assertIn('arguments', response)
        for element in response['arguments']:
            self.assertIn('uid', element)
            self.assertIn('text', element)
            self.assertIn('url', element)

    def test_get_arguments_by_statement_uid_failure1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        issue_uid = DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=3).first().issue_uid
        request = construct_dummy_request(json_body={'issue': issue_uid}, matchdict={'statement_id': 1})
        response = get_arguments_by_statement_id(request)
        self.assertEqual(response.status_code, 410)

    def test_get_arguments_by_statement_uid_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        issue_uid = DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=3).first().issue_uid
        request = construct_dummy_request(json_body={'issue': issue_uid + 1}, matchdict={'statement_id': 3})
        response = get_arguments_by_statement_id(request)
        self.assertEqual(response.status_code, 400)

    def test_get_arguments_by_statement_uid_failure3(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        issue_uid = DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=3).first().issue_uid
        request = construct_dummy_request(json_body={'issue': issue_uid}, matchdict={'statement_id': 'a'})
        response = get_arguments_by_statement_id(request)
        self.assertEqual(response.status_code, 400)


class TestGetInfosAboutArgument(TestCaseWithConfig):
    def test_valid_request_should_be_successful(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'argument_id': 7, 'lang': 'en', 'issue': 2})
        response = get_infos_about_argument(request)
        self.assertIn('supporter', response)
        self.assertIn('gravatars', response)
        self.assertIn('public_page', response)
        self.assertIn('vote_count', response)
        self.assertIn('author', response)
        self.assertIn('timestamp', response)
        self.assertIn('text', response)

    def test_get_infos_about_argument_failure1(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'argument_id': -1, 'lang': 'en', 'issue': 2})
        response = get_infos_about_argument(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_get_infos_about_argument_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'not-argument-ids': 1, 'lang': 'en', 'issue': 2})
        response = get_infos_about_argument(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class TestGetUserInformation(TestCaseWithConfig):
    def test_get_user_with_same_opinion(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_users_with_opinion(request)
        self.assertIsNotNone(response)

    def test_get_public_user_data(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        # more tests for get_public_user_data are in test_handler_opinion
        request = construct_dummy_request(json_body={'user_id': 2})
        response = get_public_user_data(request)
        self.assertIsNotNone(response)


class TestHistoryModifcations(TestCaseWithConfig):
    def test_get_user_history(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        user: User = self.user_christian
        DBDiscussionSession.add(
            History(author=user, path='http://localhost:4284/discuss/cat-or-dog'))
        transaction.commit()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_user_history(request)
        self.assertIsNotNone(response)
        self.assertLessEqual(0, len(response))

    def test_get_user_history_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request()
        response = get_user_history(request)
        self.assertEqual(response.status_code, 400)

    def test_delete_user_history(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        user: User = self.user_christian
        DBDiscussionSession.add(
            History(author=user, path='http://localhost:4284/discuss/cat-or-dog'))
        transaction.commit()
        request = construct_dummy_request()
        response = delete_user_history(request)
        transaction.commit()
        self.assertTrue(response)
        db_his = DBDiscussionSession.query(History).filter_by(author_uid=2).count()
        self.assertEqual(db_his, 0)


class TestDeleteStatistics(TestCaseWithConfig):
    def test_delete_statistics(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = delete_statistics(request)
        self.assertTrue(response)

    def test_delete_statistics_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request()
        response = delete_statistics(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class TestGetAllEditsOfUser(TestCaseWithConfig):
    def test_get_all_edits(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_all_edits_of_user(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_edits_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request()
        response = get_all_edits_of_user(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class TestGetAllPostedStatements(TestCaseWithConfig):
    def test_get_all_posted_statements(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_all_posted_statements(request)
        self.assertIsNotNone(response)
        self.assertListEqual(response, [])

    def test_get_all_posted_statements_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request()
        response = get_all_posted_statements(request)
        self.assertEqual(response.status_code, 400)


class TestGetAllArgumentClicks(TestCaseWithConfig):
    def test_get_all_argument_votes(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_all_argument_clicks(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_argument_votes_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request()
        response = get_all_argument_clicks(request)
        self.assertEqual(response.status_code, 400)

    def test_get_all_statement_votes(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request()
        response = get_all_argument_clicks(request)
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    def test_get_all_statement_votes_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request()
        response = get_all_argument_clicks(request)
        self.assertEqual(response.status_code, 400)
