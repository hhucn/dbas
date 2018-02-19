from search import ROUTE_API


def get_statements_with_value_path(issue_uid: int, search=""):
    suffix = "/statements?id={}&search={}".format(issue_uid, search)
    return ROUTE_API + suffix


def get_duplicates_or_reasons_path(issue_uid: int, statement_uid: int, search=""):
    suffix = "/duplicates_reasons?id={}&statement_uid={}&search={}".format(issue_uid, statement_uid, search)
    return ROUTE_API + suffix


def get_edits_path(issue_uid: int, statement_uid: int, search=""):
    suffix = "/edits?id={}&statement_uid={}&search={}".format(issue_uid, statement_uid, search)
    return ROUTE_API + suffix


def get_suggestions_path(issue_uid: int, is_startpoint: bool, search=""):
    suffix = "/suggestions?id={}&start={}&search={}".format(issue_uid, is_startpoint, search)
    return ROUTE_API + suffix
