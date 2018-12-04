# Common library for Admin Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
import hashlib
import logging
import os
import time
from datetime import datetime

import arrow
import transaction
from pyramid.httpexceptions import exception_response
from sqlalchemy.exc import IntegrityError, ProgrammingError

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, StatementReference, \
    SeenStatement, SeenArgument, TextVersion, PremiseGroup, Premise, Argument, ClickedArgument, ClickedStatement, \
    Message, ReviewDelete, ReviewEdit, ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, OptimizationReviewLocks, \
    ReviewCanceled, RevokedContent, RevokedContentHistory, LastReviewerDuplicate, ReviewDuplicate, \
    RevokedDuplicate, MarkedArgument, MarkedStatement, History, APIToken, StatementOrigins, StatementToIssue
from dbas.lib import get_text_for_premisegroup_uid, get_text_for_argument_uid, \
    get_text_for_statement_uid, get_profile_picture
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)

table_mapper = {
    'Issue'.lower(): {'table': Issue, 'name': 'Issue'},
    'Language'.lower(): {'table': Language, 'name': 'Language'},
    'Group'.lower(): {'table': Group, 'name': 'Group'},
    'User'.lower(): {'table': User, 'name': 'User'},
    'Settings'.lower(): {'table': Settings, 'name': 'Settings'},
    'Statement'.lower(): {'table': Statement, 'name': 'Statement'},
    'StatementReference'.lower(): {'table': StatementReference, 'name': 'StatementReference'},
    'StatementOrigins'.lower(): {'table': StatementOrigins, 'name': 'StatementOrigins'},
    'StatementToIssue'.lower(): {'table': StatementToIssue, 'name': 'StatementToIssue'},
    'SeenStatement'.lower(): {'table': SeenStatement, 'name': 'SeenStatement'},
    'SeenArgument'.lower(): {'table': SeenArgument, 'name': 'SeenArgument'},
    'TextVersion'.lower(): {'table': TextVersion, 'name': 'TextVersion'},
    'PremiseGroup'.lower(): {'table': PremiseGroup, 'name': 'PremiseGroup'},
    'Premise'.lower(): {'table': Premise, 'name': 'Premise'},
    'Argument'.lower(): {'table': Argument, 'name': 'Argument'},
    'History'.lower(): {'table': History, 'name': 'History'},
    'ClickedArgument'.lower(): {'table': ClickedArgument, 'name': 'ClickedArgument'},
    'ClickedStatement'.lower(): {'table': ClickedStatement, 'name': 'ClickedStatement'},
    'MarkedArgument'.lower(): {'table': MarkedArgument, 'name': 'MarkedArgument'},
    'MarkedStatement'.lower(): {'table': MarkedStatement, 'name': 'MarkedStatement'},
    'Message'.lower(): {'table': Message, 'name': 'Message'},
    'ReviewDelete'.lower(): {'table': ReviewDelete, 'name': 'ReviewDelete'},
    'ReviewEdit'.lower(): {'table': ReviewEdit, 'name': 'ReviewEdit'},
    'ReviewEditValue'.lower(): {'table': ReviewEditValue, 'name': 'ReviewEditValue'},
    'ReviewOptimization'.lower(): {'table': ReviewOptimization, 'name': 'ReviewOptimization'},
    'ReviewDuplicate'.lower(): {'table': ReviewDuplicate, 'name': 'ReviewDuplicate'},
    'ReviewDeleteReason'.lower(): {'table': ReviewDeleteReason, 'name': 'ReviewDeleteReason'},
    'LastReviewerDelete'.lower(): {'table': LastReviewerDelete, 'name': 'LastReviewerDelete'},
    'LastReviewerEdit'.lower(): {'table': LastReviewerEdit, 'name': 'LastReviewerEdit'},
    'LastReviewerOptimization'.lower(): {'table': LastReviewerOptimization, 'name': 'LastReviewerOptimization'},
    'LastReviewerDuplicate'.lower(): {'table': LastReviewerDuplicate, 'name': 'LastReviewerDuplicate'},
    'ReputationHistory'.lower(): {'table': ReputationHistory, 'name': 'ReputationHistory'},
    'ReputationReason'.lower(): {'table': ReputationReason, 'name': 'ReputationReason'},
    'OptimizationReviewLocks'.lower(): {'table': OptimizationReviewLocks, 'name': 'OptimizationReviewLocks'},
    'ReviewCanceled'.lower(): {'table': ReviewCanceled, 'name': 'ReviewCanceled'},
    'RevokedContent'.lower(): {'table': RevokedContent, 'name': 'RevokedContent'},
    'RevokedContentHistory'.lower(): {'table': RevokedContentHistory, 'name': 'RevokedContentHistory'},
    'RevokedDuplicate'.lower(): {'table': RevokedDuplicate, 'name': 'RevokedDuplicate'},
}

