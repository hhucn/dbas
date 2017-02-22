# DBAS Makefile

database = discussion
writer = dbas
reader = dolan

users:
	sudo -u postgres bash -c "psql -c \"CREATE USER $(writer) WITH PASSWORD 'DoimBomrylpOytAfVin0';\""
	sudo -u postgres bash -c "psql -c \"CREATE USER $(reader) WITH PASSWORD 'jfsmkRr0govXJQhvpdr1cOGfdmQTohvXJQufsnsCXW9m';\""
	sudo -u postgres bash -c "psql -c \"ALTER ROLE $(reader) WITH NOLOGIN;\""

db:
	sudo -u postgres bash -c "createdb -O dbas discussion"
	sudo -u postgres bash -c "createdb -O dbas news"
	sudo -u postgres bash -c "psql -d ${database} -c \"ALTER DEFAULT PRIVILEGES FOR ROLE ${writer} IN SCHEMA public GRANT SELECT ON tables TO ${reader};\""

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

all: users db dummy_discussion dummy_votes dummy_reviews


clean_db:
	sudo -u postgres bash -c "dropdb -U postgres discussion --if-exists"
	sudo -u postgres bash -c "dropdb -U postgres news --if-exists"

clean_users:
	sudo -u postgres bash -c "dropuser -U postgres $(reader) --if-exists"
	sudo -u postgres bash -c "dropuser -U postgres $(writer) --if-exists"

clean: clean_db clean_users

refresh:
	reload_discussion_sql development.ini
	initialize_news_sql development.ini

fieldtest: users db
	init_field_test_sql development.ini
	initialize_news_sql development.ini

minimal_db: users db
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
	# -nosetests -s --with-coverage --cover-package=dbas > nosetests_temp_output.log 2>&1
	# cat nosetests_temp_output.log
	# grep TOTAL nosetests_temp_output.log | awk '{ print "TOTAL: "$$4; }'
	# rm nosetests_temp_output.log
