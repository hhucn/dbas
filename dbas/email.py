import logging
import smtplib

from socket import error as socket_error

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

log = logging.getLogger(__name__)

def logger(who, when, what):
	log.debug(who.upper() + ' ' + when + ' <' + what + '>')

class EmailHelper(object):

	def send_mail(self, request, subject, body, recipient):
		"""
		Try except block for sending an email
		:param request: current request
		:param subject: subject text of the mail
		:param body: body text of the mail
		:param recipient: recipient of the mail
		:return: boolean if message was sent, boolean an error occured, message if an error occured
		"""
		logger('EmailHelper', 'send_mail', 'sending mail with subject \'' + subject + '\' to ' + recipient)
		send_message = False
		contact_error = False
		mailer = get_mailer(request)
		body = body +"\n\n---\n" + \
				"This is an automatically generated mail by the D-BAS System.\n" + \
				"For contact please write an mail to krauthoff@cs.uni-duesseldorf.de\n" + \
				"This system is part of a doctoral thesis and currently in an alpha-phase."
		message = Message(subject=subject, sender='dbas.hhu@gmail.com', recipients=[recipient], body=body)
		# try sending an catching errors
		try:
			mailer.send_immediately(message, fail_silently=False)
			send_message = True
			message = 'An E-Mail was sent to the given address.'
		except smtplib.SMTPConnectError as exception:
			logger('EmailHelper', 'send_mail', 'error while sending')
			code = str(exception.smtp_code)
			error = str(exception.smtp_error)
			logger('EmailHelper', 'send_mail', 'exception smtplib.SMTPConnectError smtp_code ' + code)
			logger('EmailHelper', 'send_mail', 'exception smtplib.SMTPConnectError smtp_error ' + error)
			contact_error = True
			message = 'Your message could not be send due to a system error! (' + 'smtp_code ' + code + ' || smtp_error ' + error + ')'
		except socket_error as serr:
			logger('EmailHelper', 'send_mail', 'error while sending')
			logger('EmailHelper', 'send_mail', 'socket_error ' + str(serr))
			contact_error = True
			message = 'Your message could not be send due to a system error! (' + 'socket_error ' + str(serr) + ')'

		return send_message, contact_error, message
