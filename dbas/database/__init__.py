"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import os

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension as Zte

DBDiscussionSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DBNewsSession = scoped_session(sessionmaker(extension=Zte(), expire_on_commit=False))
DiscussionBase = declarative_base()
NewsBase = declarative_base()
DBEngine = None
DBNewsEngine = None


def load_discussion_database(engine):
    db_discussion_engine = engine
    DBDiscussionSession.configure(bind=db_discussion_engine)
    DiscussionBase.metadata.bind = db_discussion_engine
    DiscussionBase.metadata.create_all(db_discussion_engine)


def load_news_database(engine):
    db_news_engine = engine
    DBNewsSession.configure(bind=db_news_engine)
    NewsBase.metadata.bind = db_news_engine
    NewsBase.metadata.create_all(db_news_engine)


def get_dbas_db_configuration(db_name, settings={}):
    """
    Gets a database name and settings and looks up database connection configurations in four environment variables
    These are:

    +--------------+------------------------------------------------------------------+
    | DBAS_DB_HOST | The hostname of the database (example: localhost, db, 10.0.0.2). |
    +--------------+------------------------------------------------------------------+
    | DBAS_DB_PORT | The port of the database (example: 5432).                        |
    +--------------+------------------------------------------------------------------+
    | DBAS_DB_USER | The database username. (example: dbas)                           |
    +--------------+------------------------------------------------------------------+
    | DBAS_DB_PW   | The passwort of the DBAS_DB_USER (example: passw0rt123)          |
    +--------------+------------------------------------------------------------------+


    :param db_name: The name of the database, as a string
    :param settings: A dict containing settings for the database connection. (optional)
    :return: A sqlalchemy engine from environment variables and settings.
    """
    prefix = 'sqlalchemy.{}.'.format(db_name)
    settings.update(get_db_environs(prefix + 'url', db_name))

    return engine_from_config(settings, prefix)


def get_db_environs(key, db_name, settings={}):
    db_user = os.environ.get("DBAS_DB_USER", None)
    db_pw = os.environ.get("DBAS_DB_PW", None)
    db_host = os.environ.get("DBAS_DB_HOST", None)
    db_host_port = os.environ.get("DBAS_DB_PORT", None)

    if all([db_user, db_pw, db_host, db_host_port]):
        settings.update(
            {key: "postgresql+psycopg2://{}:{}@{}:{}/{}?client_encoding=utf8".format(
                db_user, db_pw, db_host, db_host_port, db_name)})
        return settings
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
