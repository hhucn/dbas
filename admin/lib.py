# Common library for Admin Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de
import hashlib
import os
import time
from datetime import datetime

import arrow
import transaction
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, ProgrammingError

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, StatementReferences, \
    SeenStatement, SeenArgument, TextVersion, PremiseGroup, Premise, Argument, ClickedArgument, ClickedStatement, \
    Message, ReviewDelete, ReviewEdit, ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, OptimizationReviewLocks, \
    ReviewCanceled, RevokedContent, RevokedContentHistory, RSS, LastReviewerDuplicate, ReviewDuplicate, \
    RevokedDuplicate, MarkedArgument, MarkedStatement, History, APIToken
from dbas.lib import is_user_admin, get_text_for_premisesgroup_uid, get_text_for_argument_uid, \
    get_text_for_statement_uid, get_profile_picture
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _

table_mapper = {
    'Issue'.lower(): {'table': Issue, 'name': 'Issue'},
    'Language'.lower(): {'table': Language, 'name': 'Language'},
    'Group'.lower(): {'table': Group, 'name': 'Group'},
    'User'.lower(): {'table': User, 'name': 'User'},
    'Settings'.lower(): {'table': Settings, 'name': 'Settings'},
    'Statement'.lower(): {'table': Statement, 'name': 'Statement'},
    'StatementReferences'.lower(): {'table': StatementReferences, 'name': 'StatementReferences'},
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
    'RSS'.lower(): {'table': RSS, 'name': 'RSS'}
}

google_colors = [
    ['#f44336', '#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350', '#f44336', '#e53935', '#d32f2f', '#c62828',
     '#b71c1c', '#ff8a80', '#ff5252', '#ff1744', '#d50000'],  # red
    ['#e91e63', '#fce4ec', '#f8bbd0', '#f48fb1', '#f06292', '#ec407a', '#e91e63', '#d81b60', '#c2185b', '#ad1457',
     '#880e4f', '#ff80ab', '#ff4081', '#f50057', '#c51162'],  # pink
    ['#9c27b0', '#f3e5f5', '#e1bee7', '#ce93d8', '#ba68c8', '#ab47bc', '#9c27b0', '#8e24aa', '#7b1fa2', '#6a1b9a',
     '#4a148c', '#ea80fc', '#e040fb', '#d500f9', '#aa00ff'],  # purple
    ['#673ab7', '#ede7f6', '#d1c4e9', '#b39ddb', '#9575cd', '#7e57c2', '#673ab7', '#5e35b1', '#512da8', '#4527a0',
     '#311b92', '#b388ff', '#7c4dff', '#651fff', '#6200ea'],  # deep purple
    ['#3f51b5', '#e8eaf6', '#c5cae9', '#9fa8da', '#7986cb', '#5c6bc0', '#3f51b5', '#3949ab', '#303f9f', '#283593',
     '#1a237e', '#8c9eff', '#536dfe', '#3d5afe', '#304ffe'],  # indigo
    ['#2196f3', '#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0',
     '#0d47a1', '#82b1ff', '#448aff', '#2979ff', '#2962ff'],  # blue
    ['#03a9f4', '#e1f5fe', '#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#03a9f4', '#039be5', '#0288d1', '#0277bd',
     '#01579b', '#80d8ff', '#40c4ff', '#00b0ff', '#0091ea'],  # light blue
    ['#00bcd4', '#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1', '#26c6da', '#00bcd4', '#00acc1', '#0097a7', '#00838f',
     '#006064', '#84ffff', '#18ffff', '#00e5ff', '#00b8d4'],  # cyan
    ['#009688', '#e0f2f1', '#b2dfdb', '#80cbc4', '#4db6ac', '#26a69a', '#009688', '#00897b', '#00796b', '#00695c',
     '#004d40', '#a7ffeb', '#64ffda', '#1de9b6', '#00bfa5'],  # teal
    ['#4caf50', '#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50', '#43a047', '#388e3c', '#2e7d32',
     '#1b5e20', '#b9f6ca', '#69f0ae', '#00e676', '#00c853'],  # green
    ['#8bc34a', '#f1f8e9', '#dcedc8', '#c5e1a5', '#aed581', '#9ccc65', '#8bc34a', '#7cb342', '#689f38', '#558b2f',
     '#33691e', '#ccff90', '#b2ff59', '#76ff03', '#64dd17'],  # light green
    ['#cddc39', '#f9fbe7', '#f0f4c3', '#e6ee9c', '#dce775', '#d4e157', '#cddc39', '#c0ca33', '#afb42b', '#9e9d24',
     '#827717', '#f4ff81', '#eeff41', '#c6ff00', '#aeea00'],  # lime
    ['#ffeb3b', '#fffde7', '#fff9c4', '#fff59d', '#fff176', '#ffee58', '#ffeb3b', '#fdd835', '#fbc02d', '#f9a825',
     '#f57f17', '#ffff8d', '#ffff00', '#ffea00', '#ffd600'],  # yellow
    ['#ffc107', '#fff8e1', '#ffecb3', '#ffe082', '#ffd54f', '#ffca28', '#ffc107', '#ffb300', '#ffa000', '#ff8f00',
     '#ff6f00', '#ffe57f', '#ffd740', '#ffc400', '#ffab00'],  # amber
    ['#ff9800', '#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726', '#ff9800', '#fb8c00', '#f57c00', '#ef6c00',
     '#e65100', '#ffd180', '#ffab40', '#ff9100', '#ff6d00'],  # orange
    ['#ff5722', '#fbe9e7', '#ffccbc', '#ffab91', '#ff8a65', '#ff7043', '#ff5722', '#f4511e', '#e64a19', '#d84315',
     '#bf360c', '#ff9e80', '#ff6e40', '#ff3d00', '#dd2c00'],  # deep orange
    ['#795548', '#efebe9', '#d7ccc8', '#bcaaa4', '#a1887f', '#8d6e63', '#795548', '#6d4c41', '#5d4037', '#4e342e',
     '#3e2723'],  # brown
    ['#9e9e9e', '#fafafa', '#f5f5f5', '#eeeeee', '#e0e0e0', '#bdbdbd', '#9e9e9e', '#757575', '#616161', '#424242',
     '#212121'],  # grey
    ['#607d8b', '#eceff1', '#cfd8dc', '#b0bec5', '#90a4ae', '#78909c', '#607d8b', '#546e7a', '#455a64', '#37474f',
     '#263238'],  # blue grey
    ['#000000'],  # black
    ['#ffffff']]  # white

