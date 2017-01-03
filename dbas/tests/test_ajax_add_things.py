import unittest
import json
import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Statement, TextVersion, Argument, Premise, PremiseGroup,\
    ReviewEdit, ReviewEditValue, ReputationHistory, User
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class AjaxAddThingsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        # todo checking reputation

    def tearDown(self):
        testing.tearDown()

    def delete_last_argument_by_conclusion_uid(self, id):
        db_new_arg = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=id).order_by(Argument.uid.desc()).first()
        # delete content of premisegroup
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_new_arg.premisesgroup_uid).all()
        for premise in db_premises:
            tmp = premise.statement_uid
            premise.statement_uid = 1
            DBDiscussionSession.query(Statement).filter_by(uid=tmp).first().textversion_uid = 1
            DBDiscussionSession.query(TextVersion).filter_by(statement_uid=tmp).delete()
            DBDiscussionSession.query(Statement).filter_by(uid=tmp).delete()
        # delete premisegroup
        tmp = db_new_arg.premisesgroup_uid
        db_new_arg.premisesgroup_uid = 1
        DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=tmp).delete()
        DBDiscussionSession.query(PremiseGroup).filter_by(uid=tmp).delete()
        # delete argument
        DBDiscussionSession.query(Argument).filter_by(uid=db_new_arg.uid).delete()

    def test_set_new_start_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_start_statement as ajax
        request = testing.DummyRequest(params={'statement': 'New statement for an issue'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['url']) != 0)
        self.assertTrue(len(response['statement_uids']) != 0)
        for uid in response['statement_uids']:
            DBDiscussionSession.query(Statement).get(uid).textversion_uid = 1
            DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).delete()
            DBDiscussionSession.query(Statement).filter_by(uid=uid).delete()
        transaction.commit()

    def test_set_new_start_statement_reputation(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import set_new_start_statement as ajax
        request = testing.DummyRequest(params={'statement': 'New statement for an issue'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['url']) != 0)
        self.assertTrue(len(response['statement_uids']) != 0)
        for uid in response['statement_uids']:
            DBDiscussionSession.query(Statement).get(uid).textversion_uid = 1
            DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).delete()
            DBDiscussionSession.query(Statement).filter_by(uid=uid).delete()
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()
        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).delete()
        transaction.commit()

    def test_set_new_start_statement_failure1(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import set_new_start_statement as ajax
        request = testing.DummyRequest(params={'statement': 'New statement for an issue'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_start_statement_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_start_statement as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_start_premise(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import set_new_start_premise as ajax
        db_arg1 = len(DBDiscussionSession.query(Argument).filter_by(conclusion_uid=2).all())
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(params={
            'premisegroups': json.dumps(['this is my first premisegroup']),
            'conclusion_id': 2,
            'issue': 2,
            'supportive': 'true'
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_arg2 = len(DBDiscussionSession.query(Argument).filter_by(conclusion_uid=2).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertEquals(db_arg1 + 1, db_arg2)
        self.assertEquals(len_db_reputation1 + 1, len_db_reputation2)
        self.delete_last_argument_by_conclusion_uid(2)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()
        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).delete()
        transaction.commit()

    def test_set_new_start_premise_twice(self):
        self.config.testing_securitypolicy(userid='Björn', permissive=True)
        from dbas.views import set_new_start_premise as ajax
        db_arg1 = len(DBDiscussionSession.query(Argument).filter_by(conclusion_uid=2).all())
        len_db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(params={
            'premisegroups': json.dumps(['this is my first premisegroup']),
            'conclusion_id': 2,
            'issue': 2,
            'supportive': 'true'
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_arg2 = len(DBDiscussionSession.query(Argument).filter_by(conclusion_uid=2).all())
        len_db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertEquals(db_arg1 + 1, db_arg2)
        self.assertEquals(len_db_reputation1 + 1, len_db_reputation2)
        self.delete_last_argument_by_conclusion_uid(2)
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Björn').first()
        DBDiscussionSession.query(ReputationHistory).filter_by(reputator_uid=db_user.uid).delete()
        transaction.commit()

    def test_set_new_start_premise_failure1(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import set_new_start_premise as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_start_premise_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_start_premise as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_premises_for_argument(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_premises_for_argument as ajax
        db_arg1 = len(DBDiscussionSession.query(Argument).filter_by(uid=2).all())
        db_pgroups1 = len(DBDiscussionSession.query(PremiseGroup).all())
        request = testing.DummyRequest(params={
            'premisegroups': json.dumps(['some new reason for an argument']),
            'arg_uid': 2,
            'attack_type': 'support',
            'issue': 2
        }, matchdict={})
        response = json.loads(ajax(request))
        db_arg2 = len(DBDiscussionSession.query(Argument).filter_by(uid=2).all())
        db_pgroups2 = len(DBDiscussionSession.query(PremiseGroup).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_arg1 + 1, db_arg2)
        self.assertTrue(db_pgroups1 + 1, db_pgroups2)
        self.delete_last_argument_by_conclusion_uid(2)

    def test_set_new_premises_for_argument_failure(self):
        # author error
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import set_new_premises_for_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_correction_of_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_correction_of_statement as ajax
        db_review1 = len(DBDiscussionSession.query(ReviewEdit).all())
        db_value1 = len(DBDiscussionSession.query(ReviewEditValue).all())
        elements = {'text': 'some new text for a correction', 'uid': 2}
        request = testing.DummyRequest(params={
            'elements': json.dumps([elements])
        }, matchdict={})
        response = json.loads(ajax(request))
        db_review2 = len(DBDiscussionSession.query(ReviewEdit).all())
        db_value2 = len(DBDiscussionSession.query(ReviewEditValue).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_review1 + 1, db_review2)
        self.assertTrue(db_value1 + 1, db_value2)
        tmp = DBDiscussionSession.query(ReviewEditValue).order_by(ReviewEditValue.uid.desc()).first()
        DBDiscussionSession.query(ReviewEditValue).filter_by(uid=tmp.uid).delete()
        tmp = DBDiscussionSession.query(ReviewEdit).order_by(ReviewEdit.uid.desc()).first()
        DBDiscussionSession.query(ReviewEdit).filter_by(uid=tmp.uid).delete()
        transaction.commit()

    def test_set_correction_of_statement_failure(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import set_correction_of_statement as ajax
        request = testing.DummyRequest(params={
            'elements': json.dumps([{}])
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_issue(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={
            'info': 'Some new info',
            'title': 'Some new title',
            'lang': 'en'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        DBDiscussionSession.query(Issue).filter_by(title='Some new title').delete()
        transaction.commit()

    def test_set_new_issue_failure1(self):
        # no author
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={
            'info': 'Some new info',
            'title': 'Some new title',
            'lang': 'en'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_issue_failure2(self):
        # duplicated title
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={
            'info': 'Some new info',
            'title': 'Cat or Dog',
            'lang': 'en'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_issue_failure3(self):
        # duplicated info
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={
            'info': 'Your family argues about whether to buy a cat or dog as pet. Now your opinion matters!',
            'title': 'Some new title',
            'lang': 'en'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_issue_failure4(self):
        # wrong language
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={
            'info': 'Some new info',
            'title': 'Some new title',
            'lang': 'sw'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_new_issue_failure5(self):
        # short info
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={
            'info': 'Short',
            'title': 'Some new title',
            'lang': 'en'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_seen_statements(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_seen_statements as ajax
        request = testing.DummyRequest(params={'uids': json.dumps([40, 41])}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)

    def test_set_seen_statements_failure1(self):
        from dbas.views import set_seen_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_set_seen_statements_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_seen_statements as ajax
        request = testing.DummyRequest(params={'uids': json.dumps(['a'])}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
