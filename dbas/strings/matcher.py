"""
Provides methods for comparing strings.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import difflib
from itertools import islice

from collections import OrderedDict
from sqlalchemy import and_, func
from Levenshtein import distance

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, User, TextVersion, Issue
from dbas.user_management import get_public_profile_picture
from dbas.database.initializedb import nick_of_anonymous_user

list_length = 5
max_count_zeros = 5
index_zeros = 3
return_count = 10  # same number as in googles suggest list (16.12.2015)
mechanism = 'Levensthein'
# mechanism = 'SequenceMatcher'


def get_strings_for_start(value, issue, is_startpoint):
    """
    Checks different position-strings for a match with given value

    :param value: string
    :param issue: int
    :param is_startpoint: boolean
    :return: dict()
    """
    db_statements = DBDiscussionSession.query(Statement).filter(and_(Statement.is_startpoint == is_startpoint, Statement.issue_uid == issue)).all()
    return_array = []
    index = 1
    for statement in db_statements:
        db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=statement.textversion_uid).first()
        if value.lower() in db_textversion.content.lower():
            dist = get_distance(value, db_textversion.content)
            return_array.append({'index': 0,
                                 'distance': dist,
                                 'text': db_textversion.content,
                                 'statement_uid': db_textversion.statement_uid})
            index += 1

    return_array = __sort_array(return_array)

    # logger('fuzzy_string_matcher', 'get_strings_for_start', 'dictionary length: ' + str(len(return_array)), debug=True)

    return mechanism, return_array[:list_length]


def get_strings_for_edits(value, statement_uid):
    """
    Checks different textversion-strings for a match with given value

    :param value: string
    :param statement_uid:
    :return: dict()
    """

    # db_statement = DBDiscussionSession.query(Statement).filter(and_(Statement.uid == statement_uid,
    #                                                                Statement.issue_uid == issue)).first()
    # db_textversions = DBDiscussionSession.query(TextVersion).filter_by(uid=db_statement.textversion_uid).join(User).all()
    db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).all()

    return_array = []
    index = 1
    for textversion in db_textversions:
        if value.lower() in textversion.content.lower():
            dist = get_distance(value, textversion.content)
            return_array.append({'index': 0,
                                 'distance': dist,
                                 'text': textversion.content,
                                 'statement_uid': textversion.statement_uid})
            index += 1

    return_array = __sort_array(return_array)

    # logger('fuzzy_string_matcher', 'get_strings_for_edits', 'string: ' + value + ', string: ' + value +
    #        ', statement uid: ' + str(statement_uid) + ', dictionary length: ' + str(len(return_array)), debug=True)

    return mechanism, return_array[:list_length]


def get_strings_for_reasons(value, issue):
    """
    Checks different textversion-strings for a match with given value

    :param value: string
    :param issue: int
    :return: dict()
    """
    db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
    return_array = []

    index = 1
    for statement in db_statements:
        db_textversion = DBDiscussionSession.query(TextVersion).filter_by(uid=statement.textversion_uid).first()
        if value.lower() in db_textversion.content.lower():
            dist = get_distance(value, db_textversion.content)
            return_array.append({'index': 0,
                                 'distance': dist,
                                 'text': db_textversion.content,
                                 'statement_uid': db_textversion.statement_uid})
            index += 1

    return_array = __sort_array(return_array)

    # logger('fuzzy_string_matcher', 'get_strings_for_reasons', 'string: ' + value + ', issue: ' + str(issue) +
    #        ', dictionary length: ' + str(len(return_array)), debug=True)

    return mechanism, return_array[:list_length]


def get_strings_for_issues(value):
    """
    Checks different issue-strings for a match with given value

    :param value:
    :return:
    """
    db_issues = DBDiscussionSession.query(Issue).all()
    return_array = []

    for index, issue in enumerate(db_issues):
        dist = get_distance(value, issue.title)
        return_array.append({'index': 0,
                             'distance': dist,
                             'text': issue.title})

    return_array = __sort_array(return_array)

    # logger('fuzzy_string_matcher', 'get_strings_for_issues', 'string: ' + value +
    #        ', dictionary length: ' + str(len(return_array)), debug=True)

    return mechanism, return_array[:list_length]


def get_strings_for_search(value):
    """
    Returns all statements which have a substring of the given value

    :param value: String
    :return: dict() with Statements.uid as key and 'text', 'distance' as well as 'arguments' as values
    """
    tmp_dict = OrderedDict()
    db_statements = DBDiscussionSession.query(Statement).join(TextVersion, Statement.textversion_uid == TextVersion.uid).all()
    for statement in db_statements:
        if value.lower() in statement.textversions.content.lower():
            # get distance between input value and saved value
            dist = get_distance(value, statement.textversions.content.lower())
            tmp_dict[str(statement.uid)] = {'text': statement.textversions.content,
                                            'distance': dist,
                                            'statement': statement.uid}

    tmp_dict = __sort_dict(tmp_dict)
    return_index = list(islice(tmp_dict, list_length))
    return_dict = OrderedDict()
    for index in return_index:
        return_dict[index] = tmp_dict[index]
    return return_dict


def get_strings_for_public_nickname(value, nickname):
    """

    :param value:
    :param nickname:
    :return:
    """
    db_user = DBDiscussionSession.query(User).filter(func.lower(User.public_nickname).contains(func.lower(value)),
                                                     ~User.public_nickname.in_([nickname, 'admin', nick_of_anonymous_user])).all()
    return_array = []

    for index, user in enumerate(db_user):
        dist = get_distance(value, user.public_nickname)
        return_array.append({'index': index,
                             'distance': dist,
                             'text': user.public_nickname,
                             'avatar': get_public_profile_picture(user)})

    return_array = __sort_array(return_array)
    return mechanism, return_array[:list_length]


def __sort_array(list):
    return_list = []
    newlist = sorted(list, key=lambda k: k['distance'])

    if mechanism == 'SequenceMatcher':  # sort descending
        newlist = list(reversed(newlist))

    # add index
    for index, dict in enumerate(newlist):
        dict['index'] = index
        return_list.append(dict)

    return return_list


def __sort_dict(dictionary):
    """
    :return:
    """
    dictionary = OrderedDict(sorted(dictionary.items()))
    return_dict = OrderedDict()
    for i in list(dictionary.keys())[0:return_count]:
        return_dict[i] = dictionary[i]
    if mechanism == 'SequenceMatcher':  # sort descending
        return_dict = OrderedDict(sorted(dictionary.items(), key=lambda kv: kv[0], reverse=True))
    else:  # sort ascending
        return_dict = OrderedDict()
        for i in list(dictionary.keys())[0:return_count]:
            return_dict[i] = dictionary[i]
    return return_dict


def get_distance(string_a, string_b):
    """

    :param string_a:
    :param string_b:
    :return:
    """
    # logger('fuzzy_string_matcher', 'get_distance', string_a + ' - ' + string_b)
    if mechanism == 'Levensthein':
        dist = distance(string_a.lower(), string_b.lower())
        #  logger('fuzzy_string_matcher', 'get_distance', 'levensthein: ' + str(dist) + ', value: ' + string_a.lower() + ' in: ' + string_b.lower())
    else:
        matcher = difflib.SequenceMatcher(lambda x: x == " ", string_a.lower(), string_b.lower())
        dist = str(round(matcher.ratio() * 100, 1))[:-2]
        # logger('fuzzy_string_matcher', 'get_distance', 'SequenceMatcher: ' + str(matcher.ratio()) + ', value: ' + string_a.lower() + ' in: ' +  string_b.lower())

    return str(dist).zfill(max_count_zeros)
