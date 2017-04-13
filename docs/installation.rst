.. _installation:

============
Installation
============

The preferred way to install D-BAS is via Docker. You can find some installation
instructions `on this site <docker/index.html>`_.


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

This mode uses the pre-built images from our registry server and uses "uwsgi".


Environment Variables
=====================
You may want to configure options as environment variables instead of config entries.

D-BAS
-----
You can configure all entries in the ``app:main`` section of the ini-file in environment variables.
By default D-BAS takes all environment variables with prefix ``DBAS_`` and adds them to the configuration, after parsing the .ini file itself.
The name of the environment variable will be the key of the new configuration entry, after some transformations.

1. The prefix will be stripped.
2. All single underscores will be substituted with a dot.
3. All double underscores will be substituted with a single underscore.
4. uppercase will be lowered.

Example::

    export DBAS_FOO_BAR__BAZ=fizz
    => foo.bar_baz = fizz


Special Variables
-----------------

There are some special variables for the database connection.
These **have** to be set, otherwise an error will be raised explaning which variables aren't configured.

+--------------+------------------------------------------------------------------+
| DBAS_DB_HOST | The hostname of the database (example: localhost, db, 10.0.0.2). |
+--------------+------------------------------------------------------------------+
| DBAS_DB_PORT | The port of the database (example: 5432).                        |
+--------------+------------------------------------------------------------------+
| DBAS_DB_USER | The database username. (example: dbas)                           |
+--------------+------------------------------------------------------------------+
| DBAS_DB_PW   | The passwort of the DBAS_DB_USER (example: passw0rt123)          |
+--------------+------------------------------------------------------------------+

These variables are accessible like any other via the normal substitutions (DB.HOST, ...)


Pyramid & UWSGI
---------------
For pyramid and UWSGI specific options you may want to consult the official docs.

:pyramid: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html
:uwsgi: http://uwsgi-docs.readthedocs.io/en/latest/Configuration.html#environment-variables


Makefile
========
List of all important commands of our Makefile.

* make clean
    Drop it all!

* make all
    Creates a new database with and root and read-only user as well as dummy discussions and news.


Tests
=====

* Unit, integration and view tests::

    nosetests3

* PEP 8 and Co.::

    jshint ./dbas/static/js/{main,ajax,discussion,review}/*.js
    flake8


Manual Installation
===================

.. note::

   No longer maintained. We are now using Docker. Check the Dockerfiles if
   you want to install it directly on your machine.

Ensure that the following tools are installed:

* Python >= 3.4
* `pip <https://pip.pypa.io/en/stable/installing/>`_
* `virtualenv <http://virtualenv.readthedocs.org/en/latest/installation.html>`_
* `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/install.html>`_
* PostgreSQL and libpq-dev

Then follow these steps:

1. Create virtualenv with python3::

    $ mkvirtualenv "--python=$(which python3)" dbas

2. Install PostgreSQL and configure it::

    $ apt-get install libpq-dev python-dev postgresql

3. Install all requirements::

    $ pip install -r requirements.txt

4. Develop application::

    $ python setup.py develop

5. Create database::

    $ make init
    $ make all

6. Deploy Sass::

    $ sass static/css/main.sass  static/css/main.css --style compressed --no-cache

7. Start development web server::

    $ pserve development.ini --reload

8. If you are running Mac OS X, please install portmap *https://codingmonkeys.de/portmap/*


Mac OS specifc installation problems
====================================

psycopg2 install fails with ``library not found for -lssl with on install``
---------------------------------------------------------------------------

    $ env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
