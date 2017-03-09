#!/bin/bash
set -e

database=discussion
reader=dolan
reader_pw=jfsmkRr0govXJQhvpdr1cOGfdmQTohvXJQufsnsCXW9m
writer=dbas
writer_pw=gAjOVf8MHBgHwUH8NmyWqwQQ43En1b0Mk1wZbm2JOYzWJ8PrQbwEIoWRhz4zT6Wz

createdb ${database}
createdb beaker
createdb news

psql -d news -c "CREATE SCHEMA IF NOT EXISTS news;"

# Create writer role
psql -c "CREATE ROLE writer;"
psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT all ON tables TO writer;"
psql -c "GRANT all ON all tables IN SCHEMA public TO writer;"
psql -d news -c "GRANT all ON SCHEMA news TO writer;"
psql -c "CREATE USER ${writer} WITH PASSWORD '${writer_pw}' IN ROLE writer INHERIT;"

# Create 'group' for users which only can read 'discussion'.
psql -c "CREATE ROLE read_only_discussion;"

# Set privileges for this 'group'.
psql -d ${database} -c "GRANT CONNECT ON DATABASE ${database} TO read_only_discussion;"
psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_only_discussion;"

# Add a user with login rights and the read_only_discussion 'group'.
# IMPORTANT! use 'IN ROLE' not 'ROLE'!
psql -c "CREATE USER ${reader} WITH PASSWORD '${reader_pw}' IN ROLE read_only_discussion INHERIT;"
