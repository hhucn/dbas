import unittest
import json
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.helper.tests import add_settings_to_appconfig, verify_dictionary_of_view
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))


class AjaxText(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_ajax(self):
        self.assertTrue(1 is 1)

    def text_user_login(self):
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_user_logout(self):
        from dbas.views import user_logout as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_set_new_start_statement(self):
        from dbas.views import set_new_start_statement as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_set_new_start_premise(self):
        from dbas.views import set_new_start_premise as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_set_new_premises_for_argument(self):
        from dbas.views import set_new_premises_for_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_set_correction_of_statement(self):
        from dbas.views import set_correction_of_statement as ajax
        request = testing.DummyRequest(selfparams={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_set_new_issue(self):
        from dbas.views import set_new_issue as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_logfile_for_statements(self):
        from dbas.views import get_logfile_for_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_shortened_url(self):
        from dbas.views import get_shortened_url as ajax
        request = testing.DummyRequest(selfparams={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
    
    def text_user_registration(self):
        from dbas.views import user_registration as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_user_password_request(self):
        from dbas.views import user_password_request as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_fuzzy_search(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_switch_language(self):
        from dbas.views import switch_language as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_send_notification(self):
        from dbas.views import send_notification as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_infos_about_argument(self):
        from dbas.views import get_infos_about_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_user_with_same_opinion(self):
        from dbas.views import get_users_with_same_opinion as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_public_user_data(self):
        from dbas.views import get_public_user_data as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_user_history(self):
        from dbas.views import get_user_history as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_all_edits(self):
        from dbas.views import get_all_edits as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_all_posted_statements(self):
        from dbas.views import get_all_posted_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_all_argument_votes(self):
        from dbas.views import get_all_argument_votes as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_all_statement_votes(self):
        from dbas.views import get_all_statement_votes as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_set_user_setting(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_set_user_language(self):
        from dbas.views import set_user_language as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_delete_user_history(self):
        from dbas.views import delete_user_history as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_delete_statistics(self):
        from dbas.views import delete_statistics as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_news(self):
        from dbas.views import get_news as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_send_news(self):
        from dbas.views import send_news as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_notification_read(self):
        from dbas.views import set_notification_read as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_notification_delete(self):
        from dbas.views import set_notification_delete as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_arguments_by_statement_uid(self):
        from dbas.views import get_arguments_by_statement_uid as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_additional_service(self):
        from dbas.views import additional_service as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_flag_argument_or_statement(self):
        from dbas.views import flag_argument_or_statement as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_review_delete_argument(self):
        from dbas.views import review_delete_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_review_optimization_argument(self):
        from dbas.views import review_optimization_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_review_edit_argument(self):
        from dbas.views import review_edit_argument as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_undo_review(self):
        from dbas.views import undo_review as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_cancel_review(self):
        from dbas.views import cancel_review as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_review_lock(self):
        from dbas.views import review_lock as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_revoke_content(self):
        from dbas.views import revoke_content as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_get_references(self):
        from dbas.views import get_references as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_set_references(self):
        from dbas.views import set_references as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
        
    def text_set_seen_statements(self):
        from dbas.views import set_seen_statements as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertTrue(1 == 1)
