# DBAS Makefile

database = discussion
writer = dbas
reader = dolan

users:
	sudo -u postgres bash -c "psql -c \"CREATE USER $(writer) WITH PASSWORD 'SQL_2015&';\""
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


nosetests:
	nosetests --with-coverage --cover-package=dbas --cover-package=api --cover-package=graph --cover-package=export
	# -nosetests -s --with-coverage --cover-package=dbas > nosetests_temp_output.log 2>&1
	# cat nosetests_temp_output.log
	# grep TOTAL nosetests_temp_output.log | awk '{ print "TOTAL: "$$4; }'
	# rm nosetests_temp_output.log
