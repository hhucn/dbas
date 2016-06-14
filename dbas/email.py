"""
Provides class for sending an email

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import smtplib

from socket import error as socket_error

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from .logger import logger
from .strings import Translator


class EmailHelper:
    """
    Provides method for sending an email
    """

    @staticmethod
    def send_mail(request, subject, body, recipient, lang):
        """
        Try except block for sending an email

        :param request: current request
        :param subject: subject text of the mail
        :param body: body text of the mail
        :param recipient: recipient of the mail
        :param lang: current language
        :return: triple with boolean for sent message, message-string
        """
        logger('EmailHelper', 'send_mail', 'sending mail with subject \'' + subject + '\' to ' + recipient)
        _t = Translator(lang)
        send_message = False
        mailer = get_mailer(request)
        body = body + "\n\n---\n" + _t.get(_t.emailBodyText)
        message = Message(subject=subject, sender='dbas.hhu@gmail.com', recipients=[recipient], body=body)
        # try sending an catching errors
        try:
            mailer.send_immediately(message, fail_silently=False)
            send_message = True
            message = _t.get(_t.emailWasSent)
        except smtplib.SMTPConnectError as exception:
            logger('EmailHelper', 'send_mail', 'error while sending')
            code = str(exception.smtp_code)
            error = str(exception.smtp_error)
            logger('EmailHelper', 'send_mail', 'exception smtplib.SMTPConnectError smtp_code ' + code)
            logger('EmailHelper', 'send_mail', 'exception smtplib.SMTPConnectError smtp_error ' + error)
            message = _t.get(_t.emailWasNotSent)
        except socket_error as serr:
            logger('EmailHelper', 'send_mail', 'error while sending')
            logger('EmailHelper', 'send_mail', 'socket_error ' + str(serr))
            message = _t.get(_t.emailWasNotSent)

        return send_message, message
