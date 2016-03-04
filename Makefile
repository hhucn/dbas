# DBAS Makefile

DATABASE_DIR = dbas/static/
DATABASES = api.sqlite dbas.sqlite news.sqlite

# Remove old databases and initialize new ones
databases:
	rm -f $(addprefix $(DATABASE_DIR), $(DATABASES))
	initialize_api_sql development.ini
	initialize_discussion_sql development.ini
	initialize_news_sql development.ini

clean:
	rm -f $(addprefix $(DATABASE_DIR), $(DATABASES))

