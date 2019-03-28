import itertools
import unittest

from pyramid import testing
from pyramid_mailer.mailer import DummyMailer

from dbas.handler.email import send_mail
from dbas.helper.url import UrlManager
from dbas.lib import Attitudes, Relations
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_text_for_message


class DummyUser:
    def __init__(self):
        self.email = "foo@bar.baz"
        self.firstname = "Buz Buzzemann"


class TestMail(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def test_mail_for_justifying_statement(self):
        url = UrlManager(slug='cat-or-dog')
        url = url.get_url_for_justifying_statement(statement_uid=123, attitude=Attitudes.AGREE)

        for language, for_html in list(itertools.product(['de', 'en'], [True, False])):
            subject = "Test Mail"
            body = get_text_for_message(nickname=DummyUser().firstname, lang=language, path=url,
                                        message_content=_.statementAddedMessageContent, for_html=for_html)
            was_send, was_send_msg, msg = send_mail(mailer=DummyMailer, subject=subject, body=body,
                                                    recipient=DummyUser(),
                                                    lang=language)
            self.assertTrue(was_send)
            self.assertEqual(msg.body, body)

    def test_mail_for_reaction_on_argument(self):
        url = UrlManager(slug='cat-or-dog')
        url = url.get_url_for_reaction_on_argument(argument_uid=123,
                                                   relation=Relations.REBUT,
                                                   confrontation_argument=35)
        for language, for_html in list(itertools.product(['de', 'en'], [True, False])):
            subject = "Test Mail"
            body = get_text_for_message(nickname=DummyUser().firstname, lang=language, path=url,
                                        message_content=_.argumentAddedMessageContent, for_html=for_html)
            was_send, was_send_msg, msg = send_mail(mailer=DummyMailer, subject=subject, body=body,
                                                    recipient=DummyUser(),
                                                    lang=language)
            self.assertTrue(was_send)
            self.assertEqual(msg.body, body)
