# Methods to get a partial graph
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument, Premise, Issue
from dbas.handler.arguments import get_all_statements_for_args
from dbas.lib import get_all_arguments_by_statement
from dbas.logger import logger
from graph.lib import get_d3_data


def get_partial_graph_for_statement(uid: int, db_issue: Issue, path: str):
    """
    Returns the partial graph where the statement is embedded

    :param uid: Statement.uid
    :param db_issue: Issue
    :param path: Users history
    :return: dict()
    """
    logger('PartialGraph', 'main with uid {} and path {}'.format(uid, path.split('?')[0]))
    path = path.split('?')[0]
    if db_issue and len(path) > 1:
        path = path.split(db_issue.slug)[1]

    # if we have a attitude, we are asking for supporting/attacking a conclusion
    if 'attitude' in path:
        db_statement = DBDiscussionSession.query(Statement).get(uid)
        if not db_statement:
            return get_d3_data(db_issue)
        uid = db_statement.uid

    # special case - dont know branche
    if 'justify' in path and '/dontknow' in path:
        db_argument = DBDiscussionSession.query(Argument).get(uid)
        db_premise = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).first()
        uid = db_premise.statement_uid

    # if there is no justify, we have an argument
    if 'justify' not in path and len(path) > 1:
        db_argument = DBDiscussionSession.query(Argument).get(uid)
        db_premise = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_argument.premisegroup_uid).first()
        uid = db_premise.statement_uid
    db_arguments = get_all_arguments_by_statement(uid)

    if db_arguments is None or len(db_arguments) == 0:
        return get_d3_data(db_issue, [DBDiscussionSession.query(Statement).get(uid)], [])

    current_arg = db_arguments[0]
    del db_arguments[0]

    db_positions = __find_position_for_conclusion_of_argument(current_arg, db_arguments, [], [])
    logger('PartialGraph', 'positions are: ' + str([pos.uid for pos in db_positions]))
    graph_arg_lists = __climb_graph_down(db_positions)

    return __return_d3_data(graph_arg_lists, db_issue)


def get_partial_graph_for_argument(uid: int, db_issue: Issue):
    """
    Returns the partial graph where the argument is embedded

    :param uid: Argument.uid
    :param db_issue: Issue.uid
    :param request: Current request object
    :return: dict()
    """
    logger('PartialGraph', str(uid))

    # get argument for the uid
    db_argument = DBDiscussionSession.query(Argument).get(uid)

    db_positions = __find_position_for_conclusion_of_argument(db_argument, [], [], [])
    logger('PartialGraph', 'positions are: ' + str([pos.uid for pos in db_positions]))
    graph_arg_lists = __climb_graph_down(db_positions)

    return __return_d3_data(graph_arg_lists, db_issue)


def __return_d3_data(graph_arg_lists, db_issue: Issue):
    """

    :param graph_arg_lists:
    :param db_issue:
    :param nickname:
    :return:
    """
    logger('PartialGraph', 'main')
    graph_arg_list = []
    for key in graph_arg_lists:
        graph_arg_list += graph_arg_lists[key]
    graph_arg_list = [DBDiscussionSession.query(Argument).get(uid) for uid in list(set(graph_arg_list))]

    graph_stat_list = get_all_statements_for_args(graph_arg_list)
    graph_stat_list = [DBDiscussionSession.query(Statement).get(uid) for uid in graph_stat_list]

    logger('PartialGraph', 'stat_list: {}'.format([stat.uid for stat in graph_stat_list]))
    logger('PartialGraph', 'arg_list: {}'.format([arg.uid for arg in graph_arg_list]))
    return get_d3_data(db_issue, graph_stat_list, graph_arg_list)


def __find_position_for_conclusion_of_argument(current_arg, list_todos, list_dones, positions):
    """

    :param current_arg: Argument
    :param list_todos: List of Arguments
    :param list_dones: List of Argument.uids
    :param positions: List of Statements - return value
    :return:
    """
    a = [arg.uid for arg in list_todos] if len(list_todos) > 0 else []
    b = [p.uid for p in positions] if len(positions) > 0 else []

    logger('PartialGraph',
           'current_arg: {}, list_todos: {}, list_dones: {}, positions: {}'.format(current_arg.uid, a, list_dones, b))

    list_dones.append(current_arg.uid)
    logger('PartialGraph', 'done ' + str(current_arg.uid))

    if current_arg.conclusion_uid is None:
        db_target = DBDiscussionSession.query(Argument).get(current_arg.argument_uid)
        return __find_position_for_conclusion_of_argument(db_target, list_todos, list_dones, positions)

    db_statement = DBDiscussionSession.query(Statement).get(current_arg.conclusion_uid)
    if db_statement.is_position:
        if db_statement not in positions:
            logger('PartialGraph',
                   'conclusion of {} is a position (statement {})'.format(current_arg.uid, db_statement.uid))
            positions.append(db_statement)
    else:
        # just append arguments, where the conclusion is in the premise
        db_tmps = get_all_arguments_by_statement(current_arg.conclusion_uid)
        db_arguments = [arg for arg in db_tmps if arg.conclusion_uid != current_arg.conclusion_uid]
        for arg in db_arguments:
            if arg.uid not in list_dones and arg not in list_todos:
                list_todos.append(arg)
                logger('PartialGraph', 'append todo ' + str(arg.uid))

    # next argument
    if len(list_todos) > 0:
        current_arg = list_todos[0]
        del list_todos[0]
        logger('PartialGraph', 'next ' + str(current_arg.uid))
        return __find_position_for_conclusion_of_argument(current_arg, list_todos, list_dones, positions)

    logger('PartialGraph', 'return')
    return positions


