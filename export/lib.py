# Common library for Export Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

from dbas.lib import sql_timestamp_pretty_print
from dbas.input_validator import Validator
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, VoteArgument,\
    VoteStatement, Issue
from dbas.query_wrapper import get_not_disabled_statement_as_query, get_not_disabled_arguments_as_query


def get_dump(issue, lang):
    """

    :param issue: current issue
    :param lang: current lang
    :return: dictionary labeled with enumerated integeres, whereby these dicts are named by their table
    """
    ret_dict = dict()
    logger('ExportLib', 'get_dump', 'main')

    db_issue = DBDiscussionSession.query(Issue).filter_by(uid=issue).first()
    if not db_issue:
        return ret_dict

    ret_dict['issue'] = {'title': db_issue.title, 'info': db_issue.info}

    # getting all users
    ret_dict['user'] = __get_all_users()

    # getting all statements
    ret_dict['statement'], statement_uid_set = __get_all_statements(issue)

    # getting all textversions
    ret_dict['textversion'] = __get_all_textversions(statement_uid_set, lang)

    # getting all arguments
    ret_dict['argument'], argument_uid_set, argument_prgoup_set = __get_all_arguments(issue, lang)

    # getting all premisegroups
    ret_dict['premisegroup'], premisegroup_uid_set = __get_all_premisegroups(argument_prgoup_set)

    # getting all premises
    ret_dict['premise'] = __get_all_premises(issue, premisegroup_uid_set, lang)

    # getting all votes
    ret_dict['vote_argument'] = __get_all_votearguments(argument_uid_set)

    # getting all votes
    ret_dict['vote_statement'] = __get_all_votestatements(statement_uid_set)

    return ret_dict


def __get_all_users():
    db_users = DBDiscussionSession.query(User).all()
    user_dict = dict()
    for index, user in enumerate(db_users):
        tmp_dict = dict()
        tmp_dict['uid']         = user.uid
        tmp_dict['nickname']    = user.nickname
        user_dict[str(index)]   = tmp_dict
    return user_dict


def __get_all_statements(issue):
    db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
    statement_uid_set = set()
    statement_dict = dict()
    for index, statement in enumerate(db_statements):
        tmp_dict = dict()
        statement_uid_set.add(statement.uid)
        tmp_dict['uid']             = statement.uid
        tmp_dict['textversion_uid'] = statement.textversion_uid
        tmp_dict['is_startpoint']   = statement.is_startpoint
        statement_dict[str(index)]  = tmp_dict
    return statement_dict, statement_uid_set


def __get_all_textversions(statement_uid_set, lang):
    db_textversions = DBDiscussionSession.query(TextVersion).all()
    textversion_dict = dict()
    for index, textversion in enumerate(db_textversions):
        if textversion.uid in statement_uid_set:
            tmp_dict = dict()
            tmp_dict['uid']              = textversion.uid
            tmp_dict['statement_uid']    = textversion.statement_uid
            tmp_dict['content']          = textversion.content
            tmp_dict['author_uid']       = textversion.author_uid
            tmp_dict['timestamp']        = sql_timestamp_pretty_print(textversion.timestamp, lang)
            textversion_dict[str(index)] = tmp_dict
    return textversion_dict


def __get_all_arguments(issue, lang):
    db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()
    argument_dict = dict()
    argument_uid_set = set()
    argument_prgoup_set = set()
    for index, argument in enumerate(db_arguments):
        tmp_dict = dict()
        argument_uid_set.add(argument.uid)
        argument_prgoup_set.add(argument.premisesgroup_uid)
        tmp_dict['uid']                 = argument.uid
        tmp_dict['premisesgroup_uid']   = argument.premisesgroup_uid
        tmp_dict['conclusion_uid']      = argument.conclusion_uid if argument.conclusion_uid else 0
        tmp_dict['argument_uid']        = argument.argument_uid if argument.argument_uid else 0
        tmp_dict['is_supportive']       = argument.is_supportive
        tmp_dict['author_uid']          = argument.author_uid
        tmp_dict['timestamp']           = sql_timestamp_pretty_print(argument.timestamp, lang)
        argument_dict[str(index)]       = tmp_dict
    return argument_dict, argument_uid_set, argument_prgoup_set


