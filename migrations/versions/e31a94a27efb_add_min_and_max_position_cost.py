"""Add min and max position cost

Revision ID: e31a94a27efb
Revises: 15bc523ae63e
Create Date: 2019-04-08 14:18:56.081686

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e31a94a27efb'
down_revision = '15bc523ae63e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decidotron_decision_process', sa.Column('max_position_cost', sa.Integer(), nullable=True))
    op.add_column('decidotron_decision_process',
                  sa.Column('min_position_cost', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('decidotron_decision_process', 'min_position_cost')
    op.drop_column('decidotron_decision_process', 'max_position_cost')
    # ### end Alembic commands ###