def __climb_graph_down(db_positions):
    """

    :param db_positions:
    :return:
    """
    logger('PartialGraph', str([pos.uid for pos in db_positions]))
    graph_arg_lists = {}
    for pos in db_positions:
        args = get_all_arguments_by_statement(pos.uid)
        logger('PartialGraph', 'Position {} is present in arg: {}'.format(pos.uid, [arg.uid for arg in args]))
        uid = args[0].uid
        del args[0]
        todos = [arg.uid for arg in args]
        graph = __get_argument_net(uid, todos, [], [])
        graph_arg_lists[str(pos.uid)] = graph
    return graph_arg_lists


def __get_argument_net(uid, list_todos, list_dones, graph_arg_list):
    """

    :param uid:
    :param list_todos:
    :param list_dones:
    :param graph_arg_list:
    :return:
    """
    logger('PartialGraph',
           'main with arg uid: {}, todos: {}, dones: {}, graph: {}'.format(uid, list_todos, list_dones, graph_arg_list))
    db_argument = DBDiscussionSession.query(Argument).get(uid)

    # getting all args, where the uid is conclusion
    __append_todos_for_getting_argument_net_with_conclusion(uid, db_argument, list_todos, list_dones)

    # get arguments, where the premises are conclusions
    __append_todos_for_getting_argument_net_with_premises(uid, db_argument, list_todos, list_dones)

    # get new todos for undercuts
    __append_todos_for_getting_argument_net_with_undercuts(uid, list_todos, list_dones)

    # current uid is done and part of graph
    list_dones.append(uid)
    if uid not in graph_arg_list:
        graph_arg_list.append(uid)

    # recursion
    if len(list_todos) > 0:
        uid = list_todos[0]
        del list_todos[0]
        __get_argument_net(uid, list_todos, list_dones, graph_arg_list)

    return graph_arg_list


def __append_todos_for_getting_argument_net_with_conclusion(uid, db_argument, list_todos, list_dones):
    """

    :param uid:
    :param db_argument:
    :param list_todos:
    :param list_dones:
    :return:
    """
    if db_argument.conclusion_uid is not None:
        db_concl_args = DBDiscussionSession.query(Argument).filter(Argument.conclusion_uid == db_argument.conclusion_uid,
                                                                   Argument.is_disabled == False).all()

        # get new todos
        logger('PartialGraph',
               'conclusion ({}) args: {}'.format(db_argument.conclusion_uid, [arg.uid for arg in db_concl_args]))
        for arg in db_concl_args:
            if arg.uid not in list_todos + list_dones + [uid]:
                list_todos.append(arg.uid)


def __append_todos_for_getting_argument_net_with_premises(uid, db_argument, list_todos, list_dones):
    """

    :param uid:
    :param db_argument:
    :param list_todos:
    :param list_dones:
    :return:
    """
    db_premises = DBDiscussionSession.query(Premise).filter(Premise.premisegroup_uid == db_argument.premisegroup_uid,
                                                            Premise.is_disabled == False).all()
    db_premise_args = []
    for premise in db_premises:
        args = get_all_arguments_by_statement(premise.statement_uid)
        db_premise_args += args if args is not None else []

    # get new todos
    logger('PartialGraph', 'premises args: {}'.format([arg.uid for arg in db_premise_args]))
    for arg in db_premise_args:
        if arg.uid not in list_todos and arg.uid not in list_dones and arg.uid != uid:
            list_todos.append(arg.uid)


def __append_todos_for_getting_argument_net_with_undercuts(uid, list_todos, list_dones):
    """

    :param uid:
    :param list_todos:
    :param list_dones:
    :return:
    """
    db_undercuts = DBDiscussionSession.query(Argument).filter_by(argument_uid=uid).all()
    logger('PartialGraph', 'undercut args: {}'.format([arg.uid for arg in db_undercuts]))
    if db_undercuts is not None:
        for arg in db_undercuts:
            if arg.uid not in list_todos + list_dones + [uid]:
                list_todos.append(arg.uid)
