"""
Provides functions

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import requests

from dbas.logger import logger


def send_request_for_popup_to_socketio(nickname, type, message='', url=None, increase_counter=False):
    """
    Sends an request to the socket io server

    :param type: String (success, warning, info)
    :param nickname: nickname of the user
    :param message: Some message
    :param url: URL for the event, what happened
    :param increase_counter: True, when the notification counter in D-BAS should be increased
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
        resp = requests.get('http://localhost:5001/publish' + params)
    except:
        return None
    logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'status code for request ' + str(resp.status_code) + ' (msg=' + str(message) + ')')

    return resp.status_code


def send_request_for_recent_review_to_socketio(reviewer_name, reviewer_image_url, queue):
    """
    NOT IMPLEMENTED IN SOCKET IO

    :param reviewer_name:
    :param reviewer_image_url:
    :param queue
    :return: Status code of the request
    """
    params = '?reviewer_name=' + reviewer_name + '&img_url=' + reviewer_image_url + '&queue=' + queue

    try:
        resp = requests.get('http://localhost:5001/recent_review' + params)
    except:
        return None
    logger('Websocket.lib', 'send_request_for_popup_to_socketio', 'status code for request ' + str(resp.status_code))

    return resp.status_code
