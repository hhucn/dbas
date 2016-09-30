# Common library for Admin Component
#
# @author Tobias Krautho66
# @email krautho66@cs.uni-duesseldorf.de

from random import randint

from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Issue, Language, Group, User, Settings, Statement, StatementReferences, StatementSeenBy, ArgumentSeenBy, TextVersion, PremiseGroup, Premise, Argument, History, VoteArgument, VoteStatement, Message, ReviewDelete, ReviewEdit, ReviewEditValue, ReviewOptimization, ReviewDeleteReason, LastReviewerDelete, LastReviewerEdit, LastReviewerOptimization, ReputationHistory, ReputationReason, OptimizationReviewLocks, ReviewCanceled, RevokedContent

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
    'RevokedContent'.lower(): {'table': RevokedContent, 'name': 'RevokedContent'}
}


def get_dashboard_infos(main_page):
    """

    :param main_page:
    :return:
    """
    logger('AdminLib', 'get_dashboard_infos', 'main')
    return_dict = list()

    tmp = list()
    for key in table_mapper:
        db_elements = DBDiscussionSession.query(table_mapper[key]['table']).all()
        tmp.append(__get_dash_dict(len(db_elements), table_mapper[key]['name'], main_page + table_mapper[key]['name'], __get_random_color()))

    row = list()
    for index, el in enumerate(tmp):
        if len(row) % 4 == 0:
            return_dict.append(row)
            row = list()
        row.append(el)

    if len(row) > 0:
        return_dict.append(row)

    return return_dict


def get_table_dict(table):
    """

    :param table:
    :return:
    """
    logger('AdminLib', 'get_table_dict', str(table))
    return_dict = dict()

    has_elements = table.lower() in table_mapper
    return_dict['has_elements'] = has_elements

    if not has_elements:
        return_dict['has_elements'] = False
        return return_dict

    db_elements = DBDiscussionSession.query(table_mapper[table.lower()]['table']).all()
    return_dict['has_elements'] = True

    return_dict['name'] = table if db_elements else 'unknown table'
    return_dict['count'] = len(db_elements) if db_elements else '-1'

    if db_elements:
        head = list()
        head.append('a')
        head.append('a')
        head.append('a')
        return_dict['head'] = head

    return return_dict


def __get_dash_dict(count, name, href, color):
    """

    :param count:
    :param name:
    :param href:
    :param color:
    :return:
    """
    return {
        'count': count,
        'name': name,
        'href': href,
        'style': 'background-color: ' + color
        }


def __get_random_color():
    """

    :return:
    """
    r = lambda: randint(100, 200)
    return '#%02X%02X%02X' % (r(), r(), r())
