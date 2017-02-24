"""
Provides methods for comparing strings.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import difflib
import json
from itertools import islice

from collections import OrderedDict
from sqlalchemy import and_, func
from Levenshtein import distance

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, User, TextVersion, Issue
from dbas.lib import get_public_profile_picture
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.helper.views import get_nickname
from dbas.strings.keywords import Keywords as _
from dbas.query_wrapper import get_not_disabled_statement_as_query
from dbas.url_manager import UrlManager
import dbas.helper.issue as issue_helper

list_length = 5
max_count_zeros = 5
index_zeros = 3
return_count = 10  # same number as in googles suggest list (16.12.2015)
mechanism = 'Levensthein'
# mechanism = 'SequenceMatcher'


def get_prediction(request, _tn, for_api, api_data, request_authenticated_userid, value, mode, issue, extra=None):
    """

    :param _tn:
    :param for_api:
    :param api_data:
    :param request_authenticated_userid:
    :param value:
    :param mode:
    :param issue:
    :param extra:
    :return:
    """

    return_dict = {}
    if mode == '0':  # start statement
        return_dict['distance_name'], return_dict['values'] = get_strings_for_start(value, issue, True)
    elif mode == '1':  # edit statement popup
        return_dict['distance_name'], return_dict['values'] = get_strings_for_edits(value, extra)
    elif mode == '2':  # start premise
        return_dict['distance_name'], return_dict['values'] = get_strings_for_start(value, issue, False)
    elif mode == '3':  # adding reasons
        global mechanism
        count, extra, mechanism = __get_vars_for_reasons(extra)
        return_dict['distance_name'], return_dict['values'] = get_strings_for_reasons(value, issue, count, extra[1])
    elif mode == '4':  # getting text
        return_dict = get_strings_for_search(value)
    elif mode == '5':  # getting public nicknames
        nickname = get_nickname(request_authenticated_userid, for_api, api_data)
        return_dict['distance_name'], return_dict['values'] = get_strings_for_public_nickname(value, nickname)
    elif mode == '9':  # search everything
        tmp, suggstions = get_all_strings_for(request, value)
        return_dict = {'suggestions': suggstions}
    else:
        return_dict = {'error': _tn.get(_.internalError)}

    return return_dict


def __get_vars_for_reasons(extra):
    """

    :param extra:
    :return:
    """
    global mechanism
    try:
        extra = json.loads(extra) if extra is not None else ['', '']
    except TypeError and json.JSONDecodeError:
        extra = ['', '']
    if isinstance(extra, list):
        mechanism = 'SequenceMatcher'
    else:
        extra = ['', '']
    count = 1000 if str(extra[0]) == 'all' else list_length
    return count, extra, mechanism


def get_all_strings_for(request, value):
    """
    Checks all statements

    :param request: request
    :param value: string
    """
    issue_uid = issue_helper.get_issue_id(request)
    db_statements = get_not_disabled_statement_as_query().filter_by(issue_uid=issue_uid).all()
    return_array = []
    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).get(stat.textversion_uid)
        if value.lower() in db_tv.content.lower():
            slug = DBDiscussionSession.query(Issue).get(stat.issue_uid).get_slug()
            _um = UrlManager(request.application_url, for_api=False, slug=slug)
            url = _um.get_url_for_statement_attitude(False, db_tv.statement_uid)
            return_array.append({'value': db_tv.content, 'data': url, 'distance': get_distance(value.lower(), db_tv.content.lower())})

    return_array = __sort_array(return_array)

    return mechanism, return_array[:list_length]


def get_strings_for_start(value, issue, is_startpoint):
    """
    Checks different position-strings for a match with given value

    :param value: string
    :param issue: int
    :param is_startpoint: boolean
    :return: dict()
    """
    db_statements = get_not_disabled_statement_as_query().filter(and_(Statement.is_startpoint == is_startpoint,
                                                                      Statement.issue_uid == issue)).all()
    return_array = []
    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).get(stat.textversion_uid)
        if value.lower() in db_tv.content.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=db_tv.content, uid=db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return mechanism, return_array[:list_length]


def get_strings_for_edits(value, statement_uid):
    """
    Checks different textversion-strings for a match with given value

    :param value: string
    :param statement_uid:
    :return: dict()
    """

    db_tvs = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).all()

    return_array = []
    index = 1
    for textversion in db_tvs:
        if value.lower() in textversion.content.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=textversion.content, uid=textversion.statement_uid)
            return_array.append(rd)
            index += 1

    return_array = __sort_array(return_array)

    return mechanism, return_array[:list_length]


def get_strings_for_reasons(value, issue, count=list_length, oem_value=''):
    """
    Checks different textversion-strings for a match with given value

    :param value: string
    :param issue: int
    :param issue: count
    :return: dict()
    """
    db_statements = get_not_disabled_statement_as_query().filter_by(issue_uid=issue).all()
    return_array = []

    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).get(stat.textversion_uid)
        if value.lower() in db_tv.content.lower() and db_tv.content.lower() != oem_value.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=db_tv.content, uid=db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    # logger('fuzzy_string_matcher', 'get_strings_for_reasons', 'string: ' + value + ', issue: ' + str(issue) +
    #        ', dictionary length: ' + str(len(return_array)), debug=True)

    return mechanism, return_array[:count]


def get_strings_for_issues(value):
    """
    Checks different issue-strings for a match with given value

    :param value:
    :return:
    """
    db_issues = DBDiscussionSession.query(Issue).all()
    return_array = []

    for index, issue in enumerate(db_issues):
        rd = __get_fuzzy_string_dict(current_text=value, return_text=issue.title)
        return_array.append(rd)

    return_array = __sort_array(return_array)

    return mechanism, return_array[:list_length]


def get_strings_for_search(value):
    """
    Returns all statements which have a substring of the given value

    :param value: String
    :return: dict() with Statements.uid as key and 'text', 'distance' as well as 'arguments' as values
    """
    tmp_dict = OrderedDict()
    db_statements = get_not_disabled_statement_as_query().join(TextVersion, Statement.textversion_uid == TextVersion.uid).all()
    for stat in db_statements:
        if value.lower() in stat.textversions.content.lower():
            # get distance between input value and saved value
            rd = __get_fuzzy_string_dict(current_text=value, return_text=stat.textversions.content, uid=stat.uid)
            tmp_dict[str(stat.uid)] = rd

    tmp_dict = __sort_dict(tmp_dict)
    return_index = list(islice(tmp_dict, list_length))
    return_dict = OrderedDict()
    for index in return_index:
        return_dict[index] = tmp_dict[index]
    return return_dict


def __get_fuzzy_string_dict(index=0, current_text='', return_text='', uid=0):
    """

    :param index:
    :param current_text:
    :param return_text:
    :param uid:
    :return:
    """
    return {'index': index,
            'distance': get_distance(current_text.lower(), return_text.lower()),
            'text': return_text,
            'statement_uid': uid}


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
    """

    :param list:
    :return:
    """
    return_list = []
    newlist = sorted(list, key=lambda k: k['distance'])

    if mechanism == 'SequenceMatcher':  # sort descending
        newlist = reversed(newlist)

    # add index
    for index, dict in enumerate(newlist):
        dict['index'] = index
        return_list.append(dict)

    return return_list


def __sort_dict(dictionary):
    """

    :param dictionary:
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
        dist = distance(string_a.strip().lower(), string_b.strip().lower())
        #  logger('fuzzy_string_matcher', 'get_distance', 'levensthein: ' + str(dist) + ', value: ' + string_a.lower() + ' in: ' + string_b.lower())
    else:
        matcher = difflib.SequenceMatcher(lambda x: x == " ", string_a.lower(), string_b.lower())
        dist = str(round(matcher.ratio() * 100, 1))[:-2]
        # logger('fuzzy_string_matcher', 'get_distance', 'SequenceMatcher: ' + str(matcher.ratio()) + ', value: ' + string_a.lower() + ' in: ' +  string_b.lower())

    return str(dist).zfill(max_count_zeros)
