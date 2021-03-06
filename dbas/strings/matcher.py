"""
Provides methods for comparing strings."""

import difflib
import logging
import operator
import re
from collections import OrderedDict
from itertools import islice

from Levenshtein import distance
from sqlalchemy import func

from api.models import DataStatement, DataIssue
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, User, TextVersion, Issue, StatementToIssue
from dbas.handler.history import get_seen_statements_from
from dbas.helper.url import UrlManager
from dbas.lib import nick_of_anonymous_user, get_enabled_statement_as_query, \
    get_profile_picture
from dbas.strings.fuzzy_modes import FuzzyMode
from search import SEARCH_HOST, SEARCH_PORT
from search.requester import elastic_search, get_statements_with_similarity_to
from search.routes import is_host_resolved, is_socket_open

LOG = logging.getLogger(__name__)
RESULT_LENGTH = 10  # same number as in googles suggest list (16.12.2015)
MECHANISM = 'Levensthein'
SIMILARITY_THRESHOLD_IN_PERCENT = 0.3


def get_nicknames(db_user: User, value: str):
    """
    :param db_user: The user which nickname shall be returned.
    :param value:
    :return:
    """
    return {
        'distance_name': MECHANISM,
        'values': get_strings_for_public_nickname(value, db_user.global_nickname)
    }


def get_prediction(db_user: User, db_issue: Issue, search_value: str, mode: int, statement_uid: int) -> dict:
    """
    Get dictionary with matching words, based on the given mode

    :param statement_uid: the uid of the statement to be looked at
    :param db_user: Current user
    :param db_issue:  current Issue the user looks at, used to get the uid of the issue to search at
    :param search_value: users value, which should be the base for searching
    :param mode: form of search the user chooses
    :return: Dictionary with the corresponding search results
    """

    history = db_user.history
    seen_statements = get_seen_statements_from(history[len(history) - 1].path) if history != [] else []

    if is_host_resolved(SEARCH_HOST):
        if is_socket_open(SEARCH_HOST, SEARCH_PORT):
            elastic_results = elastic_search(db_issue, search_value, mode, statement_uid)
            elastic_results['values'] = [item for item in elastic_results.get('values') if
                                         item.get('statement_uid') not in seen_statements]
            return elastic_results
    levensthein_results = __levensthein_search(db_user, db_issue, search_value, mode, statement_uid)
    levensthein_results['values'] = [item for item in levensthein_results.get('values') if
                                     item.get('statement_uid') not in seen_statements]
    return levensthein_results


def __levensthein_search(db_user: User, db_issue: Issue, search_value: str, mode: int, statement_uid: int) -> dict:
    """
    This is the mode-specific equivalent of the Elasticsearch search.
    The D-BAS specific modes are used and packaged in a corresponding response that is expected from the frontend.

    :param db_user: Current user
    :param db_issue: current issue the user looks at, used to get the uid of the issue to search at
    :param search_value: users value, which should be the base for searching
    :param mode: form of search the user chooses
    :param statement_uid: the uid of the statement to be looked at
    :return: Dictionary with the corresponding search results
    """
    return_dict = {'distance_name': MECHANISM}

    if mode in [FuzzyMode.START_STATEMENT, FuzzyMode.START_PREMISE]:  # start statement / premise
        return_dict['values'] = get_suggestions_for_positions(search_value, db_issue.uid, mode == 0)

    elif mode == FuzzyMode.EDIT_STATEMENT:  # edit statement popup
        return_dict['values'] = get_strings_for_edits(search_value, statement_uid)

    elif mode in [FuzzyMode.ADD_REASON, FuzzyMode.FIND_DUPLICATE]:  # adding reasons / duplicates
        return_dict['values'] = get_strings_for_duplicates_or_reasons(search_value, db_issue.uid, statement_uid)

    elif mode == FuzzyMode.FIND_USER:  # getting public nicknames
        return_dict['values'] = get_strings_for_public_nickname(search_value, db_user.global_nickname)

    elif mode in [FuzzyMode.FIND_MERGESPLIT, FuzzyMode.FIND_STATEMENT]:  # search everything
        return_dict['values'] = get_all_statements_with_value(search_value, db_issue.uid)

    return return_dict


