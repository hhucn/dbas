from nose.tools import assert_in
from pyramid.interfaces import IRequest

import dbas.validators.discussion as discussion
from dbas.lib import Relations, Attitudes
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

    def test_valid_disabled_issue(self):
        request = construct_dummy_request()
        request.session = {'issue': self.issue_disabled.uid}
        response = discussion.valid_issue_by_id(request)
        self.assertFalse(response,
                         'The field-experiment-issue is disabled in the development-seed and can\'t be queried')
        self.assertIsInstance(response, bool)

    def test_valid_any_issue_by_id(self):
        request = construct_dummy_request()
        response = discussion.valid_any_issue_by_id(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'issue': self.issue_disabled.uid})
        response = discussion.valid_any_issue_by_id(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_issue_not_readonly(self):
        request = construct_dummy_request()
        request.session = {'issue': self.issue_cat_or_dog.uid}
        response = discussion.valid_issue_not_readonly(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request()
        request.session = {'issue': self.issue_read_only.uid}
        response = discussion.valid_issue_not_readonly(request)
        self.assertFalse(response)
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
        response = discussion.valid_statement(location='json_body')(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'statement_id': 1})
        response = discussion.valid_statement(location='json_body')(request)
        self.assertFalse(response, 'uid 1 is disabled and should not be returned')
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'statement_id': 'a'})
        response = discussion.valid_statement(location='json_body')(request)
        self.assertFalse(response, 'uid a is not parsable')
        self.assertIsInstance(response, bool)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'statement_id': 'a'})
        response = discussion.valid_statement(location='path')(request)
        self.assertFalse(response, 'uid a is not parsable')
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'statement_id': 2})
        response = discussion.valid_statement(location='json_body')(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'statement_id': 2})
        response = discussion.valid_statement(location='path')(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_argument_with_missing_issue_should_fail(self):
        request = construct_dummy_request()
        response = discussion.valid_argument(location='json_body', depends_on={discussion.valid_issue_by_slug})(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_valid_argument(self):
        request = construct_dummy_request()
        response = discussion.valid_argument(location='json_body')(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'argument_id': 1})
        response = discussion.valid_argument(location='json_body')(request)
        self.assertFalse(response, 'uid 1 should be disabled')
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'argument_id': 'a'})
        response = discussion.valid_argument(location='json_body')(request)
        self.assertFalse(response, 'uid a is not parsable')
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'argument_id': 'a'})
        response = discussion.valid_argument(location='json_body')(request)
        self.assertFalse(response, 'uid a is not parsable')
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'argument_id': 2})
        response = discussion.valid_argument(location='json_body')(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'argument_id': 2})
        response = discussion.valid_argument(location='path')(request)
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

    def test_valid_statement_uid(self):
        request = construct_dummy_request()
        response = discussion.valid_statement_uid(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'uid': 200})
        response = discussion.valid_statement_uid(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'uid': "79a"})
        response = discussion.valid_statement_uid(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'uid': "79"})
        response = discussion.valid_statement_uid(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'uid': 79})
        response = discussion.valid_statement_uid(request)
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

        request = construct_dummy_request({'premisegroups': [['random text', 'more text here'], [42]]})
        response = discussion.valid_premisegroups(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request({'premisegroups': [['random text', 'more text here'], ['not so short here']]})
        response = discussion.valid_premisegroups(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

    def test_valid_list_of_premisegroups_in_path(self):
        request = construct_dummy_request()
        response = discussion.valid_list_of_premisegroups_in_path(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'pgroup_ids': 'a', 'slug': self.issue_cat_or_dog.slug})
        response = discussion.valid_list_of_premisegroups_in_path(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'pgroup_ids': ['a'], 'slug': self.issue_cat_or_dog.slug})
        response = discussion.valid_list_of_premisegroups_in_path(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'pgroup_ids': [], 'slug': self.issue_cat_or_dog.slug})
        response = discussion.valid_list_of_premisegroups_in_path(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'pgroup_ids': [2], 'slug': self.issue_cat_or_dog.slug})
        response = discussion.valid_list_of_premisegroups_in_path(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'pgroup_ids': [2, 4], 'slug': self.issue_cat_or_dog.slug})
        response = discussion.valid_list_of_premisegroups_in_path(request)
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

    def test_valid_attitude(self):
        request = construct_dummy_request(matchdict={})
        response = discussion.valid_attitude(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'foo': 'bar'})
        response = discussion.valid_attitude(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'attitude': 'bar'})
        response = discussion.valid_attitude(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        attitudes = [attitude.value for attitude in Attitudes if attitude is not Attitudes.DONT_KNOW]
        for attitude in attitudes:
            request = construct_dummy_request(matchdict={'attitude': attitude})
            response = discussion.valid_attitude(request)
            self.assertTrue(response)
            self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'attitude': Attitudes.DONT_KNOW.value})
        response = discussion.valid_attitude(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_valid_relation(self):
        request = construct_dummy_request()
        response = discussion.valid_relation(request)
        self.assertFalse(response, 'Relation is missing')
        self.assertIsInstance(response, bool)

        request = construct_dummy_request(matchdict={'relation': 'foo'})
        response = discussion.valid_relation(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

        relations = [relation.value for relation in Relations if relation != Relations.SUPPORT]
        for relation in relations:
            request = construct_dummy_request(matchdict={'relation': relation})
            response = discussion.valid_relation(request)
            self.assertTrue(response)
            self.assertIsInstance(response, bool)


class TestValidIssueBySlug(TestCaseWithConfig):
    def test_slug_must_be_valid(self):
        request = construct_dummy_request(matchdict={
            'slug': ''
        })
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response, 'Slug is missing')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

        request = construct_dummy_request(matchdict={
            'slug': 1
        })
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response, 'Slug should be a string')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

        request = construct_dummy_request(matchdict={
            'slug': None
        })
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response, 'Slug should be a string')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

    def test_valid_slug_is_true(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug
        })
        response = discussion.valid_issue_by_slug(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('issue', request.validated)

    def test_disabled_slug_is_false(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_disabled.slug
        })
        response = discussion.valid_issue_by_slug(request)
        self.assertFalse(response,
                         'The field-experiment-issue is disabled in the development-seed and can\'t be queried')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)


