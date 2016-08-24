import dbas.helper.history as HistoryHelper
import dbas.user_management as UserHandler
import transaction


def get_nickname_and_session(request, for_api=None, api_data=None):
    """
    Given data from api, return nickname and session_id.

    :param for_api:
    :param api_data:
    :return:
    """
    nickname = api_data["nickname"] if api_data and for_api else request.authenticated_userid
    session_id = api_data["session_id"] if api_data and for_api else request.session.id
    return nickname, session_id


def preperation_for_view(for_api, api_data, request):
    """
    Does some elementary things like: getting nickname, sessioniod and history. Additionally boolean, if the sesseion is expired

    :param for_api: True, if the values are for the api
    :param api_data: Array with api data
    :param request: Current request
    :return: nickname, session_id, session_expired, history
    """
    nickname, session_id = get_nickname_and_session(request, for_api, api_data)
    session_expired = UserHandler.update_last_action(transaction, nickname)
    history         = request.params['history'] if 'history' in request.params else ''
    HistoryHelper.save_path_in_database(nickname, request.path, transaction)
    HistoryHelper.save_history_in_cookie(request, request.path, history)
    return nickname, session_id, session_expired, history
