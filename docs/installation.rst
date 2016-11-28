.. _installation:

============
Installation
============

*This is the classical way to install D-BAS on your local machine. If you want to use docker,
see* `docker installation instructions <docker/index.html>`_.


Requirements
============

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
List of all commands of our Makefile.

* make init
    Creates a user for postgres as well as both databases (discussion and news).

* make database
    Will drop both databases, create them, assign them to the owner and fills them with data.

* make refresh
    Just drops all data, but keeps Users, Settings and Notifications. Afterwards default data will be set.

* make clean
    Drop it all!


Mac OS specifc problems you may encounter
=========================================
psycopg2 fails 'library not found for -lssl with on install
-----------------------------------------------------------

    $ env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2

