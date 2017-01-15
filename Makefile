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

all:
	make users
	make db
	make dummy_discussion
	make dummy_votes


clean_db:
	sudo -u postgres bash -c "psql -c \"DROP DATABASE discussion;\""
	sudo -u postgres bash -c "psql -c \"DROP DATABASE news;\""

clean_users:
	sudo -u postgres bash -c "psql -c \"DROP USER $(reader);\""
	sudo -u postgres bash -c "psql -c \"DROP USER $(writer);\""

clean:
	make clean_db
	make clean_users


refresh:
	reload_discussion_sql development.ini
	initialize_news_sql development.ini


nosetests:
	nosetests --with-coverage --cover-package=dbas --cover-package=api --cover-package=graph --cover-package=export
	# -nosetests -s --with-coverage --cover-package=dbas > nosetests_temp_output.log 2>&1
	# cat nosetests_temp_output.log
	# grep TOTAL nosetests_temp_output.log | awk '{ print "TOTAL: "$$4; }'
	# rm nosetests_temp_output.log
