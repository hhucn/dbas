========
Makefile
========

* make init
    Creates a user for postgres as well as both databases (discussion and news).

* make databases
    Remove old databases and initialize new ones

* make refresh
    Will drop both databases, create them, assign them to the owner and fills them with data.

* make votes
    Creats dummy data for the voting tables

* make all
    Drops everything, inits dummy data for the discussion and the votes.

* make clean
    Drops all SQLite databases.