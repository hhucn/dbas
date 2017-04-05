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
    db_host_port = os.environ.get("DBAS_DB_PORT", None)

    if all([db_user, db_pw, db_host, db_host_port]):
        settings.update(
            {'sqlalchemy.{}.url'.format(database): "postgresql+psycopg2://{}:{}@{}:{}/{}?client_encoding=utf8".format(
                db_user, db_pw, db_host, db_host_port, database)})
    else:
        errors = "Following variables are missing:\n"
        if not db_user:
            errors += "DBAS_DB_USER\n"
        if not db_pw:
            errors += "DBAS_DB_PW\n"
        if not db_host:
            errors += "DBAS_DB_HOST\n"
        if not db_host_port:
            errors += "DBAS_DB_PORT\n"

        raise EnvironmentError("Misconfigured environment variables for database. Result the installation instructions.\n" + errors)

    return engine_from_config(settings, prefix)