class TestValidPosition(TestCaseWithConfig):
    def test_missing_slug(self):
        request = construct_dummy_request(matchdict={
            'slug': ''
        })
        response = discussion.valid_position(request)
        self.assertFalse(response, 'Slug is missing')
        self.assertIsInstance(response, bool)
        self.assertNotIn('issue', request.validated)

    def test_missing_position(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': None
        })
        response = discussion.valid_position(request)
        self.assertFalse(response, 'position_id is missing')
        self.assertIsInstance(response, bool)
        self.assertIn('issue', request.validated)
        self.assertNotIn('position', request.validated)

    def test_provided_statement_which_is_no_position(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': self.statement_cat_or_dog.uid
        })
        response = discussion.valid_position(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
        self.assertIn('issue', request.validated)
        self.assertNotIn('position', request.validated)

    def test_position_does_not_belong_to_issue(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': self.position_town.uid
        })
        response = discussion.valid_position(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
        self.assertIn('issue', request.validated)
        self.assertNotIn('position', request.validated)

    def test_position_and_issue_are_correct_should_return_true(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'position_id': self.position_cat_or_dog.uid
        })
        response = discussion.valid_position(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('issue', request.validated)
        self.assertIn('position', request.validated)


class TestValidReasonAndPositionNotEqual(TestCaseWithConfig):
    def test_same_content_should_return_false(self):
        request: IRequest = construct_dummy_request(json_body={
            'position': 'same-position-and-reason',
            'reason': 'same-position-and-reason'
        })
        self.assertFalse(discussion.valid_reason_and_position_not_equal(request))

    def test_different_position_and_reason_is_valid(self):
        request: IRequest = construct_dummy_request(
            matchdict={
                'slug': self.issue_cat_or_dog.slug
            },
            json_body={
                'position': 'some position',
                'reason': 'some valid reason for it'
            })
        self.assertTrue(discussion.valid_reason_and_position_not_equal(request))


class TestValidReactionArguments(TestCaseWithConfig):
    def test_valid_request_should_pass(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 4,
            'relation': Relations.REBUT.value,
            'arg_id_sys': 5
        })
        response = discussion.valid_reaction_arguments(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('arg_user', request.validated)
        self.assertIn('arg_sys', request.validated)

    def test_invalid_arg_id_user_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': -1,
            'relation': Relations.REBUT.value,
            'arg_id_sys': 5
        })
        response = discussion.valid_reaction_arguments(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_missing_issue_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': '',
            'arg_id_user': 4,
            'relation': Relations.REBUT.value,
            'arg_id_sys': 5
        })
        response = discussion.valid_reaction_arguments(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_invalid_arg_id_sys_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 4,
            'relation': Relations.REBUT.value,
            'arg_id_sys': -1
        })
        response = discussion.valid_reaction_arguments(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)


class TestValidSupportReaction(TestCaseWithConfig):
    def test_valid_request_should_pass(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 2,
            'arg_id_sys': 11
        })
        response = discussion.valid_support(request)
        self.assertTrue(response)
        self.assertIsInstance(response, bool)
        self.assertIn('arg_user', request.validated)
        self.assertIn('arg_sys', request.validated)

    def test_invalid_arg_id_user_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': -2,
            'arg_id_sys': 11
        })
        response = discussion.valid_support(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_missing_issue_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': '',
            'arg_id_user': 2,
            'arg_id_sys': 11
        })
        response = discussion.valid_support(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_invalid_arg_id_sys_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 2,
            'arg_id_sys': -11
        })
        response = discussion.valid_support(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)

    def test_invalid_relation_should_fail(self):
        request = construct_dummy_request(matchdict={
            'slug': self.issue_cat_or_dog.slug,
            'arg_id_user': 2,
            'arg_id_sys': 3
        })
        response = discussion.valid_support(request)
        self.assertFalse(response)
        self.assertIsInstance(response, bool)
