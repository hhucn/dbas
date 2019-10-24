import json
import unittest

import transaction
from pyramid import testing
from pyramid.httpexceptions import HTTPError

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, TextVersion, Argument, Premise, PremiseGroup, \
    ReviewEdit, ReviewEditValue, ReputationHistory, User, MarkedStatement, MarkedArgument, ClickedArgument, \
    ClickedStatement, SeenStatement, SeenArgument, StatementToIssue
from dbas.handler.history import SessionHistory
from dbas.lib import Relations
from dbas.tests.utils import construct_dummy_request
from dbas.views import set_new_premises_for_argument, set_new_start_premise, set_correction_of_some_statements, \
    set_new_issue, set_statements_as_seen, logging

LOG = logging.getLogger(__name__)


class AjaxAddThingsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

    def delete_last_argument_by_conclusion_uid(self, uid):
        db_new_arg = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=uid).order_by(
            Argument.uid.desc()).first()
        # delete content of premisegroup
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_new_arg.premisegroup_uid).all()
        for premise in db_premises:
            tmp_p_uid = premise.statement_uid
            premise.statement_uid = 1
            DBDiscussionSession.query(TextVersion).filter_by(statement_uid=tmp_p_uid).delete()
            DBDiscussionSession.query(MarkedStatement).filter_by(statement_uid=tmp_p_uid).delete()
            DBDiscussionSession.query(SeenStatement).filter_by(statement_uid=tmp_p_uid).delete()
            DBDiscussionSession.query(ClickedStatement).filter_by(statement_uid=tmp_p_uid).delete()
            DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=tmp_p_uid).delete()
            DBDiscussionSession.query(Statement).filter_by(uid=tmp_p_uid).delete()
        # delete premisegroup
        tmp_p_uid = db_new_arg.premisegroup_uid
        db_new_arg.premisegroup_uid = 1
        DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=tmp_p_uid).delete()
        DBDiscussionSession.query(PremiseGroup).filter_by(uid=tmp_p_uid).delete()
        # delete argument
        DBDiscussionSession.query(MarkedArgument).filter_by(argument_uid=db_new_arg.uid).delete()
        DBDiscussionSession.query(SeenArgument).filter_by(argument_uid=db_new_arg.uid).delete()
        DBDiscussionSession.query(ClickedArgument).filter_by(argument_uid=db_new_arg.uid).delete()
        DBDiscussionSession.query(Argument).filter_by(uid=db_new_arg.uid).delete()

    def __set_multiple_start_premises(self, view, history: SessionHistory = None):
        statement_in_issue2_uids = [el.statement_uid for el in
                                    DBDiscussionSession.query(StatementToIssue).filter_by(issue_uid=2).all()]
        db_conclusion = DBDiscussionSession.query(Statement).filter(Statement.is_disabled == False,
                                                                    Statement.uid.in_(statement_in_issue2_uids)).first()
        db_arg = DBDiscussionSession.query(Argument).filter(Argument.conclusion_uid == db_conclusion.uid,
                                                            Argument.is_disabled == False).first()
        db_arg_len1 = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_conclusion.uid).count()
        len_db_reputation1 = DBDiscussionSession.query(ReputationHistory).count()
        request = construct_dummy_request(json_body={
            'premisegroups': [['this is my first premisegroup']],
            'conclusion_id': db_conclusion.uid,
            'issue': db_arg.issue_uid,
            'supportive': True
        }, cookies={'_LOCALE_': 'en', '_HISTORY_': history.get_session_history_as_string()})
        LOG.debug(request.cookies.get('_HISTORY_'))
        response = view(request)
        transaction.commit()
        db_arg_len2 = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=db_conclusion.uid).count()
        len_db_reputation2 = DBDiscussionSession.query(ReputationHistory).count()
        self.assertFalse(response['error'])
        self.assertEquals(db_arg_len1 + 1, db_arg_len2)
        self.assertEquals(len_db_reputation1 + 1, len_db_reputation2)
        self.delete_last_argument_by_conclusion_uid(db_arg.conclusion_uid)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()
        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).delete()
        transaction.commit()

    def test_set_new_start_premise(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        session_history = SessionHistory('foobar')
        self.__set_multiple_start_premises(set_new_start_premise, session_history)

    def test_set_new_start_premise_twice(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        session_history = SessionHistory('foobar')
        self.__set_multiple_start_premises(set_new_start_premise, session_history)

    def test_set_new_start_premise_failure1(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request(json_body={'issue': 2})
        response = set_new_start_premise(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_set_new_start_premise_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'issue': 2})
        response = set_new_start_premise(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_set_new_premises_for_argument(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_arg1 = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=2).count()
        db_pgroups1 = DBDiscussionSession.query(PremiseGroup).count()
        request = construct_dummy_request(json_body={
            'premisegroups': [['some new reason for an argument']],
            'argument_id': 2,
            'attack_type': Relations.SUPPORT.value,
            'issue': 2
        }, cookies={'_LOCALE_': 'en', '_HISTORY_': 'foobar'})
        response = set_new_premises_for_argument(request)
        db_arg2 = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=2).count()
        db_pgroups2 = DBDiscussionSession.query(PremiseGroup).count()
        self.assertIsNotNone(response)
        self.assertNotIsInstance(response, HTTPError, response)
        self.assertEqual(db_arg1 + 1, db_arg2)
        self.assertEqual(db_pgroups1 + 1, db_pgroups2)
        self.delete_last_argument_by_conclusion_uid(2)

    def test_set_new_premises_for_argument_failure(self):
        # author error
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request(json_body={'issue': 2})
        response = set_new_premises_for_argument(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_set_correction_of_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review1 = DBDiscussionSession.query(ReviewEdit).count()
        db_value1 = DBDiscussionSession.query(ReviewEditValue).count()
        elements = [{'text': 'some new text for a correction', 'uid': 19}]
        request = construct_dummy_request(matchdict={'slug': 'cat-or-dog'}, params={}, json_body={
            'elements': elements
        })
        response = set_correction_of_some_statements(request)
        db_review2 = DBDiscussionSession.query(ReviewEdit).count()
        db_value2 = DBDiscussionSession.query(ReviewEditValue).count()
        self.assertIsNotNone(response)
        self.assertFalse(response['error'])
        self.assertEqual(db_review1 + 1, db_review2)
        self.assertEqual(db_value1 + 1, db_value2)
        tmp = DBDiscussionSession.query(ReviewEditValue).order_by(ReviewEditValue.uid.desc()).first()
        DBDiscussionSession.query(ReviewEditValue).filter_by(uid=tmp.uid).delete()
        tmp = DBDiscussionSession.query(ReviewEdit).order_by(ReviewEdit.uid.desc()).first()
        DBDiscussionSession.query(ReviewEdit).filter_by(uid=tmp.uid).delete()
        transaction.commit()

    def test_set_correction_of_statement_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        request = construct_dummy_request(matchdict={'slug': 'cat-or-dog'}, params={}, json_body={
            'elements': [{}]
        }, )
        response = set_correction_of_some_statements(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
        self.assertGreater(len(json.loads(response.body.decode('utf-8'))['errors']), 0)

    def __get_dummy_request_for_new_issue(self):
        return construct_dummy_request(json_body={
            'info': 'Some new info',
            'title': 'Some new title',
            'long_info': 'Some new long info',
            'lang': 'en',
            'is_public': False,
            'is_read_only': False
        }, matchdict={'slug': 'cat-or-dog'})

    def test_set_new_issue(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = self.__get_dummy_request_for_new_issue()
        response = set_new_issue(request)

        self.assertIsNotNone(response)
        self.assertEqual(DBDiscussionSession.query(Issue).filter_by(title=request.json_body['title']).count(), 1)
        # Calling .delete() on the queryset instead of on the session does not cascade. Beware!
        issue = DBDiscussionSession.query(Issue).filter_by(title=request.json_body['title']).first()
        DBDiscussionSession.delete(issue)
        transaction.commit()

    def test_set_new_issue_failure1(self):
        # no author
        request = self.__get_dummy_request_for_new_issue()
        response = set_new_issue(request)

        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_set_new_issue_failure2(self):
        # duplicated title
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = self.__get_dummy_request_for_new_issue()
        db_issue = DBDiscussionSession.query(Issue).get(1)
        request.json_body['title'] = db_issue.title
        response = set_new_issue(request)

        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_set_new_issue_failure3(self):
        # duplicated info
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = self.__get_dummy_request_for_new_issue()
        db_issue = DBDiscussionSession.query(Issue).get(1)
        request.json_body['info'] = db_issue.info
        response = set_new_issue(request)

        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_set_new_issue_failure4(self):
        # wrong language
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        request = self.__get_dummy_request_for_new_issue()
        request.json_body['lang'] = 'sw'
        response = set_new_issue(request)

        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_set_seen_statements(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={'uids': [40, 41]})
        response = set_statements_as_seen(request)

        self.assertIsNotNone(response)

    def test_set_seen_statements_failure1(self):
        request = construct_dummy_request(json_body={})
        response = set_statements_as_seen(request)

        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)
