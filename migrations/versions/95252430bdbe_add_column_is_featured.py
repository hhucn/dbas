"""Add column is_featured

Revision ID: 95252430bdbe
Revises: 15bc523ae63e
Create Date: 2019-03-27 18:47:08.445962

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '95252430bdbe'
down_revision = 'e31a94a27efb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('issues', sa.Column('is_featured', sa.Boolean(), server_default='False', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('issues', 'is_featured')
    # ### end Alembic commands ###