def get_all_statements_with_value(search_value: str, issue_uid: int) -> list:
    """
    Returns all statements matching the given search_value

    :param issue_uid: uid of the issue to be searched in
    :param search_value: text to be searched for
    :return: statements matching the given search value in the given issue, uses levensthein.
    """
    issues_statements_uids = [el.statement_uid for el in
                              DBDiscussionSession.query(StatementToIssue).filter_by(issue_uid=issue_uid).all()]
    db_statements = get_enabled_statement_as_query().filter(Statement.uid.in_(issues_statements_uids)).all()
    return_array = []
    slug = DBDiscussionSession.query(Issue).get(issue_uid).slug
    _um = UrlManager(slug=slug)
    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=stat.uid).order_by(
            TextVersion.uid.asc()).first()
        if search_value.lower() in db_tv.content.lower():
            rd = __get_fuzzy_string_dict(current_text=search_value, return_text=db_tv.content, uid=db_tv.statement_uid)
            rd['url'] = _um.get_url_for_statement_attitude(db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:RESULT_LENGTH]


def __get_levensthein_similarity_in_percent(a: str, b: str) -> float:
    """
    This method calculated the levensthein similarity between two string in percent.

    :param a:
    :param b:
    :return: Levensthein distance between two strings in percent.
    """
    if len(a) == 0 or len(b) == 0:
        return 0

    lev_dist: int = int(get_distance(a, b))
    bigger: int = max(len(a), len(b))
    return float((bigger - lev_dist) / bigger)


def get_all_statements_by_levensthein_similar_to(search_value: str) -> dict:
    """
    Returns the top 10 of the matching statements for the search_value.
    This method calculates the the similarity with the levensthein-distance.
    The results are sorted from best to worst match

    :param search_value: text to be searched for
    :return: statements matching the given search by using levensthein-distance(sorted best to worst).
    """
    matching_results = []

    statements = DBDiscussionSession.query(Statement).all()
    for statement in statements:
        textversion: TextVersion = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement.uid).first()
        author: User = DBDiscussionSession.query(User).filter_by(uid=textversion.author_uid).first()
        statement_to_issue: StatementToIssue = DBDiscussionSession.query(StatementToIssue).filter_by(
            statement_uid=statement.uid).first()
        issue: Issue = DBDiscussionSession.query(Issue).filter_by(uid=statement_to_issue.issue_uid).first()
        result: dict = __transform_levensthein_search_results(statement=DataStatement(statement, textversion),
                                                              author=author,
                                                              issue=DataIssue(issue))
        score = int(get_distance(search_value, textversion.content))
        if __get_levensthein_similarity_in_percent(search_value,
                                                   textversion.content) >= SIMILARITY_THRESHOLD_IN_PERCENT:
            matching_results = matching_results + [(result, score)]

    matching_results.sort(key=operator.itemgetter(1), reverse=False)
    matching_results = [result[0] for result in matching_results]
    return matching_results[:RESULT_LENGTH]


def get_all_statements_matching(search_value: str) -> dict:
    """
    This returns all similar statements and the corresponding information for a given search term.
    Either Elasticsearch or the Levensthein distance is used. The default is Levensthein distance.
    If search is running on port 5000, the results will be generated by Elasticsearch.
    It is tested with each request whether the host (search) is reachable or not.

    :param search_value: A word or sentence to be searched for.
    :return: A dictionary containing the results and additional information of the search.
    """
    if is_host_resolved(SEARCH_HOST):
        if is_socket_open(SEARCH_HOST, SEARCH_PORT):
            LOG.debug("Switching to elasticsearch for: %s", search_value)
            search_response = get_statements_with_similarity_to(search_value)
            if "results" not in search_response:
                LOG.warning("Got no results from elasticsearch, response is %s", str(search_response))
                return {}
            return get_statements_with_similarity_to(search_value)["results"]
    LOG.debug("Switching to levensthein fallback for: %s", search_value)
    return get_all_statements_by_levensthein_similar_to(search_value)


