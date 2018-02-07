from cornice import Errors
from cornice.util import json_error

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, Issue
from dbas.handler.language import get_language_from_cookie
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
import dbas.handler.issue as issue_helper
from pyramid.httpexceptions import HTTPBadRequest


def combine(*decorators):
    """
    Requires a list of decorators, which will be chained together

    :param decorators:
    :return:
    """
    def floo(view_callable):
        for decorator in decorators:
            view_callable = decorator(view_callable)
        return view_callable
    return floo


def valid_user(view_callable, **kwargs):
    """

    :param view_callable:
    :return:
    """
    def inner(context, request):
        db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
        if db_user:
            kwargs['user'] = db_user
            return view_callable(context, request, kwargs)
        else:
            _tn = Translator(get_language_from_cookie(request))
            return HTTPBadRequest({
                'path': request.path,
                'message': _tn.get(_.checkNickname)
            })
    return inner


def valid_issue(view_callable, **kwargs):
    """

    :param view_callable:
    :return:
    """

    def inner(context, request):
        issue_id = issue_helper.get_issue_id(request)
        db_issue = DBDiscussionSession.query(Issue).get(issue_id)
        kwargs['issue'] = db_issue
        return view_callable(context, request)
    return inner


# def valid_user(request):
#     db_user = DBDiscussionSession.query(User).filter_by(nickname=request.authenticated_userid).first()
#
#     if db_user:
#         request.validated['user'] = db_user
#     else:
#         request.errors.add('body', 'Invalid user', 'Authenticated userid not found in database')
#         request.errors.status = 400


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
