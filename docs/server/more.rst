====
More
====

Session Management
==================
Redis is used as backend for beaker management, therefore every tempate is cached.

WebSockets
==========
Information about websockets with nginx http://nginx.org/en/docs/http/websocket.html
Socket.io http://socket.io/

Deployment
==========
- http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/deployment/nginx.html
- Grep for *dbas.cs* in code and replace it with the real address / currently it is hardcoded :\

- The short story: http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/deployment/gunicorn.html
- Then ''gunicorn --paste production.ini --daemon''

- Got problems with UTF8 and debian? https://wiki.debian.org/ChangeLanguage