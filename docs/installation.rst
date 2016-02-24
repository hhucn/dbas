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

1. Create virtualenv with python3

.. code-block:: console

    $ mkvirtualenv --python=$(which python3) dbas

2. Install all requirements

.. code-block:: console

    $ pip install -r requirements.txt

3. Develop application

.. code-block:: console

    $ python setup.py develop

4. Create database

.. code-block:: console

    $ initialize_news_sql development.ini
    $ initialize_discussion_sql development.ini
    $ initialize_api_sql development.ini

5. Start development webserver

.. code-block:: console

    $ pserve development.ini --reload
