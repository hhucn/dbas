import unittest

from cornice import Errors
from nose.tools import assert_false, assert_equal, assert_true, assert_in
from pyramid import testing

import dbas.validators.discussion as discussion
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, Argument


class DiscussionTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def __prepare_dict(self, jbody):
        request = testing.DummyRequest(json_body=jbody)
        setattr(request, 'errors', Errors())
        setattr(request, 'cookies', {'_LOCALE_': 'en'})
        request.validated = {}
        return request

    def test_valid_issue(self):
        request = self.__prepare_dict({})
        response = discussion.valid_issue(request)
        assert_true(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'issue': 1})
        response = discussion.valid_issue(request)
        assert_true(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({})
        request.matchdict = {'issue': 1}
        response = discussion.valid_issue(request)
        assert_true(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({})
        request.params = {'issue': 1}
        response = discussion.valid_issue(request)
        assert_true(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({})
        request.session = {'issue': 1}
        response = discussion.valid_issue(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_new_issue(self):
        request = self.__prepare_dict({})
        response = discussion.valid_new_issue(request)
        assert_false(response)
        assert_equal(bool, type(response))

        db_issue = DBDiscussionSession.query(Issue).get(1)
        request = self.__prepare_dict({'title': db_issue.title,
                                       'info': 'some info',
                                       'long_info': 'some longer info'})
        response = discussion.valid_new_issue(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'title': 'some title',
                                       'info': db_issue.info,
                                       'long_info': 'some longer info'})
        response = discussion.valid_new_issue(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'title': 'some title',
                                       'info': 'some info',
                                       'long_info': db_issue.long_info})
        response = discussion.valid_new_issue(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'title': 'some title',
                                       'info': 'some info',
                                       'long_info': 'some longer info'})
        response = discussion.valid_new_issue(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_issue_not_readonly(self):
        db_issue = DBDiscussionSession.query(Issue).get(1)
        db_issue.set_read_only(True)
        request = self.__prepare_dict({'issue': db_issue.uid})
        response = discussion.valid_issue_not_readonly(request)
        assert_false(response)
        assert_equal(bool, type(response))
        db_issue.set_read_only(False)

        db_issue = DBDiscussionSession.query(Issue).get(1)
        request = self.__prepare_dict({'issue': db_issue.uid})
        response = discussion.valid_issue_not_readonly(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_conclusion(self):
        request = self.__prepare_dict({})
        response = discussion.valid_conclusion(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'conclusion_id': '2',
                                       'issue': 2})
        response = discussion.valid_conclusion(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'conclusion_id': 2,
                                       'issue': 1})
        response = discussion.valid_conclusion(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'conclusion_id': 2,
                                       'issue': 2})
        response = discussion.valid_conclusion(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_statement(self):
        request = self.__prepare_dict({})
        response = discussion.valid_statement(request)
        assert_false(response)
        assert_equal(bool, type(response))

        db_statement = DBDiscussionSession.query(Statement).get(1)
        db_statement.set_disable(True)
        request = self.__prepare_dict({'uid': 1})
        response = discussion.valid_statement(request)
        assert_false(response)
        assert_equal(bool, type(response))
        db_statement.set_disable(False)

        request = self.__prepare_dict({'uid': 1})
        response = discussion.valid_statement(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_argument(self):
        request = self.__prepare_dict({})
        response = discussion.valid_argument(request)
        assert_false(response)
        assert_equal(bool, type(response))

        db_argument = DBDiscussionSession.query(Argument).get(1)
        db_argument.set_disable(True)
        request = self.__prepare_dict({'uid': 1})
        response = discussion.valid_argument(request)
        assert_false(response)
        assert_equal(bool, type(response))
        db_argument.set_disable(False)

        request = self.__prepare_dict({'uid': 1})
        response = discussion.valid_argument(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_text_length_of(self):
        request = self.__prepare_dict({})
        inner = discussion.valid_text_length_of('statement')
        response = inner(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'statement': 'shrt'})
        inner = discussion.valid_text_length_of('statement')
        response = inner(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'statement': 'loooooooong'})
        inner = discussion.valid_text_length_of('statement')
        response = inner(request)
        assert_true(response)
        assert_equal(bool, type(response))
        assert_in('statement', request.validated)

        request = self.__prepare_dict({'blorgh': 'more loooooooong'})
        inner = discussion.valid_text_length_of('blorgh')
        response = inner(request)
        assert_true(response)
        assert_equal(bool, type(response))
        assert_in('blorgh', request.validated)

    def test_valid_premisegroup(self):
        request = self.__prepare_dict({})
        response = discussion.valid_premisegroup(request)
        assert_false(response)
        assert_equal(bool, type(response))

        for uid in ['a', 0, 1000]:
            request = self.__prepare_dict({'uid': uid})
            response = discussion.valid_premisegroup(request)
            assert_false(response)
            assert_equal(bool, type(response))

        request = self.__prepare_dict({'uid': 2})
        response = discussion.valid_premisegroup(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_premisegroups(self):
        request = self.__prepare_dict({})
        response = discussion.valid_premisegroups(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'premisegroups': []})
        response = discussion.valid_premisegroups(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'premisegroups': [{}]})
        response = discussion.valid_premisegroups(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'premisegroups': [['random text', 'more text here'], ['shrt']]})
        response = discussion.valid_premisegroups(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'premisegroups': [['random text', 'more text here'], ['not so short here']]})
        response = discussion.valid_premisegroups(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_statement_or_argument(self):
        request = self.__prepare_dict({})
        response = discussion.valid_statement_or_argument(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'is_argument': True})
        response = discussion.valid_statement_or_argument(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'is_argument': True,
                                       'uid': 1000})
        response = discussion.valid_statement_or_argument(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'is_argument': True,
                                       'uid': 2})
        response = discussion.valid_statement_or_argument(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_text_values(self):
        request = self.__prepare_dict({})
        response = discussion.valid_text_values(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'text_values': 'just a string'})
        response = discussion.valid_text_values(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'text_values': ['sm', 'all', 'str']})
        response = discussion.valid_text_values(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'text_values': ['long string 1', 'another one']})
        response = discussion.valid_text_values(request)
        assert_true(response)
        assert_equal(bool, type(response))

    def test_valid_fuzzy_search_mode(self):
        request = self.__prepare_dict({})
        response = discussion.valid_fuzzy_search_mode(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'type': ''})
        response = discussion.valid_fuzzy_search_mode(request)
        assert_false(response)
        assert_equal(bool, type(response))

        request = self.__prepare_dict({'type': -1})
        response = discussion.valid_fuzzy_search_mode(request)
        assert_false(response)
        assert_equal(bool, type(response))

        for mode in [0, 1, 2, 3, 4, 5, 8, 9]:
            request = self.__prepare_dict({'type': mode})
            response = discussion.valid_fuzzy_search_mode(request)
            assert_true(response)
            assert_equal(bool, type(response))
