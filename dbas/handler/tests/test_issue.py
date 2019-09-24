import dbas.handler.issue as ih
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, User
from dbas.strings.translator import Translator
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig


class TestIssueDictByIssue(TestCaseWithConfig):
    def test_get_issue_dict_for(self):
        lang = 'en'
        issue_cat: Issue = DBDiscussionSession.query(Issue).get(2)
        response = ih.get_issue_dict_for(issue_cat,
                                         issue_cat.uid, lang)
        self.assertTrue(len(response) > 0)
        self.assertTrue(len(response['error']) == 0)


class IssueHandlerTests(TestCaseWithConfig):
    def test_prepare_json_of_issue(self):
        response = ih.prepare_json_of_issue(self.issue_town, self.user_anonymous)
        self.assertTrue(len(response) > 0)

    def test_get_number_of_arguments(self):
        response = ih.get_number_of_arguments(0)
        self.assertTrue(response == 0)
        response = ih.get_number_of_arguments(1)
        self.assertTrue(response > 0)

    def test_get_number_of_statements(self):
        response = ih.get_number_of_statements(0)
        self.assertTrue(response == 0)
        response = ih.get_number_of_statements(1)
        self.assertTrue(response > 0)

    def test_get_number_of_active_participation_users(self):
        response = ih.get_number_of_authors(8)
        self.assertTrue(response == 0)
        response = ih.get_number_of_authors(2)
        self.assertTrue(response > 0)
        response = ih.get_number_of_authors(4)
        self.assertTrue(response > 0)

    def test_get_id_of_slug(self):
        queried_issue = ih.get_id_of_slug(self.issue_cat_or_dog.slug)
        self.assertEqual(queried_issue.uid, self.issue_cat_or_dog.uid)

    def test_get_issue_id(self):
        request = construct_dummy_request(matchdict={'issue': 1})
        issue1 = ih.get_issue_id(request)
        self.assertEqual(issue1, 1)

        request = construct_dummy_request(params={'issue': 2})
        issue2 = ih.get_issue_id(request)
        self.assertEqual(issue2, 2)

        request = construct_dummy_request(session={'issue': 3})
        issue3 = ih.get_issue_id(request)
        self.assertEqual(issue3, 3)

        request = construct_dummy_request(json_body={'issue': 4})
        issue4 = ih.get_issue_id(request)
        self.assertEqual(issue4, 4)

    def test_get_title_for_slug(self):
        queried_title = ih.get_title_for_slug(self.issue_cat_or_dog.slug)
        self.assertEqual(queried_title, self.issue_cat_or_dog.title)

    def test_get_issues_overview(self):
        response = ih.get_issues_overview_for(self.user_tobi, 'http://test.url')
        self.assertIn('user', response)
        self.assertIn('other', response)
        self.assertTrue(len(response['user']) > 0)
        self.assertTrue(len(response['other']) == 0)

        response = ih.get_issues_overview_for(self.user_christian, 'http://test.url')
        self.assertIn('user', response)
        self.assertIn('other', response)
        self.assertTrue(len(response['user']) == 0)
        self.assertTrue(len(response['other']) > 0)

    def test_get_issues_overview_on_start(self):
        response = ih.get_issues_overview_on_start(self.user_tobi)
        self.assertIn('issues', response)
        self.assertIn('readable', response['issues'])
        self.assertIn('writable', response['issues'])
        self.assertIn('data', response)

    def test_set_discussions_properties(self):
        db_walter = DBDiscussionSession.query(User).filter_by(nickname='Walter').one_or_none()
        issue_slug = 'cat-or-dog'
        db_issue = DBDiscussionSession.query(Issue).filter_by(slug=issue_slug).one()
        translator = Translator('en')

        enable = True
        response = ih.set_discussions_properties(db_walter, db_issue, enable, 'somekeywhichdoesnotexist', translator)
        self.assertTrue(len(response['error']) > 0)

        db_christian = DBDiscussionSession.query(User).filter_by(nickname='Christian').one_or_none()
        response = ih.set_discussions_properties(db_christian, db_issue, enable, 'somekeywhichdoesnotexist', translator)
        self.assertTrue(len(response['error']) > 0)

        response = ih.set_discussions_properties(db_christian, db_issue, enable, 'somekeywhichdoesnotexist', translator)
        self.assertTrue(len(response['error']) > 0)

        db_tobias = DBDiscussionSession.query(User).filter_by(nickname='Tobias').one_or_none()
        response = ih.set_discussions_properties(db_tobias, db_issue, enable, 'enable', translator)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(DBDiscussionSession.query(Issue).filter_by(slug=issue_slug).one().is_disabled is False)

        enable = False
        response = ih.set_discussions_properties(db_tobias, db_issue, enable, 'enable', translator)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(DBDiscussionSession.query(Issue).filter_by(slug=issue_slug).one().is_disabled is True)

        enable = True
        response = ih.set_discussions_properties(db_tobias, db_issue, enable, 'enable', translator)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(DBDiscussionSession.query(Issue).filter_by(slug=issue_slug).one().is_disabled is False)
