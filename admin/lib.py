# Common library for Admin Component
#
# @author Tobias Krauthoff
# @email krautho66@cs.uni-duesseldorf.de


import arrow
import transaction
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, StatementReferences, \
    StatementSeenBy, ArgumentSeenBy, TextVersion, PremiseGroup, Premise, Argument, History, VoteArgument, VoteStatement, \
    Message, ReviewDelete, ReviewEdit, ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, \
    LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, OptimizationReviewLocks, \
    ReviewCanceled, RevokedContent, RevokedContentHistory
from dbas.lib import get_profile_picture, is_user_admin
from dbas.logger import logger
from dbas.strings.keywords import Keywords as _
from sqlalchemy.exc import IntegrityError, ProgrammingError

table_mapper = {
    'Issue'.lower(): {'table': Issue, 'name': 'Issue'},
    'Language'.lower(): {'table': Language, 'name': 'Language'},
    'Group'.lower(): {'table': Group, 'name': 'Group'},
    'User'.lower(): {'table': User, 'name': 'User'},
    'Settings'.lower(): {'table': Settings, 'name': 'Settings'},
    'Statement'.lower(): {'table': Statement, 'name': 'Statement'},
    'StatementReferences'.lower(): {'table': StatementReferences, 'name': 'StatementReferences'},
    'StatementSeenBy'.lower(): {'table': StatementSeenBy, 'name': 'StatementSeenBy'},
    'ArgumentSeenBy'.lower(): {'table': ArgumentSeenBy, 'name': 'ArgumentSeenBy'},
    'TextVersion'.lower(): {'table': TextVersion, 'name': 'TextVersion'},
    'PremiseGroup'.lower(): {'table': PremiseGroup, 'name': 'PremiseGroup'},
    'Premise'.lower(): {'table': Premise, 'name': 'Premise'},
    'Argument'.lower(): {'table': Argument, 'name': 'Argument'},
    'History'.lower(): {'table': History, 'name': 'History'},
    'VoteArgument'.lower(): {'table': VoteArgument, 'name': 'VoteArgument'},
    'VoteStatement'.lower(): {'table': VoteStatement, 'name': 'VoteStatement'},
    'Message'.lower(): {'table': Message, 'name': 'Message'},
    'ReviewDelete'.lower(): {'table': ReviewDelete, 'name': 'ReviewDelete'},
    'ReviewEdit'.lower(): {'table': ReviewEdit, 'name': 'ReviewEdit'},
    'ReviewEditValue'.lower(): {'table': ReviewEditValue, 'name': 'ReviewEditValue'},
    'ReviewOptimization'.lower(): {'table': ReviewOptimization, 'name': 'ReviewOptimization'},
    'ReviewDeleteReason'.lower(): {'table': ReviewDeleteReason, 'name': 'ReviewDeleteReason'},
    'LastReviewerDelete'.lower(): {'table': LastReviewerDelete, 'name': 'LastReviewerDelete'},
    'LastReviewerEdit'.lower(): {'table': LastReviewerEdit, 'name': 'LastReviewerEdit'},
    'LastReviewerOptimization'.lower(): {'table': LastReviewerOptimization, 'name': 'LastReviewerOptimization'},
    'ReputationHistory'.lower(): {'table': ReputationHistory, 'name': 'ReputationHistory'},
    'ReputationReason'.lower(): {'table': ReputationReason, 'name': 'ReputationReason'},
    'OptimizationReviewLocks'.lower(): {'table': OptimizationReviewLocks, 'name': 'OptimizationReviewLocks'},
    'ReviewCanceled'.lower(): {'table': ReviewCanceled, 'name': 'ReviewCanceled'},
    'RevokedContent'.lower(): {'table': RevokedContent, 'name': 'RevokedContent'},
    'RevokedContentHistory'.lower(): {'table': RevokedContentHistory, 'name': 'RevokedContentHistory'}
}

