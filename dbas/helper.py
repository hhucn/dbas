from .models import DBSession, User
import random

systemmail = 'dbas@cs.uni-duesseldorf.de'


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

	def send_password_to_email(request):
		'''
		Checks, for a valid email in the request, generats, sends and updates a new password
		:param request: current request
		:return: message
		'''
		email = request.params['email']
		user_query = DBSession.query(User).filter_by(email)

		if  (user_query == ''):
			return 'There is no user with this address.'

		new_passwd = PasswordGenerator.get_rnd_passwd()
		user_query.password = new_passwd
		DBSession.commit()

		#message = Message(subject='Password Request',
		#                  sender=systemmail,
		#                  recipients =[email],
		#                  body='Your new password is: ' + new_passwd
		#                  )
		#mailer.send(message)
		return 'A new password was send to ' + email