# list of all columns with FK of users/statement table
_user_columns = ['author_uid', 'reputator_uid', 'reviewer_uid', 'from_author_uid', 'to_author_uid', 'detector_uid']
_statement_columns = ['conclusion_uid', 'duplicate_statement_uid', 'original_statement_uid']
_arrow_columns = ['timestamp', 'date', 'last_login', 'last_action', 'registered']

# list of all columns, which will not be displayed
_forbidden_columns = ['token', 'token_timestamp']


def get_overview(page):
    """
    Returns a nested data structure with information about the database

    :param page: Name of the overview page
    :return: [[{'name': .., 'content': [{'name': .., 'count': .., 'href': ..}, ..] }], ..]
    """
    LOG.debug("main")
    return_list = list()

    # all tables for the 'general' group
    general = list()
    general.append(__get_dash_dict('Issue', page + 'Issue'))
    general.append(__get_dash_dict('Language', page + 'Language'))

    # all tables for the 'users' group
    users = list()
    users.append(__get_dash_dict('Group', page + 'Group'))
    users.append(__get_dash_dict('User', page + 'User'))
    users.append(__get_dash_dict('Settings', page + 'Settings'))
    users.append(__get_dash_dict('Message', page + 'Message'))
    general.append(__get_dash_dict('History', page + 'History'))

    # all tables for the 'content' group
    content = list()
    content.append(__get_dash_dict('Statement', page + 'Statement'))
    content.append(__get_dash_dict('StatementOrigins', page + 'StatementOrigins'))
    content.append(__get_dash_dict('StatementToIssue', page + 'StatementToIssue'))
    content.append(__get_dash_dict('TextVersion', page + 'TextVersion'))
    content.append(__get_dash_dict('StatementReference', page + 'StatementReference'))
    content.append(__get_dash_dict('PremiseGroup', page + 'PremiseGroup'))
    content.append(__get_dash_dict('Premise', page + 'Premise'))
    content.append(__get_dash_dict('Argument', page + 'Argument'))

    # all tables for the 'voting' group
    voting = list()
    voting.append(__get_dash_dict('ClickedArgument', page + 'ClickedArgument'))
    voting.append(__get_dash_dict('ClickedStatement', page + 'ClickedStatement'))
    voting.append(__get_dash_dict('MarkedArgument', page + 'MarkedArgument'))
    voting.append(__get_dash_dict('MarkedStatement', page + 'MarkedStatement'))
    voting.append(__get_dash_dict('SeenArgument', page + 'SeenArgument'))
    voting.append(__get_dash_dict('SeenStatement', page + 'SeenStatement'))

    # all tables for the 'reviews' group
    reviews = list()
    reviews.append(__get_dash_dict('ReviewDelete', page + 'ReviewDelete'))
    reviews.append(__get_dash_dict('ReviewEdit', page + 'ReviewEdit'))
    reviews.append(__get_dash_dict('ReviewEditValue', page + 'ReviewEditValue'))
    reviews.append(__get_dash_dict('ReviewOptimization', page + 'ReviewOptimization'))
    reviews.append(__get_dash_dict('ReviewDeleteReason', page + 'ReviewDeleteReason'))
    reviews.append(__get_dash_dict('ReviewDuplicate', page + 'ReviewDuplicate'))

    # all tables for the 'reviewer' group
    reviewer = list()
    reviewer.append(__get_dash_dict('LastReviewerDelete', page + 'LastReviewerDelete'))
    reviewer.append(__get_dash_dict('LastReviewerEdit', page + 'LastReviewerEdit'))
    reviewer.append(__get_dash_dict('LastReviewerOptimization', page + 'LastReviewerOptimization'))
    reviewer.append(__get_dash_dict('LastReviewerDuplicate', page + 'LastReviewerDuplicate'))

    # all tables for the 'reputation' group
    reputation = list()
    reputation.append(__get_dash_dict('ReputationHistory', page + 'ReputationHistory'))
    reputation.append(__get_dash_dict('ReputationReason', page + 'ReputationReason'))
    reputation.append(__get_dash_dict('OptimizationReviewLocks', page + 'OptimizationReviewLocks'))
    reputation.append(__get_dash_dict('ReviewCanceled', page + 'ReviewCanceled'))
    reputation.append(__get_dash_dict('RevokedContent', page + 'RevokedContent'))
    reputation.append(__get_dash_dict('RevokedContentHistory', page + 'RevokedContentHistory'))
    reputation.append(__get_dash_dict('RevokedDuplicate', page + 'RevokedDuplicate'))

    # first row
    return_list.append([{'name': 'General', 'content': general},
                        {'name': 'Users', 'content': users},
                        {'name': 'Content', 'content': content},
                        {'name': 'Voting', 'content': voting}])
    # second row
    return_list.append([{'name': 'Reviews', 'content': reviews},
                        {'name': 'Reviewer', 'content': reviewer},
                        {'name': 'Reputation', 'content': reputation}])

    return return_list


