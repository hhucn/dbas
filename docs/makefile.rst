========
Makefile
========
make reload (default)
    Drop everything, init dummy data for the discussion, the votes and reviews.

make users
    Create the users *dbas* and *dolan*.

make db
    Initialize new databases. You have to run *make users* once before!

make dummys
    Create dummy data for all databases.

make drop
    Drop all SQLite databases.

make drop_db
    Drop the *discussion* and the *news* databases.

make drop_users
    Drop all users if they exist.

make unit-coverage
    Run all unit tests with coverage
