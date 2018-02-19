import unittest

import transaction
from pyramid import testing

from dbas.database.discussion_model import ReviewMerge, DBDiscussionSession, ReviewSplit, PremiseGroup, \
    LastReviewerMerge, Argument, PremiseGroupSplitted, ReviewSplitValues, LastReviewerSplit, ReviewMergeValues, \
    PremiseGroupMerged, ArgumentsAddedByPremiseGroupSplit, LastReviewerDelete, LastReviewerDuplicate, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReviewCanceled, ReviewDelete, ReviewDuplicate, \
    ReviewEdit, ReviewEditValue, ReviewOptimization, RevokedContentHistory, Statement
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.lib import get_text_for_premisesgroup_uid, get_text_for_argument_uid


class AjaxReviewTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        DBDiscussionSession.add(ReviewOptimization(detector=2, statement=10))
        DBDiscussionSession.flush()
        transaction.commit()
        # test every ajax method, which is not used in other classes

    def tearDown(self):
        DBDiscussionSession.query(ReviewOptimization).filter_by(detector_uid=2, statement_uid=10).delete()
        DBDiscussionSession.flush()
        transaction.commit()
        testing.tearDown()

    def test_flag_argument_or_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        DBDiscussionSession.query(ReviewDelete).filter_by(statement_uid=2).delete()
        DBDiscussionSession.query(ReviewOptimization).filter_by(statement_uid=2).delete()
        transaction.commit()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 2,
            'reason': 'offtopic',
            'is_argument': False,
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) != 0)
        self.assertTrue(len(response['info']) == 0)

    def test_flag_argument_or_statement_twice(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 2,
            'reason': 'offtopic',
            'is_argument': False,
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['info']) != 0)
        DBDiscussionSession.query(ReviewDelete).filter_by(statement_uid=2).delete()
        DBDiscussionSession.query(ReviewOptimization).filter_by(statement_uid=2).delete()
        transaction.commit()

    def test_flag_argument_or_statement_error_user(self):
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(json_body={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_flag_argument_or_statement_error_reason(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 2,
            'reason': 'some_fake_reason',
            'is_argument': False,
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_flag_argument_or_statement_error_uid(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 'a',
            'reason': 'offtopic',
            'is_argument': False,
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def __exec_request_and_check_reviewes(self, db_review, ajax, keyword, bool, nickname, reviewer_type):
        self.config.testing_securitypolicy(userid=nickname, permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(reviewer_type).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(json_body={
            keyword: bool,
            'review_uid': db_review.uid
        })
        response = ajax(request)
        db_reviews2 = len(DBDiscussionSession.query(reviewer_type).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(response)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

    def test_review_delete_argument(self):
        db_review = DBDiscussionSession.query(ReviewDelete).filter(ReviewDelete.statement_uid is not None,
                                                                   ReviewDelete.is_executed == False).first()
        from dbas.views import review_delete_argument as ajax

        # 1:0
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_delete', True, 'Pascal', LastReviewerDelete)

        # 1:1
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_delete', False, 'Kurt', LastReviewerDelete)

        # 2:1
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_delete', True, 'Torben', LastReviewerDelete)

        # 3:1
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_delete', True, 'Friedrich', LastReviewerDelete)

        # 4:1
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_delete', True, 'Thorsten', LastReviewerDelete)
        transaction.commit()
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        db_statement = DBDiscussionSession.query(Statement).get(db_review.statement_uid)
        self.assertTrue(db_statement.is_disabled)
        self.assertEquals(db_reputation1 + 1, db_reputation2)

    def test_review_delete_argument_uid_error(self):
        from dbas.views import review_delete_argument as ajax

        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        request = testing.DummyRequest(json_body={
            'should_delete': True,
            'review_uid': 'a'
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_review_delete_argument_author_error(self):
        db_review = DBDiscussionSession.query(ReviewDelete).filter(ReviewDelete.statement_uid is not None,
                                                                   ReviewDelete.is_executed == False).first()
        from dbas.views import review_delete_argument as ajax

        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_delete', True, 'Pascal', LastReviewerDelete)

    def test_review_optimization_argument(self):  # TODO check the voting method
        db_review = DBDiscussionSession.query(ReviewOptimization).filter(ReviewOptimization.statement_uid is not None,
                                                                         ReviewOptimization.is_executed == False).first()
        from dbas.views import review_optimization_argument as ajax

        # 0:1
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_optimized', False, 'Kurt',
                                               LastReviewerOptimization)

        # 0:2
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_optimized', False, 'Pascal',
                                               LastReviewerOptimization)

        # 0:3
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.__exec_request_and_check_reviewes(db_review, ajax, 'should_optimized', False, 'Torben',
                                               LastReviewerOptimization)
        transaction.commit()
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertEqual(db_reputation1, db_reputation2)

    def test_review_optimization_argument_for_edit(self):  # TODO how to accept new corrections
        db_review = DBDiscussionSession.query(ReviewOptimization).filter(ReviewOptimization.statement_uid is not None,
                                                                         ReviewOptimization.is_executed == False).first()
        from dbas.views import review_optimization_argument as ajax
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).all())
        db_edits1 = len(DBDiscussionSession.query(ReviewEdit).all())
        db_values1 = len(DBDiscussionSession.query(ReviewEditValue).all())
        request = testing.DummyRequest(json_body={
            'should_optimized': True,
            'review_uid': db_review.uid,
            'new_data': [{
                'statement': 22,
                'type': 'statement',
                'argument': 0,
                'val': 'The purpose of a pet is to have something to take care of and to cuddle with'
            }]
        })
        response = ajax(request)
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerEdit).filter_by(review_uid=db_review.uid).all())
        db_edits2 = len(DBDiscussionSession.query(ReviewEdit).all())
        db_values2 = len(DBDiscussionSession.query(ReviewEditValue).all())
        self.assertIsNotNone(response)
        self.assertTrue(response)
        self.assertTrue(db_reviews1 + 1, db_reviews2)
        self.assertNotEqual(db_edits1, db_edits2)
        self.assertNotEqual(db_values1, db_values2)

    def test_review_optimization_argument_author_error(self):
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import review_optimization_argument as ajax
        request = testing.DummyRequest(json_body={
            'is_edit_okay': True,
            'review_uid': db_review.uid
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_review_optimization_argument_uid_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_optimization_argument as ajax
        request = testing.DummyRequest(json_body={
            'is_edit_okay': True,
            'review_uid': 'a'
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_review_edit_argument(self):
        db_review = DBDiscussionSession.query(ReviewEdit).filter_by(is_executed=False).first()

        from dbas.views import review_edit_argument as ajax

        user_ids = ['Torben', 'Pascal']
        for user in user_ids:
            self.config.testing_securitypolicy(userid=user, permissive=True)
            db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
            request = testing.DummyRequest(json_body={
                'is_edit_okay': True,
                'review_uid': db_review.uid
            })
            response = ajax(request)
            transaction.commit()
            db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
            self.assertIsNotNone(response)
            self.assertTrue(response)
            self.assertTrue(db_reviews1 + 1, db_reviews2)

        self.config.testing_securitypolicy(userid='Hermann', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        db_reputation1 = len(DBDiscussionSession.query(ReputationHistory).all())
        request = testing.DummyRequest(json_body={
            'is_edit_okay': True,
            'review_uid': db_review.uid
        })
        response = ajax(request)
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        db_reputation2 = len(DBDiscussionSession.query(ReputationHistory).all())
        self.assertIsNotNone(response)
        self.assertTrue(response)
        self.assertTrue(db_reviews1 + 1, db_reviews2)
        self.assertNotEqual(db_reputation1, db_reputation2)

        self.config.testing_securitypolicy(userid='Torben', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(json_body={
            'should_optimized': False,
            'review_uid': db_review.uid
        })
        response = ajax(request)
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDelete).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)
        self.assertTrue(db_reviews1, db_reviews2)

    def test_review_edit_argument_author_error(self):
        db_review = DBDiscussionSession.query(ReviewEdit).first()
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import review_edit_argument as ajax
        request = testing.DummyRequest(json_body={
            'should_optimized': True,
            'review_uid': db_review.uid,
            'new_data': 'new data for some statement'
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_review_edit_argument_uid_error(self):

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_edit_argument as ajax
        request = testing.DummyRequest(json_body={
            'should_optimized': True,
            'review_uid': 'a',
            'new_data': 'new data for some statement'
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def __exec_request_and_check_duplicates(self, db_review, ajax, bool, nickname):
        self.config.testing_securitypolicy(userid=nickname, permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(json_body={
            'is_duplicate': bool,
            'review_uid': db_review.uid
        })
        response = ajax(request)
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(response)
        self.assertTrue(db_reviews1 + 1, db_reviews2)

    def test_review_duplicate_statement(self):
        db_review = DBDiscussionSession.query(ReviewDuplicate).filter_by(is_executed=False).first()

        from dbas.views import review_duplicate_statement as ajax

        # 1:1
        self.__exec_request_and_check_duplicates(db_review, ajax, True, 'Pascal')

        # 1:2
        self.__exec_request_and_check_duplicates(db_review, ajax, True, 'Kurt')

        # 1:3
        self.__exec_request_and_check_duplicates(db_review, ajax, True, 'Torben')

        # 1:4
        self.__exec_request_and_check_duplicates(db_review, ajax, True, 'Thorsten')

        self.config.testing_securitypolicy(userid='Friedrich', permissive=True)
        db_reviews1 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        request = testing.DummyRequest(json_body={
            'should_optimized': False,
            'review_uid': db_review.uid
        })
        response = ajax(request)
        transaction.commit()
        db_reviews2 = len(DBDiscussionSession.query(LastReviewerDuplicate).filter_by(review_uid=db_review.uid).all())
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)
        self.assertTrue(db_reviews1, db_reviews2)

    def test_review_duplicate_statement_author_error(self):
        db_review = DBDiscussionSession.query(ReviewDuplicate).first()
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import review_duplicate_statement as ajax
        request = testing.DummyRequest(json_body={
            'is_duplicate': True,
            'review_uid': db_review.uid,
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_review_duplicate_uid_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_duplicate_statement as ajax
        request = testing.DummyRequest(json_body={
            'is_duplicate': True,
            'review_uid': 'a'
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_undo_review(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import undo_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(json_body={
            'queue': 'deletes',
            'uid': 5
        })
        self.assertTrue(ajax(request))
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertNotEqual(db_canceled1, db_canceled2)

    def test_undo_review_author_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import undo_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(json_body={
            'queue': 'deletes',
            'uid': 5
        })
        response = ajax(request)
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_canceled1, db_canceled2)

    def test_cancel_review(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import cancel_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(json_body={
            'queue': 'deletes',
            'uid': 4
        })
        response = ajax(request)
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertTrue(response)
        self.assertNotEqual(db_canceled1, db_canceled2)

    def test_cancel_review_author_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import cancel_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(json_body={
            'queue': 'deletes',
            'uid': 4
        })
        response = ajax(request)
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_canceled1, db_canceled2)

    def test_cancel_review_queue_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import cancel_review as ajax
        db_canceled1 = len(DBDiscussionSession.query(ReviewCanceled).all())
        request = testing.DummyRequest(json_body={
            'queue': 'some_queue',
            'uid': 4
        })
        response = ajax(request)
        db_canceled2 = len(DBDiscussionSession.query(ReviewCanceled).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_canceled1, db_canceled2)

    def test_review_lock(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': db_review.uid,
            'lock': True
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) != 0)
        self.assertTrue(len(response['info']) == 0)
        self.assertTrue(response['is_locked'])

    def test_review_lock_twice(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': db_review.uid,
            'lock': True
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['info']) != 0)
        self.assertTrue(response['is_locked'])

    def test_review_lock_author_error(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': db_review.uid,
            'lock': True
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertEqual(400, response.status_code)

    def test_review_lock_id_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': 100,
            'lock': 'true'
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_review_unlock(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewOptimization).first()
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': db_review.uid,
            'lock': False
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) != 0)
        self.assertTrue(len(response['info']) == 0)
        self.assertFalse(response['is_locked'])

    def test_revoke_content(self):
        self.config.testing_securitypolicy(userid=nick_of_anonymous_user, permissive=True)
        from dbas.views import revoke_statement_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(json_body={
            'uid': 2,
        })
        self.assertTrue(ajax(request))
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertNotEqual(db_content1, db_content2)

    def test_revoke_content_uid_error1(self):
        self.config.testing_securitypolicy(userid=nick_of_anonymous_user, permissive=True)
        from dbas.views import revoke_statement_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(json_body={
            'uid': 'a',
        })
        response = ajax(request)
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_content1, db_content2)

    def test_revoke_content_uid_error2(self):
        self.config.testing_securitypolicy(userid=nick_of_anonymous_user, permissive=True)
        from dbas.views import revoke_statement_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(json_body={
            'uid': 150,
        })
        response = ajax(request)
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_content1, db_content2)

    def test_revoke_content_author_error1(self):
        self.config.testing_securitypolicy(userid='', permissive=True)
        from dbas.views import revoke_statement_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(json_body={
            'uid': 3,
        })
        response = ajax(request)
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_content1, db_content2)

    def test_revoke_content_author_error2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import revoke_statement_content as ajax
        db_content1 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        request = testing.DummyRequest(json_body={
            'uid': 3,
        })
        response = ajax(request)
        db_content2 = len(DBDiscussionSession.query(RevokedContentHistory).all())
        self.assertEqual(400, response.status_code)
        self.assertEqual(db_content1, db_content2)

    def test_duplicate_statement_review(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        uid = 15

        from dbas.lib import get_text_for_argument_uid, get_all_arguments_by_statement
        from dbas.views import flag_argument_or_statement as ajax
        argument_uid = get_all_arguments_by_statement(uid)[0].uid

        db_review1 = len(DBDiscussionSession.query(ReviewDuplicate).all())
        request = testing.DummyRequest(json_body={
            'uid': uid,  # 'cats are very independent
            'reason': 'duplicate',
            'extra_uid': 1,  # Cats are fucking stupid and bloody fuzzy critters!,
            'is_argument': False
        })
        response = ajax(request)
        db_review2 = len(DBDiscussionSession.query(ReviewDuplicate).all())
        self.assertIsNotNone(response)
        self.assertEqual(response['info'], '')
        self.assertNotEqual(len(response['success']), 0)
        self.assertLess(db_review1, db_review2)

        db_review = DBDiscussionSession.query(ReviewDuplicate).filter_by(duplicate_statement_uid=uid,
                                                                         original_statement_uid=1).first()
        self.assertFalse(db_review.is_executed)

        # vote for duplicate
        from dbas.views import review_duplicate_statement as ajax
        oem_text = get_text_for_argument_uid(argument_uid)
        for name in ['Marga', 'Emmi', 'Rupert']:
            self.config.testing_securitypolicy(userid=name, permissive=True)
            db_review1 = len(DBDiscussionSession.query(LastReviewerDuplicate).all())
            request = testing.DummyRequest(json_body={
                'is_duplicate': True,
                'review_uid': db_review.uid
            })
            response = ajax(request)
            db_review2 = len(DBDiscussionSession.query(LastReviewerDuplicate).all())
            self.assertIsNotNone(response)
            self.assertTrue(response)
            self.assertLess(db_review1, db_review2)

        new_text = get_text_for_argument_uid(argument_uid)
        self.assertNotEqual(oem_text, new_text)
        self.assertTrue('fucking' in new_text)

        # we only can revoke decisions, which are executed (refresh the object)
        db_review = DBDiscussionSession.query(ReviewDuplicate).filter_by(duplicate_statement_uid=uid,
                                                                         original_statement_uid=1).first()
        self.assertTrue(db_review.is_executed)
        self.assertIsNotNone(DBDiscussionSession.query(ReviewDuplicate).get(db_review.uid))

        # revoke the decision
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import undo_review as ajax
        request = testing.DummyRequest(json_body={
            'uid': db_review.uid,
            'queue': 'duplicates',
        })
        self.assertTrue(ajax(request))

        new_oem_text = get_text_for_argument_uid(argument_uid)
        from Levenshtein import distance
        self.assertTrue(
            oem_text == new_oem_text or distance(oem_text.strip().lower(), new_oem_text.strip().lower()) == 12)
        self.assertFalse('fucking' in new_oem_text)

    def test_split_or_merge_statement_key_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uidd': 1,
            'key': 'it crashes',
            'text_values': []
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_statement_pgroup_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 0,
            'key': 'split',
            'text_values': ['']
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_statement_textvalue_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 2,
            'key': 'split',
            'text_values': ['']
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_statement_user_error(self):
        self.config.testing_securitypolicy(userid='nobody', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 1,
            'key': 'split',
            'text_values': []
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 20,
            'key': 'split',
            'text_values': ['it is based on the cats race', 'not every cat is capricious']
        })
        # oem of 20 is: 'the fact, that cats are capricious, is based on the cats race'
        db_review1 = len(DBDiscussionSession.query(ReviewSplit).all())
        db_values1 = len(DBDiscussionSession.query(ReviewSplitValues).all())
        response = ajax(request)
        db_review2 = len(DBDiscussionSession.query(ReviewSplit).all())
        db_values2 = len(DBDiscussionSession.query(ReviewSplitValues).all())
        self.assertEqual(len(response['info']), 0)
        self.assertNotEqual(len(response['success']), 0)
        self.assertEqual(db_review1 + 1, db_review2)
        self.assertEqual(db_values1 + 2, db_values2)

        tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=20).first()
        DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=20).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_merge_statement_pgroup_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 0,
            'key': 'merge',
            'text_values': ['']
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_merge_statement_textvalue_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 2,
            'key': 'merge',
            'text_values': ['']
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_merge_statement_user_error(self):
        self.config.testing_securitypolicy(userid='nobody', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 1,
            'key': 'merge',
            'text_values': []
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_merge_statement(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': 20,
            'key': 'merge',
            'text_values': ['it is based on the cats race', 'not every cat is capricious']
        })
        # oem of 20 is: 'the fact, that cats are capricious, is based on the cats race'
        db_review1 = len(DBDiscussionSession.query(ReviewMerge).all())
        db_values1 = len(DBDiscussionSession.query(ReviewMergeValues).all())
        response = ajax(request)
        db_review2 = len(DBDiscussionSession.query(ReviewMerge).all())
        db_values2 = len(DBDiscussionSession.query(ReviewMergeValues).all())
        self.assertEqual(len(response['info']), 0)
        self.assertNotEqual(len(response['success']), 0)
        self.assertEqual(db_review1 + 1, db_review2)
        self.assertEqual(db_values1 + 2, db_values2)

        tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=20).first()
        DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=20).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_split_premisegroup_key_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'pgroup_uidd': 1,
            'key': 'split',
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_premisegroup_pgroup_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'pgroup_uid': 0,
            'key': 'split',
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_premisegroup_user_error(self):
        self.config.testing_securitypolicy(userid='some_user', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'pgroup_uid': 0,
            'key': 'split',
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_split_premisegroup(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'uid': 21,
            'key': 'split',
        })
        db_review1 = len(DBDiscussionSession.query(ReviewSplit).all())
        db_values1 = len(DBDiscussionSession.query(ReviewSplitValues).all())
        response = ajax(request)
        db_review2 = len(DBDiscussionSession.query(ReviewSplit).all())
        db_values2 = len(DBDiscussionSession.query(ReviewSplitValues).all())
        self.assertEqual(len(response['info']), 0)
        self.assertNotEqual(len(response['success']), 0)
        self.assertEqual(db_review1 + 1, db_review2)
        self.assertEqual(db_values1, db_values2)

        tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=21).first()
        DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(PremiseGroupSplitted).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=21).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_merge_premisegroup_pgroup_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'uid': 0,
            'key': 'merge',
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_merge_premisegroup_user_error(self):
        self.config.testing_securitypolicy(userid='some_user', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'uid': 0,
            'key': 'merge',
        })
        self.assertEqual(400, ajax(request).status_code)

    def test_merge_premisegroup(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import split_or_merge_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'uid': 21,
            'key': 'merge',
        })
        db_review1 = len(DBDiscussionSession.query(ReviewMerge).all())
        db_values1 = len(DBDiscussionSession.query(ReviewMergeValues).all())
        response = ajax(request)
        db_review2 = len(DBDiscussionSession.query(ReviewMerge).all())
        db_values2 = len(DBDiscussionSession.query(ReviewMergeValues).all())
        self.assertEqual(len(response['info']), 0)
        self.assertNotEqual(len(response['success']), 0)
        self.assertEqual(db_review1 + 1, db_review2)
        self.assertEqual(db_values1, db_values2)

        tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=21).first()
        DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=21).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_review_splitted_premisegroup_uid_error(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import review_splitted_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': 0,
            'should_split': True,
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_review_splitted_premisegroup_user_error(self):
        self.config.testing_securitypolicy(userid='some_child', permissive=True)
        from dbas.views import review_splitted_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': 1,
            'should_split': True,
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_review_splitted_premisegroup(self, pgroup_uid=21, resetdb=True):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        # add something for a review
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': pgroup_uid,
            'key': 'split',
            'text_values': ['it is based on the cats race', 'not every cat is capricious']
        })
        # oem of pgroup pgroup_uid is: 'the fact, that cats are capricious, is based on the cats race'
        ajax(request)
        tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=pgroup_uid).first()

        db_arguments_with_pgroup = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=pgroup_uid).all()

        # vote 1:0
        from dbas.views import review_splitted_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_split': True
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_split=True).all())
        con = len(db_review.filter_by(should_split=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 1)
        self.assertEqual(con, 0)

        # vote 2:0
        self.config.testing_securitypolicy(userid='Christian', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_split': True,
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_split=True).all())
        con = len(db_review.filter_by(should_split=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 2)
        self.assertEqual(con, 0)

        # vote 2:1
        self.config.testing_securitypolicy(userid='Bob', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_split': False,
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_split=True).all())
        con = len(db_review.filter_by(should_split=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 2)
        self.assertEqual(con, 1)

        # vote 3:1
        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_split': True,
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_split=True).all())
        con = len(db_review.filter_by(should_split=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 3)
        self.assertEqual(con, 1)

        # vote 4:1
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_split': True,
        })
        arg_old_len = len(DBDiscussionSession.query(Argument).all())

        response = ajax(request)

        arg_new_len = len(DBDiscussionSession.query(Argument).all())
        db_review = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_split=True).all())
        con = len(db_review.filter_by(should_split=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 4)
        self.assertEqual(con, 1)
        self.assertEqual(arg_old_len + 1, arg_new_len)

        # now the vote is executed
        self.assertTrue(DBDiscussionSession.query(ReviewSplit).get(tmp.uid).is_executed)

        # check the new premisegroups
        for arg in db_arguments_with_pgroup:
            tmp_arg = DBDiscussionSession.query(Argument).get(arg.uid)
            self.assertNotEqual(pgroup_uid, tmp_arg.premisesgroup_uid)
            self.assertNotEqual(arg.premisesgroup_uid, tmp_arg.premisesgroup_uid)

        # remove added args
        add_args = DBDiscussionSession.query(ArgumentsAddedByPremiseGroupSplit).filter_by(review_uid=tmp.uid).all()
        self.assertEqual(len(add_args), 1)  # one argument was added and one was modified
        map(lambda arg: DBDiscussionSession.query(Argument).filter_by(arg.uid).delete(), add_args)

        if resetdb:
            DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(PremiseGroupSplitted).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ArgumentsAddedByPremiseGroupSplit).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.flush()
            DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=pgroup_uid).delete()
            DBDiscussionSession.flush()
            transaction.commit()

    def test_review_merged_premisegroup(self, pgroup_uid=27, resetdb=True):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        # add something for a review
        from dbas.views import split_or_merge_statement as ajax
        request = testing.DummyRequest(json_body={
            'uid': pgroup_uid,
            'key': 'merge',
            'text_values': ['cats are small and fluffy']
        })
        ajax(request)
        tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=pgroup_uid).first()

        # vote 1:0
        from dbas.views import review_merged_premisegroup as ajax
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_merge': True
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_merge=True).all())
        con = len(db_review.filter_by(should_merge=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 1)
        self.assertEqual(con, 0)

        # vote 2:0
        self.config.testing_securitypolicy(userid='Christian', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_merge': True,
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_merge=True).all())
        con = len(db_review.filter_by(should_merge=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 2)
        self.assertEqual(con, 0)

        # vote 2:1
        self.config.testing_securitypolicy(userid='Bob', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_merge': False,
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_merge=True).all())
        con = len(db_review.filter_by(should_merge=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 2)
        self.assertEqual(con, 1)

        # vote 3:1
        self.config.testing_securitypolicy(userid='Pascal', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_merge': True,
        })
        response = ajax(request)
        db_review = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_merge=True).all())
        con = len(db_review.filter_by(should_merge=False).all())
        self.assertTrue(response)
        self.assertEqual(pro, 3)
        self.assertEqual(con, 1)

        # vote 4:1
        self.config.testing_securitypolicy(userid='Kurt', permissive=True)
        request = testing.DummyRequest(json_body={
            'review_uid': tmp.uid,
            'should_merge': True,
        })
        pgroup_old_len = len(DBDiscussionSession.query(PremiseGroup).all())
        db_new_pgroup = DBDiscussionSession.query(PremiseGroup).order_by(PremiseGroup.uid.desc()).first()
        db_arguments_with_pgroup = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=pgroup_uid).all()
        old_text, trash = get_text_for_premisesgroup_uid(pgroup_uid)
        old_argument_text = get_text_for_argument_uid(db_arguments_with_pgroup[0].uid)
        pgroup_merged_old_len = len(DBDiscussionSession.query(PremiseGroupMerged).all())
        response = ajax(request)

        new_text, trash = get_text_for_premisesgroup_uid(db_new_pgroup.uid)
        new_argument_text = get_text_for_argument_uid(db_arguments_with_pgroup[0].uid)
        pgroup_new_len = len(DBDiscussionSession.query(PremiseGroup).all())
        pgroup_merged_new_len = len(DBDiscussionSession.query(PremiseGroupMerged).all())
        db_review = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid)
        pro = len(db_review.filter_by(should_merge=True).all())
        con = len(db_review.filter_by(should_merge=False).all())

        self.assertTrue(response)
        self.assertEqual(pro, 4)
        self.assertEqual(con, 1)
        self.assertEqual(pgroup_old_len + 1, pgroup_new_len)
        self.assertEqual(pgroup_merged_old_len + 1, pgroup_merged_new_len)

        # now the vote is executed
        self.assertTrue(DBDiscussionSession.query(ReviewMerge).get(tmp.uid).is_executed)

        # check the new premisegroups in every argument
        map(lambda arg: self.assertEqual(arg.premisesgroup_uid, db_new_pgroup.uid), db_arguments_with_pgroup)

        # check text change
        self.assertNotEqual(old_text, new_text)
        self.assertNotEqual(old_argument_text, new_argument_text)

        if resetdb:
            DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=tmp.uid).delete()
            DBDiscussionSession.flush()
            DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=pgroup_uid).delete()
            DBDiscussionSession.flush()
            transaction.commit()

    def test_cancel_review_splitted_merged_premisegroup_errors(self):
        self.config.testing_securitypolicy(userid='someone', permissive=True)
        from dbas.views import cancel_review as ajax

        # user error
        request = testing.DummyRequest(json_body={
            'queue': 'splits',
            'uid': 1
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # uid error
        request = testing.DummyRequest(json_body={
            'queue': 'splits',
            'uid': 'a'
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        # queue error
        request = testing.DummyRequest(json_body={
            'queue': 'asd',
            'uid': 1
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        # no review error
        request = testing.DummyRequest(json_body={
            'queue': 'splits',
            'uid': 1000
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_cancel_review_splitted_premisegroup(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        # add something for a review
        from dbas.views import split_or_merge_statement as ajax

        request = testing.DummyRequest(json_body={
            'uid': 33,
            'key': 'split',
            'text_values': ['cats are small and fluffy', 'split it up man']
        })

        len1 = len(DBDiscussionSession.query(ReviewSplit).all())
        ajax(request)
        len2 = len(DBDiscussionSession.query(ReviewSplit).all())
        self.assertEqual(len1 + 1, len2)
        db_review = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=33).first()

        from dbas.views import cancel_review as ajax
        request = testing.DummyRequest(json_body={
            'queue': 'merges',
            'uid': db_review.uid,
        })

        response = ajax(request)
        len3 = len(DBDiscussionSession.query(ReviewSplit).all())
        self.assertTrue(response)
        self.assertEqual(len2, len3)

    def test_cancel_review_merged_premisegroup(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        # add something for a review
        from dbas.views import split_or_merge_statement as ajax

        request = testing.DummyRequest(json_body={
            'uid': 15,
            'key': 'merge',
            'text_values': ['cats are small and fluffy']
        })

        len1 = len(DBDiscussionSession.query(ReviewMerge).all())
        ajax(request)
        len2 = len(DBDiscussionSession.query(ReviewMerge).all())
        self.assertEqual(len1 + 1, len2)
        db_review = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=15).first()

        from dbas.views import cancel_review as ajax
        request2 = testing.DummyRequest(json_body={
            'queue': 'merges',
            'uid': db_review.uid,
        })

        response = ajax(request2)
        len3 = len(DBDiscussionSession.query(ReviewMerge).all())
        self.assertTrue(response)
        self.assertEqual(len2, len3)

    def test_undo_merge_split_review_errors(self):
        from dbas.views import undo_review as ajax

        # uid
        self.config.testing_securitypolicy(userid='peter', permissive=True)
        request = testing.DummyRequest(json_body={
            'queue': 'merges',
            'uid': 'a',
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        # no admin
        request = testing.DummyRequest(json_body={
            'queue': 'merges',
            'uid': 2,
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        # queue
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(json_body={
            'queue': 'HAHA',
            'uid': 2,
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

        # no uid
        request = testing.DummyRequest(json_body={
            'queue': 'merges',
            'uid': 5,
        })
        response = ajax(request)
        self.assertEqual(400, response.status_code)

    def test_undo_review_splitted_premisegroup(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        uid = 22

        # get one argument with the old premisegroup
        db_argument_old = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=uid).first()
        old_text = get_text_for_argument_uid(db_argument_old.uid)
        self.test_review_splitted_premisegroup(pgroup_uid=uid, resetdb=False)
        # get one argument with the new premisegroup
        db_new_pgroup = DBDiscussionSession.query(PremiseGroupSplitted).filter_by(old_premisegroup_uid=uid).first()
        db_argument_new1 = DBDiscussionSession.query(Argument).get(db_argument_old.uid)
        db_argument_new2 = DBDiscussionSession.query(Argument).filter_by(
            premisesgroup_uid=db_new_pgroup.new_premisegroup_uid).first()
        new_text1 = get_text_for_argument_uid(db_argument_new1.uid)
        new_text2 = get_text_for_argument_uid(db_argument_new2.uid)

        # text has to differ
        self.assertNotEqual(old_text, new_text1)
        self.assertNotEqual(old_text, new_text2)

        from dbas.views import undo_review as ajax
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=uid).first()
        request = testing.DummyRequest(json_body={
            'queue': 'splits',
            'uid': db_review.uid
        })
        self.assertTrue(ajax(request))

        resetted_text = get_text_for_argument_uid(db_argument_old.uid)
        self.assertEqual(len(old_text), len(resetted_text))
        for i in range(len(old_text)):
            self.assertEqual(old_text[i], resetted_text[i])
        self.assertEqual(old_text, resetted_text)

        tmp = DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=uid).first()
        DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(PremiseGroupSplitted).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ArgumentsAddedByPremiseGroupSplit).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.flush()
        DBDiscussionSession.query(ReviewSplit).filter_by(premisesgroup_uid=uid).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_undo_review_merged_premisegroup(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        uid = 14

        # get one argument with the old premisegroup
        db_argument_old = DBDiscussionSession.query(Argument).filter_by(premisesgroup_uid=uid).first()
        old_text = get_text_for_argument_uid(db_argument_old.uid)
        self.test_review_merged_premisegroup(pgroup_uid=uid, resetdb=False)
        # get one argument with the new premisegroup
        db_new_pgroup = DBDiscussionSession.query(PremiseGroupMerged).filter_by(old_premisegroup_uid=uid).first()
        db_argument_new1 = DBDiscussionSession.query(Argument).get(db_argument_old.uid)
        db_argument_new2 = DBDiscussionSession.query(Argument).filter_by(
            premisesgroup_uid=db_new_pgroup.new_premisegroup_uid).first()
        new_text1 = get_text_for_argument_uid(db_argument_new1.uid)
        new_text2 = get_text_for_argument_uid(db_argument_new2.uid)

        # text has to differ
        self.assertNotEqual(old_text, new_text1)
        self.assertNotEqual(old_text, new_text2)

        from dbas.views import undo_review as ajax
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_review = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=uid).first()
        request = testing.DummyRequest(json_body={
            'queue': 'merges',
            'uid': db_review.uid
        })
        self.assertTrue(ajax(request))

        resetted_text = get_text_for_argument_uid(db_argument_old.uid)
        self.assertEqual(len(old_text), len(resetted_text))
        for i in range(len(old_text)):
            self.assertEqual(old_text[i], resetted_text[i])
        self.assertEqual(old_text, resetted_text)

        tmp = DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=uid).first()
        DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=tmp.uid).delete()
        DBDiscussionSession.flush()
        DBDiscussionSession.query(ReviewMerge).filter_by(premisesgroup_uid=uid).delete()
        DBDiscussionSession.flush()
        transaction.commit()