def get_table_dict(table_name, main_page):
    """
    Returns information about a specific table

    :param table_name: Name of the table
    :param main_page: URL
    :return: Dictionary with head, row, count and has_elements
    """
    LOG.debug("%s", table_name)

    # check for elements
    table = table_mapper[table_name.lower()]['table']
    db_elements = DBDiscussionSession.query(table).all()

    count = len(db_elements)
    if count == 0:
        return {
            'has_elements': False,
            'name': table_name,
            'count': count
        }

    # getting all keys
    columns = [r.key for r in table.__table__.columns]
    # remove all unnecessary columns
    for bad in _forbidden_columns:
        if bad in columns:
            columns.remove(bad)

    # getting data
    # data = [[str(getattr(row, c.name)) for c in row.__table__.columns] for row in db_elements]
    data = get_rows_of(columns, db_elements, main_page)
    if table_mapper[table_name.lower()]['name'] == 'History':
        data = data[::-1]

    # save it
    return {
        'name': table_name,
        'has_elements': True,
        'count': count,
        'head': columns,
        'row': data,
    }


def __get_language(uid, query):
    """
    Returns ui_locales of a language

    :param uid: of language
    :param query: of all languages
    :return: string
    """
    return query.get(uid).ui_locales


def __get_author_data(uid, query, main_page):
    """
    Returns a-tag with gravatar of current author and users page as href

    :param uid: of user
    :param query: of all users
    :params main_page: URL
    :return: string
    """
    db_user = query.get(uid)
    if not db_user:
        return 'Missing author with uid ' + str(uid), False

    img = '<img class="img-circle" src="{}">'.format(get_profile_picture(db_user, 20, True))
    return '<a href="{}/user/{}">{} {}</a> ({})'.format(main_page, db_user.uid, img, db_user.nickname,
                                                        db_user.uid), True


def __get_dash_dict(name, href):
    """
    Returns dictionary with all attributes

    :param name: name of current table
    :param href: link for current table
    :return: {'count': count, 'name': name, 'href': href}
    """
    count = DBDiscussionSession.query(table_mapper[name.lower()]['table']).count()
    return {
        'name': name,
        'href': href,
        'count': count,
    }


