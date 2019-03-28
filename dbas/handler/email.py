"""
Provides class for sending an email

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
import os
import smtplib
from socket import error as socket_error
from threading import Thread
from typing import Tuple

from pyramid_mailer import Mailer
from pyramid_mailer.message import Message

from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_text_for_message
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


def send_mail_due_to_added_text(lang, url, recipient, mailer):
    """
    Will send an email to the recipient

    :param lang: ui_locales
    :param url: current url
    :param recipient: User
    :param mailer: current mailer
    :return: duple with boolean for sent message, message-string
    """
    _t = Translator(lang)
    subject = _t.get(_.statementAdded)
    body = get_text_for_message(recipient.firstname, lang, url, _.statementAddedMessageContent, False)

    return send_mail(mailer, subject, body, recipient.email, lang)


def send_mail(mailer: Mailer, subject: str, body: str, recipient: str, lang: str) -> Tuple[bool, str, Message]:
    """
    Try except block for sending an email

    :param mailer: current mailer
    :param subject: subject text of the mail
    :param body: body text of the mail
    :param recipient: recipient of the mail
    :param lang: current language
    :return: Triple with boolean for sent message, a verbose message and the complete message
    """
    LOG.debug("Sending mail with subject '%s' to %s", subject, recipient)
    _t = Translator(lang)
    was_mail_thread_started = False
    sender = os.environ.get("MAIL_DEFAULT__SENDER")
    message = Message(subject=subject, sender=sender, recipients=[recipient], body=body)

    try:
        t = Thread(target=__thread_to_send_mail, args=(mailer, message, recipient, body,))
        t.start()
        was_mail_thread_started = True
        status_message = _t.get(_.emailWasSent)
    except smtplib.SMTPConnectError as exception:
        code = str(exception.smtp_code)
        error = str(exception.smtp_error)
        LOG.error("Exception smtplib.SMTPConnectionError smtp code / error %s / %s", code, error)
        status_message = _t.get(_.emailWasNotSent)
    except socket_error as serr:
        LOG.error("Socket error while sending %s", serr)
        status_message = _t.get(_.emailWasNotSent)

    return was_mail_thread_started, status_message, message


def __thread_to_send_mail(mailer, message, recipient, body):
    LOG.debug("Start thread to send mail to %s with %s", recipient, body[:30])
    try:
        mailer.send_immediately(message, fail_silently=False)
    except TypeError as e:
        LOG.error("TypeError %s", e)
    LOG.debug("End thread to send mail to %s with %s", recipient, body[:30])
