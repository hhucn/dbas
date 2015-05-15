import logging
import random
import smtplib


from socket import error as socket_error
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from cryptacular.bcrypt import BCRYPTPasswordManager

systemmail = 'dbas@cs.uni-duesseldorf.de'
log = logging.getLogger(__name__)

def logger(who, when, what):
	#print(time.strftime("%H:%M:%S") + ' ' + who.upper() + '| ' + when + ': ' + what)
	log.debug(who.upper() + ' ' + when + ' <' + what + '>')

class PasswordGenerator(object):

	# http://interactivepython.org/runestone/static/everyday/2013/01/3_password.html
	def get_rnd_passwd(self):
		'''
		Generates a password with the length of 8 out of [a-z][A-Z][+-*/#!*?]
		:return: new secure password
		'''
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		upperalphabet = alphabet.upper()
		symbols= '+-*/#!*?'
		pw_len = 8
		pwlist = []

		for i in range(pw_len//3):
			pwlist.append(alphabet[random.randrange(len(alphabet))])
			pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
			pwlist.append(str(random.randrange(10)))
		for i in range(pw_len-len(pwlist)):
			pwlist.append(alphabet[random.randrange(len(alphabet))])

		pwlist.append(symbols[random.randrange(len(symbols))])
		pwlist.append(symbols[random.randrange(len(symbols))])

		random.shuffle(pwlist)
		pwstring = ''.join(pwlist)

		return pwstring


class PasswordHandler(object):

	def get_hashed_password(self, password):
		manager = BCRYPTPasswordManager()
		return manager.encode(password)


	def send_password_to_email(request, password):
		'''
		Checks, for a valid email in the request, generats, sends and updates a new password
		:param request: current request
		:params password: the new password
		:return: message
		'''
		email = request.params['email']

		subject = 'D-BAS Password Request'
		systemmail = 'krauthoff@cs.uni-duesseldorf.de'
		body = 'Your new password is: ' + password
		logger('main_contact','form.contact.submitted','sending mail')
		mailer = get_mailer(request)
		message = Message(subject=subject,
		                  sender=systemmail,
		                  recipients =[email],
		                  body=body
		                  )
		sendError = False
		sendMessage = False
		# try sending an catching errors
		try:
			mailer.send_immediately(message, fail_silently=False)
			sendMessage = True
			message = 'A new password was send to ' + email
		except smtplib.SMTPConnectError as exception:
			logger('helper','send_password_to_email','error while sending')
			logger('helper','send_password_to_email', str(exception.smtp_code))
			logger('helper','send_password_to_email', str(exception.smtp_error))
			sendError = True
			message = 'A message could not be send due to a system error! (' + 'smtp_code ' + str(exception.smtp_code) + ' || smtp_error ' + str(exception.smtp_error) + ')'
		except socket_error as serr:
			logger('helper','send_password_to_email','error while sending')
			logger('helper','send_password_to_email','socket_error ' + str(serr))
			sendError = True
			message = 'A message could not be send due to a system error! (' + 'socket_error ' + str(serr) + ')'

		return message, sendMessage, sendError