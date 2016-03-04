DATABASES_DIR = dbas/static/

clean:
	rm $(DATABASES_DIR)*.sqlite

databases:
	rm $(DATABASES_DIR)*.sqlite
	initialize_api_sql development.ini
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini
