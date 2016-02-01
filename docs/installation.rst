.. _installation:

Installation
------------
Requirements (Tested on Debian\Ubuntu,  64-Bit is mandatory):

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

    $ initialize_sql development.ini

5. Start development webserver

.. code-block:: console

    $ pserve development.ini --reload
