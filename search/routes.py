import socket
from contextlib import closing

from search import ROUTE_API


def get_statements_with_value_path(issue_uid: int, search_value: str = '') -> str:
    """
    Create the query string to get statements matching a certain string.
    This method contains all parameters used in search(service).

    :param issue_uid: uid of the issue to search in
    :param search_value: text to be searched for
    :return: query satisfied the requirements of search(service) to get statements fitting search_value
    """
    suffix = '/statements?id={}&search={}'.format(issue_uid, search_value)
    return ROUTE_API + suffix


def get_duplicates_or_reasons_path(issue_uid: int, statement_uid: int, search_value: str = '') -> str:
    """
    Create the query string to get duplicates or reasons matching a certain string.
    This method contains all parameters used in search(service).

    :param issue_uid: uid of the issue to search in
    :param statement_uid: uid of the statement which is supposed to be a duplicate or reason
    :param search_value: text to be searched for
    :return: query satisfied the requirements of search(service) to get duplicates or reasons fitting search_value
    """
    suffix = '/duplicates_reasons?id={}&statement_uid={}&search={}'.format(issue_uid, statement_uid, search_value)
    return ROUTE_API + suffix


def get_edits_path(issue_uid: int, statement_uid: int, search_value: str = '') -> str:
    """
    Create the query string to get edits matching a certain string to a given statement uid.
    This method contains all parameters used in search(service).

    :param issue_uid: uid of the issue to search in
    :param statement_uid: uid of the statement which had some edits
    :param search_value: text to be searched for
    :return: query satisfied the requirements of search(service) to get edits fitting search_value
    """
    suffix = '/edits?id={}&statement_uid={}&search={}'.format(issue_uid, statement_uid, search_value)
    return ROUTE_API + suffix


def get_suggestions_path(issue_uid: int, position: bool, search_value: str = '') -> str:
    """
    Create the query string to get suggestions matching a certain string of a given issue.
    This method contains all parameters used in search(service).

    :param issue_uid: uid of the issue to search in
    :param position: position of the statement
    :param search_value: text to be searched for
    :return: query satisfied the requirements of search(service) to get suggestions fitting search_value
    """
    suffix = '/suggestions?id={}&position={}&search={}'.format(issue_uid, position, search_value)
    return ROUTE_API + suffix


def get_statements_path(value: str):
    """
    This is the route to query all similar statements in the search index of version 2.

    :param value: The string to be searched for
    :return: The regarding path which is required by search
    """

    suffix = '/v2/statement?q={}'.format(value)
    return ROUTE_API + suffix


def is_socket_open(host, port):
    """
    This function checks whether the port of an existing host is open and addressable.

    :param host: The existing host whose port is to be checked.
    :param port: The port to be checked.
    :return: True, if the port is open, otherwise False
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def is_host_resolved(hostname):
    """
    This function checks whether a host exists and is occupied.

    :param hostname: The host to search for.
    :return: True, if the host exists, otherwise False
    """

    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        return False
