"""
Common file to extract and prepare information provided by the database.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
"""


def extract_issue_information(db_issue):
    """
    Given an Issue object from the database, extract public information and pack it into a dict.

    :param db_issue:
    :return: public issue information
    :rtype: dict
    """
    if db_issue:
        return {"uid": db_issue.uid,
                "title": db_issue.title,
                "info": db_issue.info,
                "slug": db_issue.slug}


def extract_author_information(db_user):
    """
    Given a User from the database, extract public information and return it as a dictionary.

    :param db_user:
    :return: public author information
    :rtype: dict
    """
    if db_user:
        return {"uid": db_user.uid,
                "nickname": db_user.public_nickname}


def extract_reference_information(db_ref):
    """
    Given the database object of a reference, extract and prepare a dictionary with relevant information.

    :param db_ref: StatementReference from database
    :return: prepared reference information
    :rtype: dict
    """
    if db_ref:
        return {"uid": db_ref.uid,
                "title": db_ref.reference,
                "host": db_ref.host,
                "path": db_ref.path,
                "statement_uid": db_ref.statement_uid}
