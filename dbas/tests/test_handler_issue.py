import unittest
import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue
from dbas.strings.translator import Translator

import dbas.handler.issue as ih


class IssueHandlerTests(unittest.TestCase):

    def test_set_issue(self):
        nickname = ''
        info = 'info'
        long_info = 'long_info'
        title = 'title'
        lang = ''
        ui_locales = ''

        response = ih.set_issue(nickname, info, long_info, title, lang, 'http://test.url', ui_locales)
        self.assertTrue(len(response['error']) > 0)

        nickname = 'Tobias'
        response = ih.set_issue(nickname, info, long_info, title, lang, 'http://test.url', ui_locales)
        self.assertTrue(len(response['error']) > 0)

        lang = 'en'
        response = ih.set_issue(nickname, info, long_info, title, lang, 'http://test.url', ui_locales)
        self.assertTrue(len(response['error']) > 0)

        ui_locales = 'en'
        response = ih.set_issue(nickname, info, long_info, title, lang, 'http://test.url', ui_locales)
        self.assertTrue(len(response['error']) > 0)

        info = 'infoinfoinfo'
        long_info = 'long_infolong_infolong_info'
        title = 'titletitletitle'
        response = ih.set_issue(nickname, info, long_info, title, lang, 'http://test.url', ui_locales)
        self.assertTrue(len(response['error']) == 0)

        response = ih.set_issue(nickname, info, long_info, title, lang, 'http://test.url', ui_locales)
        self.assertTrue(len(response['error']) > 0)

        DBDiscussionSession.query(Issue).filter_by(title=title).delete()
        DBDiscussionSession.flush()
        transaction.commit()

    def test_prepare_json_of_issue(self):
        uid = 1
        lang = 'en'
        for_api = False
        response = ih.prepare_json_of_issue(uid, 'http://test.url', lang, for_api)
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

    def test_get_issue_dict_for(self):
        for_api = False
        uid = 1
        lang = 'en'
        response = ih.get_issue_dict_for('', 'http://test.url', for_api, uid, lang)
        self.assertTrue(len(response['error']) > 0)

        issue = DBDiscussionSession.query(Issue).first()
        for_api = False
        uid = issue.uid
        lang = 'en'
        response = ih.get_issue_dict_for(issue, 'http://test.url', for_api, uid, lang)
        self.assertTrue(len(response) > 0)
        self.assertTrue(len(response['error']) == 0)

    def test_get_id_of_slug(self):
        issue = DBDiscussionSession.query(Issue).filter_by(is_disabled=False).first()
        slug = issue.slug
        request = testing.DummyRequest(matchdict={})
        response = ih.get_id_of_slug(slug, request, False)
        self.assertEqual(response, issue.uid)

    def test_get_issue_id(self):
        request = testing.DummyRequest(matchdict={'issue': 1})
        response = ih.get_issue_id(request)
        self.assertEqual(response, 1)

        request = testing.DummyRequest(params={'issue': 1})
        response = ih.get_issue_id(request)
        self.assertEqual(response, 1)

        request = testing.DummyRequest(session={'issue': 1})
        response = ih.get_issue_id(request)
        self.assertEqual(response, 1)

    def test_get_title_for_slug(self):
        issue = DBDiscussionSession.query(Issue).first()
        slug = issue.slug
        response = ih.get_title_for_slug(slug)
        self.assertEqual(issue.title, response)

    def test_get_issues_overiew(self):
        nickname = 'Tobias'
        response = ih.get_issues_overiew(nickname, 'http://test.url')
        self.assertIn('user', response)
        self.assertIn('other', response)
        self.assertTrue(len(response['user']) > 0)
        self.assertTrue(len(response['other']) == 0)

        nickname = 'Christian'
        response = ih.get_issues_overiew(nickname, 'http://test.url')
        self.assertIn('user', response)
        self.assertIn('other', response)
        self.assertTrue(len(response['user']) == 0)
        self.assertTrue(len(response['other']) > 0)

    def test_set_discussions_availability(self):
        nickname = ''
        uid = 0
        enable = True
        translator = Translator('en')
        response = ih.set_discussions_availability(nickname, uid, enable, translator)
        self.assertTrue(len(response['error']) > 0)

        nickname = 'Christian'
        uid = 0
        response = ih.set_discussions_availability(nickname, uid, enable, translator)
        self.assertTrue(len(response['error']) > 0)

        uid = DBDiscussionSession.query(Issue).first().uid
        response = ih.set_discussions_availability(nickname, uid, enable, translator)
        self.assertTrue(len(response['error']) > 0)

        nickname = 'Tobias'
        response = ih.set_discussions_availability(nickname, uid, enable, translator)
        transaction.commit()
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(DBDiscussionSession.query(Issue).get(uid).is_disabled is False)

        enable = False
        response = ih.set_discussions_availability(nickname, uid, enable, translator)
        transaction.commit()
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(DBDiscussionSession.query(Issue).get(uid).is_disabled is True)
