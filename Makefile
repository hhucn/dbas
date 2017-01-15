reload: drop users dummys

users:
	psql -U postgres -c "CREATE USER dbas PASSWORD 'SQL_2015&';" && echo "dbas";\
	psql -U postgres -c "CREATE ROLE dolan PASSWORD 'jfsmkRr0govXJQhvpdr1cOGfdmQTohvXJQufsnsCXW9m';" && echo "dolan" || true

db:
	createdb -U postgres -O dbas discussion
	createdb -U postgres -O dbas news

dummys: dummy_discussion dummy_votes dummy_reviews

dummy_discussion: db
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini
	psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO dolan;"

dummy_votes: dummy_discussion
	init_discussion_testvotes development.ini

dummy_reviews: dummy_discussion
	init_review_tests development.ini

drop: drop_db drop_users

drop_db:
	dropdb -U postgres discussion --if-exists
	dropdb -U postgres news --if-exists

drop_users:
	dropuser -U postgres dbas --if-exists
	dropuser -U postgres dolan --if-exists

unit-coverage: drop_db dummys
	nosetests --with-coverage dbas graph admin api export
	# -nosetests -s --with-coverage --cover-package=dbas > nosetests_temp_output.log 2>&1
	# cat nosetests_temp_output.log
	# grep TOTAL nosetests_temp_output.log | awk '{ print "TOTAL: "$$4; }'
	# rm nosetests_temp_output.log