def get_suggestions_for_positions(search_value: str, issue_uid: int, position: bool) -> list:
    """
    Checks different position-strings for a match with given value

    :param search_value: text to be searched for
    :param issue_uid: uid of the issue to be searched in
    :param position: position of the statement
    :return: suggestions for statements with a certain position matching the search_value
    """
    statement2issues_uid = [el.statement_uid for el in
                            DBDiscussionSession.query(StatementToIssue).filter_by(issue_uid=issue_uid).all()]
    db_statements = get_enabled_statement_as_query().filter(Statement.is_position == position,
                                                            Statement.uid.in_(statement2issues_uid)).all()
    return_array = []
    for stat in db_statements:
        db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=stat.uid).order_by(
            TextVersion.uid.asc()).first()
        if search_value.lower() in db_tv.content.lower():
            rd = __get_fuzzy_string_dict(current_text=search_value, return_text=db_tv.content, uid=db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:RESULT_LENGTH]


def get_strings_for_edits(search_value: str, statement_uid: int) -> list:
    """
    Returns suggestions for edits of certain statement matching search_value.

    :param search_value: text to be searched for
    :param statement_uid: the uid of the statement with edits
    :return: suggestions for edits of a certain statement matching the search_value
    """
    db_tvs = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement_uid).all()

    return_array = []
    for textversion in db_tvs:
        if search_value.lower() in textversion.content.lower():
            rd = __get_fuzzy_string_dict(current_text=search_value, return_text=textversion.content,
                                         uid=textversion.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:RESULT_LENGTH]


def get_strings_for_duplicates_or_reasons(search_value: str, issue_uid: int, statement_uid: int) -> list:
    """
    Checks different textversion-strings for a match with given value

    :param search_value: string
    :param issue_uid: Issue.uid
    :param statement_uid: integer
    :return: dict()
    """
    issues_statements_uids = [el.statement_uid for el in
                              DBDiscussionSession.query(StatementToIssue).filter_by(issue_uid=issue_uid).all()]
    db_statements = get_enabled_statement_as_query().filter(Statement.uid.in_(issues_statements_uids)).all()
    return_array = []

    for stat in db_statements:
        if stat.uid is statement_uid:
            continue

        db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=stat.uid).order_by(
            TextVersion.uid.asc()).first()
        if search_value.lower() in db_tv.content.lower():  # and db_tv.content.lower() != oem_value.lower():
            rd = __get_fuzzy_string_dict(current_text=search_value, return_text=db_tv.content,
                                         uid=db_tv.statement_uid)
            return_array.append(rd)

    return_array = __sort_array(return_array)

    return return_array[:RESULT_LENGTH]


def get_strings_for_search(search_value: str) -> dict:
    """
    Returns all statements which have a substring of the given value

    :param search_value: String
    :return: dict() with Statements.uid as key and 'text', 'distance' as well as 'arguments' as values
    """
    tmp_dict = OrderedDict()
    db_statements = get_enabled_statement_as_query().join(TextVersion,
                                                          Statement.textversion_uid == TextVersion.uid).all()
    for stat in db_statements:
        if search_value.lower() in stat.textversion.content.lower():
            # get distance between input value and saved value
            rd = __get_fuzzy_string_dict(current_text=search_value, return_text=stat.textversion.content, uid=stat.uid)
            tmp_dict[str(stat.uid)] = rd

    tmp_dict = __sort_dict(tmp_dict)
    return_index = list(islice(tmp_dict, RESULT_LENGTH))
    return_dict = OrderedDict()
    for index in return_index:
        return_dict[index] = tmp_dict[index]
    return return_dict


def __get_fuzzy_string_dict(index: int = 0, current_text: str = '', return_text: str = '', uid: int = 0) -> dict:
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
            'html': __highlight_fuzzy_string(return_text, current_text),
            'statement_uid': uid}


