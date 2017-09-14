"""Pylons bootstrap environment.

Place 'pylons_config_file' into alembic.ini, and the application will
be loaded from there.

"""
from alembic import context
from paste.deploy import loadapp
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from dbas import get_dbas_environs
from pyramid.paster import get_appsettings
from dbas.database import get_db_environs, DiscussionBase
import logging

# disable logging from dbas/__init__.py
logging.disable(logging.DEBUG)

try:
    # if pylons app already in, don't create a new app
    from pylons import config as pylons_config
    pylons_config['__file__']
except:
    config = context.config
    # can use config['__file__'] here, i.e. the Pylons
    # ini file, instead of alembic.ini
    config_file = config.get_main_option('pylons_config_file')
    fileConfig(config_file)
    wsgi_app = loadapp('config:%s' % config_file, relative_to='.')


# customize this section for non-standard engine configurations.
meta = __import__('dbas.database').database
# meta = __import__("%s.model.meta" % wsgi_app.config['pylons.package']).model.meta

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
    def process_revision_directives(context, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    engine = _get_dbas_engine()

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


def _get_dbas_engine():
    settings = get_appsettings('development.ini', name='main')
    settings.update(get_dbas_environs())
    settings.update(get_db_environs(key="session.url", db_name="beaker"))
    settings.update(get_db_environs("sqlalchemy.discussion.url", db_name="discussion"))
    # settings.update(get_db_environs("sqlalchemy.news.url", db_name="news"))
    return engine_from_config(settings, "sqlalchemy.discussion.")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
