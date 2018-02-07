import json
from pyramid.response import Response


def bad_request(path, message):
    """
    Returns 400-Reponse with requested_path and message in its body

    :param path: current request.path
    :param message: current error message
    :return: Response with 400 status code
    """
    body = {
        'requested_path': path,
        'message': message,
    }
    response = Response(json.dumps(body).encode('utf-8'))
    response.status_int = 400
    response.content_type = 'application/json'
    return response
