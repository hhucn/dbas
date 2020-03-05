"""Arguments must have an argument or conclusion

Revision ID: 774ee46152bc
Revises: 40d18ad407a9
Create Date: 2020-03-05 16:31:20.276837

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '774ee46152bc'
down_revision = '40d18ad407a9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint("ck_arguments_must-have-descendent", "arguments",
                               "(argument_uid is not null) != (conclusion_uid is not null)")


def downgrade():
    op.drop_constraint("ck_arguments_must-have-descendent", "arguments")
