from nose.tools import assert_in

import dbas.validators.discussion as discussion
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request


class TestDiscussionValidators(TestCaseWithConfig):
    def test_valid_issue_by_id(self):
        request = construct_dummy_request()
        response = discussion.valid_issue_by_id(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'issue': self.issue_cat_or_dog.uid})
        response = discussion.valid_issue_by_id(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request()
        request.matchdict = {'issue': self.issue_cat_or_dog.uid}
        response = discussion.valid_issue_by_id(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request()
        request.params = {'issue': self.issue_cat_or_dog.uid}
        response = discussion.valid_issue_by_id(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request()
        request.session = {'issue': self.issue_cat_or_dog.uid}
        response = discussion.valid_issue_by_id(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_issue_by_id_disabled_issue(self):
        request = construct_dummy_request()
        request.session = {'issue': self.issue_disabled.uid}
        response = discussion.valid_issue_by_id(request)
        self.assertFalse(response,
                         'The field-experiment-issue is disabled in the development-seed and can\'t be queried')
        self.assertIsInstance(response, bool)

    def test_valid_new_issue(self):
        request = construct_dummy_request()
        response = discussion.valid_new_issue(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'title': self.issue_cat_or_dog.title,
                                           'info': 'some info',
                                           'long_info': 'some longer info'})
        response = discussion.valid_new_issue(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'title': 'some title',
                                           'info': self.issue_cat_or_dog.info,
                                           'long_info': 'some longer info'})
        response = discussion.valid_new_issue(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'title': 'some title',
                                           'info': 'some info',
                                           'long_info': self.issue_cat_or_dog.long_info})
        response = discussion.valid_new_issue(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'title': 'some title',
                                           'info': 'some info',
                                           'long_info': 'some longer info'})
        response = discussion.valid_new_issue(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_issue_not_readonly(self):
        self.issue_cat_or_dog.set_read_only(True)
        request = construct_dummy_request({'issue': self.issue_cat_or_dog.uid})
        response = discussion.valid_issue_not_readonly(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
        self.issue_cat_or_dog.set_read_only(False)

        request = construct_dummy_request({'issue': self.issue_cat_or_dog.uid})
        response = discussion.valid_issue_not_readonly(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_conclusion(self):
        request = construct_dummy_request()
        response = discussion.valid_conclusion(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'conclusion_id': '2',
                                           'issue': 2})
        response = discussion.valid_conclusion(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'conclusion_id': 2,
                                           'issue': 1})
        response = discussion.valid_conclusion(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'conclusion_id': 2,
                                           'issue': 2})
        response = discussion.valid_conclusion(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_statement(self):
        request = construct_dummy_request()
        response = discussion.valid_statement(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        db_statement = DBDiscussionSession.query(Statement).get(1)
        db_statement.set_disable(True)
        request = construct_dummy_request({'uid': 1})
        response = discussion.valid_statement(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
        db_statement.set_disable(False)

        request = construct_dummy_request({'uid': 1})
        response = discussion.valid_statement(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_argument(self):
        request = construct_dummy_request()
        response = discussion.valid_argument(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        db_argument = DBDiscussionSession.query(Argument).get(1)
        db_argument.set_disable(True)
        request = construct_dummy_request({'uid': 1})
        response = discussion.valid_argument(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
        db_argument.set_disable(False)

        request = construct_dummy_request({'uid': 1})
        response = discussion.valid_argument(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_text_length_of(self):
        request = construct_dummy_request()
        inner = discussion.valid_text_length_of('statement')
        response = inner(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'statement': 'shrt'})
        inner = discussion.valid_text_length_of('statement')
        response = inner(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'statement': 'loooooooong'})
        inner = discussion.valid_text_length_of('statement')
        response = inner(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        assert_in('statement', request.validated)

        request = construct_dummy_request({'blorgh': 'more loooooooong'})
        inner = discussion.valid_text_length_of('blorgh')
        response = inner(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        assert_in('blorgh', request.validated)

    def test_valid_premisegroup(self):
        request = construct_dummy_request()
        response = discussion.valid_premisegroup(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        for uid in ['a', 0, 1000]:
            request = construct_dummy_request({'uid': uid})
            response = discussion.valid_premisegroup(request)
            self.assertFalse(response)
            self.assertIsInstance(response, bool)

        request = construct_dummy_request({'uid': 2})
        response = discussion.valid_premisegroup(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_premisegroups(self):
        request = construct_dummy_request()
        response = discussion.valid_premisegroups(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'premisegroups': []})
        response = discussion.valid_premisegroups(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'premisegroups': [{}]})
        response = discussion.valid_premisegroups(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'premisegroups': [['random text', 'more text here'], ['shrt']]})
        response = discussion.valid_premisegroups(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'premisegroups': [['random text', 'more text here'], ['not so short here']]})
        response = discussion.valid_premisegroups(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_statement_or_argument(self):
        request = construct_dummy_request()
        response = discussion.valid_statement_or_argument(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'is_argument': True})
        response = discussion.valid_statement_or_argument(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'is_argument': True,
                                           'uid': 1000})
        response = discussion.valid_statement_or_argument(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'is_argument': True,
                                           'uid': 2})
        response = discussion.valid_statement_or_argument(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_text_values(self):
        request = construct_dummy_request()
        response = discussion.valid_text_values(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'text_values': 'just a string'})
        response = discussion.valid_text_values(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'text_values': ['sm', 'all', 'str']})
        response = discussion.valid_text_values(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'text_values': ['long string 1', 'another one']})
        response = discussion.valid_text_values(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)


class TestValidIssueBySlug(TestCaseWithConfig):
    def test_slug_must_be_valid(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = ''
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response, 'Slug is missing')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

        request = construct_dummy_request()
        request.matchdict['slug'] = 1
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response, 'Slug should be a string')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

        request = construct_dummy_request()
        request.matchdict['slug'] = None
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response, 'Slug should be a string')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

    def test_valid_slug_is_true(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = self.issue_cat_or_dog.slug
        response = discussion.valid_issue_by_slug(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('issue', request.validated)

    def test_disabled_slug_is_false(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = self.issue_disabled.slug
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response,
                         'The field-experiment-issue is disabled in the development-seed and can\'t be queried')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)


class TestValidPosition(TestCaseWithConfig):
    def test_missing_slug(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = ''
        response = discussion.valid_position(request)
        self.assertFalse(response, 'Slug is missing')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

    def test_missing_position(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = self.issue_cat_or_dog.slug
        request.matchdict['position_id'] = None
        response = discussion.valid_position(request)
        self.assertFalse(response, 'position_id is missing')
        self.assertIsInstance(response, bool)

    def test_provided_statement_which_is_no_position(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = self.issue_cat_or_dog.slug
        request.matchdict['position_id'] = self.statement_cat_or_dog.uid
        response = discussion.valid_position(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_position_does_not_belong_to_issue(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = self.issue_cat_or_dog.slug
        request.matchdict['position_id'] = self.position_town.uid
        response = discussion.valid_position(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_position_and_issue_are_correct_should_return_true(self):
        request = construct_dummy_request()
        request.matchdict['slug'] = self.issue_cat_or_dog.slug
        request.matchdict['position_id'] = self.position_cat_or_dog.uid
        response = discussion.valid_position(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
