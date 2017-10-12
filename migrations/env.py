"""Pylons bootstrap environment.

Place 'pylons_config_file' into alembic.ini, and the application will
be loaded from there.

"""
import os

from alembic import context
from sqlalchemy import engine_from_config

from dbas.database import get_db_environs, DiscussionBase

# customize this section for non-standard engine configurations.
meta = __import__('dbas.database').database

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = DiscussionBase.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # raise NotImplementedError("Offline migraton not implemented!")

    context.configure(
        url=_get_dbas_engine().url, target_metadata=target_metadata,
        literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # specify here how the engine is acquired
    engine = _get_dbas_engine()

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.execute('SET search_path TO public')
            context.run_migrations()


def _get_dbas_engine():
    settings = dict()  # get_dbas_environs()
    os.environ['DBAS_DB_USER'] = 'postgres'
    settings.update(get_db_environs("sqlalchemy.discussion.url", db_name="discussion"))
    return engine_from_config(settings, "sqlalchemy.discussion.")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
