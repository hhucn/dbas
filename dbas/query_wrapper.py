"""
Provides helping function for querying the database.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument, Premise, Issue


def get_not_disabled_statement_as_query():
    """
    Returns query with all statements, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Statement).filter_by(is_disabled=False)


def get_not_disabled_arguments_as_query():
    """
    Returns query with all arguments, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Argument).filter_by(is_disabled=False)


def get_not_disabled_premises_as_query():
    """
    Returns query with all premises, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Premise).filter_by(is_disabled=False)


def get_not_disabled_issues_as_query():
    """
    Returns query with all issues, which are not disabled

    :return: Query
    """
    return DBDiscussionSession.query(Issue).filter_by(is_disabled=False)