google_colors = [
    ['#f44336', '#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350', '#f44336', '#e53935', '#d32f2f', '#c62828', '#b71c1c', '#ff8a80', '#ff5252', '#ff1744', '#d50000'],  # red
    ['#e91e63', '#fce4ec', '#f8bbd0', '#f48fb1', '#f06292', '#ec407a', '#e91e63', '#d81b60', '#c2185b', '#ad1457', '#880e4f', '#ff80ab', '#ff4081', '#f50057', '#c51162'],  # pink
    ['#9c27b0', '#f3e5f5', '#e1bee7', '#ce93d8', '#ba68c8', '#ab47bc', '#9c27b0', '#8e24aa', '#7b1fa2', '#6a1b9a', '#4a148c', '#ea80fc', '#e040fb', '#d500f9', '#aa00ff'],  # purple
    ['#673ab7', '#ede7f6', '#d1c4e9', '#b39ddb', '#9575cd', '#7e57c2', '#673ab7', '#5e35b1', '#512da8', '#4527a0', '#311b92', '#b388ff', '#7c4dff', '#651fff', '#6200ea'],  # deep purple
    ['#3f51b5', '#e8eaf6', '#c5cae9', '#9fa8da', '#7986cb', '#5c6bc0', '#3f51b5', '#3949ab', '#303f9f', '#283593', '#1a237e', '#8c9eff', '#536dfe', '#3d5afe', '#304ffe'],  # indigo
    ['#2196f3', '#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1', '#82b1ff', '#448aff', '#2979ff', '#2962ff'],  # blue
    ['#03a9f4', '#e1f5fe', '#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#03a9f4', '#039be5', '#0288d1', '#0277bd', '#01579b', '#80d8ff', '#40c4ff', '#00b0ff', '#0091ea'],  # light blue
    ['#00bcd4', '#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1', '#26c6da', '#00bcd4', '#00acc1', '#0097a7', '#00838f', '#006064', '#84ffff', '#18ffff', '#00e5ff', '#00b8d4'],  # cyan
    ['#009688', '#e0f2f1', '#b2dfdb', '#80cbc4', '#4db6ac', '#26a69a', '#009688', '#00897b', '#00796b', '#00695c', '#004d40', '#a7ffeb', '#64ffda', '#1de9b6', '#00bfa5'],  # teal
    ['#4caf50', '#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50', '#43a047', '#388e3c', '#2e7d32', '#1b5e20', '#b9f6ca', '#69f0ae', '#00e676', '#00c853'],  # green
    ['#8bc34a', '#f1f8e9', '#dcedc8', '#c5e1a5', '#aed581', '#9ccc65', '#8bc34a', '#7cb342', '#689f38', '#558b2f', '#33691e', '#ccff90', '#b2ff59', '#76ff03', '#64dd17'],  # light green
    ['#cddc39', '#f9fbe7', '#f0f4c3', '#e6ee9c', '#dce775', '#d4e157', '#cddc39', '#c0ca33', '#afb42b', '#9e9d24', '#827717', '#f4ff81', '#eeff41', '#c6ff00', '#aeea00'],  # lime
    ['#ffeb3b', '#fffde7', '#fff9c4', '#fff59d', '#fff176', '#ffee58', '#ffeb3b', '#fdd835', '#fbc02d', '#f9a825', '#f57f17', '#ffff8d', '#ffff00', '#ffea00', '#ffd600'],  # yellow
    ['#ffc107', '#fff8e1', '#ffecb3', '#ffe082', '#ffd54f', '#ffca28', '#ffc107', '#ffb300', '#ffa000', '#ff8f00', '#ff6f00', '#ffe57f', '#ffd740', '#ffc400', '#ffab00'],  # amber
    ['#ff9800', '#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726', '#ff9800', '#fb8c00', '#f57c00', '#ef6c00', '#e65100', '#ffd180', '#ffab40', '#ff9100', '#ff6d00'],  # orange
    ['#ff5722', '#fbe9e7', '#ffccbc', '#ffab91', '#ff8a65', '#ff7043', '#ff5722', '#f4511e', '#e64a19', '#d84315', '#bf360c', '#ff9e80', '#ff6e40', '#ff3d00', '#dd2c00'],  # deep orange
    ['#795548', '#efebe9', '#d7ccc8', '#bcaaa4', '#a1887f', '#8d6e63', '#795548', '#6d4c41', '#5d4037', '#4e342e', '#3e2723'],  # brown
    ['#9e9e9e', '#fafafa', '#f5f5f5', '#eeeeee', '#e0e0e0', '#bdbdbd', '#9e9e9e', '#757575', '#616161', '#424242', '#212121'],  # grey
    ['#607d8b', '#eceff1', '#cfd8dc', '#b0bec5', '#90a4ae', '#78909c', '#607d8b', '#546e7a', '#455a64', '#37474f', '#263238'],  # blue grey
    ['#000000'],  # black
    ['#ffffff']]  # white

# list of all columns with FK of users table
_user_columns = ['author_uid', 'reputator_uid', 'reviewer_uid']

# list of all columns, which will not be displayed
_forbidden_columns = ['token', 'token_timestamp']


