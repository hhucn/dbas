# DBAS Makefile

DATABASES_DIR = dbas/static/


# Remove old databases and initialize new ones
databases:
	rm -f $(DATABASES_DIR)*.sqlite
	initialize_api_sql development.ini
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini

clean:
	rm $(DATABASES_DIR)*.sqlite