def __get_all_premisegroups(argument_prgoup_set):
    db_premisegroups = DBDiscussionSession.query(PremiseGroup).all()
    premisegroup_dict = dict()
    premisegroup_uid_set = set()
    for index, premisegroup in enumerate(db_premisegroups):
        if premisegroup.uid in argument_prgoup_set:
            tmp_dict = dict()
            premisegroup_uid_set.add(premisegroup.uid)
            tmp_dict['uid']                 = premisegroup.uid
            tmp_dict['author_uid']          = premisegroup.author_uid
            premisegroup_dict[str(index)]   = tmp_dict
    return premisegroup_dict, premisegroup_uid_set


def __get_all_premises(issue, premisegroup_uid_set, lang):
    db_premises = DBDiscussionSession.query(Premise).filter_by(issue_uid=issue).all()
    premise_dict = dict()
    for index, premise in enumerate(db_premises):
        if premise.premisesgroup_uid in premisegroup_uid_set:
            tmp_dict = dict()
            tmp_dict['premisesgroup_uid'] = premise.premisesgroup_uid
            tmp_dict['statement_uid']     = premise.statement_uid
            tmp_dict['is_negated']        = premise.is_negated
            tmp_dict['author_uid']        = premise.author_uid
            tmp_dict['timestamp']         = sql_timestamp_pretty_print(premise.timestamp, lang)
            premise_dict[str(index)]      = tmp_dict
    return premise_dict


def __get_all_votearguments(argument_uid_set):
    db_votes = DBDiscussionSession.query(VoteArgument).all()
    vote_dict = dict()
    for index, vote in enumerate(db_votes):
        if vote.argument_uid in argument_uid_set:
            tmp_dict = dict()
            tmp_dict['uid']          = vote.uid
            tmp_dict['argument_uid'] = vote.argument_uid
            tmp_dict['author_uid']   = vote.author_uid
            tmp_dict['is_up_vote']   = vote.is_up_vote
            tmp_dict['is_valid']     = vote.is_valid
            vote_dict[str(index)]    = tmp_dict
    return vote_dict


def __get_all_votestatements(statement_uid_set):
    db_votes = DBDiscussionSession.query(VoteStatement).all()
    vote_dict = dict()
    for index, vote in enumerate(db_votes):
        if vote.statement_uid in statement_uid_set:
            tmp_dict = dict()
            tmp_dict['uid']           = vote.uid
            tmp_dict['statement_uid'] = vote.statement_uid
            tmp_dict['author_uid']    = vote.author_uid
            tmp_dict['is_up_vote']    = vote.is_up_vote
            tmp_dict['is_valid']      = vote.is_valid
            vote_dict[str(index)]     = tmp_dict
    return vote_dict


def get_minimal_graph_export(issue):
    """
    Returns type of tables column

    :param table: current table
    :param col_name: current columns name
    :return: String or raise NameError
    """
    logger('X', str(issue), str(Validator.is_integer((issue))))
    if Validator.is_integer(issue):
        db_statements = get_not_disabled_statement_as_query().filter_by(issue_uid=issue).all()
        db_arguments = get_not_disabled_arguments_as_query().filter_by(issue_uid=issue).all()
    else:
        db_statements = get_not_disabled_statement_as_query().all()
        db_arguments = get_not_disabled_arguments_as_query().all()

    nodes = [s.uid for s in db_statements]

    inferences = []
    undercuts = []

    # getting all arguments
    for arg in db_arguments:
        # getting premises of current argument
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=arg.premisesgroup_uid).all()
        premises = [p.statement_uid for p in db_premises]

        if arg.conclusion_uid is None:
            # undercut
            undercuts.append({'id': arg.uid,
                              'premises': premises,
                              'conclusion': arg.argument_uid})
        else:
            # not an undercut
            inferences.append({'id': arg.uid,
                               'premises': premises,
                               'conclusion': arg.conclusion_uid})

    return {'nodes': nodes,
            'inferences': inferences,
            'undercuts': undercuts}
