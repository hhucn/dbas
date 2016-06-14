"""
Common file to extract and prepare information provided by the database.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de
"""


def extract_author_information(db_user):
    pass


def extract_reference_information(db_ref):
    """
    Given the database object of a reference, extract and prepare a dictionary with relevant information.

    :param db_ref: StatementReference from database
    :return: prepared reference information
    :rtype: dict
    """
    ref = dict()

    if db_ref:
        ref = {"uid": db_ref.uid,
               "reference": db_ref.reference,
               "host": db_ref.host,
               "path": db_ref.path,
               "author_uid": db_ref.author_uid,
               "statement_uid": db_ref.statement_uid,
               "issue_uid": db_ref.issue_uid,
               "created": db_ref.created}

    return ref