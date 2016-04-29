#!/bin/bash
set -e

/etc/init.d/postgresql start

psql -c "create user dbas with password 'SQL_2015&';"
psql -c "create database discussion;"
psql -c "create database news;"
psql -c "alter database discussion owner to dbas;"
psql -c "alter database news owner to dbas;"