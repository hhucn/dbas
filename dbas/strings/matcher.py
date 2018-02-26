"""
Provides methods for comparing strings.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import difflib
from collections import OrderedDict
from itertools import islice

from Levenshtein import distance
from sqlalchemy import and_, func

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, User, TextVersion, Issue
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.helper.views import get_nickname
from dbas.lib import get_public_profile_picture
from dbas.query_wrapper import get_not_disabled_statement_as_query
from dbas.strings.keywords import Keywords as _
from dbas.url_manager import UrlManager
from search.requester import get_suggestions, get_edits, get_duplicates_or_reasons, get_statements_with_value

list_length = 5
max_count_zeros = 5
index_zeros = 3
return_count = 10  # same number as in googles suggest list (16.12.2015)
mechanism = 'Levensthein'
elastic = 'ElasticSearch'


# mechanism = 'SequenceMatcher'


def get_prediction(_tn, for_api, api_data, request_authenticated_userid, issue_uid, application_url, value, mode, issue,
                   extra=None):
    """
    Get dictionary with matching words, based on the given mode

    :param _tn: Translator
    :param for_api: Boolean
    :param api_data: data from the api
    :param request_authenticated_userid: users nickname
    :param issue_uid: issue_uid
    :param application_url: application_url
    :param value: users value, which should be the base for searching
    :param mode: int
    :param issue: Issue.uid
    :param extra: Array
    :return: Dictionary
    """

    return_dict = {}

    if mode in ['0', '2']:
        search = get_suggestions(issue_uid, (False, True)[mode == '0'], value)
        levensthein = get_strings_for_start(value, issue, (False, True)[mode == '0'])
        return_dict['values'], return_dict['distance_name'] = __get_result_or_fallback(search, levensthein)

    elif mode == '1':  # edit statement popup
        search = get_edits(issue_uid, extra, value)
        levensthein = get_strings_for_edits(value, extra)
        return_dict['values'], return_dict['distance_name'] = __get_result_or_fallback(search, levensthein)

    elif mode == '3' or mode == '4':  # adding reasons / duplicates
        try:
            uid = int(extra)
        except (TypeError, ValueError):
            uid = None

        search = get_duplicates_or_reasons(issue_uid, uid, value)
        levensthein = get_strings_for_duplicates_or_reasons(value, issue, uid)
        return_dict['values'], return_dict['distance_name'] = __get_result_or_fallback(search, levensthein)

    elif mode == '5':  # getting public nicknames
        nickname = get_nickname(request_authenticated_userid, for_api, api_data)
        return_dict['values'] = get_strings_for_public_nickname(value, nickname)
        return_dict['distance_name'] = mechanism

    elif mode in ['8', '9']:
        search = get_statements_with_value(issue_uid, application_url, value)
        levensthein = get_all_statements_with_value(issue_uid, application_url, value)
        return_dict['values'], return_dict['distance_name'] = __get_result_or_fallback(search, levensthein)

    else:
        return_dict = {'error': _tn.get(_.internalError)}

    return return_dict


def __get_result_or_fallback(elastic_search, levensthein_search):
    if elastic_search is None or len(elastic_search) == 0:
        return levensthein_search, mechanism
    return elastic_search, elastic


def get_all_statements_with_value(issue_uid, application_url, value):
    """
    Returns all statements, where with the value

    :param issue_uid: issue_uid
    :param application_url: application_url
    :param value: string
    :return: dict()
    """
    db_statements = get_not_disabled_statement_as_query().filter_by(issue_uid=issue_uid).all()
    return_array = []
    slug = DBDiscussionSession.query(Issue).get(issue_uid).slug
    _um = UrlManager(application_url, for_api=False, slug=slug)
    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=stat.uid).order_by(
            TextVersion.uid.asc()).first()
        if value.lower() in db_tv.content.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=db_tv.content, uid=db_tv.statement_uid)
            rd['url'] = _um.get_url_for_statement_attitude(False, db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:list_length]


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
        db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=stat.uid).order_by(
            TextVersion.uid.asc()).first()
        if value.lower() in db_tv.content.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=db_tv.content, uid=db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:list_length]


def get_strings_for_edits(value, statement_uid):
    """
    Checks different textversion-strings for a match with given value

    :param value: string
    :param statement_uid: Statement.uid
    :return: dict()
    """

    db_tvs = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).all()  # TODO #432

    return_array = []
    index = 1
    for textversion in db_tvs:
        if value.lower() in textversion.content.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=textversion.content,
                                         uid=textversion.statement_uid)  # TODO #432
            return_array.append(rd)
            index += 1

    return_array = __sort_array(return_array)

    return return_array[:list_length]


def get_strings_for_duplicates_or_reasons(value, issue, oem_value_uid=None):
    """
    Checks different textversion-strings for a match with given value

    :param value: string
    :param issue: Issue.uid
    :param oem_value_uid: integer
    :return: dict()
    """

    db_statements = get_not_disabled_statement_as_query().filter(and_(Statement.issue_uid == issue,
                                                                      Statement.uid != oem_value_uid)).all()
    return_array = []

    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=stat.uid).order_by(
            TextVersion.uid.asc()).first()
        if value.lower() in db_tv.content.lower():
            rd = __get_fuzzy_string_dict(current_text=value, return_text=db_tv.content,
                                         uid=db_tv.statement_uid)  # TODO #432
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:list_length]


def get_strings_for_issues(value):
    """
    Checks different issue-strings for a match with given value

    :param value: string
    :return: dict()
    """
    db_issues = DBDiscussionSession.query(Issue).all()
    return_array = []

    for index, issue in enumerate(db_issues):
        rd = __get_fuzzy_string_dict(current_text=value, return_text=issue.title)
        return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:list_length]


def get_strings_for_search(value):
    """
    Returns all statements which have a substring of the given value

    :param value: String
    :return: dict() with Statements.uid as key and 'text', 'distance' as well as 'arguments' as values
    """
    tmp_dict = OrderedDict()
    db_statements = get_not_disabled_statement_as_query().join(TextVersion,
                                                               Statement.textversion_uid == TextVersion.uid).all()
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
    Returns dictionary with index, distance, text and statement_uid as keys

    :param index: int
    :param current_text: string
    :param return_text: string
    :param uid: int
    :return: dict()
    """
    return {'index': index,
            'distance': get_distance(current_text.lower(), return_text.lower()),
            'text': return_text,
            'statement_uid': uid}


