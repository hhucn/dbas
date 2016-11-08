"""
Provides functions

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import requests

from dbas.lib import get_profile_picture
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User


def send_request_for_info_popup_to_socketio(nickname, message='', url=None, increase_counter=False):
    """

    :param nickname:
    :param main_page:
    :param message:
    :param url:
    :param increase_counter:
    :return:
    """
    if url:
        use_https = 'dbas.cs' in url
        __send_request_for_popup_to_socketio(nickname, 'info', message, url, increase_counter, use_https)


def send_request_for_success_popup_to_socketio(nickname, message='', url=None, increase_counter=False):
    """

    :param nickname:
    :param main_page:
    :param message:
    :param url:
    :param increase_counter:
    :return:
    """
    if url:
        use_https = 'dbas.cs' in url
        __send_request_for_popup_to_socketio(nickname, 'success', message, url, increase_counter, use_https)


def send_request_for_warning_popup_to_socketio(nickname, message='', url=None, increase_counter=False):
    """

    :param nickname:
    :param message:
    :param url:
    :param increase_counter:
    :return:
    """
    __send_request_for_popup_to_socketio(nickname, 'warning', message, url, increase_counter)


def __send_request_for_popup_to_socketio(nickname, type, message='', url=None, increase_counter=False, use_https=False):
    """
    Sends an request to the socket io server

    :param type: String (success, warning, info)
    :param nickname: nickname of the user
    :param message: Some message
    :param url: URL for the event, what happened
    :param increase_counter: True, when the notification counter in D-BAS should be increased
    :param use_https: Boolean
    :return: Status code of the request
    """
    if type not in ['success', 'warning', 'info']:
        type = 'info'

    params = '?type=' + type + '&nickname=' + nickname + '&'
    if message:
        params += 'msg=' + message + '&'
    if url:
        params += 'url=' + url + '&'
    if increase_counter:
        params += 'increase_counter=True&'
    params = params[:-1]

    try:
        https = 'https' if use_https else 'http'
        resp = requests.get(https + '://localhost:5001/recent_review' + params)
    except:
        return None
    logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'status code for request ' + str(resp.status_code) + ' (msg=' + str(message) + ')')

    return resp.status_code


def send_request_for_recent_delete_review_to_socketio(nickname, main_page):
    """

    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, 'deletes', use_https)


def send_request_for_recent_edit_review_to_socketio(nickname, main_page):
    """

    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, 'edits', use_https)


def send_request_for_recent_optimization_review_to_socketio(nickname, main_page):
    """

    :param nickname:
    :param main_page:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, 'optimizations', use_https)


def __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, queue, use_https):
    """

    :param reviewer_name:
    :param reviewer_image_url:
    :param queue
    :param use_https
    :return: Status code of the request
    """
    params = '?reviewer_name=' + reviewer_name + '&img_url=' + reviewer_image_url + '&queue=' + queue

    try:
        if use_https:
            link = 'https://dbas.cs.uni-duesseldorf.de:5001/'
        else:
            link = 'http://localhost:5001/'
        resp = requests.get(link + 'recent_review' + params)
    except Exception as e:
        logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'Error: ' + str(e), error=True)
        return None
    logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'status code for request ' + str(resp.status_code))

    return resp.status_code