def get_overview(page):
    """
    Returns a nested data structure with information about the database

    :param page: Name of the main page
    :return:[[{'name': .., 'content': [{'name': .., 'count': .., 'href': ..}, ..] }], ..]
    """
    logger('AdminLib', 'get_dashboard_infos', 'main')
    return_list = list()

    # all tables for the 'general' group
    general = list()
    general.append(__get_dash_dict(len(DBDiscussionSession.query(Issue).all()), 'Issue', page + 'Issue'))
    general.append(__get_dash_dict(len(DBDiscussionSession.query(Language).all()), 'Language', page + 'Language'))
    general.append(__get_dash_dict(len(DBDiscussionSession.query(History).all()), 'History', page + 'History'))

    # all tables for the 'users' group
    users = list()
    users.append(__get_dash_dict(len(DBDiscussionSession.query(Group).all()), 'Group', page + 'Group'))
    users.append(__get_dash_dict(len(DBDiscussionSession.query(User).all()), 'User', page + 'User'))
    users.append(__get_dash_dict(len(DBDiscussionSession.query(Settings).all()), 'Settings', page + 'Settings'))
    users.append(__get_dash_dict(len(DBDiscussionSession.query(Message).all()), 'Message', page + 'Message'))

    # all tables for the 'content' group
    content = list()
    content.append(__get_dash_dict(len(DBDiscussionSession.query(Statement).all()), 'Statement', page + 'Statement'))
    content.append(__get_dash_dict(len(DBDiscussionSession.query(TextVersion).all()), 'TextVersion', page + 'TextVersion'))
    content.append(__get_dash_dict(len(DBDiscussionSession.query(StatementReferences).all()), 'StatementReferences', page + 'StatementReferences'))
    content.append(__get_dash_dict(len(DBDiscussionSession.query(PremiseGroup).all()), 'PremiseGroup', page + 'PremiseGroup'))
    content.append(__get_dash_dict(len(DBDiscussionSession.query(Premise).all()), 'Premise', page + 'Premise'))
    content.append(__get_dash_dict(len(DBDiscussionSession.query(Argument).all()), 'Argument', page + 'Argument'))

    # all tables for the 'voting' group
    voting = list()
    voting.append(__get_dash_dict(len(DBDiscussionSession.query(VoteArgument).all()), 'VoteArgument', page + 'VoteArgument'))
    voting.append(__get_dash_dict(len(DBDiscussionSession.query(VoteStatement).all()), 'VoteStatement', page + 'VoteStatement'))
    voting.append(__get_dash_dict(len(DBDiscussionSession.query(StatementSeenBy).all()), 'StatementSeenBy', page + 'StatementSeenBy'))
    voting.append(__get_dash_dict(len(DBDiscussionSession.query(ArgumentSeenBy).all()), 'ArgumentSeenBy', page + 'ArgumentSeenBy'))

    # all tables for the 'reviews' group
    reviews = list()
    reviews.append(__get_dash_dict(len(DBDiscussionSession.query(ReviewDelete).all()), 'ReviewDelete', page + 'ReviewDelete'))
    reviews.append(__get_dash_dict(len(DBDiscussionSession.query(ReviewEdit).all()), 'ReviewEdit', page + 'ReviewEdit'))
    reviews.append(__get_dash_dict(len(DBDiscussionSession.query(ReviewEditValue).all()), 'ReviewEditValue', page + 'ReviewEditValue'))
    reviews.append(__get_dash_dict(len(DBDiscussionSession.query(ReviewOptimization).all()), 'ReviewOptimization', page + 'ReviewOptimization'))
    reviews.append(__get_dash_dict(len(DBDiscussionSession.query(ReviewDeleteReason).all()), 'ReviewDeleteReason', page + 'ReviewDeleteReason'))

    # all tables for the 'reviewer' group
    reviewer = list()
    reviewer.append(__get_dash_dict(len(DBDiscussionSession.query(LastReviewerDelete).all()), 'LastReviewerDelete', page + 'LastReviewerDelete'))
    reviewer.append(__get_dash_dict(len(DBDiscussionSession.query(LastReviewerEdit).all()), 'LastReviewerEdit', page + 'LastReviewerEdit'))
    reviewer.append(__get_dash_dict(len(DBDiscussionSession.query(LastReviewerOptimization).all()), 'LastReviewerOptimization', page + 'LastReviewerOptimization'))

    # all tables for the 'reputation' group
    reputation = list()
    reputation.append(__get_dash_dict(len(DBDiscussionSession.query(ReputationHistory).all()), 'ReputationHistory', page + 'ReputationHistory'))
    reputation.append(__get_dash_dict(len(DBDiscussionSession.query(ReputationReason).all()), 'ReputationReason', page + 'ReputationReason'))
    reputation.append(__get_dash_dict(len(DBDiscussionSession.query(OptimizationReviewLocks).all()), 'OptimizationReviewLocks', page + 'OptimizationReviewLocks'))
    reputation.append(__get_dash_dict(len(DBDiscussionSession.query(ReviewCanceled).all()), 'ReviewCanceled', page + 'ReviewCanceled'))
    reputation.append(__get_dash_dict(len(DBDiscussionSession.query(RevokedContent).all()), 'RevokedContent', page + 'RevokedContent'))
    reputation.append(__get_dash_dict(len(DBDiscussionSession.query(RevokedContentHistory).all()), 'RevokedContentHistory', page + 'RevokedContentHistory'))

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
    :params main_page: URL
    :return: Dictionary with head, row, count and has_elements
    """
    logger('AdminLib', 'get_table_dict', str(table_name))
    return_dict = dict()

    # check for table
    if not table_name.lower() in table_mapper:
        return_dict['is_existing'] = False
        return return_dict
    return_dict['is_existing'] = True
    return_dict['name'] = table_name

    # check for elements
    db_elements = DBDiscussionSession.query(table_mapper[table_name.lower()]['table']).all()
    return_dict['count'] = len(db_elements)
    if len(db_elements) == 0:
        return_dict['has_elements'] = False
        return return_dict
    return_dict['has_elements'] = True

    # getting all keys
    table = table_mapper[table_name.lower()]['table']
    columns = [r.key for r in table.__table__.columns]
    # remove all unnecessary columns
    for bad in _forbidden_columns:
        if bad in columns:
            columns.remove(bad)

    # getting data
    # data = [[str(getattr(row, c.name)) for c in row.__table__.columns] for row in db_elements]
    data = __get_rows_of(columns, db_elements, main_page)

    # save it
    return_dict['head'] = columns
    return_dict['row'] = data

    return return_dict


def __get_language(uid, query):
    """
    Returns ui_locales of a language

    :param uid: of language
    :param query: of all languages
    :return: string
    """
    return query.filter_by(uid=uid).first().ui_locales


def __get_author_data(uid, query, main_page):
    """
    Returns a-tag with gravatar of current author and users page as href

    :param uid: of user
    :param query: of all users
    :params main_page: URL
    :return: string
    """
    db_user = query.filter_by(uid=int(uid)).first()
    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=int(uid)).first()
    if not db_user:
        return 'Missing author with uid ' + str(uid), False
    if not db_settings:
        return 'Missing settings of author with uid ' + str(uid), False
    img = '<img class="img-circle" src="' + get_profile_picture(db_user, 20, True) + '">'

    link_begin = '<a href="' + main_page + '/user/' + db_user.get_global_nickname() + '">'
    link_end = '</a>'
    return link_begin + db_user.nickname + ' ' + img + link_end, True


def __get_dash_dict(count, name, href):
    """
    Returns dictionary with all attributes

    :param count: number of element in current table
    :param name: name of current table
    :param href: link for current table
    :return: {'count': count, 'name': name, 'href': href}
    """
    return {'count': count, 'name': name, 'href': href}


def __get_rows_of(columns, db_elements, main_page):
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
            # all keywords for getting a user
            if column in _user_columns:
                text, success = __get_author_data(attribute, db_users, main_page)
                if success:
                    tmp.append(text)
            # resolve language
            elif column == 'lang_uid':
                tmp.append(__get_language(attribute, db_languages))
            # resolve password
            elif column == 'password':
                tmp.append(str(attribute)[:5] + '...')
            else:
                tmp.append(str(attribute))
        data.append(tmp)
    return data


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
        # if current type is int
        if str(__find_type(table, key)) == 'INTEGER':
            # check for foreign key of author or language
            if key in _user_columns:
                db_user = DBDiscussionSession.query(User).filter_by(nickname=values[index]).first()
                if not db_user:
                    return _tn.get(_.userNotFound), False
                update_dict[key] = db_user.uid

            elif key == 'lang_uid':
                db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=values[index]).first()
                if not db_lang:
                    return _tn.get(_.userNotFound), False
                update_dict[key] = db_lang.uid

            else:
                update_dict[key] = int(values[index])

        # if current type is bolean
        elif str(__find_type(table, key)) == 'BOOLEAN':
            update_dict[key] = True if values[index].lower() == 'true' else False

        # if current type is text
        elif str(__find_type(table, key)) == 'TEXT':
            update_dict[key] = str(values[index])

        # if current type is date
        elif str(__find_type(table, key)) == 'ARROWTYPE':
            update_dict[key] = arrow.get(str(values[index]))

        else:
            update_dict[key] = values[index]

    return update_dict, True


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
