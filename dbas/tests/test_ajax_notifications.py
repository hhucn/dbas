import json
import unittest

import transaction
from pyramid import testing
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Message


class AjaxNotificationTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.test_author_uid = 2

    def tearDown(self):
        testing.tearDown()

    def add_messages(self):
        DBDiscussionSession.add(Message(from_author_uid=1,
                                        to_author_uid=self.test_author_uid,
                                        topic='Hey you',
                                        content='wanne buy some galsses?',
                                        is_inbox=True,
                                        read=False))
        DBDiscussionSession.add(Message(from_author_uid=self.test_author_uid,
                                        to_author_uid=1,
                                        topic='Hey you',
                                        content='wanne buy some galsses?',
                                        is_inbox=False,
                                        read=True))
        DBDiscussionSession.flush()
        transaction.commit()
        self.new_inbox_uid = DBDiscussionSession.query(Message).filter(and_(
            Message.from_author_uid == 1,
            Message.to_author_uid == self.test_author_uid,
            Message.topic == 'Hey you',
            Message.content == 'wanne buy some galsses?')).first().uid
        self.new_send_uid = DBDiscussionSession.query(Message).filter(and_(
            Message.from_author_uid == self.test_author_uid,
            Message.to_author_uid == 1,
            Message.topic == 'Hey you',
            Message.content == 'wanne buy some galsses?')).first().uid

    def delete_messages(self):
        DBDiscussionSession.query(Message).filter(and_(Message.topic == 'Hey you', Message.content == 'wanne buy some galsses?')).delete()
        transaction.commit()

    def test_notification_read(self):
        self.add_messages()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_unread1 = len(DBDiscussionSession.query(Message).filter_by(read=False).all())
        from dbas.views import set_notifications_read as ajax
        request = testing.DummyRequest(json_body={'ids': [self.new_inbox_uid]})
        response = ajax(request)
        db_unread2 = len(DBDiscussionSession.query(Message).filter_by(read=False).all())
        self.assertIsNotNone(response)
        self.assertEqual(db_unread1 - 1, db_unread2)
        self.delete_messages()

    def test_notification_delete(self):
        self.add_messages()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_notifications_delete as ajax
        db_message1 = len(DBDiscussionSession.query(Message).filter_by(to_author_uid=self.test_author_uid).all())
        db_message1 += len(DBDiscussionSession.query(Message).filter_by(from_author_uid=self.test_author_uid).all())
        request = testing.DummyRequest(params={'ids': json.dumps([self.new_inbox_uid])}, matchdict={})
        response = ajax(request)
        transaction.commit()
        db_message2 = len(DBDiscussionSession.query(Message).filter_by(to_author_uid=self.test_author_uid).all())
        db_message2 += len(DBDiscussionSession.query(Message).filter_by(from_author_uid=self.test_author_uid).all())
        self.assertIsNotNone(response)
        self.assertTrue(db_message1 != db_message2)
        self.assertTrue(len(response['error']) == 0)
        self.delete_messages()

    def test_send_notification(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_some_notification as ajax
        db_len1 = len(DBDiscussionSession.query(Message).filter(and_(Message.topic == 'Some text for a message',
                                                                     Message.content == 'Some text for a message')).all())
        request = testing.DummyRequest(params={
            'recipient': 'Christian',
            'title': 'Some text for a message',
            'text': 'Some text for a message',
        }, matchdict={})
        response = ajax(request)
        db_len2 = len(DBDiscussionSession.query(Message).filter(and_(Message.topic == 'Some text for a message',
                                                                     Message.content == 'Some text for a message')).all())
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(db_len1 != db_len2)
        DBDiscussionSession.query(Message).filter(and_(Message.topic == 'Some text for a message',
                                                       Message.content == 'Some text for a message')).delete()
        transaction.commit()

    def test_notification_read_failure1(self):
        from dbas.views import set_notifications_read as ajax
        request = testing.DummyRequest(json_body={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_notification_read_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_some_notification as ajax
        request = testing.DummyRequest(json_body={'id': 2})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_notification_delete_failure(self):
        from dbas.views import set_notifications_delete as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_send_notification_failure1(self):
        from dbas.views import send_some_notification as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_send_notification_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_some_notification as ajax
        request = testing.DummyRequest(params={
            'recipient': 'Tobias',
            'title': 'Some new text for a message',
            'text': 'Some new text for a message',
        }, matchdict={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
