# DBAS Makefile

init:
	sudo -u postgres bash -c "psql -c \"create user dbas with password 'SQL_2015&';\""
	sudo -u postgres bash -c "psql -c \"create database discussion;\""
	sudo -u postgres bash -c "psql -c \"create database news;\""

database:
	sudo -u postgres bash -c "psql -c \"create database discussion;\""
	sudo -u postgres bash -c "psql -c \"create database news;\""
	sudo -u postgres bash -c "psql -c \"alter database discussion owner to dbas;\""
	sudo -u postgres bash -c "psql -c \"alter database news owner to dbas;\""
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini

refresh:
	reload_discussion_sql development.ini
	initialize_news_sql development.ini

all:
	sudo -u postgres bash -c "psql -c \"create database discussion;\""
	sudo -u postgres bash -c "psql -c \"create database news;\""
	sudo -u postgres bash -c "psql -c \"alter database discussion owner to dbas;\""
	sudo -u postgres bash -c "psql -c \"alter database news owner to dbas;\""
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini
	init_discussion_testvotes development.ini
	init_review_tests development.ini

clean:
	sudo -u postgres bash -c "psql -c \"drop database discussion;\""
	sudo -u postgres bash -c "psql -c \"drop database news;\""

nosetests:
	nosetests --with-coverage --cover-package=dbas --cover-package=api --cover-package=graph --cover-package=export
	# -nosetests -s --with-coverage --cover-package=dbas > nosetests_temp_output.log 2>&1
	# cat nosetests_temp_output.log
	# grep TOTAL nosetests_temp_output.log | awk '{ print "TOTAL: "$$4; }'
	# rm nosetests_temp_output.log

mac_refresh:
	dropdb discussion
	dropdb news
	createdb -O dbas discussion
	createdb -O dbas news
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini
	init_discussion_testvotes development.ini
	init_review_tests development.ini