from cornice import Errors
from cornice.util import json_error

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User


def valid_user(request):
    db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).one_or_none()

    if db_user:
        request.validated['user'] = db_user
    else:
        request.errors.add('body', 'Invalid user', 'Authenticated userid not found in database')
        request.errors.status = 400


class validate(object):
    """
        Applies all validators to this function.
        If one of the validators adds an error, the function will not be called.
        In this situation a response is given with a json body, containing all errors from all validators.

        Decorate a function like this

        .. code-block:: python
        @validate(validators=(check_for_user, check_for_issue, )
        def my_view(request)
    """

    def __init__(self, validators=()):
        self.validators = validators

    def __call__(self, func):
        def inner(request):
            if not hasattr(request, 'validated'):
                setattr(request, 'validated', {})
            if not hasattr(request, 'errors'):
                setattr(request, 'errors', Errors())
            if not hasattr(request, 'info'):
                setattr(request, 'info', {})

            for validator in self.validators:
                validator(request)

            if len(request.errors) > 0:
                return json_error(request)

            return func(request)

        return inner
