from dbas.handler.user import update_last_action
from dbas.views import user_logout


def check_authentication(view_callable):
    """
    The entry routine performed by a bulk of functions.
    Checks whether the user is authenticated and if not logs user out.

    This function is not pure!

    :param view_callable:
    :return:
    """
    def inner(context, request):
        session_expired = update_last_action(request.authenticated_userid)
        if session_expired:
            return user_logout(request, True)
        else:
            return view_callable(context, request)
    return inner
