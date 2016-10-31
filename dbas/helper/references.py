from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementReferences, User
from dbas.query_wrapper import get_not_disabled_arguments_as_query, get_not_disabled_premises_as_query
from dbas.lib import get_text_for_statement_uid, get_profile_picture, get_public_nickname_based_on_settings
from dbas.logger import logger


def get_references_for_argument(uid, main_page):
    """
    Returns all references for the premises group of given argument

    :param uid: uid of the argument
    :param main_page: current main page
    :return: dict
    """
    logger('ReferenceHelper', 'get_references_for_argument', str(uid))
    db_arguments = get_not_disabled_arguments_as_query()
    db_argument = db_arguments.filter_by(uid=uid).first()

    db_premises = get_not_disabled_premises_as_query()
    db_premises = db_premises.filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()

    data = {}
    for premise in db_premises:
        tmp_uid = premise.statement_uid
        references_array = __get_references_for_statement(tmp_uid, main_page)[tmp_uid]
        data[premise.statement_uid] = references_array
    return data


def get_references_for_statements(uids, main_page):
    """
    Returns all references for the current given statements

    :param uid: uids of the statement
    :param main_page: current main page
    :return: dict
    """
    data = {}
    for uid in uids:
        references_array = __get_references_for_statement(uid, main_page)[uid]
        data[uid] = references_array
    return data


def __get_references_for_statement(uid, main_page):
    """
    Returns all references for the current given statement

    :param uid: uid of the statement
    :param main_page: current main page
    :return: dict
    """
    logger('ReferenceHelper', 'get_references_for_statement', str(uid))
    db_references = DBDiscussionSession.query(StatementReferences).filter_by(statement_uid=uid).all()
    references_array = [__get_values_of_reference(ref, main_page) for ref in db_references]
    return {uid: references_array}


def __get_values_of_reference(reference, main_page):
    """
    Creates dictionary with all values of the column

    :param reference: Current database row
    :param main_page: current main page
    :return: Dictionary with all columns
    """
    db_user = DBDiscussionSession.query(User).filter_by(uid=int(reference.author_uid)).first()

    img = get_profile_picture(db_user, 20, True)
    name = get_public_nickname_based_on_settings(db_user)
    link = main_page + '/user/' + name

    return {'uid': reference.uid,
            'reference': reference.reference,
            'host': reference.host,
            'path': reference.path,
            'author': {'img': img,
                       'name': name,
                       'link': link},
            'created': str(reference.created.humanize),
            'statement_text': get_text_for_statement_uid(reference.statement_uid)}
