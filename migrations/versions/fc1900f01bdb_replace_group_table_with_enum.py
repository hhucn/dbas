"""Replace group table with Enum

Revision ID: fc1900f01bdb
Revises: 774ee46152bc
Create Date: 2020-04-12 10:01:36.720751

"""
import enum

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = 'fc1900f01bdb'
down_revision = '774ee46152bc'
branch_labels = None
depends_on = None


class Group(enum.Enum):
    ADMIN = 1
    AUTHOR = 2
    USER = 3
    SPECIAL = 4


users = sa.Table('users', sa.MetaData(),
                 sa.Column('uid', sa.Integer, primary_key=True),
                 sa.Column('group', sa.Enum(Group, name='group')),
                 sa.Column('group_uid', sa.Integer),
                 )

groups = sa.Table('groups', sa.MetaData(),
                  sa.Column('uid', sa.INTEGER(), autoincrement=True, nullable=False),
                  sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
                  sa.PrimaryKeyConstraint('uid', name='groups_pkey'),
                  sa.UniqueConstraint('name', name='groups_name_key'))


def upgrade():
    enum_type = sa.Enum(Group)

    # this is a workaround to a bug in alembic to create the enum type correctly
    # see https://stackoverflow.com/a/55160320/3616102
    op.create_table(
        '_dummy',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('status', enum_type)
    )
    op.drop_table('_dummy')
    # end workaround

    op.add_column('users', sa.Column('group', enum_type))

    for group in Group:
        op.execute(users.update().where(users.columns.group_uid == group.value).values(group=group))

    op.alter_column('users', 'group', nullable=False)

    op.drop_constraint('users_group_uid_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'group_uid')

    op.drop_table('groups')


def downgrade():
    op.create_table('groups',
                    sa.Column('uid', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('uid', name='groups_pkey'),
                    sa.UniqueConstraint('name', name='groups_name_key'))

    op.add_column('users', sa.Column('group_uid', sa.INTEGER(), autoincrement=False, nullable=True))

    op.create_foreign_key('users_group_uid_fkey', 'users', 'groups', ['group_uid'], ['uid'])

    for uid, name in enumerate(["admins", "authors", "users", "specials"], start=1):
        op.execute(groups.insert().values(uid=uid, name=name))
        op.execute(users.update().where(users.columns.group == Group(uid)).values(group_uid=uid))

    op.drop_column('users', 'group')

    if op.get_bind().dialect.name == "postgresql":
        op.execute('DROP TYPE IF EXISTS "group";')
