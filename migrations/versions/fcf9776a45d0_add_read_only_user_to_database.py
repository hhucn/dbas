"""Add read-only user to database

Revision ID: fcf9776a45d0
Revises: 95252430bdbe
Create Date: 2019-09-02 12:07:39.247726

"""
from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'fcf9776a45d0'
down_revision = '95252430bdbe'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute(text("""
        CREATE ROLE readaccess;

        -- Grant access to existing tables
        GRANT USAGE ON SCHEMA public TO readaccess;
        -- GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;
        GRANT SELECT ON arguments,
                        issues,
                        languages,
                        premisegroups,
                        premises,
                        statement_to_issue,
                        statements,
                        textversions
                     TO readaccess;

        -- Grant access to future tables
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readaccess;

        -- Create a final user with password
        CREATE USER guest WITH PASSWORD 'guest';
        GRANT readaccess TO guest;
    """))


def downgrade():
    connection = op.get_bind()
    connection.execute(text("""
        REASSIGN OWNED BY readaccess TO postgres;
        DROP OWNED BY readaccess;
        DROP ROLE readaccess;
        DROP USER guest;
    """))
