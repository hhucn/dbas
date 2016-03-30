.. _installation:

============
Installation
============

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

2. Install all requirements::

    $ pip install -r requirements.txt

3. Develop application::

    $ python setup.py develop

4. Install PostgreSQL and configure it::

    $ apt-get install libpq-dev python-dev postgresql
    $ pip install db-psycopg2

6. Create user and tables::

    $ sudo -u postgres bash -c psql
    $ create user dbas with password 'SQL_2015&';
    $ create database discussion;
    $ create database news;
    $ alter database discussion owner to dbas;
    $ alter database news owner to dbas;

  Alternatively, you can use our Makefile from the project's root directory to initialize the database::

    $ make init_postgres
    $ make postgres

7. Create database::

    $ initialize_news_sql development.ini
    $ initialize_discussion_sql development.ini

  Alternatively, you can use our Makefile from the project's root directory to initialize the database::

    $ make databases

8. Start development web server::

    $ pserve development.ini --reload

9. If you are running Mac OS X, please install portmap *https://codingmonkeys.de/portmap/*


Makefile
========
List of all commands of our makefile.

* make init_postgres
    Creates a user for postgres as well as both databases (discussion and news).

* make init_postgres
    Will drop both databases, create them, assign them to the owner and fills them with data.

* make reload_postgres:
    Just drops all data, but keeps Users, Settings and Notifications. Afterwards default data will be set.

* make clean_postgres:
    Drop it all!


.. deprecated:: 0.5.8
    Previously used for sqlite. Will be remove in the near future.

* make databases
    Remove old databases and initialize new ones

* make clean
    Drops all SQLite databases.