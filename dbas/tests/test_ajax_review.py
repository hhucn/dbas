import unittest
import json
import transaction

from pyramid import testing
from sqlalchemy import and_
from dbas.database import DBDiscussionSession
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.database.discussion_model import ReviewDelete, ReviewOptimization, RevokedContentHistory, ReviewCanceled, \
    LastReviewerDelete, ReviewEdit, Statement, ReputationHistory, ReviewEditValue, LastReviewerOptimization, \
    LastReviewerEdit, LastReviewerDuplicate, ReviewDuplicate
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

class AjaxReviewTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')

        # test every ajax method, which is not used in other classes

    def tearDown(self):
        testing.tearDown()

    def test_flag_argument_or_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        DBDiscussionSession.query(ReviewDelete).filter_by(statement_uid=2).delete()
        DBDiscussionSession.query(ReviewOptimization).filter_by(statement_uid=2).delete()
        transaction.commit()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={
            'uid': 2,
            'reason': 'offtopic',
            'is_argument': 'false',
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) != 0)
        self.assertTrue(len(response['info']) == 0)

    def test_flag_argument_or_statement_twice(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={
            'uid': 2,
            'reason': 'offtopic',
            'is_argument': 'false',
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['info']) != 0)
        DBDiscussionSession.query(ReviewDelete).filter_by(statement_uid=2).delete()
        DBDiscussionSession.query(ReviewOptimization).filter_by(statement_uid=2).delete()
        transaction.commit()

    def test_flag_argument_or_statement_error_user(self):
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_flag_argument_or_statement_error_reason(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={
            'uid': 2,
            'reason': 'some_fake_reason',
            'is_argument': 'false',
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_flag_argument_or_statement_error_uid(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={
            'uid': 'a',
            'reason': 'offtopic',
            'is_argument': 'false',
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_delete_argument(self):
        db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.statement_uid is not None,
                                                                        ReviewDelete.is_executed == False)).first()
        from dbas.views import review_delete_argument as ajax

        # 1:0
        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_delete': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 1:1
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_delete': 'false',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 2:1
        self.config.testing_securitypolicy(userid='Torben', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_delete': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 3:1
        self.config.testing_securitypolicy(userid='Friedrich', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_delete': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 4:1
        self.config.testing_securitypolicy(userid='Thorsten', permissive=True)
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(params={
            'should_delete': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        db_statement = DBDiscussionSession.query(Statement).get(db_review.statement_uid)
        self.assertTrue(db_statement.is_disabled)
        self.assertEquals(db_reputation1 + 1, db_reputation2)

    def test_review_delete_argument_uid_error(self):
        from dbas.views import review_delete_argument as ajax

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        request = testing.DummyRequest(params={
            'should_delete': 'true',
            'review_uid': 'a'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_delete_argument_author_error(self):
        db_review = DBDiscussionSession.query(ReviewDelete).filter(and_(ReviewDelete.statement_uid is not None,
                                                                        ReviewDelete.is_executed == False)).first()
        from dbas.views import review_delete_argument as ajax

        # 1:0
        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_delete': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

    def test_review_optimization_argument(self):  # TODO check the voting method
        db_review = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.statement_uid is not None,
                                                                              ReviewOptimization.is_executed == False)).first()
        from dbas.views import review_optimization_argument as ajax

        # 0:1
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_optimized': 'false',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 0:2
        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_optimized': 'false',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 0:3
        self.config.testing_securitypolicy(userid='Torben', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).all())
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(params={
            'should_optimized': 'false',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerOptimization).filter_by(review_uid=db_review.uid).all())
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)
        self.assertEqual(db_reputation1, db_reputation2)

    def test_review_optimization_argument_for_edit(self):  # TODO how to accept new corrections
        db_review = DBDiscussionSession.query(ReviewOptimization).filter(and_(ReviewOptimization.statement_uid is not None,
                                                                              ReviewOptimization.is_executed == False)).first()
        from dbas.views import review_optimization_argument as ajax
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).all())
        db_edits1 = len(DBDiscussionSession.query(ReviewEdit).all())
        db_values1 = len(DBDiscussionSession.query(ReviewEditValue).all())
        request = testing.DummyRequest(params={
            'should_optimized': 'true',
            'review_uid': db_review.uid,
            'new_data': json.dumps([{
                'statement': 22,
                'type': 'statement',
                'argument': 0,
                'val': 'The purpose of a pet is to have something to take care of and to cuddle with'
            }])
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).all())
        db_edits2 = len(DBDiscussionSession.query(ReviewEdit).all())
        db_values2 = len(DBDiscussionSession.query(ReviewEditValue).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)
        self.assertNotEqual(db_edits1, db_edits2)
        self.assertNotEqual(db_values1, db_values2)

    def test_review_optimization_argument_author_error(self):
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import review_optimization_argument as ajax
        request = testing.DummyRequest(params={
            'is_edit_okay': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_optimization_argument_uid_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_optimization_argument as ajax
        request = testing.DummyRequest(params={
            'is_edit_okay': 'true',
            'review_uid': 'a'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_edit_argument(self):
        db_review = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()

        from dbas.views import review_edit_argument as ajax

        self.config.testing_securitypolicy(userid='Torben', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'is_edit_okay': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'is_edit_okay': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        self.config.testing_securitypolicy(userid='Hermann', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(params={
            'is_edit_okay': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)
        self.assertNotEqual(db_reputation1, db_reputation2)

        self.config.testing_securitypolicy(userid='Torben', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_optimized': 'false',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertTrue(db_reviews1, db_reviews2)

    def test_review_edit_argument_author_error(self):
        db_review = DBDiscussionSession.query(ReviewEdit).first()
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import review_edit_argument as ajax
        request = testing.DummyRequest(params={
            'should_optimized': 'true',
            'review_uid': db_review.uid,
            'new_data': 'new data for some statement'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_edit_argument_uid_error(self):

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_edit_argument as ajax
        request = testing.DummyRequest(params={
            'should_optimized': 'true',
            'review_uid': 'a',
            'new_data': 'new data for some statement'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_duplicate_statement(self):
        db_review = DBDiscussionSession.query(ReviewDuplicate).filter_by(is_executed=False).first()

        from dbas.views import review_duplicate_statement as ajax

        # 1:1
        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'is_duplicate': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 1:2
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'is_duplicate': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 1:3
        self.config.testing_securitypolicy(userid='Torben', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'is_duplicate': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

        # 1:4
        self.config.testing_securitypolicy(userid='Thorsten', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(params={
            'is_duplicate': 'true',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_reviews1 + 1, db_reviews2)
        self.assertNotEqual(db_reputation1, db_reputation2)

        self.config.testing_securitypolicy(userid='Friedrich', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(params={
            'should_optimized': 'false',
            'review_uid': db_review.uid
        }, matchdict={})
        response = json.loads(ajax(request))
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertTrue(db_reviews1, db_reviews2)

    def test_review_duplicate_statement_author_error(self):
        db_review = DBDiscussionSession.query(ReviewDuplicate).first()
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import review_duplicate_statement as ajax
        request = testing.DummyRequest(params={
            'is_duplicate': 'true',
            'review_uid': db_review.uid,
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_review_duplicate_uid_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_duplicate_statement as ajax
        request = testing.DummyRequest(params={
            'is_duplicate': 'true',
            'review_uid': 'a'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_undo_review(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import undo_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(params={
            'queue': 'deletes',
            'uid': 5
        }, matchdict={})
        response = json.loads(ajax(request))
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) != 0)
        self.assertNotIn('info', response)
        self.assertNotEqual(db_canceled1, db_canceled2)

    def test_undo_review_author_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import undo_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(params={
            'queue': 'deletes',
            'uid': 5
        }, matchdict={})
        response = json.loads(ajax(request))
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)
        self.assertNotIn('success', response)
        self.assertTrue(len(response['info']) != 0)
        self.assertEqual(db_canceled1, db_canceled2)

    def test_cancel_review(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import cancel_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(params={
            'queue': 'deletes',
            'uid': 4
        }, matchdict={})
        response = json.loads(ajax(request))
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) != 0)
        self.assertNotIn('info', response)
        self.assertNotEqual(db_canceled1, db_canceled2)

    def test_cancel_review_author_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import cancel_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(params={
            'queue': 'deletes',
            'uid': 4
        }, matchdict={})
        response = json.loads(ajax(request))
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)
        self.assertNotIn('success', response)
        self.assertTrue(len(response['info']) != 0)
        self.assertEqual(db_canceled1, db_canceled2)

    def test_cancel_review_queue_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import cancel_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(params={
            'queue': 'some_queue',
            'uid': 4
        }, matchdict={})
        response = json.loads(ajax(request))
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)
        self.assertNotIn('success', response)
        self.assertTrue(len(response['info']) != 0)
        self.assertEqual(db_canceled1, db_canceled2)

    def test_review_lock(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={
            'review_uid': db_review.uid,
            'lock': 'true'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) != 0)
        self.assertTrue(len(response['info']) == 0)
        self.assertTrue(response['is_locked'])

    def test_review_lock_twice(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={
            'review_uid': db_review.uid,
            'lock': 'true'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['info']) != 0)
        self.assertTrue(response['is_locked'])

    def test_review_lock_author_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={
            'review_uid': db_review.uid,
            'lock': 'true'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['info']) == 0)

    def test_review_lock_id_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={
            'review_uid': 100,
            'lock': 'true'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['info']) == 0)

    def test_review_unlock(self):
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={
            'review_uid': db_review.uid,
            'lock': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['success']) != 0)
        self.assertTrue(len(response['info']) == 0)
        self.assertFalse(response['is_locked'])

    def test_revoke_content(self):
        self.config.testing_securitypolicy(userid=nick_of_anonymous_user, permissive=True)
        from dbas.views import revoke_some_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(params={
            'uid': 2,
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(response['is_deleted'])
        self.assertNotEqual(db_content1, db_content2)

    def test_revoke_content_uid_error1(self):
        self.config.testing_securitypolicy(userid=nick_of_anonymous_user, permissive=True)
        from dbas.views import revoke_some_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(params={
            'uid': 'a',
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertFalse(response['is_deleted'])
        self.assertEqual(db_content1, db_content2)

    def test_revoke_content_uid_error2(self):
        self.config.testing_securitypolicy(userid=nick_of_anonymous_user, permissive=True)
        from dbas.views import revoke_some_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(params={
            'uid': 150,
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertFalse(response['is_deleted'])
        self.assertEqual(db_content1, db_content2)

    def test_revoke_content_author_error1(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import revoke_some_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(params={
            'uid': 3,
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertFalse(response['is_deleted'])
        self.assertEqual(db_content1, db_content2)

    def test_revoke_content_author_error2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import revoke_some_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(params={
            'uid': 3,
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertFalse(response['is_deleted'])
        self.assertEqual(db_content1, db_content2)

    def test_duplicate_statement_review(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        from dbas.lib import get_text_for_argument_uid, get_all_arguments_by_statement
        from dbas.views import flag_argument_or_statement as ajax
        argument_uid = get_all_arguments_by_statement(5)[0].uid

        db_review1 = len(DBDiscussionSession.query(ReviewDuplicate).all())
        oem_text = get_text_for_argument_uid(argument_uid)
        request = testing.DummyRequest(params={
            'uid': 5,  # 'cats are very independent
            'reason': 'duplicate',
            'extra_uid': 1,  # Cats are fucking stupid and bloody fuzzy critters!,
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        db_review2 = len(DBDiscussionSession.query(ReviewDuplicate).all())
        self.assertIsNotNone(response)
        self.assertEqual(response['error'], '')
        self.assertEqual(response['info'], '')
        self.assertGreater(len(response['success']), 0)
        self.assertLess(db_review1, db_review2)

        db_review = DBDiscussionSession.query(ReviewDuplicate).filter_by(duplicate_statement_uid=5, original_statement_uid=1).first()

        # vote for duplicate
        from dbas.views import review_duplicate_statement as ajax
        for name in ['Marga', 'Emmi', 'Rupert']:
            self.config.testing_securitypolicy(userid=name, permissive=True)
            db_review1 = len(DBDiscussionSession.query(LastReviewerDuplicate).all())
            request = testing.DummyRequest(params={
                'is_duplicate': 'true',
                'review_uid': db_review.uid
            }, matchdict={})
            response = json.loads(ajax(request))
            db_review2 = len(DBDiscussionSession.query(LastReviewerDuplicate).all())
            self.assertIsNotNone(response)
            self.assertEqual(len(response['error']), 0)
            self.assertLess(db_review1, db_review2)

        new_text = get_text_for_argument_uid(argument_uid)
        self.assertNotEqual(oem_text, new_text)
        self.assertTrue('fucking' in new_text)

        # revoke the decision
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import undo_review as ajax
        request = testing.DummyRequest(params={
            'uid': db_review.uid,
            'queue': 'duplicates',
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertGreater(len(response['success']), 0)
        self.assertEqual(len(response['error']), 0)

        new_oem_text = get_text_for_argument_uid(argument_uid)
        self.assertEqual(oem_text, new_oem_text)
        self.assertFalse('fucking' in new_oem_text)
