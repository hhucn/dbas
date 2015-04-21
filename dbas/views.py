import re
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
    )

from pyramid.renderers import get_renderer

from pyramid.view import (
    view_config,
    notfound_view_config,
    forbidden_view_config
    )

from pyramid.security import (
    remember,
    forget,
    )

from .security import USERS


class Prototype(object):
    def __init__(self, request):
        self.request = request

    # main page
    @view_config(route_name='main_page', renderer='templates/index.pt', permission='view')
    def main_page(self):
        return dict(
            title='Main',
            project='DBAS',
            logged_in = self.request.authenticated_userid
        )

    # login page
    #@view_config(route_name='main_login', renderer='templates/login.pt')
    #def main_login(self):
    #    return dict(title='Login',project='DBAS')
    @view_config(route_name='main_login', renderer='templates/login.pt', permission='view')
    @forbidden_view_config(renderer='templates/login.pt')
    def main_login(self):
        login_url = self.request.route_url('main_login')
        referrer = self.request.url

        if referrer == login_url:
            referrer = '/' # never use the login form itself as came_from
        came_from = self.request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        reg_failed = False
        goto_url = self.request.route_url('main_content')

        if 'form.login.submitted' in self.request.params:
            login = self.request.params['login']
            password = self.request.params['password']
            if USERS.get(login) == password:
                headers = remember(self.request, login)
                return HTTPFound(
                    location = goto_url,
                    headers = headers
                )
            message = 'Failed login'
            reg_failed = True

        if 'form.registration.submitted' in self.request.params:
            message = 'Registration login'

        return dict(
            title='Login',
            project='DBAS',
            message = message,
            url = self.request.application_url + '/login',
            came_from = came_from,
            login = login,
            password = password,
            registration_failed = reg_failed,
            logged_in = self.request.authenticated_userid
        )

    # logout page
    @view_config(route_name='main_logout', renderer='templates/logout.pt', permission='view')
    def main_logout(self):
        # rediret to the logout page, when we are logged in
        # otherwise redirect to the main page
        if (self.request.authenticated_userid):
            headers = forget(self.request)
            return HTTPFound(
                location = self.request.route_url('main_logout_redirect'),
                headers = headers
            )
        else:
            return HTTPFound(
                location = self.request.route_url('main_page')
            )

    # logout redirect page
    @view_config(route_name='main_logout_redirect', renderer='templates/logout.pt', permission='view')
    def main_logout_redirect(self):
        logout_url = self.request.route_url('main_logout')
        referrer = self.request.url

        # return the regulary logout page, when we came fron /logout
        # otherwise redirect to the main page
        if referrer == logout_url:
            return dict(
                title='Logout',
                project='DBAS',
                logged_in = self.request.authenticated_userid
            )
        else:
            return HTTPFound(
                location = self.request.route_url('main_page')

            )

    # contact page
    @view_config(route_name='main_contact', renderer='templates/contact.pt', permission='view')
    def main_contact(self):
        return dict(
            title='Contact',
            project='DBAS',
            logged_in = self.request.authenticated_userid
        )

    # content page, after login
    @view_config(route_name='main_content', renderer='templates/content.pt', permission='use')
    def main_content(self):
        return dict(
            title='Content',
            project='DBAS',
            logged_in = self.request.authenticated_userid
        )

    # impressum
    @view_config(route_name='main_impressum', renderer='templates/impressum.pt', permission='view')
    def main_impressum(self):
        return dict(
            title='Impressum',
            project='DBAS',
            logged_in = self.request.authenticated_userid)

    # 404 page
    @notfound_view_config(renderer='templates/404.pt')
    def notfound(self):
        self.request.response.status = 404
        return dict(
            title='Error',
            project='DBAS',
            page_notfound_viewname=self.request.view_name,
            logged_in = self.request.authenticated_userid
        )
