# Common library for Export Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, PremiseGroup, MarkedArgument,\
    MarkedStatement, Issue, Settings, Language, ClickedArgument, ClickedStatement
from dbas.input_validator import is_integer
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_statement_as_query, get_not_disabled_arguments_as_query
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from admin.lib import table_mapper, get_rows_of


def get_dump(issue):
    """
    Dump of D-BAS main tables

    :param issue: current issue
    :return: dictionary labeled with enumerated integers, whereby these dicts are named by their table
    """
    ret_dict = dict()
    logger('ExportLib', 'get_dump', 'main')

    db_issue = DBDiscussionSession.query(Issue).get(issue)
    if not db_issue:
        return ret_dict

    ret_dict['issue'] = {'title': db_issue.title, 'info': db_issue.info}

    # getting all users
    ret_dict['user'] = __get_all_users()

    # getting all statements
    ret_dict['statement'], statement_uid_set = __get_all_statements(issue)

    # getting all textversions
    ret_dict['textversion'] = __get_all_textversions(statement_uid_set)

    # getting all arguments
    ret_dict['argument'], argument_uid_set, argument_prgoup_set = __get_all_arguments(issue)

    # getting all premisegroups
    ret_dict['premisegroup'], premisegroup_uid_set = __get_all_premisegroups(argument_prgoup_set)

    # getting all premises
    ret_dict['premise'] = __get_all_premises(issue, premisegroup_uid_set)

    # getting all votes
    ret_dict['marked_argument'] = __get_all_marked_arguments(argument_uid_set)

    # getting all votes
    ret_dict['marked_statement'] = __get_all_marked_statements(statement_uid_set)

    return ret_dict


def __get_all_users():
    """
    Returns all users

    :return: dict()
    """
    db_users = DBDiscussionSession.query(User).all()
    return [user.to_small_dict() for user in db_users]


def __get_all_statements(issue):
    """
    Returns all statements for the issue

    :param issue: Issue.uid
    :return: dict()
    """
    db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
    statement_uid_set = {statement.uid for statement in db_statements}
    statement_dict = [statement.to_dict() for statement in db_statements]
    return statement_dict, statement_uid_set


def __get_all_textversions(statement_uid_set):
    """
    Returns all statements for the issue

    :param statement_uid_set:
    :return: [dict()]
    """
    db_textversions = DBDiscussionSession.query(TextVersion).filter(TextVersion.uid.in_(statement_uid_set)).all()
    return [tv.to_dict() for tv in db_textversions]


def __get_all_arguments(issue):
    """
    Returns all statements for the issue

    :param issue: Issue.uid
    :return: [dict()], [dict()], [dict()]
    """
    db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()
    argument_dict = [arg.to_dict() for arg in db_arguments]
    argument_uid_set = {arg.uid for arg in db_arguments}
    argument_prgoup_set = {arg.premisesgroup_uid for arg in db_arguments}
    return argument_dict, argument_uid_set, argument_prgoup_set


def __get_all_premisegroups(argument_prgoup_set):
    """
    Returns all pgroups for the issue

    :param argument_prgoup_set: [Premisegroup.uid
    :return: [dict()], [dict()]
    """
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


def __get_all_premises(issue, premisegroup_uid_set):
    """
    Returns all statements for the issue

    :param issue: Issue.uid
    :param premisegroup_uid_set: [PremiseGroup.uid]
    :return: [dict()]
    """
    db_premises = DBDiscussionSession.query(Premise).filter(and_(Premise.issue_uid == issue,
                                                                 Premise.premisesgroup_uid.in_(premisegroup_uid_set))).all()
    return [premise.to_dict() for premise in db_premises]


def __get_all_marked_arguments(argument_uid_set):
    """
    Returns all marked arguments

    :param argument_uid_set: [Argument.uid]
    :return: [dict()]
    """
    db_votes = DBDiscussionSession.query(MarkedArgument).filter(MarkedArgument.argument_uid.in_(argument_uid_set)).all()
    return [vote.to_dict() for vote in db_votes]


def __get_all_marked_statements(statement_uid_set):
    """
    Returns all marked statements

    :param statement_uid_set: [Statement.uid]
    :return: [dict()]
    """
    db_votes = DBDiscussionSession.query(MarkedStatement).filter(MarkedStatement.statement_uid.in_(statement_uid_set)).all()
    return [vote.to_dict() for vote in db_votes]


def get_doj_nodes(issue):
    """
    Returns type of tables column

    :param issue: Issue.uid
    :return: dict()
    """
    logger('Export', 'lib', 'get_doj_nodes for {}'.format(issue))
    if is_integer(issue):
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
                               'is_supportive': arg.is_supportive,
                               'conclusion': arg.conclusion_uid})

    return {
        'nodes': nodes,
        'inferences': inferences,
        'undercuts': undercuts
    }


