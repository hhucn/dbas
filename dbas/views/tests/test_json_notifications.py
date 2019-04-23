import unittest

import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Message
from dbas.tests.utils import construct_dummy_request


class AjaxNotificationTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.test_author_uid = 2

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
        self.new_inbox_uid = DBDiscussionSession.query(Message).filter(
            Message.from_author_uid == 1,
            Message.to_author_uid == self.test_author_uid,
            Message.topic == 'Hey you',
            Message.content == 'wanne buy some galsses?').first().uid
        self.new_send_uid = DBDiscussionSession.query(Message).filter(
            Message.from_author_uid == self.test_author_uid,
            Message.to_author_uid == 1,
            Message.topic == 'Hey you',
            Message.content == 'wanne buy some galsses?').first().uid

    def delete_messages(self):
        DBDiscussionSession.query(Message).filter(Message.topic == 'Hey you',
                                                  Message.content == 'wanne buy some galsses?').delete()
        transaction.commit()

    def test_notification_read(self):
        self.add_messages()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        db_unread1 = DBDiscussionSession.query(Message).filter_by(read=False).count()
        from dbas.views import set_notifications_read as ajax
        request = construct_dummy_request(json_body={'ids': [self.new_inbox_uid]})
        response = ajax(request)
        db_unread2 = DBDiscussionSession.query(Message).filter_by(read=False).count()
        self.assertIsNotNone(response)
        self.assertEqual(db_unread1 - 1, db_unread2)
        self.delete_messages()

    def test_notification_delete(self):
        self.add_messages()
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_notifications_delete as ajax
        db_message1 = DBDiscussionSession.query(Message).filter_by(to_author_uid=self.test_author_uid).count()
        db_message1 += DBDiscussionSession.query(Message).filter_by(from_author_uid=self.test_author_uid).count()
        request = construct_dummy_request(json_body={'ids': [self.new_inbox_uid]})
        response = ajax(request)
        transaction.commit()
        db_message2 = DBDiscussionSession.query(Message).filter_by(to_author_uid=self.test_author_uid).count()
        db_message2 += DBDiscussionSession.query(Message).filter_by(from_author_uid=self.test_author_uid).count()
        self.assertIsNotNone(response)
        self.assertTrue(db_message1 != db_message2)
        self.delete_messages()

    def test_send_notification(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_some_notification as ajax
        db_len1 = DBDiscussionSession.query(Message).filter(Message.topic == 'Some text for a message',
                                                            Message.content == 'Some text for a message').count()
        request = construct_dummy_request(json_body={
            'recipient': 'Christian',
            'title': 'Some text for a message',
            'text': 'Some text for a message',
        })
        response = ajax(request)
        db_len2 = DBDiscussionSession.query(Message).filter(Message.topic == 'Some text for a message',
                                                            Message.content == 'Some text for a message').count()
        self.assertIsNotNone(response)
        self.assertTrue(db_len1 != db_len2)
        DBDiscussionSession.query(Message).filter(Message.topic == 'Some text for a message',
                                                  Message.content == 'Some text for a message').delete()
        transaction.commit()

    def test_notification_read_failure1(self):
        from dbas.views import set_notifications_read as ajax
        request = construct_dummy_request(json_body={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_notification_delete_failure(self):
        from dbas.views import set_notifications_delete as ajax
        request = construct_dummy_request(json_body={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_notification_read_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_some_notification as ajax
        request = construct_dummy_request(json_body={'id': 2})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_send_notification_failure1(self):
        from dbas.views import send_some_notification as ajax
        request = construct_dummy_request(json_body={})
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)

    def test_send_notification_failure2(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import send_some_notification as ajax
        request = construct_dummy_request(json_body={
            'recipient': 'Tobias',
            'title': 'Some new text for a message',
            'text': 'Some new text for a message',
        })
        response = ajax(request)
        self.assertIsNotNone(response)
        self.assertTrue(400, response.status_code)
