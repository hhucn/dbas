========
Makefile
========

* make databases
    Remove old databases and initialize new ones

* make init_postgres
    Creates a user for postgres as well as both databases (discussion and news).

* make init_postgres
    Will drop both databases, create them, assign them to the owsner and fills them with data.

* make reload_postgres:
    Just drops all data, but keeps Users, Settings and Notifications. Afterwards default data will be set.

* make clean_postgres:
    Drop it all!

* make clean
    Drops all SQLite databases.