def get_strings_for_public_nickname(value, nickname):
    """
    Returns dictionaries with public nicknames of users, where the nickname containts the value

    :param value: String
    :param nickname: current users nickname
    :return: dict()
    """
    db_user = DBDiscussionSession.query(User).filter(func.lower(User.public_nickname).contains(func.lower(value)),
                                                     ~User.public_nickname.in_(
                                                         [nickname, 'admin', nick_of_anonymous_user])).all()
    return_array = []

    for index, user in enumerate(db_user):
        dist = get_distance(value, user.public_nickname)
        return_array.append({'index': index,
                             'distance': dist,
                             'text': user.public_nickname,
                             'avatar': get_public_profile_picture(user)})

    return_array = __sort_array(return_array)
    return return_array[:list_length]


def __sort_array(list):
    """
    Returns sorted array, based on the distance

    :param list: Array
    :return: Array
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
    Returns sorted dictionary, based on the distance

    :param dictionary: dict()
    :return: dict()
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
    Returns the distance between two string. Distance is based on Levensthein or difflibs Sequence Matcher

    :param string_a: String
    :param string_b: String
    :return: distance as zero filled string
    """
    # logger('fuzzy_string_matcher', 'get_distance', string_a + ' - ' + string_b)
    if mechanism == 'Levensthein':
        return get_lev_distance(string_a, string_b)
    else:
        return get_difflib_distance(string_a, string_b)


def get_lev_distance(a, b):
    """
    Returns the levensthein distance between to strings

    :param a: first string
    :param b: second string
    :return: distance between a and b
    """
    dist = distance(a.strip().lower(), b.strip().lower())
    #  logger('fuzzy_string_matcher', 'get_distance', 'levensthein: ' + str(dist) + ', value: ' + a.lower() + ' in: ' + b.lower())
    return str(dist).zfill(max_count_zeros)


def get_difflib_distance(a, b):
    """
    Returns the difflib distance between to strings

    :param a: first string
    :param b: second string
    :return: distance between a and b
    """
    matcher = difflib.SequenceMatcher(lambda x: x == " ", a.lower(), b.lower())
    dist = str(round(matcher.ratio() * 100, 1))[:-2]
    # logger('fuzzy_string_matcher', 'get_distance', 'SequenceMatcher: ' + str(matcher.ratio()) + ', value: ' + a.lower() + ' in: ' +  b.lower())
    return str(dist).zfill(max_count_zeros)
