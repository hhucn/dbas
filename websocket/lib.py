"""
Provides functions

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import time

import urllib.request

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User
from dbas.lib import get_profile_picture, get_global_url
from dbas.logger import logger

fallback_port = 5222


def send_request_for_info_popup_to_socketio(nickname, port, message='', url=None, increase_counter=False):
    """
    Sends request to the socketio server for an info popup

    :param nickname: Current users nickname
    :param port: Port of the notification server
    :param message: String
    :param url: Issue.uid
    :param increase_counter: Boolean
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main')
    if url:
        use_https = 'localhost' not in url
        __send_request_for_popup_to_socketio(nickname, port, 'info', message, url, increase_counter, use_https)


def send_request_for_info_popup_to_socketio_with_delay(nickname, port, message='', url=None, increase_counter=False,
                                                       delay=5):
    """
    Sends request to the socketio server for an info popup with a specific delay

    :param nickname: Current users nickname
    :param port: Port of the notification server
    :param message: String
    :param url: String
    :param increase_counter: Boolean
    :param delay: int
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main sleeping for ' + str(delay))
    time.sleep(delay)
    logger('Websocket.lib', 'enough sleep')
    if url:
        use_https = 'localhost' not in url
        __send_request_for_popup_to_socketio(nickname, port, 'info', message, url, increase_counter, use_https)


def send_request_for_success_popup_to_socketio(nickname, port, message='', url=None, increase_counter=False):
    """
    Sends request to the socketio server for a success popup

    :param nickname: Current users nickname
    :param port: Port of the notification server
    :param message: String
    :param url: String
    :param increase_counter:
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main')
    if url:
        use_https = 'localhost' not in url
        __send_request_for_popup_to_socketio(nickname, port, 'success', message, url, increase_counter, use_https)


def send_request_for_warning_popup_to_socketio(nickname, port, message='', url=None, increase_counter=False):
    """
    Sends request to the socketio server for a warning popup

    :param nickname: Current users nickname
    :param port: Port of the notification server
    :param message: String
    :param url: String
    :param increase_counter:
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main')
    __send_request_for_popup_to_socketio(nickname, port, 'warning', message, url, increase_counter)


def __send_request_for_popup_to_socketio(nickname, port, popup_type, message='', url=None, increase_counter=False,
                                         use_https=False):
    """
    Sends an request to the socket io server

    :param popup_type: String (success, warning, info)
    :param nickname: nickname of the user
    :param port: Port of the notification server
    :param message: Some message
    :param url: URL for the event, what happened
    :param increase_counter: True, when the notification counter in D-BAS should be increased
    :param use_https: Boolean
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main')

    if popup_type not in ['success', 'warning', 'info']:
        popup_type = 'info'

    params = '?type={}&nickname={}&'.format(popup_type, nickname)
    if message:
        params += 'msg={}&'.format(message)
    if url:
        params += 'url={}&'.format(url)
    if increase_counter:
        params += 'increase_counter=True&'
    params = params[:-1]

    if not port:
        port = fallback_port

    if use_https:
        link = '{}:{}/'.format(get_global_url(), port)
    else:
        link = 'http://localhost:{}/'.format(port)
    rurl = '{}publish{}'.format(link, params)

    return __open_url(rurl)


def send_request_for_recent_reviewer_socketio(nickname, main_page, port, queue):
    """
    Sends request to the socketio server for updating the last reviewer view

    :param nickname: Current users nickname
    :param main_page: URL of the app itself
    :param port: Port of the notification server
    :param queue: Key of the last reviewers queue
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main - nickname {} for queue {}'.format(nickname, queue))
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    reviewer_name = db_user.get_global_nickname()
    reviewer_image_url = get_profile_picture(db_user)
    use_https = 'dbas' in main_page
    return __send_request_for_recent_review_to_socketio(port, reviewer_name, reviewer_image_url, queue, use_https)


def __send_request_for_recent_review_to_socketio(port, reviewer_name, reviewer_image_url, queue, use_https):
    """
    Sends request to the socketio server for updating the last reviewer view

    :param port: Port of the notification server
    :param reviewer_name: User.nickname
    :param reviewer_image_url: String
    :param queue: String
    :param use_https: Boolean
    :return: Status code of the request
    """
    logger('Websocket.lib', 'main')
    params = '?reviewer_name=' + reviewer_name + '&img_url=' + reviewer_image_url + '&queue=' + queue

    if not port:
        port = fallback_port

    if use_https:
        link = '{}:{}/'.format(get_global_url(), port)
    else:
        link = 'http://localhost:{}/'.format(port)
    rurl = '{}recent_review{}'.format(link, params)

    return __open_url(rurl)


def __open_url(url):
    """
    Calls url via urllib and returns status code on success or none on error

    :param url: String
    :return: None or HTTP status code
    """
    try:
        resp = urllib.request.urlopen(url)
        logger('Websocket.lib', 'Content of request {}'.format(resp.read()))
    except Exception as e:
        logger('Websocket.lib', 'Error {} by calling {}'.format(e, url), error=True)
        return None
    logger('Websocket.lib', 'Status code of request {}'.format(resp.getcode()))
    return resp.getcode()


def get_port(request):
    """
    Lets have a look into the settings if there is a websocket port, otherwise 5222 will be returned

    :param request: pyramid's request object
    :return: int
    """
    return request.registry.settings.get('settings:services:websocket_port', fallback_port)
