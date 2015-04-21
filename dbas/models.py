from pyramid.security import (
    Allow,
    Everyone,
    )

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit'),
                (Allow, 'group:editors', 'use'),
                (Allow, 'group:users', 'use') ]
    def __init__(self, request):
        pass
