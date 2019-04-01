.. _installation:

============
Installation
============

The preferred way to install D-BAS is via Docker. You can find some installation
instructions `on the Dockers index site <docker/index.html>`_.


The Docker Way
==============

Currently, there are two docker-compose definitions which can be used to deploy
D-BAS. Both rely on our registry server, which means, that you need to have
access to our registry server as long as this is hosted in our institute.

Development Mode
----------------

To start D-BAS with interactive development mode (the webserver sees your
changes and automatically restarts itself to show the changes in the browser),
use the default compose file::

    $ docker-compose up

Production Mode
---------------

Use a different compose file::

    $ docker-compose -f docker-compose.production.yml up

This mode uses the pre-built images from our registry server and uses "uwsgi" as webserver.

Troubleshooting
---------------

If your access is denied, please try::

    $ docker login gitlab.cs.uni-duesseldorf.de:5001

Or take a look at dbas > Registry for the newest information (Port *5001* may not be up to date).

If your container stucks during the first start up, please install D-BAS manually via::

    $ docker-compose exec web ./build_assets.sh

Afterwards everything should be fine.


Environment Variables
=====================
You may want to configure options as environment variables instead of config entries.
The core variables are stored in `.env` to make sure D-BAS is completely up with `docker-compose up`.

D-BAS
-----
D-BAS needs some environment variables to start und run properly.
For the production mode the core variables have to be overwritten.
Those variables **have** to be set, otherwise an error will be raised explaining which variables aren't configured.
The core variables which are stored in `.env` are:

