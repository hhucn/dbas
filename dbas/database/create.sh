#!/bin/sh

sudo -u postgres sh

pg_ctl start -
psql -c "CREATE USER ${writer} WITH SUPERUSER PASSWORD 'gAjOVf8MHBgHwUH8NmyWqwQQ43En1b0Mk1wZbm2JOYzWJ8PrQbwEIoWRhz4zT6Wz';"
psql -c "CREATE USER ${reader} WITH PASSWORD 'jfsmkRr0govXJQhvpdr1cOGfdmQTohvXJQufsnsCXW9m' NOLOGIN;"
createdb -O ${writer} ${database}
createdb -O ${writer} news
createdb -O ${writer} beaker
psql -d ${database} -c "ALTER DEFAULT PRIVILEGES FOR ROLE ${writer} IN SCHEMA public GRANT SELECT ON tables TO ${reader};"
pg_ctl stop

sudo -u root sh