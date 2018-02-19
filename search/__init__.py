import os

PROTOCOL = os.environ['PROTOCOL']
SEARCH_HOST = os.environ['SEARCH_NAME']
SEARCH_PORT = 5000
ROUTE_API = '{}://{}:{}'.format(PROTOCOL, SEARCH_HOST, SEARCH_PORT)
