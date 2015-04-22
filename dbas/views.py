from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget

from .models import DBSession, User
from .security import USERS

class Dbas(object):
	def __init__(self, request):
		'''
		Object initialization
		:param request: init http request
		:return:
		'''
		self.request = request

	# main page
	@view_config(route_name='main_page', renderer='templates/index.pt', permission='view')
	def main_page(self):
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
	@view_config(route_name='main_login', renderer='templates/login.pt', permission='view')
	@forbidden_view_config(renderer='templates/login.pt')
	def main_login(self):
		"""
		View-configuration for the login template
		:return:
		"""
		login_url = self.request.route_url('main_login')
		referrer = self.request.url

		if referrer == login_url:
			referrer = '/' # never use the login form itself as came_from
		came_from = self.request.params.get('came_from', referrer)
		message = ''
		login = ''
		password = ''
		firstname = ''
		surename = ''
		email = ''
		reg_failed = False
		goto_url = self.request.route_url('main_content')

		if 'form.login.submitted' in self.request.params:
			login = self.request.params['login']
			password = self.request.params['password']
			# user = DBSesseion.query(User)
			if USERS.get(login) == password:
				headers = remember(self.request, login)
				return HTTPFound(
					location = goto_url,
					headers = headers
				)
			message = 'Failed login'

		if 'form.registration.submitted' in self.request.params:
			firstname = self.request.params['firstname']
			surename = self.request.params['surename']
			email = self.request.params['email']
			password = self.request.params['password']
			reg_failed = True
			if (not reg_failed):
				DBSession.add(User(firstname, surename, email, password, 'users'))
			else:
				message = 'Registration failed'


		return dict(
			title='Login',
			project='DBAS',
			message = message,
			url = self.request.application_url + '/login',
			came_from = came_from,
			login = login,
			password = password,
            firstname = firstname,
            surename = surename,
            email = email,
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
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='view')
	def main_contact(self):
		'''
		View configuration for the contact view.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		'''
		return dict(
			title='Contact',
			project='DBAS',
			logged_in = self.request.authenticated_userid
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
	@view_config(route_name='main_impressum', renderer='templates/impressum.pt', permission='view')
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