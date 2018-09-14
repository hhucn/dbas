"""
Provides class for sending an email

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import logging
import os
import smtplib
from pyramid_mailer import Mailer
from pyramid_mailer.message import Message
from socket import error as socket_error

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, TextVersion, Language, Statement
from dbas.lib import get_global_url
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_text_for_add_text_message, get_text_for_edit_text_message, \
    get_text_for_add_argument_message
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
    body = get_text_for_add_text_message(recipient.firstname, lang, url, False)

    return send_mail(mailer, subject, body, recipient.email, lang)


def send_mail_due_to_added_argument(lang, url, recipient, mailer):
    """
    Will send an email to the recipient

    :param lang: ui_locales
    :param url: current url
    :param recipient: User
    :param mailer: Instance of pyramid mailer
    :return: duple with boolean for sent message, message-string
    """
    _t = Translator(lang)
    subject = _t.get(_.argumentAdded)
    body = get_text_for_add_argument_message(recipient.firstname, lang, url, False)

    return send_mail(mailer, subject, body, recipient.email, lang)


def send_mail_due_to_edit_text(statement_uid: int, previous_author: User, current_author: User, url: str,
                               mailer: Mailer):
    """
    Will send an email to the author of the statement.

    :param statement_uid: Statement.uid
    :param previous_author: User
    :param current_author: User
    :param url: current url
    :param mailer: current mailer
    :return: duple with boolean for sent message, message-string
    """
    db_statement = DBDiscussionSession.query(Statement).get(statement_uid)
    db_textversion_old = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid)
    db_textversion_new = DBDiscussionSession.query(TextVersion).get(db_statement.uid)

    db_previous_author = DBDiscussionSession.query(User).get(previous_author)
    db_current_author = DBDiscussionSession.query(User).get(current_author)

    db_language = DBDiscussionSession.query(Language).get(db_previous_author.setting.lang_uid)
    _t = Translator(db_language.ui_locales)
    subject = _t.get(_.textversionChangedTopic)
    body = get_text_for_edit_text_message(db_language.ui_locales, db_current_author.public_nickname,
                                          db_textversion_old.content, db_textversion_new.content, url, False)
    recipient = db_previous_author.email

    return send_mail(mailer, subject, body, recipient, db_language.ui_locales)


def send_mail(mailer, subject, body, recipient, lang):
    """
    Try except block for sending an email

    :param mailer: current mailer
    :param subject: subject text of the mail
    :param body: body text of the mail
    :param recipient: recipient of the mail
    :param lang: current language
    :return: duple with boolean for sent message, message-string
    """
    LOG.debug("Sending mail with subject '%s' to %s", subject, recipient)
    _t = Translator(lang)
    if not mailer:
        LOG.debug("Mailer is none")
        return False, _t.get(_.internalKeyError)

    send_message = False
    body = body + '\n\n---\n' + _t.get(_.emailBodyText).format(get_global_url())
    sender = os.environ.get("MAIL_DEFAULT__SENDER", None)
    message = Message(subject=subject, sender=sender, recipients=[recipient], body=body)

    # try sending an catching errors
    try:
        from threading import Thread
        t = Thread(target=__thread_to_send_mail, args=(mailer, message, recipient, body,))
        t.start()
        send_message = True
        message = _t.get(_.emailWasSent)
    except smtplib.SMTPConnectError as exception:
        code = str(exception.smtp_code)
        error = str(exception.smtp_error)
        LOG.debug("Exception smtplib.SMTPConnectionError smtp code / error %s / %s", code, error)
        message = _t.get(_.emailWasNotSent)
    except socket_error as serr:
        LOG.debug("Socker error while sending %s", serr)
        message = _t.get(_.emailWasNotSent)

    return send_message, message


def __thread_to_send_mail(mailer, message, recipient, body):
    LOG.debug("Start thread to send mail to %s with %s", recipient, body[:30])
    try:
        mailer.send_immediately(message, fail_silently=False)
    except TypeError as e:
        LOG.debug("TypeError %s", e)
    LOG.debug("End thread to send mail to %s with %s", recipient, body[:30])
