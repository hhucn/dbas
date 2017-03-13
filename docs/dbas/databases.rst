========
Database
========

More information about handling of the database can be find in the Docker's entrypoint_.

Steps for creating a new database
=================================

1. Add a console script under console_scripts in setup.py.
2. Specify path for the database in development.ini and production.ini.
3. Load database in dbas/__init__.py.
4. Add session, engine and methods in dbas/database/__init__.py.
5. Define a new model <new_model>.py in dbas/database/.
6. Define a function for creation in dbas/database/initializedb.py. Name of the method is the same as in the console script
7. Optional: add dummy data in dbas/database/initializedb.py.
8. Call

.. code-block:: console

    $ python setup.py develop
    $ <console_script_name> development.ini


Description
===========

.. automodule:: dbas.database
    :members:


Discussion Model
================

.. automodule:: dbas.database.discussion_model
    :members:


News Model
==========

.. automodule:: dbas.database.news_model
    :members:

Initialize Dummy DB
===================

.. automodule:: dbas.database.initializedb
    :members:
