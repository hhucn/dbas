# DBAS Makefile

database = discussion
writer = dbas
reader = dolan
writer_pw = gAjOVf8MHBgHwUH8NmyWqwQQ43En1b0Mk1wZbm2JOYzWJ8PrQbwEIoWRhz4zT6Wz
reader_pw = jfsmkRr0govXJQhvpdr1cOGfdmQTohvXJQufsnsCXW9m

users: clean_users
	# Create group `writer`, has all table privileges in `public`
	psql -U postgres -c "CREATE ROLE writer;"
	# `writer` gets all privileges on new tables in scheme `public`.
	psql -U postgres -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT all ON tables TO writer;"
	# `writer` gets all privileges on existing tables in scheme `public`.
	psql -U postgres -c "GRANT all ON all tables IN SCHEMA public TO writer;"
	psql -U postgres -d news -c "GRANT all ON SCHEMA news TO writer;"
	# Create `writer` user ${writer} (dbas)
	psql -U postgres -c "CREATE USER ${writer} WITH PASSWORD '${writer_pw}' IN ROLE writer INHERIT;"

	## Create group `read_only_discussion` ##
	psql -U postgres -c "CREATE ROLE read_only_discussion;"
	psql -U postgres -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_only_discussion;"
	psql -U postgres -d ${database} -c "GRANT CONNECT ON DATABASE ${database} TO read_only_discussion;"
	# Create `read_only_discussion` user ${reader} (dolan)
	psql -U postgres -c "CREATE USER ${reader} WITH PASSWORD '${reader_pw}' IN ROLE read_only_discussion INHERIT;"

db: clean_db
	createdb -U postgres ${database}
	createdb -U postgres news
	psql -U postgres -d news -c "CREATE SCHEMA IF NOT EXISTS news;"

dummy_discussion:
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini

dummy_votes:
	init_discussion_testvotes development.ini

dummy_reviews:
	init_review_tests development.ini

dummys:
	dummy_discussion
	dummy_votes
	dummy_reviews

merge_discussion:
	merge_main_discussion development.ini

all: db users dummy_discussion dummy_votes dummy_reviews

clean_db:
	dropdb -U postgres discussion --if-exists
	dropdb -U postgres news --if-exists
	psql -U postgres -c "DROP SCHEMA IF EXISTS news;"

clean_users:
	# There is no "IF EXISTS" flag for DROP OWNED the "|| true" is a cheap workaround
	psql -U postgres -c "DROP OWNED BY writer;" || true
	dropuser -U postgres writer --if-exists
	psql -U postgres -c "DROP OWNED BY read_only_discussion;" || true
	dropuser -U postgres read_only_discussion --if-exists
	dropuser -U postgres $(reader) --if-exists
	dropuser -U postgres $(writer) --if-exists

clean: clean_db clean_users

refresh:
	reload_discussion_sql development.ini
	initialize_news_sql development.ini

fieldtest: db users
	init_field_test_sql development.ini
	initialize_news_sql development.ini

minimal_db: db users
	init_empty_sql development.ini

docker_dump_db:
	docker-compose -f docker-compose-export-db.yml up --force-recreate --abort-on-container-exit
	docker start dbas_db_1
	sleep 1 # wait for db inside of dbas_db_1
	docker exec dbas_db_1 pg_dumpall -U postgres --file=db.sql -c --if-exists
	docker cp dbas_db_1:db.sql ./db.sql
	echo ">>> Now push db.sql to the seeded branch in the postgres repo! <<<"

nosetests:
	nosetests --with-coverage --cover-package=dbas --cover-package=api --cover-package=graph --cover-package=export
