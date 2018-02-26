import os

SEARCH_PROTOCOL = os.environ.get('SEARCH_PROTOCOL')
SEARCH_HOST = os.environ.get('SEARCH_NAME')
SEARCH_PORT = os.environ.get('SEARCH_PORT', 5000)
ROUTE_API = '{}://{}:{}'.format(SEARCH_PROTOCOL, SEARCH_HOST, SEARCH_PORT)
