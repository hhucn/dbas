from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
    )
from pyramid.renderers import get_renderer
from pyramid.view import (
    view_config,
    notfound_view_config
    )

class Prototype(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='main_page', renderer='templates/home.pt')
    def main_page(self):
        return dict(title='Main',project='dbas')

    @view_config(route_name='main_login', renderer='templates/login.pt')
    def main_login(self):
        return dict(title='Login',project='dbas')

    @view_config(route_name='main_contact', renderer='templates/contact.pt')
    def main_contact(self):
        return dict(title='Contact',project='dbas')

    #@view_config(context=HTTPNotFound, renderer='404.pt')
    #def not_found(self):
    #    request.response.status = 404
    #    return {}
    @notfound_view_config(renderer='templates/404.pt')
    def notfound(self):
        self.request.response.status = 404
        return dict(title='Error',project='dbas')
