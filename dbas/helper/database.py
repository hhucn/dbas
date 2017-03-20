from sqlalchemy import engine_from_config
import os

def dbas_configuration(settings, prefix):

    database = "discussion"
    if prefix.startswith("sqlalchemy-discussion."):
        database = "discussion"
    elif prefix.startswith("sqlalchemy-news."):
        database = "news"

    url = "postgresql+psycopg2://{}:{}@{}/{}?client_encoding=utf8".format(os.environ["DB_USER"], os.environ["DB_PW"], os.environ["DB_URL"], database)
    return engine_from_config(settings, prefix, url=url)