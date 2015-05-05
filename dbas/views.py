import time
import transaction

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget

from .database import DBSession
from .database.model import User, Group
from .helper import PasswordHandler, PasswordGenerator


def logger(who, when, what):
	print(time.strftime("%H:%M:%S") + ' ' + who.upper() + '| ' + when + ': ' + what);


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
		#ret_message = PasswordHandler.send_password_to_email(self.request)
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
			nickname = self.request.params['nickname']
			password = self.request.params['password']
			DBUser = DBSession.query(User).filter_by(nickname=nickname).first()

			if (not DBUser):
				logger('main_login','form.login.submitted','user \'' + nickname + '\' does not exists')
				message = 'User does not exists'
			elif (not DBUser.password == password): # DBUser.validate_password(password)
				logger('main_login','form.login.submitted','wrong password')
				message = 'Wrong password'

			if (DBUser and DBUser.password == password):
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
			firstname = self.request.params['firstname']
			surename = self.request.params['surename']
			nickname = self.request.params['nickname']
			email = self.request.params['email']
			password = self.request.params['password']
			passwordconfirm = self.request.params['passwordconfirm']

			DBNick = DBSession.query(User).filter_by(nickname=nickname).first()
			DBMail = DBSession.query(User).filter_by(email=email).first()
			logger('main_login','form.registration.submitted','Validating email')
			is_mail_valid = validate_email(email,check_mx=True)

			# sanity check, if everything is fine
			if (not password == passwordconfirm):
				logger('main_login','form.registration.submitted','Passwords are not equal')
				message = 'Passwords are not equal'
				password = ''
				passwordconfirm = ''
				reg_failed = True
			elif (DBNick):
				logger('main_login','form.registration.submitted','Nickname \'' + nickname + '\' is taken')
				message = 'Nickname is taken'
				nickname = ''
				reg_failed = True
			elif (DBMail):
				logger('main_login','form.registration.submitted','E-Mail \'' + email + '\' is taken')
				message = 'E-Mail is taken'
				email = ''
				reg_failed = True
			elif (not is_mail_valid):
				logger('main_login','form.registration.submitted','E-Mail \'' + email + '\' is not valid')
				message = 'E-Mail is not valid'
				email = ''
				reg_failed = True
			else:
				group = DBSession.query(Group).filter_by(name='editors').first()
				if (not group):
					message = 'An error occured, please try again later or contact the author'
					reg_failed = True
					logger('main_login','form.registration.submitted','Error occured')
				else:
					logger('main_login','form.registration.submitted','Adding user')

					newuser = User(firstname=firstname, surename=surename, email=email,nickname=nickname,password=password)
					#newuser._set_password(password)
					newuser.group = group.uid
					DBSession.add(newuser)
					transaction.commit()

					checknewuser = DBSession.query(User).filter_by(nickname=nickname).first()
					if (checknewuser):
						logger('main_login','form.registration.submitted','New data was added with uid ' + str(checknewuser.uid))
						message = 'Your account was added and you are able to login now'
						reg_success = True
					else:
						logger('main_login','form.registration.submitted','New data was not added')
						message = 'Your account with the nick could not be added. Please try again or contact the author'
						reg_failed = True


		# case: user registration
		if 'form.passwordrequest.submitted' in self.request.params:
			logger('main_login','form.passwordrequest.submitted','requesting params')
			email = self.request.params['email']
			DBMail = DBSession.query(User).filter_by(email=email).first()
			if (DBMail):
				logger('main_login','form.passwordrequest.submitted','New password was sent')
				pwd = PasswordGenerator.get_rnd_passwd()
				hashedpwd = PasswordHandler.get_hashed_password(pwd)
				DBSession.update(User).where(email=email).values(password=hashedpwd)
				message = PasswordHandler.send_password_to_email(self.request, pwd)
			else:
				logger('main_login','form.passwordrequest.submitted','Mail unknown')
				mesasge = 'The given e-mail address is unkown'


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
		sendMessage = False
		if 'form.contact.submitted' in self.request.params:
			name = self.request.params['name']
			mail = self.request.params['mail']
			phone = self.request.params['phone']
			content = self.request.params['message']
			subject = 'Contact D-BAS'
			systemmail = 'dbas@cs.uni-duesseldorf.de'
			body = 'Name: ' + name + '\n' + 'Mail: ' + mail + '\n' + 'Phone: ' + phone + '\n' + 'Message:\n' + content
#           message = Message()
#           if (not mail == ''):
#           	message = Message(subject=subject,
#           	                  sender=systemmail,
#           	                  recipients =["krauthoff@cs.uni-duesseldorf.de",mail],
#           	                  body=body
#           	                )
#           else:
#           	message = Message(subject=subject,
#           	                  sender=systemmail,
#           	                  recipients =["krauthoff@cs.uni-duesseldorf.de"],
#           	                  body=body
#           	                )
#           mailer.send(message)
			sendMessage = True
		return dict(
			title='Contact',
			project='DBAS',
			logged_in = self.request.authenticated_userid,
			contact_msg_send = sendMessage
		)

	# content page, after login
	@view_config(route_name='main_content', renderer='templates/content.pt', permission='use')
	def main_content(self):
		'''
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		logger('main_content','def','main')
		return dict(
			title='Content',
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
		logger('main_content','def','view \'' + self.request.view_name + '\' not found')
		return dict(
			title='Error',
			project='DBAS',
			page_notfound_viewname=self.request.view_name,
			logged_in = self.request.authenticated_userid
		)