def get_rows_of(columns, db_elements, main_page):
    """
    Returns array with all data of a table

    :param columns: which should be displayed
    :param db_elements: which should be displayed
    :param main_page: URL
    :return: []
    """
    db_languages = DBDiscussionSession.query(Language)
    db_users = DBDiscussionSession.query(User)
    data = []
    for row in db_elements:
        tmp = []
        for column in columns:
            attribute = getattr(row, column)
            __resolve_attribute(attribute, column, main_page, db_languages, db_users, tmp)
        data.append(tmp)
    return data


def __resolve_attribute(attribute, column, main_page, db_languages, db_users, tmp):
    user_columns = {col: __resolve_user_attribute for col in _user_columns}
    statement_columns = {col: __resolve_statement_attribute for col in _statement_columns}
    arrow_columns = {col: __resolve_arrow_attribute for col in _arrow_columns}

    column_matcher = {
        'lang_uid': __resolve_lang_attribute,
        'password': __resolve_password_attribute,
        'premisegroup_uid': __resolve_premisesgroup_attribute,
        'argument_uid': __resolve_argument_attribute,
        'textversion_uid': __resolve_textversion_attribute,
        'path': __resolve_path_attribute,
        'email': __resolve_email_attribute,
    }
    column_matcher.update(user_columns)
    column_matcher.update(statement_columns)
    column_matcher.update(arrow_columns)

    if column in column_matcher:
        column_matcher[column](attribute, main_page, db_languages, db_users, tmp)
    else:
        tmp.append(str(attribute))


def __resolve_user_attribute(attribute, main_page, db_languages, db_users, tmp):
    text, success = __get_author_data(attribute, db_users, main_page)
    text = str(text) if success else ''
    tmp.append(text)


def __resolve_statement_attribute(attribute, main_page, db_languages, db_users, tmp):
    text = get_text_for_statement_uid(attribute) if attribute is not None else 'None'
    tmp.append(str(attribute) + ' - ' + str(text))


def __resolve_arrow_attribute(attribute, main_page, db_languages, db_users, tmp):
    tmp.append(attribute.format('YYYY-MM-DD HH:mm:ss'))


def __resolve_lang_attribute(attribute, main_page, db_languages, db_users, tmp):
    tmp.append(__get_language(attribute, db_languages))


def __resolve_password_attribute(attribute, main_page, db_languages, db_users, tmp):
    tmp.append(str(attribute)[:5] + '...')


def __resolve_premisesgroup_attribute(attribute, main_page, db_languages, db_users, tmp):
    text = ''
    uids = []
    if attribute is not None:
        text = get_text_for_premisegroup_uid(attribute)
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=attribute).join(Statement).all()
        uids = [premise.statement.uid for premise in db_premises]
    tmp.append('{} - {} {}'.format(attribute, text, uids))


def __resolve_argument_attribute(attribute, main_page, db_languages, db_users, tmp):
    text = get_text_for_argument_uid(attribute) if attribute is not None else 'None'
    tmp.append('{} - {}'.format(attribute, text))


def __resolve_textversion_attribute(attribute, main_page, db_languages, db_users, tmp):
    text = 'None'
    if attribute is not None:
        db_tv = DBDiscussionSession.query(TextVersion).get(attribute)
        text = db_tv.content if db_tv else ''
    tmp.append('{} - {}'.format(attribute, text))


def __resolve_path_attribute(attribute, main_page, db_languages, db_users, tmp):
    tmp.append('<a href="{}/{}{}" target="_blank">{}</a>'.format(main_page, 'discuss', attribute, attribute))


def __resolve_email_attribute(attribute, main_page, db_languages, db_users, tmp):
    db_user = DBDiscussionSession.query(User).filter_by(email=str(attribute)).first()
    img = '<img class="img-circle" src="{}">'.format(get_profile_picture(db_user, 25))
    tmp.append('{} {}'.format(img, attribute))


