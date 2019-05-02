from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import TextVersion, Statement, StatementToIssue
from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request


class AjaxTest(TestCaseWithConfig):
    def test_wrong_user(self):
        from admin.views import main_update as ajax1
        from admin.views import main_delete as ajax2
        from admin.views import main_add as ajax3
        ajax = [ajax1, ajax2, ajax3]
        for a in ajax:
            request = construct_dummy_request(json_body={}, validated={})
            self.assertEqual(400, a(request).status_code)

    def test_main_update(self):
        from admin.views import main_update as ajax

        request = construct_dummy_request(json_body={}, validated={})
        self.assertEqual(400, ajax(request).status_code)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={
            'table': 'TextVersion',
            'uids': [44],
            'keys': ['author_uid'],
            'values': ['Teresa (5)']
        }, validated={})
        response = ajax(request)
        self.assertTrue(response)
        self.assertEqual(5, DBDiscussionSession.query(TextVersion).get(44).author_uid)

    def test_main_delete_error(self):
        from admin.views import main_delete as ajax
        request = construct_dummy_request(json_body={}, validated={})
        self.assertEqual(400, ajax(request).status_code)

    def test_main_delete(self):
        from admin.views import main_delete as ajax
        db_s1 = DBDiscussionSession.query(Statement).all()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = construct_dummy_request(json_body={
            'table': 'statement',
            'uids': [db_s1[-1].uid]
        }, validated={})
        DBDiscussionSession.query(StatementToIssue).filter_by(statement_uid=db_s1[-1].uid).delete()
        self.assertIsNotNone(ajax(request))

    def test_main_add_and_delete_error(self):
        from admin.views import main_add as ajax_add
        from admin.views import main_delete as ajax_del

        request = construct_dummy_request(json_body={}, validated={})
        self.assertEqual(400, ajax_add(request).status_code)
        request = construct_dummy_request(json_body={}, validated={})
        self.assertEqual(400, ajax_del(request).status_code)

    def test_main_add_and_delete(self):
        from admin.views import main_add as ajax_add
        from admin.views import main_delete as ajax_del
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request_add = construct_dummy_request(json_body={
            'table': 'Statement',
            'new_data': {
                'is_position': False,
                'is_disabled': False
            }
        }, validated={})

        self.assertTrue(ajax_add(request_add))

        request_del = construct_dummy_request(json_body={
            'table': '',
            'uids': DBDiscussionSession.query(Statement).order_by(Statement.uid.desc()).first().uid
        }, validated={})
        self.assertTrue(ajax_del(request_del))
