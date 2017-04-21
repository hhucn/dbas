========
Database
========


Init script for the database entrypoint
=======================================

D-BAS uses a initialization scripts at the beginning, which can be found in `docker/db`. Everytime Docker
starts, these scripts and sql files will be used. If you rather want an empty database at the beginning, remove the seed
and use the init script to create an empty database.

All files in `docker/db` ending on `.sh` or `.sql` will be executed in the concrete order, in which they would appear
when you type `ls` in the directory. Therefore, `001_foo` will be executed before `002_bar` or solely `baz.sql` etc.


Dump a database
===============

Current database can be saved via::

    $ docker exec dbas_db_1 pg_dumpall -U postgres > /some/path/for/saving/database.sql

To use this dump as an entrypoint, you have to remove the root user from the database with::

    $ sed -e '/CREATE ROLE postgres/d' \
          -e '/ALTER ROLE postgres/d' \
          -i /some/path/for/saving/database.sql

Steps for creating a new database
=================================

1. Remove all `*.sql`-files in `docker/db`.
2. Remove the `.bak` ending of the `001_init`-script in `docker/db`. This will create a fresh and empty database.
3. Be sure, that you deleted your old `dbas_db_1`-container.
4. Run `docker-compose up`.
5. Execute some initialization methods which are already given, like creating an englisch and german discussion as well as news::

    $ docker exec dbas_web_1 init_field_test_sql development.ini
    $ docker exec dbas_web_1 init_news_sql development.ini

6. Dump your like in the section above.
7. Undo 1. and 2. and maybe set your fresh dump as your new seed.


.. deprecated:: 1.3.1
   This comes from the good ol' times where we manually set up a database. We are now using Docker and its entrypoint
   scripts simplify the seeding process.

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
