import transaction

import smtplib
from socket import error as socket_error

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .database import DBSession
from .database.model import User, Group
from .helper import PasswordHandler, PasswordGenerator, logger


class Dbas(object):
	def __init__(self, request):
		'''
		Object initialization
		:param request: init http request
		:return:
		'''
		self.request = request

	# main page
	@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
	def main_page(self):
		logger('main_page','def','main page')
		"""
		View configuration for the main page
		:return:
		"""
		return dict(
			title='Main',
			project='DBAS',
			logged_in = self.request.authenticated_userid
		)

	# login page
	@view_config(route_name='main_login', renderer='templates/login.pt', permission='everybody')
	@forbidden_view_config(renderer='templates/login.pt')
	def main_login(self):
		"""
		View-configuration for the login template
		:return:
		"""
		# check for already logged in users
		logger('main_login','def','login page')
		if (self.request.authenticated_userid):
			return HTTPFound(
				location = self.request.route_url('main_content'),
			)

		login_url = self.request.route_url('main_login')
		referrer = self.request.url

		if referrer == login_url:
			referrer = self.request.route_url('main_page') # never use the login form itself as came_from
		came_from = self.request.params.get('came_from', referrer)

		# some variables
		message = ''
		password = ''
		passwordconfirm = ''
		firstname = ''
		surename = ''
		nickname = ''
		email = ''
		reg_failed = False
		log_failed = False
		reg_success = False
		goto_url = self.request.route_url('main_content')

		# case: user login
		if 'form.login.submitted' in self.request.params:
			logger('main_login','form.login.submitted','requesting params')

			#requesting parameters
			nickname = self.request.params['nickname']
			password = self.request.params['password']
			DBUser = DBSession.query(User).filter_by(nickname=nickname).first()

			# check for user and password validations
			if (not DBUser):
				logger('main_login','form.login.submitted','user \'' + nickname + '\' does not exists')
				message = 'User does not exists'
			elif (not DBUser.validate_password(password)): # DBUser.validate_password(password)
				logger('main_login','form.login.submitted','wrong password')
				message = 'Wrong password'
			else:
				logger('main_login','form.login.submitted','login successful')
				headers = remember(self.request, nickname)
				return HTTPFound(
					location = goto_url,
					headers = headers
				)
			log_failed = True

		# case: user registration
		if 'form.registration.submitted' in self.request.params:
			logger('main_login','form.registration.submitted','Requesting params')

			# getting parameter
			firstname = self.request.params['firstname']
			surename = self.request.params['surename']
			nickname = self.request.params['nickname']
			email = self.request.params['email']
			password = self.request.params['password']
			passwordconfirm = self.request.params['passwordconfirm']

			#database queries mail verification
			DBNick = DBSession.query(User).filter_by(nickname=nickname).first()
			DBMail = DBSession.query(User).filter_by(email=email).first()
			logger('main_login','form.registration.submitted','Validating email')
			is_mail_valid = validate_email(email,check_mx=True)

			# are the password equal?
			if (not password == passwordconfirm):
				logger('main_login','form.registration.submitted','Passwords are not equal')
				message = 'Passwords are not equal'
				password = ''
				passwordconfirm = ''
				reg_failed = True
			# is the nick already taken?
			elif (DBNick):
				logger('main_login','form.registration.submitted','Nickname \'' + nickname + '\' is taken')
				message = 'Nickname is taken'
				nickname = ''
				reg_failed = True
			# is the email already taken?
			elif (DBMail):
				logger('main_login','form.registration.submitted','E-Mail \'' + email + '\' is taken')
				message = 'E-Mail is taken'
				email = ''
				reg_failed = True
			# is the email valid?
			elif (not is_mail_valid):
				logger('main_login','form.registration.submitted','E-Mail \'' + email + '\' is not valid')
				message = 'E-Mail is not valid'
				email = ''
				reg_failed = True
			else:
				# getting the editors group
				group = DBSession.query(Group).filter_by(name='editors').first()

				# does the group exists?
				if (not group):
					message = 'An error occured, please try again later or contact the author'
					reg_failed = True
					logger('main_login','form.registration.submitted','Error occured')
				else:
					# creating a new user with hased password
					logger('main_login','form.registration.submitted','Adding user')
					hashedPassword = PasswordHandler.get_hashed_password(self, password)
					newuser = User(firstname=firstname, surename=surename, email=email,nickname=nickname,password=hashedPassword)
					newuser.group = group.uid
					DBSession.add(newuser)
					transaction.commit()

					# sanity check, whether the user exists
					checknewuser = DBSession.query(User).filter_by(nickname=nickname).first()
					if (checknewuser):
						logger('main_login','form.registration.submitted','New data was added with uid ' + str(checknewuser.uid))
						message = 'Your account was added and you are able to login now'
						reg_success = True
					else:
						logger('main_login','form.registration.submitted','New data was not added')
						message = 'Your account with the nick could not be added. Please try again or contact the author'
						reg_failed = True


		# case: user password request
		if 'form.passwordrequest.submitted' in self.request.params:
			logger('main_login','form.passwordrequest.submitted','requesting params')
			email = self.request.params['email']
			logger('main_login','form.passwordrequest.submitted','email is ' + email)
			DBUser = DBSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if (DBUser):
				# get password and hashed password
				pwd = PasswordGenerator.get_rnd_passwd(self)
				logger('main_login','form.passwordrequest.submitted','New password is ' + pwd)
				hashedpwd = PasswordHandler.get_hashed_password(self, pwd)
				logger('main_login','form.passwordrequest.submitted','New hashed password is ' + hashedpwd)

				# set the hased one
				DBUser.password = hashedpwd
				DBSession.add(DBUser)
				transaction.commit()
				message, reg_success, reg_failed = PasswordHandler.send_password_to_email(self.request, pwd)

				# logger
				if (reg_success):
					logger('main_login','form.passwordrequest.submitted','New password was sent')
				elif (reg_failed):
					logger('main_login','form.passwordrequest.submitted','Error occured')
			else:
				logger('main_login','form.passwordrequest.submitted','Mail unknown')
				message = 'The given e-mail address is unkown'
				reg_failed = True


		return dict(
			title='Login',
			project='DBAS',
			message = message,
			url = self.request.application_url + '/login',
			came_from = came_from,
			password = password,
			passwordconfirm = passwordconfirm,
            firstname = firstname,
            surename = surename,
			nickname=nickname,
            email = email,
			login_failed = log_failed,
			registration_failed = reg_failed,
			registration_success = reg_success,
			logged_in = self.request.authenticated_userid
		)

	# logout page
	@view_config(route_name='main_logout', renderer='templates/logout.pt', permission='use')
	def main_logout(self):
		'''
		View configuration for the logout view. This will will automatically redirect to main_logout_redirect via JS
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		logger('main_logout','def','user will be logged out')
		return dict(
			title='Logout',
			project='DBAS',
			logged_in = self.request.authenticated_userid
		)

	# logout redirect page
	@view_config(route_name='main_logout_redirect', permission='use')
	def main_logout_redirect(self):
		'''
		View configuration for the redirect logout view. This method will forget the headers of self.request
		:return: HTTPFound with location for the main page
		'''
		logger('main_logout_redirect','def','headers are now forgotten')
		logger('main_logout_redirect','def','redirecting to the main_page')
		headers = forget(self.request)
		return HTTPFound(
			location = self.request.route_url('main_page'),
			headers = headers
		)

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		'''
		View configuration for the contact view.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		logger('main_contact','def','contact page')
		contact_error = False
		sendMessage = False
		message=''
		name=''
		email=''
		phone=''
		content=''
		spam=''
		if 'form.contact.submitted' in self.request.params:
			logger('main_contact','form.contact.submitted','requesting params')
			name = self.request.params['name']
			email = self.request.params['mail']
			phone = self.request.params['phone']
			content = self.request.params['content']
			spam = self.request.params['spam']

			logger('main_contact','form.contact.submitted','validating email')
			is_mail_valid = validate_email(email,check_mx=True)

			# sanity checks
			if (not name):
				logger('main_contact','form.contact.submitted','name empty')
				contact_error = True
				message = "Your name is empty!"

			elif (not is_mail_valid):
				logger('main_contact','form.contact.submitted','mail is not valid')
				contact_error = True
				message = "Your e-mail is empty!"

			elif (not content):
				logger('main_contact','form.contact.submitted','content is empty')
				contact_error = True
				message = "Your content is empty!"

			elif (not spam):
				logger('main_contact','form.contact.submitted','anti-spam is empty')
				contact_error = True
				message = "Your anti-spam message is empty!"

			elif (not int(spam) == 4):
				logger('main_contact','form.contact.submitted','wrong anti spam answer')
				contact_error = True
				mesage = "Your anti-spam answer is wrong!"

			else:
				subject = 'Contact D-BAS'
				systemmail = 'krauthoff@cs.uni-duesseldorf.de'
				body = 'Name: ' + name + '\n' + 'Mail: ' + email + '\n' + 'Phone: ' + phone + '\n' + 'Message:\n' + content
				logger('main_contact','form.contact.submitted','sending mail')
				mailer = get_mailer(self.request)
				message = Message(subject=subject,
               	                  sender=systemmail,
               	                  recipients =["krauthoff@cs.uni-duesseldorf.de",email],
               	                  body=body
               	                )
				# try sending an catching errors
				try:
					mailer.send_immediately(message, fail_silently=False)
					sendMessage = True
					name=''
					email=''
					phone=''
					content=''
				except smtplib.SMTPConnectError as exception:
					logger('main_contact','form.contact.submitted','error while sending')
					logger('main_contact','exception smtplib.SMTPConnectError smtp_code', str(exception.smtp_code))
					logger('main_contact','exception smtplib.SMTPConnectError smtp_error', str(exception.smtp_error))
					contact_error = True
					message = 'Your message could not be send due to a system error! (' + 'smtp_code ' + str(exception.smtp_code) + ' || smtp_error ' + str(exception.smtp_error) + ')'
				except socket_error as serr:
					logger('main_contact','form.contact.submitted','error while sending')
					logger('main_contact','form.contact.submitted','socket_error ' + str(serr))
					contact_error = True
					message = 'Your message could not be send due to a system error! (' + 'socket_error ' + str(serr) + ')'


		return dict(
			title='Contact',
			project='DBAS',
			logged_in=self.request.authenticated_userid,
			was_message_send=sendMessage,
			contact_error=contact_error,
			message=message,
			name=name,
			mail=email,
			phone=phone,
			content=content,
			spam=spam
		)

	# content page, after login
	@view_config(route_name='main_content', renderer='templates/content.pt', permission='use')
	def main_content(self):
		'''
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		DBUser = DBSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).first()
		msg = 'you are not the admin. Therefore no rainbow-colored ponys!'
		if (DBUser):
			if (DBUser.nickname == 'admin'):
				msg = 'you are the special kind of guy who is called admin :)'

		logger('main_content','def','main')
		return dict(
			title='Content',
			project='DBAS',
			logged_in = self.request.authenticated_userid,
			message=msg
		)

	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		'''
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		logger('main_settings','def','main')
		oldpw = ''
		newpw = ''
		confirmpw = ''
		message = ''
		error = False
		success = False

		db_firstname = 'unknown'
		db_surname = 'unknown'
		db_nickname = 'unknown'
		db_mail = 'unknown'
		db_group = 'unknown'

		DBUser = DBSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).first()
		if (DBUser):
			db_firstname = DBUser.firstname
			db_surname = DBUser.surname
			db_nickname = DBUser.nickname
			db_mail = DBUser.email
			DBGroup = DBSession.query(Group).filter_by(uid=DBUser.group).first()
			if (DBGroup):
				db_group = DBGroup.name

		if 'form.passwordchange.submitted' in self.request.params:
			logger('main_settings','form.changepassword.submitted','requesting params')
			oldpw = self.request.params['passwordold']
			newpw = self.request.params['password']
			confirmpw = self.request.params['passwordconfirm']

			# is the old password given?
			if (not oldpw):
				logger('main_settings','form.changepassword.submitted','old pwd is empty')
				message = 'The old password field is empty.'
				error = True
			# is the new password given?
			elif (not newpw):
				logger('main_settings','form.changepassword.submitted','new pwd is empty')
				message = 'The new password field is empty.'
				error = True
			# is the cofnrimation password given?
			elif (not confirmpw):
				logger('main_settings','form.changepassword.submitted','confirm pwd is empty')
				message = 'The password confirmation field is empty.'
				error = True
			# is new password equals the confirmation?
			elif (not newpw == confirmpw):
				logger('main_settings','form.changepassword.submitted','new pwds not equal')
				message = 'The new passwords are not equal'
				error = True
			# is new old password equals the new one?
			elif (oldpw == newpw):
				logger('main_settings','form.changepassword.submitted','pwds are the same')
				message = 'The new and old password are the same'
				error = True
			else:
				# is the old password valid?
				if (not DBUser.validate_password(oldpw)):
					logger('main_settings','form.changepassword.submitted','old password is wrong')
					message = 'Your old password is wrong.'
					error = True
				else:
					logger('main_login','form.passwordrequest.submitted','new password is ' + newpw)
					hashedpwd = PasswordHandler.get_hashed_password(self, newpw)
					logger('main_login','form.passwordrequest.submitted','New hashed password is ' + hashedpwd)

					# set the hased one
					DBUser.password = hashedpwd
					DBSession.add(DBUser)
					transaction.commit()

					logger('main_settings','form.changepassword.submitted','password was changed')
					message = 'Your password was changed'
					success = True

		return dict(
			title='Settings',
			project='DBAS',
			logged_in = self.request.authenticated_userid,
			passwordold = oldpw ,
			password = newpw ,
			passwordconfirm = confirmpw,
			change_error = error,
			change_success = success,
			message = message,
			db_firstname = db_firstname,
			db_surname = db_surname,
			db_nickname = db_nickname,
			db_mail = db_mail,
			db_group = db_group
		)

	# news page for everybody
	@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
	def main_news(self):
		'''
		View configuration for the news.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		logger('main_news','def','main')
		return dict(
			title='News',
			project='DBAS',
			logged_in = self.request.authenticated_userid
		)

	# impressum
	@view_config(route_name='main_impressum', renderer='templates/impressum.pt', permission='everybody')
	def main_impressum(self):
		'''
		View configuration for the impressum.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		logger('main_impressum','def','main')
		return dict(
			title='Impressum',
			project='DBAS',
			logged_in = self.request.authenticated_userid)

	# 404 page
	@notfound_view_config(renderer='templates/404.pt')
	def notfound(self):
		'''
		View configuration for the impressum.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		self.request.response.status = 404
		logger('notfound','def','view \'' + self.request.view_name + '\' not found')
		return dict(
			title='Error',
			project='DBAS',
			page_notfound_viewname=self.request.view_name,
			logged_in = self.request.authenticated_userid
		)
