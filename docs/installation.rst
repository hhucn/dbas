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

Then follow these steps:

1. Create virtualenv with python3::

    $ mkvirtualenv "--python=$(which python3)" dbas

2. Install all requirements::

    $ pip install -r requirements.txt

3. Develop application::

    $ python setup.py develop

4. Create database::

    $ initialize_news_sql development.ini
    $ initialize_discussion_sql development.ini
    $ initialize_api_sql development.ini

  Alternatively, you can use our Makefile from the project's root directory to initialize the database::

    $ make databases

5. Start development web server::

    $ pserve development.ini --reload

6. If you are running Mac OS X, please install portmap *https://codingmonkeys.de/portmap/*