def get_doj_user(user_id, discussion_id):
    """
    Returns user data for the DoJ
    
    :param user_id: User.id 
    :param user_id: Issue.id 
    :return: dict()
    """
    logger('Export', 'lib', 'get_doj_user for {} {}'.format(user_id, discussion_id))
    if not user_id or not is_integer(user_id) or not discussion_id or not is_integer(discussion_id):
        return {}

    db_user = DBDiscussionSession.query(User).get(int(user_id))
    db_issue = DBDiscussionSession.query(Issue).get(int(discussion_id))
    if not db_user or not db_issue:
        return {}

    db_all_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=discussion_id).all()
    db_all_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=discussion_id).all()
    all_statements_ids = [s.uid for s in db_all_statements]
    all_arguments_ids = [s.uid for s in db_all_arguments]
    logger('X', 'X', str(all_arguments_ids))

    asd = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.author_uid == user_id,
                                                                      ClickedArgument.is_valid == True)
    logger('X', 'X', str(all_arguments_ids))

    # arguments and statements with a star
    db_star_stat = DBDiscussionSession.query(MarkedStatement).filter(MarkedStatement.uid.in_(all_statements_ids),
                                                                     MarkedStatement.author_uid == user_id).all()
    db_star_arg = DBDiscussionSession.query(MarkedArgument).filter(MarkedArgument.uid.in_(all_arguments_ids),
                                                                   MarkedArgument.author_uid == user_id).all()

    # clicked and valid statements and arguments
    db_click_stat = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.statement_uid.in_(all_statements_ids),
                                                                       ClickedStatement.author_uid == user_id,
                                                                       ClickedStatement.is_valid == True)
    db_click_args = DBDiscussionSession.query(ClickedArgument).filter(ClickedArgument.argument_uid.in_(all_arguments_ids),
                                                                      ClickedArgument.author_uid == user_id,
                                                                      ClickedArgument.is_valid == True)
    db_click_acc_stat = db_click_stat.filter(ClickedStatement.is_up_vote == True).all()
    db_click_rej_stat = db_click_stat.filter(ClickedStatement.is_up_vote == False).all()
    db_click_acc_arg = db_click_args.filter(ClickedArgument.is_up_vote == True).all()
    db_click_rej_arg = db_click_args.filter(ClickedArgument.is_up_vote == False).all()

    # acceptd/rejected statements
    accepted_statements = [s.uid for s in db_click_acc_stat]
    rejected_statements = [s.uid for s in db_click_rej_stat]

    # clicked arguments, which are undercuts
    db_rej_arg = DBDiscussionSession.query(Argument).filter(Argument.uid.in_([s.uid for s in db_click_acc_arg]),
                                                            Argument.author_uid == user_id,
                                                            Argument.argument_uid is not None,
                                                            Argument.is_supportive == False,
                                                            Argument.issue_uid == discussion_id).all()

    # acceptd/rejected conclusions
    for el in db_click_acc_arg:
        db_arg = DBDiscussionSession.query(Argument).filter(Argument.uid == el.argument_uid,
                                                            Argument.argument_uid == None).first()
        if db_arg:
            if db_arg.is_supportive:
                accepted_statements += [db_arg.conclusion_uid]
            else:
                rejected_statements += [db_arg.conclusion_uid]

    return {
        'marked_statements': list(set([s.uid for s in db_star_stat])),
        'marked_arguments': list(set([s.uid for s in db_star_arg])),
        'rejected_arguments': list(set([s.uid for s in db_rej_arg] + [s.uid for s in db_click_rej_arg])),
        'accepted_statements_via_click': list(set(accepted_statements)),
        'rejected_statements_via_click': list(set(rejected_statements)),
    }


def get_table_rows(nickname, table_name, ids):
    """
    Returns the rows with given ids from given table

    :param nickname: User.nickname
    :param table_name: Some Table from out database
    :param ids: FK's
    :return: list with table rows
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
    if not db_user:
        _t = Translator('en')
        return {'error': _t.get(_.notLoggedIn)}

    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_user.uid).first()
    db_lang = DBDiscussionSession.query(Language).get(db_settings.lang_uid)
    _t = Translator(db_lang.ui_locales)

    # admin rights?
    if db_user.groups.uid != 1:
        return {'error': _t.get(_.noRights),
                'group': str(db_user.groups.uid)}

    # catch empty input
    if table_name is None or ids is None or len(ids) == 0:
        return {'error': _t.get(_.inputEmpty),
                'table': str(table_name),
                'ids': str(ids)}

    # catch wrong table
    if table_name.lower() not in table_mapper:
        return {'error': _t.get(_.internalKeyError)}

    # catch empty table
    table = table_mapper[table_name.lower()]['table']
    db_elements = DBDiscussionSession.query(table)
    if len(db_elements.all()) == 1:
        return {'error': _t.get(_.internalKeyError),
                'table': table_mapper[table_name.lower()]['name']}

    columns = [r.key for r in table.__table__.columns]

    for bad in ['firstname', 'surname', 'token', 'token_timestamp', 'password', 'email', 'nickname']:
        if bad in columns:
            columns.remove(bad)

    row = db_elements.filter(table.uid.in_(ids))
    try:
        ret_list = get_rows_of(columns, row, '')
    except:
        return {'error': _t.get(_.internalKeyError),
                'table': table_mapper[table_name.lower()]['name']}

    return ret_list
