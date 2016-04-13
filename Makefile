# DBAS Makefile

init_postgres:
	sudo -u postgres bash -c "psql -c \"create user dbas with password 'SQL_2015&';\""
	sudo -u postgres bash -c "psql -c \"create database discussion;\""
	sudo -u postgres bash -c "psql -c \"create database news;\""

postgres:
	sudo -u postgres bash -c "psql -c \"drop database discussion;\""
	sudo -u postgres bash -c "psql -c \"drop database news;\""
	sudo -u postgres bash -c "psql -c \"create database discussion;\""
	sudo -u postgres bash -c "psql -c \"create database news;\""
	sudo -u postgres bash -c "psql -c \"alter database discussion owner to dbas;\""
	sudo -u postgres bash -c "psql -c \"alter database news owner to dbas;\""
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini

refresh_postgres:
	reload_discussion_sql development.ini
	initialize_news_sql development.ini

clean_postgres:
	sudo -u postgres bash -c "psql -c \"drop database discussion;\""
	sudo -u postgres bash -c "psql -c \"drop database news;\""