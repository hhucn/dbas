"""Add public_nicknames as view for read-only user

Revision ID: 4a6556fcb264
Revises: fcf9776a45d0
Create Date: 2019-09-03 12:57:16.237803

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
from sqlalchemy import text

revision = '4a6556fcb264'
down_revision = 'fcf9776a45d0'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute(text("""
        CREATE VIEW public_nicknames AS
        SELECT users.uid, users.public_nickname
        FROM users;
    """))


def downgrade():
    connection = op.get_bind()
    connection.execute(text("""
        DROP VIEW public_nicknames;
    """))