+--------------+------------------------------------------------------------------------+
| AUTHN_SECRET | The authentication secret of the database user. (example ABCDEF!2D)    |
+--------------+------------------------------------------------------------------------+
| DB_HOST      | The hostname of the database. (example: localhost, db, 10.0.0.2)       |
+--------------+------------------------------------------------------------------------+
| DB_PORT      | The port of the database. (example: 5432)                              |
+--------------+------------------------------------------------------------------------+
| DB_USER      | The database username. (example: dbas)                                 |
+--------------+------------------------------------------------------------------------+
| DB_PW        | The passwort of the DB_USER. (example: passw0rt123)                    |
+--------------+------------------------------------------------------------------------+
| URL          | The global url of D-BAS. (example: https://dbas.cs.uni-duesseldorf.de )|
+--------------+------------------------------------------------------------------------+
| KEY_PATH     | The path to the private key of your ES256 key pair. (For JWT)          |
+--------------+------------------------------------------------------------------------+
| PUBKEY_PATH  | The path to the public key of your ES256 key pair.                     |
+--------------+------------------------------------------------------------------------+

Special Variables
-----------------

There is the opportunity to modify special variables if you need them.
By creating a `development.env` or `production.env` file and adding them to the specific `docker-compose` file with::

    env_file:
      - development.env

Those variables can be set in `development.env` or `production.env`.
Notice: Existing environment-variables which are defined in `.env` can be overwritten if they are set in `development.env` or `production.env`.
You can add those variables if you want to start services like the sematic-search in `docker-compose.search.yml`.

Those special variables are defined as bellow.

+----------------------------+------------------------------------------------------------------------+
| MAIL_HOST                  | The hist of the imap account                                           |
+----------------------------+------------------------------------------------------------------------+
| MAIL_PORT                  | The port of the mail host                                              |
+----------------------------+------------------------------------------------------------------------+
| MAIL_USERNAME              | The username of the imap account                                       |
+----------------------------+------------------------------------------------------------------------+
| MAIL_PASSWORD              | The password if the imap account                                       |
+----------------------------+------------------------------------------------------------------------+
| MAIL_SSL                   | A boolean to enable or disable ssl for mail traffic                    |
+----------------------------+------------------------------------------------------------------------+
| MAIL_TLS                   | A boolean to enable or disable tls for mail traffic                    |
+----------------------------+------------------------------------------------------------------------+
| MAIL_DEFAULT__SENDER       | The total mail address                                                 |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_SERVER            | LDAPs server address (Notice: Must be in single quotes                 |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_BASE              | LDAPs base address (Notice: Must be in single quotes)                  |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_ACCOUNT_SCOPE     | Scope of the LDAP search (Notice: Must be in single quotes)            |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_ACCOUNT_FILTER    | Filter of the LDAP search (Notice: Must be in single quotes)           |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_ACCOUNT_FIRSTNAME | Key of the LDAP firstname (Notice: Must be in single quotes)           |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_ACCOUNT_LAST      | Key of the LDAP lastname (Notice: Must be in single quotes)            |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_ACCOUNT_TITLE     | Key of the LDAP title (Notice: Must be in single quotes)               |
+----------------------------+------------------------------------------------------------------------+
| HHU_LDAP_ACCOUNT_EMAIL     | Key of the LDAP title (Notice: Must be in single quotes)               |
+----------------------------+------------------------------------------------------------------------+
| OAUTH_GOOGLE_CLIENTID      | ID for o auth with GOOGLE                                              |
+----------------------------+------------------------------------------------------------------------+
| OAUTH_GOOGLE_CLIENTKEY     | Key for o auth with GOOGLE                                             |
+----------------------------+------------------------------------------------------------------------+
| OAUTH_GITHUB_CLIENTID      | ID for o auth with GitHub                                              |
+----------------------------+------------------------------------------------------------------------+
| OAUTH_GITHUB_CLIENTKEY     | Key for o auth with GitHub                                             |
+----------------------------+------------------------------------------------------------------------+
| OAUTH_FACEBOOK_CLIENTID    | ID for o auth with Facebook                                            |
+----------------------------+------------------------------------------------------------------------+
| OAUTH_FACEBOOK_CLIENTKEY   | Key for o auth with Facebook                                           |
+----------------------------+------------------------------------------------------------------------+
| DBAS_HOST                  | Name of the dbas container which needs the semantic-search             |
+----------------------------+------------------------------------------------------------------------+
| DBAS_PORT                  | Port of the dbas container which needs the semantic-search             |
+----------------------------+------------------------------------------------------------------------+
| DBAS_PROTOCOL              | The Protocol which is used by the running dbas container (e.g. http)   |
+----------------------------+------------------------------------------------------------------------+
| SEARCH_PROTOCOL            | The Protocol which is used by the running search container (e.g. http) |
+----------------------------+------------------------------------------------------------------------+
| SEARCH_PORT                | Port of the container which returns the search results, default 5000   |
+----------------------------+------------------------------------------------------------------------+
| SEARCH_NAME                | Name of the container which returns the search results, default search |
+----------------------------+------------------------------------------------------------------------+
| WEBSOCKET_PORT             | Port of the node.js server                                             |
+----------------------------+------------------------------------------------------------------------+
| MIN_LENGTH_OF_STATEMENT    | The minimal length of any statement, default 10                        |
+----------------------------+------------------------------------------------------------------------+

Generate keys for the API
-------------------------
You have to generate an ec256 keypair for the generation of user api tokens.

For example::

    openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
    openssl ec -in private-key.pem -pubout -out public-key.pem

You have to provide a path to them in `KEY_PATH` and `PUBKEY_PATH`.

Add user as admin
-----------------

A CLI function is offered to promote a user to an admin (or demote him)
Usage::

    promote_to_admin <nickname>
    demote_to_user <nickname>

If you are in a docker environment, don't forget to call this command inside the
containers::

    docker-compose exec web promote_to_admin <nickname>

You can find your username in the settings.

OAuth
-----

D-BAS offers the possibility to use the open authentication protocol implemented by Google, Facebook,
Github and Twitter. Please add the variables `OAUTH_service_CLIENTID` and `OAUTH_service_CLIENTKEY`
for each service you want to use, where you have to replace **service** with e.g. GOOGLE (important: uppercase).

The login buttons will be displayed automatically. For more information, have a look `on D-BAS' OAuth site <dbas/oauth.html>`_.


Pyramid & UWSGI
---------------
For pyramid and UWSGI specific options you may want to consult the official docs.

:pyramid: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html
:uwsgi: http://uwsgi-docs.readthedocs.io/en/latest/Configuration.html#environment-variables


Tests
=====

The development of D-BAS is test-driven and every method should be tested. We are using unittests, view tests as well
as frontend tests. You can call them via::

    nosetests3

This will run the files in `tests/` and the tests of every module like `dbas/tests`, `api/tests` etc. In addition we
are checking the syntax of the python and javascript code with::

    jshint ./dbas/static/js/{main,ajax,discussion,review,d3}/*.js
    flake8

To execute tests using a running D-BAS docker container, use one of the following commands::

    # run all tests
    docker-compose exec web nosetests
    # run all tests, verbose mode (prints names of executed tests)
    docker-compose exec web nosetests -v
    # execute only specific tests
    docker-compose exec web nosetests -v dbas.review.queue.tests.test_lib

.. note::
   Some tests have side effects, rely on the side effects of previous tests, or require a clean environment (if you are
   using docker, do a ``docker-compose down && docker-compose up`` to get a clean environment).


Debugger
========

You can use PyCharm’s remote debugging feature to debug D-BAS running in a docker container or debugging unit tests.

To set up remote debugging, follow these steps:
  1. Install pydev inside your D-BAS docker container:
     ::

      docker-compose exec web pip install pydevd

  2. Add `pydevd` to your `requirements.txt`.
  3. In PyCharm, create a "Python Remote Debug" configuration for `localhost:4444`.
  4. Add the following code snippet in the end of `dbas/__init__.py`
     ::

      # NEVER COMMIT THIS
      # based upon http://blog.digital-horror.com/how-to-setup-pycharms-remote-debugger-for-docker/
      import pydevd

      try:
          pydevd.settrace('YOUR_IP', port=4444, stdoutToServer=True, stderrToServer=True)
      except Exception as e:
          print(e)

Don't forget to replace `YOUR_IP` with an ip of your development machine reachable from within the container, e.g.
196.168.2.42.

.. note::
   If no remote debugger is running, D-BAS still works, but a `ConnectionRefusedError` is printed after few seconds.

To debug a D-BAS instance:
  1. Start the remote debugger configuration.
  2. Restart the D-BAS instance (either manually with `docker-compose up`, or by changing the code, which restarts D-BAS automatically).
  3. PyCharm breaks the program when the debugger is connected. Click Continue.
  4. Debug as usual.

To debug unit tests:
  1. If the remote debugger is already running, make sure that the running D-BAS instance is not connected to it (if it is, restart the debugger, which disconnects the connected instance and will wait for a new connection).
  2. Start the remote debugger if it is not running.
  3. Start the unit tests.
  4. PyCharm breaks the program when the debugger is connected. Click Continue.
  5. Debug as usual.

.. note::
   If you start the unit tests while the remote debugger is already connected, the unit tests hang because they cannot
   connect to the debugger.
