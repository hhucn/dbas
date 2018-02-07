import json
from pyramid.response import Response


def http_exception(path: str, status_code=404, message='Not Found') -> Response:
    """
    Returns 4xx-Reponse with requested_path and message in its body

    :param path: current request.path
    :param status_code: current http status code, default is 404
    :param message: current error message, default is 'Not Found'
    :return: Response with 404 status code
    """
    body = {
        'requested_path': path,
        'message': message,
    }
    response = Response(json.dumps(body).encode("utf-8"))
    response.status_int = status_code
    response.content_type = 'application/json'
    return response