def get_strings_for_public_nickname(search_value: str, nickname: str) -> list:
    """
    Returns dictionaries with public nicknames of users, where the nickname containts the value

    :param search_value: String
    :param nickname: current users nickname
    :return: dict()
    """
    db_user = DBDiscussionSession.query(User).filter(
        func.lower(User.public_nickname).contains(func.lower(search_value)),
        ~User.public_nickname.in_(
            [nickname, 'admin', nick_of_anonymous_user])).all()
    return_array = []

    for index, user in enumerate(db_user):
        dist = get_distance(search_value, user.public_nickname)
        return_array.append({
            'index': index,
            'distance': dist,
            'text': user.public_nickname,
            'html': __highlight_fuzzy_string(user.public_nickname, search_value),
            'avatar': get_profile_picture(user)
        })

    return_array = __sort_array(return_array)
    return return_array[:RESULT_LENGTH]


def __sort_array(inlist: list) -> list:
    """
    Returns sorted array, based on the distance

    :param inlist: Array
    :return: Array
    """
    return_list = []
    newlist = sorted(inlist, key=lambda k: k['distance'])

    if MECHANISM == 'SequenceMatcher':  # sort descending
        newlist = reversed(newlist)

    for index, dic in enumerate(newlist):
        dic['index'] = index
        return_list.append(dic)

    return return_list


def __sort_dict(dictionary: dict) -> dict:
    """
    Returns sorted dictionary, based on the distance

    :param dictionary: dict()
    :return: dict()
    """
    dictionary = OrderedDict(sorted(dictionary.items()))
    return_dict = OrderedDict()
    for i in list(dictionary.keys())[0:RESULT_LENGTH]:
        return_dict[i] = dictionary[i]
    if MECHANISM == 'SequenceMatcher':  # sort descending
        return_dict = OrderedDict(sorted(dictionary.items(), key=lambda kv: kv[0], reverse=True))
    else:  # sort ascending
        return_dict = OrderedDict()
        for i in list(dictionary.keys())[0:RESULT_LENGTH]:
            return_dict[i] = dictionary[i]
    return return_dict


def get_distance(string_a: str, string_b: str) -> str:
    """
    Returns the distance between two string. Distance is based on Levensthein or difflibs Sequence Matcher

    :param string_a: String
    :param string_b: String
    :return: distance as zero filled string
    """
    if MECHANISM == 'Levensthein':
        return get_lev_distance(string_a, string_b)
    else:
        return get_difflib_distance(string_a, string_b)


def get_lev_distance(a: str, b: str) -> str:
    """
    Returns the levensthein distance between to strings

    :param a: first string
    :param b: second string
    :return: distance between a and b
    """
    dist = distance(a.strip().lower(), b.strip().lower())
    return str(dist).zfill(RESULT_LENGTH)


def get_difflib_distance(a: str, b: str) -> str:
    """
    Returns the difflib distance between to strings

    :param a: first string
    :param b: second string
    :return: distance between a and b
    """
    matcher = difflib.SequenceMatcher(lambda x: x == " ", a.lower(), b.lower())
    dist = str(round(matcher.ratio() * 100, 1))[:-2]
    return str(dist).zfill(RESULT_LENGTH)


def __highlight_fuzzy_string(target: str, search_value: str) -> str:
    """
    Highlight every existence of target in the search_value with the <em> tag.
    This <em> tag can be replaces with any other tag.

    :param target: the haystack to search in
    :param search_value: the needle to search for target
    :return: a highlighted html string
    """
    res = re.compile(re.escape(search_value), re.IGNORECASE)
    return res.sub('<em>{}</em>'.format(search_value), target)


def __transform_levensthein_search_results(statement: DataStatement, author: User, issue: DataIssue) -> dict:
    """
    This is the json format of the results by searching with Levensthein.

    :param statement: See ApiStatement
    :param author: See ApiAuthor
    :param issue: See ApiIssue
    :return: The data-structure which is used for the results in the searching interface.
    """
    return {
        "isPosition": statement.isPosition,
        "uid": statement.uid,
        "text": statement.text,
        "author": author,
        "issue": issue
    }
