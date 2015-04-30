from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget

from .models import DBSession, User
from .security import USERS
from .helper import PasswordHandler

# from validate_email import validate_email
# is_valid = validate_email(email,check_mx=True)

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
		firstname = ''
		surename = ''
		email = ''
		reg_failed = False
		log_failed = False
		goto_url = self.request.route_url('main_content')

		# case: user login
		if 'form.login.submitted' in self.request.params:
			email = self.request.params['email']
			password = self.request.params['password']
			# user = DBSession.query(User).filter_by(email=email)
			#if (email in user.email):
			#	password = users.passwords

			if USERS.get(email) == password:
				headers = remember(self.request, email)
				return HTTPFound(
					location = goto_url,
					headers = headers
				)
			message = 'Failed login, please check your username and password'
			log_failed = True

		# case: user registration
		if 'form.registration.submitted' in self.request.params:
			firstname = self.request.params['firstname']
			surename = self.request.params['surename']
			email = self.request.params['email']
			password = self.request.params['password']
			users = DBSession.query(User)
			reg_failed = email in users
			if (not reg_failed):
				print("Register " + firstname + " " + surename + " " + email)
				# DBSession.add(User(firstname, surename, email, password, 'users'))
			else:
				message = 'E-Mail is already taken'


		return dict(
			title='Login',
			project='DBAS',
			message = message,
			url = self.request.application_url + '/login',
			came_from = came_from,
			password = password,
            firstname = firstname,
            surename = surename,
            email = email,
			login_failed = log_failed,
			registration_failed = reg_failed,
			logged_in = self.request.authenticated_userid
		)

	# logout page
	@view_config(route_name='main_logout', renderer='templates/logout.pt', permission='use')
	def main_logout(self):
		'''
		View configuration for the logout view. This will will automatically redirect to main_logout_redirect via JS
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
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
		return dict(
			title='Error',
			project='DBAS',
			page_notfound_viewname=self.request.view_name,
			logged_in = self.request.authenticated_userid
		)


# notices
# USE cryptacular
# salt.update(os.urandom(60))
# salt = sha1()
# hash = sha1()
# hash.update(password_8bit + salt.hexdigest())
# hashed_password = salt.hexdigest() + hash.hexdigest()