DATABASES_DIR = dbas/static/


databases:
	initialize_api_sql development.ini
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini

clean:
	rm $(DATABASES_DIR)*.sqlite