def update_row(table_name, uids, keys, values):
    """
    Updates the data in a specific row of an table

    :param table_name: Name of the table
    :param uids: Array with uids
    :param keys: Array with keys
    :param values: Array with values
    :return: Empty string or error message
    """
    table = table_mapper[table_name.lower()]['table']
    _tn = Translator('en')
    try:
        update_dict = __update_row_dict(table, values, keys, _tn)
    except ProgrammingError as e:
        LOG.error("%s", e)
        return exception_response(400, error='SQLAlchemy ProgrammingError: ' + str(e))

    try:
        __update_row(table, table_name, uids, update_dict)
    except IntegrityError as e:
        LOG.error("%s", e)
        return exception_response(400, error='SQLAlchemy IntegrityError: ' + str(e))
    except ProgrammingError as e:
        LOG.error("%s", e)
        return exception_response(400, error='SQLAlchemy ProgrammingError: ' + str(e))

    DBDiscussionSession.flush()
    transaction.commit()
    return True


def delete_row(table_name, uids):
    """
    Deletes a row in a table

    :param table_name: Name of the table
    :param uids: Array with uids
    :param nickname: Current nickname of the user
    :param _tn: Translator
    :return: Empty string or error message
    """
    LOG.debug("%s %s", table_name, uids)
    table = table_mapper[table_name.lower()]['table']
    try:
        # check if there is a table, where uid is not the PK!
        if table_name.lower() == 'settings':
            uid = DBDiscussionSession.query(User).filter_by(nickname=uids[0]).first().uid
            DBDiscussionSession.query(table).filter_by(author_uid=uid).delete()
        elif table_name.lower() == 'premise':
            DBDiscussionSession.query(table).filter(Premise.premisegroup_uid == uids[0],
                                                    Premise.statement_uid == uids[1]).delete()
        else:
            DBDiscussionSession.query(table).filter_by(uid=uids[0]).delete()

    except IntegrityError as e:
        LOG.error("%s", e)
        return exception_response(400, error='SQLAlchemy IntegrityError: ' + str(e))
    except ProgrammingError as e:
        LOG.error("%s", e)
        return exception_response(400, error='SQLAlchemy ProgrammingError: ' + str(e))

    DBDiscussionSession.flush()
    transaction.commit()
    return True


def add_row(table_name, data):
    """
    Updates data of a row in the table

    :param table_name: Name of the table
    :param data: Dictionary with data for the update
    :return: Empty string or error message
    """
    LOG.debug("%s", data)

    table = table_mapper[table_name.lower()]['table']
    try:
        if 'uid' in data:
            del data['uid']
        new_one = table(**data)
        DBDiscussionSession.add(new_one)
    except IntegrityError as e:
        LOG.error("%s", e)
        return exception_response(400, error='SQLAlchemy IntegrityError: ' + str(e))

    DBDiscussionSession.flush()
    transaction.commit()
    return True


def update_badge():
    """
    Returns the new count for the badge of every table

    :return: dict(), string
    """
    ret_array = []
    for t in table_mapper:
        ret_array.append({
            'name': table_mapper[t]['name'],
            'count': DBDiscussionSession.query(table_mapper[t]['table']).count()
        })

    return ret_array


def __update_row_dict(table, values, keys, _tn):
    """
    Create a dictionary out of values and keys with data, which is compatible with the table

    :param table: current table
    :param values: for inserting
    :param keys: for inserting
    :param _tn: Translator
    :return: {}
    """
    update_dict = dict()
    for index, key in enumerate(keys):
        value_type = str(__find_type(table, key))
        # if current type is int
        if value_type == 'INTEGER':
            tmp_key, tmp_val, success = __get_int_data(key, values[index], _tn)
            if not success:
                raise ProgrammingError
            update_dict[tmp_key] = tmp_val

        # if current type is bolean
        elif value_type == 'BOOLEAN':
            update_dict[key] = values[index].lower() == 'true'

        # if current type is text
        elif value_type == 'TEXT':
            update_dict[key] = str(values[index])

        # if current type is date
        elif value_type == 'ARROWTYPE':
            update_dict[key] = arrow.get(str(values[index]))

        else:
            update_dict[key] = values[index]

    return update_dict


