"""
Provides functions

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import requests

from dbas.logger import logger


def send_request_to_socketio(type, nickname, message=None, url=None):
    """
    Sends an request to the socket io server

    :param type: String (success, warning, info, notifications, mention, edittext)
    :param nickname: User.nickname
    :param message: String
    :param url: String
    :return: Status code of the request
    """
    params = '?type=' + type + '&nickname=' + nickname + '&'
    if message:
        params += 'msg=' + message + '&'
    if url:
        params += 'url=' + url + '&'

    resp = requests.get('http://localhost:5001/publish' + params[:-1])
    logger('Websocket.lib', 'send_edit_text_notification', 'status code for request ' + str(resp.status_code) + ' (msg=' + str(message) + ')')

    return resp.status_code
