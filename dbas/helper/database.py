from sqlalchemy import engine_from_config


def dbas_db_configuration(db_name, settings={}):
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
    prefix = 'sqlalchemy.{}.url'.format(db_name)

    engine_from_config(get_db_environs(prefix, db_name, settings), prefix)
