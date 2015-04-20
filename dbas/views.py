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

from .security import USERS


class Prototype(object):
    def __init__(self, request):
        self.request = request

    # main page
    @view_config(route_name='main_page', renderer='templates/home.pt', permission='view')
    def main_page(self):
        return dict(title='Main',project='DBAS')

    # login page
    @view_config(route_name='main_login', renderer='templates/login.pt', permission='view')
    def main_login(self):
        return dict(title='Login',project='DBAS')

    # logout page
    @view_config(route_name='main_logout', renderer='templates/logout.pt', permission='view')
    def main_login(self):
        return dict(title='Logout',project='DBAS')

    # contact page
    @view_config(route_name='main_contact', renderer='templates/contact.pt', permission='view')
    def main_contact(self):
        return dict(title='Contact',project='DBAS')

    # page, after login
    @view_config(route_name='main_content', renderer='templates/content.pt', permission='view')
    def main_content(self):
        return dict(title='Content',project='DBAS')

    # 404 page
    @notfound_view_config(renderer='templates/404.pt')
    def notfound(self):
        self.request.response.status = 404
        return dict(title='Error',project='DBAS')