def __get_int_data(key, val, _tn):
    # check for foreign key of author or language
    if key in _user_columns:
        # clear key / cut "(uid)"
        val = val[:val.rfind(" (")]
        db_user = DBDiscussionSession.query(User).filter_by(nickname=val).first()
        if not db_user:
            return _tn.get(_.userNotFound), '', False
        return key, db_user.uid, True

    elif key == 'lang_uid':
        db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=val).first()
        if not db_lang:
            return _tn.get(_.langNotFound), '', False
        return key, db_lang.uid

    else:
        return key, int(val), False


def __update_row(table, table_name, uids, update_dict):
    """
    Updates the row

    :param table: current table
    :param table_name: name of the table
    :param uids: all uids of the PKs
    :param update_dict: dictionary with all values
    :return: None
    """
    if table_name.lower() == 'settings':
        uid = DBDiscussionSession.query(User).filter_by(nickname=uids[0]).first().uid
        DBDiscussionSession.query(table).filter_by(author_uid=uid).update(update_dict)
    elif table_name.lower() == 'premise':
        DBDiscussionSession.query(table).filter(Premise.premisegroup_uid == uids[0],
                                                Premise.statement_uid == uids[1]).update(update_dict)
    else:
        DBDiscussionSession.query(table).filter_by(uid=uids[0]).update(update_dict)


def __find_type(table, col_name):
    """
    Returns type of tables column

    :param table: current table
    :param col_name: current columns name
    :return: String or raise NameError
    """
    if hasattr(table, '__table__') and col_name in table.__table__.c:
        return table.__table__.c[col_name].type
    for base in table.__bases__:
        return __find_type(base, col_name)
    raise NameError(col_name)


def get_application_tokens():
    """

    :return: A list of all not disabled tokens as dicts.
    """
    tokens = DBDiscussionSession.query(APIToken) \
        .filter_by(disabled=False).all()
    return [token.__dict__ for token in tokens]


def revoke_application_token(token_id: int):
    """
    Revoke a app token by setting it's disabled field.

    :param token_id: The id of the token to revoke
    """
    DBDiscussionSession.query(APIToken).get(token_id).disabled = True
    transaction.commit()


def generate_application_token(owner: str) -> str:
    """
    Generates a new application token.
    A hash (SHA256) of the token is stored in the database, together with it's owner and creation date.
    The owner is used as a prefix salt, when the token is hashed.


    :param owner: The owner of the token.
    :return: The token to use for authorization.
    """
    current_time = datetime.now()

    token = hashlib.sha256(''.join([str(time.time()), owner, str(os.urandom(256))]).encode()).hexdigest()

    hashed_token = __hash_token_with_owner(owner, token)

    new_row = APIToken(current_time, hashed_token, owner)

    DBDiscussionSession.add(new_row)
    DBDiscussionSession.flush()
    transaction.commit()

    return hashed_token[:5] + ":" + token


def __hash_token_with_owner(owner, token):
    return hashlib.sha256((owner + token).encode()).hexdigest()


def check_api_token(token: str) -> bool:
    """
    Checks if a token is valid or not.

    :param token: The token to check.
    :return: True if the token is valid and not disabled.
    """

    token_components = token.split(":")
    if len(token_components) is 2:
        hash_identifier, auth_token = token_components

        api_tokens = DBDiscussionSession.query(APIToken) \
            .filter(APIToken.token.startswith(hash_identifier),
                    APIToken.disabled == False)

        for api_token in api_tokens:
            return __hash_token_with_owner(api_token.owner, auth_token) == api_token.token

    return False
