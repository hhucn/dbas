"""
Provides helping function for querying the database.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument, Premise, Issue, ClickedStatement


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


def get_visible_issues_for_user_as_query(user_uid):
    """
    Returns query with all issues, which are visible for the user

    :param user_uid:
    :return: Query
    """
    db_valid_issues = DBDiscussionSession.query(Issue).filter(Issue.is_disabled == False,
                                                              Issue.is_private == False).all()
    set_of_visited_issues = {tmp.uid for tmp in db_valid_issues}

    db_clicked_statements = DBDiscussionSession.query(ClickedStatement).filter_by(author_uid=user_uid).all()
    db_statements = DBDiscussionSession.query(Statement).filter(
        Statement.uid.in_([tmp.statement_uid for tmp in db_clicked_statements])).all()
    db_valid_issues = DBDiscussionSession.query(Issue).filter(
        Issue.uid.in_([tmp.issue_uid for tmp in db_statements])).all()
    for issue in db_valid_issues:
        set_of_visited_issues.add(issue.uid)

    return DBDiscussionSession.query(Issue).filter(Issue.uid.in_(list(set_of_visited_issues)))
