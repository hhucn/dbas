.. _installation:

============
Installation
============

*This is the classical way to install D-BAS on your local machine. If you want to use docker,
see* `docker installation instructions <docker/index.html>`_.


Requirements for development
============================

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


Mac OS specifc problems you may encounter
=========================================
psycopg2 fails 'library not found for -lssl with on install
-----------------------------------------------------------

    $ env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2

