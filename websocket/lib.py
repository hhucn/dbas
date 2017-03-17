"""
Provides functions

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import time

import requests

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.lib import get_profile_picture, get_global_url
from dbas.logger import logger

port = 5222


def send_request_for_info_popup_to_socketio(nickname, message='', url=None, increase_counter=False):
    """
    Sends request to the socketio server for an info popup

    :param nickname: User.nickname
    :param message: String
    :param url: Issue.uid
    :param increase_counter:
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_info_popup_to_socketio', 'main')
    if url:
        use_https = 'dbas.cs' in url
        __send_request_for_popup_to_socketio(nickname, 'info', message, url, increase_counter, use_https)


def send_request_for_info_popup_to_socketio_with_delay(nickname, message='', url=None, increase_counter=False, delay=5):
    """
    Sends request to the socketio server for an info popup with a specific delay

    :param nickname: User.nickname
    :param message: String
    :param url: String
    :param increase_counter: Boolean
    :param delay: int
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_info_popup_to_socketio_with_delay', 'main sleeping for ' + str(delay))
    time.sleep(delay)
    logger('Websocket.lib', 'send_request_for_info_popup_to_socketio_with_delay', 'enough sleep')
    if url:
        use_https = 'dbas.cs' in url
        __send_request_for_popup_to_socketio(nickname, 'info', message, url, increase_counter, use_https)


def send_request_for_success_popup_to_socketio(nickname, message='', url=None, increase_counter=False):
    """
    Sends request to the socketio server for a success popup

    :param nickname: User.nickname
    :param message: String
    :param url: String
    :param increase_counter:
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_success_popup_to_socketio', 'main')
    if url:
        use_https = 'dbas.cs' in url
        __send_request_for_popup_to_socketio(nickname, 'success', message, url, increase_counter, use_https)


def send_request_for_warning_popup_to_socketio(nickname, message='', url=None, increase_counter=False):
    """
    Sends request to the socketio server for a warning popup

    :param nickname: User.nickname
    :param message: String
    :param url: String
    :param increase_counter:
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_warning_popup_to_socketio', 'main')
    __send_request_for_popup_to_socketio(nickname, 'warning', message, url, increase_counter)


def __send_request_for_popup_to_socketio(nickname, popup_type, message='', url=None, increase_counter=False, use_https=False):
    """
    Sends an request to the socket io server

    :param popup_type: String (success, warning, info)
    :param nickname: nickname of the user
    :param message: Some message
    :param url: URL for the event, what happened
    :param increase_counter: True, when the notification counter in D-BAS should be increased
    :param use_https: Boolean
    :return: Status code of the request
    """
    logger('Websocket.lib', '__send_request_for_popup_to_socketio', 'main')
    if popup_type not in ['success', 'warning', 'info']:
        popup_type = 'info'

    params = '?type=' + popup_type + '&nickname=' + nickname + '&'
    if message:
        params += 'msg=' + message + '&'
    if url:
        params += 'url=' + url + '&'
    if increase_counter:
        params += 'increase_counter=True&'
    params = params[:-1]

    try:
        https = 'https' if use_https else 'http'
        resp = requests.get(https + '://localhost:' + str(port) + '/publish' + params)
    except:
        return None
    logger('Websocket.lib', '__send_request_for_popup_to_socketio', 'status code for request ' + str(resp.status_code) + ' (msg=' + str(message) + ')')

    return resp.status_code


def send_request_for_recent_delete_review_to_socketio(nickname, main_page):
    """
    Sends request to the socketio server for updating the last reviewer view

    :param nickname: User.nickname
    :param main_page: String
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_recent_delete_review_to_socketio', 'main - nickname ' + str(nickname))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname()
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, 'deletes', use_https)


def send_request_for_recent_edit_review_to_socketio(nickname, main_page):
    """
    Sends request to the socketio server for updating the last reviewer view

    :param nickname: User.nickname
    :param main_page: String
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_recent_edit_review_to_socketio', 'main - nickname ' + str(nickname))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname()
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, 'edits', use_https)


def send_request_for_recent_optimization_review_to_socketio(nickname, main_page):
    """
    Sends request to the socketio server for updating the last reviewer view

    :param nickname: User.nickname
    :param main_page: String
    :return: Status code of the request
    """
    logger('Websocket.lib', 'send_request_for_recent_optimization_review_to_socketio', 'main - nickname ' + str(nickname))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname()
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, 'optimizations', use_https)


def __send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, queue, use_https):
    """
    Sends request to the socketio server for updating the last reviewer view

    :param reviewer_name: User.nickname
    :param reviewer_image_url: String
    :param queue: String
    :param use_https: Boolean
    :return: Status code of the request
    """
    logger('Websocket.lib', '__send_request_for_recent_review_to_socketio', 'main')
    params = '?reviewer_name=' + reviewer_name + '&img_url=' + reviewer_image_url + '&queue=' + queue

    try:
        if use_https:
            link = get_global_url() + ':' + str(port) + '/'
        else:
            link = 'http://localhost:' + str(port) + '/'
        resp = requests.get(link + 'recent_review' + params)
    except Exception as e:
        logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'Error: ' + str(e), error=True)
        return None
    logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'status code for request ' + str(resp.status_code))

    return resp.status_code
