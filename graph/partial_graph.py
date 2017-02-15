# Methods to get a partial graph
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
    graph_arg_lists = __climb_graph_down(db_positions)
    return __get_nodes_and_edges(graph_arg_lists)


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
    graph_arg_lists = __climb_graph_down(db_positions)
    return __get_nodes_and_edges(graph_arg_lists)


def __find_position_for_conclusion_of_argument(current_arg, list_todos, list_dones, positions):
    a = [arg.uid for arg in list_todos] if len(list_todos) > 0 else []
    b = [p.uid for p in positions] if len(positions) > 0 else []

    logger('PartialGraph', '__find_position_for_conclusion_of_argument',
           'current_arg: {}, list_todos: {}, list_dones: {}, positions: {}'.format(current_arg.uid, a, list_dones, b))

    list_dones.append(current_arg.uid)
    logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'done ' + str(current_arg.uid))

    if current_arg.conclusion_uid is not None:
        db_statement = DBDiscussionSession.query(Statement).get(current_arg.conclusion_uid)
        if db_statement.is_startpoint:
            if db_statement not in positions:
                logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'conclusion of {} is a position ({})'.format(current_arg.uid, db_statement.uid))
                positions.append(db_statement)

        # just append arguments, where the conclusion is in the premise
        db_tmps = get_all_arguments_by_statement(current_arg.conclusion_uid)
        db_arguments = [arg for arg in db_tmps if arg.conclusion_uid != current_arg.conclusion_uid]
        for arg in db_arguments:
            if arg.uid not in list_dones:
                if arg not in list_todos:
                    list_todos.append(arg)
                    logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'append todo ' + str(arg.uid))

        if len(list_todos) > 0:
            current_arg = list_todos[0]
            del list_todos[0]
            logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'next ' + str(current_arg.uid))
            return __find_position_for_conclusion_of_argument(current_arg, list_todos, list_dones, positions)

        logger('PartialGraph', '__find_position_for_conclusion_of_argument', 'return')
        return positions

    else:
        db_target = DBDiscussionSession.query(Argument).get(current_arg.argument_uid)
        return __find_position_for_conclusion_of_argument(db_target, list_todos, list_dones, positions)


def __climb_graph_down(db_positions):
    logger('PartialGraph', '__climb_graph_down', str([pos.uid for pos in db_positions]))
    graph_arg_lists = {}
    for pos in db_positions:
        args = get_all_arguments_by_statement(pos.uid)
        uid = args[0].uid
        del args[0]
        todos = [arg.uid for arg in args]
        graph = __get_arguments_connected_with_position(uid, todos, [], [])
        graph_arg_lists[str(pos.uid)] = graph
    return graph_arg_lists


def __get_arguments_connected_with_position(uid, list_todos, list_dones, graph_arg_list):
    logger('PartialGraph', '__get_arguments_connected_with_position', 'uid: {}, todos: {}, dones: {}, graph: {}'.format(uid, list_todos, list_dones, graph_arg_list))

    # get argument for the uid
    db_argument = DBDiscussionSession.query(Argument).get(uid)

    # get arguments for the premises
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
    db_premise_args = []
    for premise in db_premises:
        db_premise_args = db_premise_args + get_all_arguments_by_statement(premise.statement_uid)

    # get new todos
    for arg in db_premise_args:
        if arg.uid not in list_todos and arg.uid not in list_dones:
            list_todos.append(arg.uid)

    # all undercuts
    db_undercuts = DBDiscussionSession.query(Argument).filter_by(argument_uid=uid).all()

    # get new todos
    if db_undercuts is not None:
        for arg in db_undercuts:
            if arg.uid not in list_todos and arg.uid not in list_dones:
                list_todos.append(arg.uid)

    # current uid is done and part of graph
    list_dones.append(uid)
    if uid not in graph_arg_list:
        graph_arg_list.append(uid)

    # recursion
    if len(list_todos) > 0:
        uid = list_todos[0]
        del list_todos[0]
        __get_arguments_connected_with_position(uid, list_todos, list_dones, graph_arg_list)
    return graph_arg_list


def __get_nodes_and_edges(graph_arg_list):
    logger('PartialGraph', '__get_nodes_and_edges', str(graph_arg_list))
    edges = []
    nodes = []

    for position_id in graph_arg_list:
        argument_uids = graph_arg_list[str(position_id)]
        for arg in argument_uids:
            db_arg = DBDiscussionSession.query(Argument).get(arg)
            # save all premises
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_arg.premisesgroup_uid).all()

            # save conclusion
            nodes = nodes + [premise.uid for premise in db_premises]
            while db_arg.conclusion_uid is None:
                db_arg = DBDiscussionSession.query(Argument).get(db_arg.argument_uid)
            nodes.append(db_arg.conclusion_uid)

            edges = edges + [[premise.uid, db_arg.conclusion_uid] for premise in db_premises]

    nodes = list(set(nodes))

    logger('PartialGraph', '__get_nodes_and_edges', 'return nodes ({}): {}'.format(len(nodes), nodes))
    logger('PartialGraph', '__get_nodes_and_edges', 'return edges ({}): {}'.format(len(edges), edges))
    return {'nodes': nodes, 'edges': edges}
