"""Add host and voting start field

Revision ID: 9a2e714ef52e
Revises: 2a1107018fad
Create Date: 2019-03-08 16:55:19.377160

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9a2e714ef52e'
down_revision = '2a1107018fad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decidotron_decision_process', sa.Column('host', sa.String(), nullable=False))
    op.add_column('decidotron_decision_process', sa.Column('votes_start', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('decidotron_decision_process', 'votes_start')
    op.drop_column('decidotron_decision_process', 'host')
    # ### end Alembic commands ###