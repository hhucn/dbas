from sqlalchemy import engine_from_config
import os


def dbas_db_configuration(settings, prefix):

    database = "discussion"
    if prefix.startswith("sqlalchemy.discussion."):
        database = "discussion"
    elif prefix.startswith("sqlalchemy.news."):
        database = "news"

    db_user = os.environ.get("DBAS_DB_USER", None)
    db_pw = os.environ.get("DBAS_DB_PW", None)
    db_host = os.environ.get("DBAS_DB_HOST", None)

    if db_user and db_pw and db_host:
        settings.update(
            {'sqlalchemy.{}.url'.format(database): "postgresql+psycopg2://{}:{}@{}/{}?client_encoding=utf8".format(
                db_user, db_pw, db_host, database)})

    return engine_from_config(settings, prefix)
