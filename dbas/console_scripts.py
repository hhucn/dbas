# coding=utf-8
import sys

import transaction
from sqlalchemy import engine_from_config
from sqlalchemy.orm.exc import NoResultFound

from dbas import get_db_environs, load_discussion_database
from dbas.database.discussion_model import User

# Set up the database session. Without this, you can not use DBDiscussionSession!
settings = {}  # Add console script specific configuration here.
settings.update(get_db_environs("sqlalchemy.discussion.url", db_name="discussion"))

discussion_engine = engine_from_config(settings, "sqlalchemy.discussion.")
load_discussion_database(discussion_engine)


def promote_user(argv=sys.argv):
    if len(argv) < 2:
        print("Please enter a nickname!")
        sys.exit(1)

    username: str = argv[1]

    with transaction.manager:
        try:
            User.by_nickname(username).promote_to_admin()
        except NoResultFound:
            print(f"The user `{username}` does not exist! Make sure you use the private and not the public nickname!")
            sys.exit(1)


def demote_user(argv=sys.argv):
    if len(argv) < 2:
        print("Please enter a nickname!")
        sys.exit(1)

    username: str = argv[1]

    with transaction.manager:
        try:
            User.by_nickname(username).demote_to_user()
        except NoResultFound:
            print(f"The user `{username}` does not exist! Make sure you use the private and not the public nickname!")
            sys.exit(1)
