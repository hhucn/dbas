# Common library for Admin Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument, Premise
from dbas.lib import get_all_arguments_by_statement
from dbas.logger import logger


def get_partial_graph_for_statement(uid):
    logger('PartialGraph', 'get_partial_graph_for_statement', str(uid))
    db_arguments = get_all_arguments_by_statement(uid)

    current_arg = db_arguments[0]
    del db_arguments[0]

    db_positions = __find_position_for_conclusion_of_argument(current_arg, db_arguments, [], [])
    graph_lists = {}
    for pos in db_positions:
        args = get_all_arguments_by_statement(pos.uid)
        uid = args[0].uid
        del args[0]
        todos = [arg.uid for arg in args]
        graph = __get_arguments_connected_with_position(uid, todos, [], [])
        graph_lists[str(uid)] = graph
    logger('PartialGraph', 'get_partial_graph_for_statement', str(graph_lists))
    logger('PartialGraph', 'get_partial_graph_for_statement', str(graph_lists))
    logger('PartialGraph', 'get_partial_graph_for_statement', str(graph_lists))


def get_partial_graph_for_argument(uid):
    logger('PartialGraph', 'get_partial_graph_for_argument', str(uid))
    # get argument for the uid
    db_argument = DBDiscussionSession.query(Argument).get(uid)

    # get arguments for the premises
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    db_premise_args = []
    for premise in db_premises:
        db_premise_args = db_premise_args + get_all_arguments_by_statement(premise.statement_uid)

    db_positions = __find_position_for_conclusion_of_argument(db_argument, db_premise_args, [], [])
    graph_lists = {}
    for pos in db_positions:
        args = get_all_arguments_by_statement(pos.uid)
        uid = args[0].uid
        del args[0]
        todos = [arg.uid for arg in args]
        graph = __get_arguments_connected_with_position(uid, todos, [], [])
        graph_lists[str(uid)] = graph
    logger('PartialGraph', 'get_partial_graph_for_argument', str(graph_lists))
    logger('PartialGraph', 'get_partial_graph_for_argument', str(graph_lists))
    logger('PartialGraph', 'get_partial_graph_for_argument', str(graph_lists))


def __find_position_for_conclusion_of_argument(current_arg, list_todos, list_dones, positions):
    a = [arg.uid for arg in list_todos] if len(list_todos) > 0 else []
    b = [p.uid for p in positions] if len(positions) > 0 else []

    logger('PartialGraph', '__find_position_for_conclusion_of_argument',
           'current_arg: {}, list_todos: {}, list_dones: {}, positions: {}'.format(current_arg.uid, a, list_dones, b))
    if current_arg.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).get(current_arg.conclusion_uid)
        if db_statement.is_startpoint:
            if db_statement not in positions:
               #  logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'conclusion of {} is a position ({})'.format(current_arg.uid, db_statement.uid))
                positions.append(db_statement)

            list_dones.append(current_arg.uid)
            # logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'done ' + str(current_arg.uid))

            if len(list_todos) > 0:
                current_arg = list_todos[0]
                del list_todos[0]
                # logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'next ' + str(current_arg.uid))
            else:
                # logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'return')
                return positions

        if current_arg.conclusion_uid is not None:
            db_tmp = get_all_arguments_by_statement(current_arg.conclusion_uid)
            # just append arguments, where the conclusion is in the premise
            db_arguments = [arg for arg in db_tmp if arg.conclusion_uid != current_arg.conclusion_uid]
        else:
            db_arguments = [DBDiscussionSession.query(Argument).get(current_arg.argument_uid)]

        for arg in db_arguments:
            if arg.uid not in list_dones:
                # logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'append todo ' + str(arg.uid))
                list_todos.append(arg)
        return __find_position_for_conclusion_of_argument(current_arg, list_todos, list_dones, positions)

    else:
        db_target = DBDiscussionSession.query(Argument).get(current_arg.argument_uid)
        return __find_position_for_conclusion_of_argument(db_target, list_todos, list_dones, positions)


def __get_arguments_connected_with_position(uid, list_todos, list_dones, graph_list):
    logger('PartialGraph', '__get_arguments_connected_with_position', 'uid: {}, todos: {}, dones: {}, graph: {}'.format(uid, list_todos, list_dones, graph_list))

    # get argument for the uid
    db_argument = DBDiscussionSession.query(Argument).get(uid)

    # get arguments for the premises
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    db_premise_args = []
    for premise in db_premises:
        db_premise_args = db_premise_args + get_all_arguments_by_statement(premise.statement_uid)

    # all undercuts
    db_undercuts = DBDiscussionSession.query(Argument).filter_by(argument_uid=uid).all()

    list_dones.append(uid)
    if uid not in graph_list:
        graph_list.append(uid)

    for arg in db_premise_args:
        if arg.uid not in list_todos and arg.uid not in list_dones:
            list_todos.append(arg.uid)

    if db_undercuts is not None:
        for arg in db_undercuts:
            if arg.uid not in list_todos and arg.uid not in list_dones:
                list_todos.append(arg.uid)

    if len(list_todos) > 0:
        uid = list_todos[0]
        del list_todos[0]
        __get_arguments_connected_with_position(uid, list_todos, list_dones, graph_list)
    else:
        return graph_list
