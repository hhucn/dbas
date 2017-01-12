# DBAS Makefile

users:
	sudo -u postgres bash -c "psql -c \"CREATE USER dbas WITH PASSWORD 'SQL_2015&';\""
	sudo -u postgres bash -c "psql -c \"CREATE USER dolan WITH PASSWORD 'jfsmkRr0govXJQhvpdr1cOGfdmQTohvXJQufsnsCXW9m';\""
	sudo -u postgres bash -c "psql -c \"ALTER role dolan with nologin;\""

db:
	sudo -u postgres bash -c "createdb -O dbas discussion"
	sudo -u postgres bash -c "createdb -O dbas news"

dummy_discussion:
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini
	sudo -u postgres bash -c "psql -d discussion -c \"GRANT SELECT ON ALL TABLES IN SCHEMA public TO dolan;\""

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
	sudo -u postgres bash -c "psql -c \"DROP USER dbas;\""
	sudo -u postgres bash -c "psql -c \"DROP USER dolan;\""

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