# list of all columns with FK of users/statement table
_user_columns = ['author_uid', 'reputator_uid', 'reviewer_uid', 'from_author_uid', 'to_author_uid', 'detector_uid']
_statement_columns = ['conclusion_uid', 'duplicate_statement_uid', 'original_statement_uid']
_arrow_columns = ['timestamp', 'date', 'last_login', 'last_action', 'registered']

# list of all columns, which will not be displayed
_forbidden_columns = ['token', 'token_timestamp']


def get_overview(page):
    """
    Returns a nested data structure with information about the database

    :param page: Name of the main page
    :return: [[{'name': .., 'content': [{'name': .., 'count': .., 'href': ..}, ..] }], ..]
    """
    logger('AdminLib', 'get_dashboard_infos', 'main')
    return_list = list()

    # all tables for the 'general' group
    general = list()
    general.append(__get_dash_dict('Issue', page + 'Issue'))
    general.append(__get_dash_dict('Language', page + 'Language'))
    general.append(__get_dash_dict('RSS', page + 'RSS'))

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
    content.append(__get_dash_dict('TextVersion', page + 'TextVersion'))
    content.append(__get_dash_dict('StatementReferences', page + 'StatementReferences'))
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
    logger('AdminLib', 'get_table_dict', str(table_name))

    # check for table
    if not table_name.lower() in table_mapper:
        return {'is_existing': False}

    # check for elements
    db_elements = DBDiscussionSession.query(table_mapper[table_name.lower()]['table']).all()

    count = len(db_elements)
    if count == 0:
        return {'is_existing': True,
                'has_elements': False,
                'name': table_name,
                'count': count}

    # getting all keys
    table = table_mapper[table_name.lower()]['table']
    columns = [r.key for r in table.__table__.columns]
    # remove all unnecessary columns
    for bad in _forbidden_columns:
        if bad in columns:
            columns.remove(bad)

    # getting data
    # data = [[str(getattr(row, c.name)) for c in row.__table__.columns] for row in db_elements]
    data = get_rows_of(columns, db_elements, main_page)

    # save it
    return {
        'is_existing': True,
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

    db_settings = DBDiscussionSession.query(Settings).get(uid)
    if not db_settings:
        return 'Missing settings of author with uid ' + str(uid), False

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
    return {'name': name, 'href': href}


def get_rows_of(columns, db_elements, main_page):
    """
    Returns array with all data of a table

    :param columns: which should be displayed
    :param db_elements: which should be displayed
    :params main_page: URL
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
    if column in _user_columns:
        text, success = __get_author_data(attribute, db_users, main_page)
        text = str(text) if success else ''
        tmp.append(text)
        return

    if column == 'lang_uid':
        tmp.append(__get_language(attribute, db_languages))
        return

    if column == 'password':
        tmp.append(str(attribute)[:5] + '...')
        return

    if column == 'premisesgroup_uid':
        text, uid_list = get_text_for_premisesgroup_uid(attribute) if attribute is not None else ('None', '[-]')
        tmp.append(str(attribute) + ' - ' + str(text) + ' ' + str(uid_list))
        return

    if column in _statement_columns:
        text = get_text_for_statement_uid(attribute) if attribute is not None else 'None'
        tmp.append(str(attribute) + ' - ' + str(text))
        return

    if column == 'argument_uid':
        text = get_text_for_argument_uid(attribute) if attribute is not None else 'None'
        tmp.append(str(attribute) + ' - ' + str(text))
        return

    if column == 'textversion_uid':
        text = 'None'
        if attribute is not None:
            db_tv = DBDiscussionSession.query(TextVersion).get(attribute)
            text = db_tv.content if db_tv else ''
        tmp.append(str(attribute) + ' - ' + str(text))
        return

    if column == 'path':
        tmp.append('<a href="{}/{}{}" target="_blank">{}</a>'.format(main_page, 'discuss', attribute, attribute))
        return

    if column == 'email':
        db_user = DBDiscussionSession.query(User).filter_by(email=str(attribute)).first()
        img = '<img class="img-circle" src="{}">'.format(get_profile_picture(db_user, 25))
        tmp.append('{} {}'.format(img, attribute))
        return

    if column in _arrow_columns:
        tmp.append(attribute.format('YYYY-MM-DD HH:mm:ss'))
        return

    tmp.append(str(attribute))


def update_row(table_name, uids, keys, values, nickname, _tn):
    """
    Updates the data in a specific row of an table

    :param table_name: Name of the table
    :param uids: Array with uids
    :param keys: Array with keys
    :param values: Array with values
    :param nickname: Current nickname of the user
    :param _tn: Translator
    :return: Empty string or error message
    """
    if not is_user_admin(nickname):
        return _tn.get(_.noRights)

    if not table_name.lower() in table_mapper:
        return _tn.get(_.internalKeyError)

    table = table_mapper[table_name.lower()]['table']
    try:
        update_dict, success = __update_row_dict(table, values, keys, _tn)
        if not success:
            return update_dict  # update_dict is a string
    except ProgrammingError as e:
        logger('AdminLib', 'update_row ProgrammingError in __update_row_dict', str(e))
        return 'SQLAlchemy ProgrammingError: ' + str(e)

    try:
        __update_row(table, table_name, uids, update_dict)

    except IntegrityError as e:
        logger('AdminLib', 'update_row IntegrityError', str(e))
        return 'SQLAlchemy IntegrityError: ' + str(e)
    except ProgrammingError as e:
        logger('AdminLib', 'update_row ProgrammingError', str(e))
        return 'SQLAlchemy ProgrammingError: ' + str(e)

    DBDiscussionSession.flush()
    transaction.commit()
    return ''


def delete_row(table_name, uids, nickname, _tn):
    """
    Deletes a row in a table

    :param table_name: Name of the table
    :param uids: Array with uids
    :param nickname: Current nickname of the user
    :param _tn: Translator
    :return: Empty string or error message
    """
    logger('AdminLib', 'delete_row', table_name + ' ' + str(uids) + ' ' + nickname)
    if not is_user_admin(nickname):
        return _tn.get(_.noRights)

    if not table_name.lower() in table_mapper:
        return _tn.get(_.internalKeyError)

    table = table_mapper[table_name.lower()]['table']
    try:
        # check if there is a table, where uid is not the PK!
        if table_name.lower() == 'settings':
            uid = DBDiscussionSession.query(User).filter_by(nickname=uids[0]).first().uid
            DBDiscussionSession.query(table).filter_by(author_uid=uid).delete()
        elif table_name.lower() == 'premise':
            DBDiscussionSession.query(table).filter(Premise.premisesgroup_uid == uids[0],
                                                    Premise.statement_uid == uids[1]).delete()
        else:
            DBDiscussionSession.query(table).filter_by(uid=uids[0]).delete()

    except IntegrityError as e:
        logger('AdminLib', 'delete_row IntegrityError', str(e))
        return 'SQLAlchemy IntegrityError: ' + str(e)
    except ProgrammingError as e:
        logger('AdminLib', 'delete_row ProgrammingError', str(e))
        return 'SQLAlchemy ProgrammingError: ' + str(e)

    DBDiscussionSession.flush()
    transaction.commit()
    return ''


def add_row(table_name, data, nickname, _tn):
    """
    Updates data of a row in the table

    :param table_name: Name of the table
    :param data: Dictionary with data for teh update
    :param nickname: Current nickname of the user
    :param _tn: Translator
    :return: Empty string or error message
    """
    logger('AdminLib', 'add_row', str(data))
    if not is_user_admin(nickname):
        return _tn.get(_.noRights)

    if not table_name.lower() in table_mapper:
        return _tn.get(_.internalKeyError)

    table = table_mapper[table_name.lower()]['table']
    try:
        if 'uid' in data:
            del data['uid']
        new_one = table(**data)
        DBDiscussionSession.add(new_one)
    except IntegrityError as e:
        logger('AdminLib', 'add_row IntegrityError', str(e))
        return 'SQLAlchemy IntegrityError: ' + str(e)

    DBDiscussionSession.flush()
    transaction.commit()
    return ''


def update_badge(nickname, _tn):
    """
    Returns the new count for the badge of every table

    :param nickname: Current nickname of the user
    :param _tn: Translator
    :return: dict(), string
    """
    logger('AdminLib', 'update_badge', '')
    if not is_user_admin(nickname):
        return None, _tn.get(_.noRights)
    ret_array = []
    for t in table_mapper:
        ret_array.append({
            'name': table_mapper[t]['name'],
            'count': DBDiscussionSession.query(table_mapper[t]['table']).count()
        })

    return ret_array, ''


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
            tmp_key, tmp_val, error = __get_int_data(key, values[index], _tn)
            if error:
                return tmp_key, tmp_val
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

    return update_dict, True


def __get_int_data(key, val, _tn):
    # check for foreign key of author or language
    if key in _user_columns:
        # clear key / cut "(uid)"
        val = val[:val.rfind(" (")]
        db_user = DBDiscussionSession.query(User).filter_by(nickname=val).first()
        if not db_user:
            return _tn.get(_.userNotFound), '', True
        return key, db_user.uid

    elif key == 'lang_uid':
        db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=val).first()
        if not db_lang:
            return _tn.get(_.userNotFound), '', True
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
        DBDiscussionSession.query(table).filter(Premise.premisesgroup_uid == uids[0],
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

    return hashed_token[:5] + "-" + token


def __hash_token_with_owner(owner, token):
    return hashlib.sha256((owner + token).encode()).hexdigest()


def check_token(token: str) -> bool:
    """
    Checks if a token is valid or not.

    :param token: The token to check.
    :return: True if the token is valid and not disabled.
    """

    token_components = token.split("-")
    if len(token_components) is 2:
        hash_identifier, auth_token = token_components

        api_tokens = DBDiscussionSession.query(APIToken) \
            .filter(and_(APIToken.token.startswith(hash_identifier),
                         APIToken.disabled == False))

        for api_token in api_tokens:
            return __hash_token_with_owner(api_token.owner, auth_token) == api_token.token

    return False
