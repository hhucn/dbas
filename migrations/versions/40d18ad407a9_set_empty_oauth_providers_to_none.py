"""Set empty oauth_providers to None

Revision ID: 40d18ad407a9
Revises: 4a6556fcb264
Create Date: 2019-09-27 11:32:17.408827

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '40d18ad407a9'
down_revision = '4a6556fcb264'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute("update users set oauth_provider = null where oauth_provider = ''")
    connection.execute("update users set oauth_provider_id = null where oauth_provider_id = ''")


def downgrade():
    pass
