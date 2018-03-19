# Common library for Graph Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

import requests

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, TextVersion, Premise, Issue, User, ClickedStatement, Statement, \
    SeenStatement
from dbas.lib import get_profile_picture
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_arguments_as_query, get_not_disabled_statement_as_query

green = '#64DD17'
red = '#F44336'
grey = '#424242'


def get_d3_data(issue, all_statements=None, all_arguments=None):
    """
    Given an issue, create an dictionary and return it

    :param issue: Current uid of issue
    :param all_statements:
    :param all_arguments:
    :return: dictionary
    """
    a = [a.uid for a in all_statements] if all_statements is not None else 'all'
    b = [b.uid for b in all_arguments] if all_arguments is not None else 'all'
    logger('Graph.lib', 'main - statements: {}, arguments: {}'.format(a, b))
    edge_type = 'arrow'
    nodes_array = []
    edges_array = []
    extras_dict = {}
    db_issue = DBDiscussionSession.query(Issue).get(issue)
    if not db_issue:
        return {}

    logger('Graph.lib', 'title: ' + db_issue.title)

    db_textversions = DBDiscussionSession.query(TextVersion).all()
    if all_statements is None:
        all_statements = get_not_disabled_statement_as_query().filter_by(issue_uid=issue).all()

    if all_arguments is None:
        all_arguments = get_not_disabled_arguments_as_query().filter_by(issue_uid=issue).all()

    # issue
    node_dict = __get_node_dict(uid='issue',
                                label=db_issue.info,
                                node_type='issue',
                                timestamp=db_issue.date.timestamp)

    nodes_array.append(node_dict)
    all_node_ids = ['issue']

    # for each statement a node will be added
    all_ids, nodes, edges, extras = __prepare_statements_for_d3_data(all_statements, db_textversions, edge_type)
    all_node_ids += all_ids
    nodes_array += nodes
    edges_array += edges
    extras_dict.update(extras)

    # for each argument edges will be added as well as the premises
    all_ids, nodes, edges, extras = __prepare_arguments_for_d3_data(all_arguments, edge_type)
    all_node_ids += all_ids
    nodes_array += nodes
    edges_array += edges
    extras_dict.update(extras)

    error = __sanity_check_of_d3_data(all_node_ids, edges_array)

    d3_dict = {'nodes': nodes_array, 'edges': edges_array, 'extras': extras_dict}
    logger('Graph.lib', 'end')
    return d3_dict, error


def get_opinion_data(issue):
    """

    :param issue:
    :return:
    """
    db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
    db_all_seen = DBDiscussionSession.query(SeenStatement)
    db_all_votes = DBDiscussionSession.query(ClickedStatement)
    ret_dict = dict()
    for statement in db_statements:
        db_seen = db_all_seen.filter_by(statement_uid=statement.uid).count()
        db_votes = db_all_votes.filter(ClickedStatement.statement_uid == statement.uid,
                                       ClickedStatement.is_up_vote == True,
                                       ClickedStatement.is_valid == True).count()
        ret_dict[str(statement.uid)] = (db_votes / db_seen) if db_seen != 0 else 1

    return ret_dict


def get_doj_data(issue):
    """

    :param issue:
    :return:
    """
    logger('Graph.lib', 'main')
    url = 'http://localhost:5101/evaluate/dojs?issue=' + str(issue)
    try:
        resp = requests.get(url)
    except Exception as e:
        logger('Graph.lib', 'Error: ' + str(e), error=True)
        logger('Graph.lib', 'return empty doj')
        return {}

    if resp.status_code == 200:
        import json
        doj = json.loads(resp.text)
        return doj['dojs'] if 'dojs' in doj else {}
    else:
        logger('Graph.lib', 'status ' + str(resp.status_code), error=True)
        logger('Graph.lib', 'return empty doj')
        return {}


def get_path_of_user(base_url, path, issue):
    """

    :param base_url:
    :param path:
    :param issue:
    :return:
    """
    logger('Graph.lib', 'main ' + path)

    # replace everything what we do not need
    db_issue = DBDiscussionSession.query(Issue).get(issue)
    kill_it = [base_url, '/discuss/', '/discuss', db_issue.slug, '#graph', '#']
    for k in kill_it:
        path = path.replace(k, '')

    # split in current step and history
    if '?history=' in path:
        current, history = path.split('?history=')
        history = history.split('-')
        history += [current]
    else:
        history = [path]

    logger('Graph.lib', 'main ' + str(history))

    tlist = []
    for h in history:
        steps = __get_statements_of_path_step(h)
        if steps:
            tlist += steps

    # return same neighbours
    if len(tlist) > 1:
        ret_list = [x for index, x in enumerate(tlist[: - 1]) if tlist[index] != tlist[index + 1]] + [tlist[- 1]]
    else:
        ret_list = tlist

    logger('Graph.lib', 'returning path ' + str(ret_list))
    return ret_list


def __get_statements_of_path_step(step):
    """

    :param step:
    :return:
    """
    statements = []
    splitted = step.split('/')

    if 'justify' in step and len(splitted) > 2:
        logger('Graph.lib', 'append {} -> {}'.format(splitted[2], 'issue'))
        statements.append([int(splitted[2]), 'issue'])

    # elif 'justify' in step:
    #     if len(splitted) == 4:  # statement
    #         statements.append([int(splitted[2])])
    #     else:  # argument
    #         db_arg = DBDiscussionSession.query(Argument).get(splitted[2])
    #         db_prems = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_arg.premisesgroup_uid)
    #         statements.append([premise.statement_uid for premise in db_prems])

    elif 'reaction' in step:
        collected_arguments = []
        db_argument = DBDiscussionSession.query(Argument).get(splitted[2])
        collected_arguments.append(db_argument)
        while db_argument.argument_uid is not None:
            db_argument = DBDiscussionSession.query(Argument).get(db_argument.argument_uid)
            if db_argument not in collected_arguments:
                collected_arguments.append(db_argument)
        target = db_argument.conclusion_uid

        for arg in collected_arguments:
            db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=arg.premisesgroup_uid)
            for premise in db_premises:
                statements.append([premise.statement_uid, target])
                logger('Graph.lib', 'append {} -> {}'.format(premise.statement_uid, target))

    # reaction / {arg_id_user}
    # justify / {statement_or_arg_id}
    # attitude / * statement_id
    # choose / {is_argument}
    # jump / {arg_id}

    return statements if len(statements) > 0 else None


def __prepare_statements_for_d3_data(db_statements, db_textversions, edge_type):
    """

    :param db_statements:
    :param db_textversions:
    :param edge_type:
    :return:
    """
    logger('Graph.lib', 'def')
    all_ids = []
    nodes = []
    edges = []
    extras = {}
    tv_map = {tv.uid: tv for tv in db_textversions}
    for statement in db_statements:
        text = tv_map[statement.textversion_uid]
        text = text.content if text else 'None'
        node_dict = __get_node_dict(uid='statement_' + str(statement.uid),
                                    label=text,
                                    node_type='position' if statement.is_position else 'statement',
                                    author=__get_author_of_statement(statement.uid),
                                    editor=__get_editor_of_statement(statement.uid),
                                    timestamp=statement.get_first_timestamp().timestamp)
        extras[node_dict['id']] = node_dict
        all_ids.append('statement_' + str(statement.uid))
        nodes.append(node_dict)
        if statement.is_position:
            edge_dict = __get_edge_dict(uid='edge_' + str(statement.uid) + '_issue',
                                        source='statement_' + str(statement.uid),
                                        target='issue',
                                        color=grey,
                                        edge_type=edge_type)
            edges.append(edge_dict)

    return all_ids, nodes, edges, extras


def __prepare_arguments_for_d3_data(db_arguments, edge_type):
    """

    :param db_arguments:
    :param edge_type:
    :return:
    """

    all_ids = []
    nodes = []
    edges = []
    extras = {}
    logger('Graph.lib', 'def')

    # for each argument edges will be added as well as the premises
    for argument in db_arguments:
        counter = 1
        # we have an argument with:
        #  1) with one premise and no undercut is done on this argument
        #  2) with at least two premises  one conclusion or an undercut is done on this argument
        db_premises = DBDiscussionSession.query(Premise).filter(Premise.premisesgroup_uid == argument.premisesgroup_uid,
                                                                Premise.is_disabled == False).all()
        db_undercuts = DBDiscussionSession.query(Argument).filter_by(argument_uid=argument.uid).all()
        # target of the edge (case 1) or last edge (case 2)
        target = 'argument_' + str(argument.argument_uid)
        if argument.conclusion_uid is not None:
            target = 'statement_' + str(argument.conclusion_uid)

        if len(db_premises) == 1 and len(db_undercuts) == 0:
            __add_edge_to_dict(edges, argument, counter, db_premises[0], target, edge_type)
        else:
            __add_edge_and_node_to_dict(edges, nodes, all_ids, argument, counter, db_premises, target, edge_type)

    return all_ids, nodes, edges, extras


def __add_edge_to_dict(edges, argument, counter, premise, target, edge_type):
    edges.append(__get_edge_dict(uid='edge_' + str(argument.uid) + '_' + str(counter),
                                 source='statement_' + str(premise.statement_uid),
                                 target=target,
                                 color=green if argument.is_supportive else red,
                                 edge_type=edge_type))


def __add_edge_and_node_to_dict(edges, nodes, all_ids, argument, counter, db_premises, target, edge_type):
    edge_source = []
    # edge from premisegroup to the middle point
    for premise in db_premises:
        edge_dict = __get_edge_dict(uid='edge_' + str(argument.uid) + '_' + str(counter),
                                    source='statement_' + str(premise.statement_uid),
                                    target='argument_' + str(argument.uid),
                                    color=green if argument.is_supportive else red,
                                    edge_type='')
        edges.append(edge_dict)
        edge_source.append('statement_' + str(premise.statement_uid))
        counter += 1

    # edge from the middle point to the conclusion/argument
    edge_dict = __get_edge_dict(uid='edge_' + str(argument.uid) + '_0',
                                source='argument_' + str(argument.uid),
                                target=target,
                                color=green if argument.is_supportive else red,
                                edge_type=edge_type)
    edges.append(edge_dict)

    # add invisible point in the middle of the edge (to enable pgroups and undercuts)
    node_dict = __get_node_dict(uid='argument_' + str(argument.uid),
                                label='',
                                edge_source=edge_source,
                                edge_target=target,
                                timestamp=argument.timestamp.timestamp)
    nodes.append(node_dict)
    all_ids.append('argument_' + str(argument.uid))


def __sanity_check_of_d3_data(all_node_ids, edges_array):
    """

    :param all_node_ids:
    :param edges_array:
    :return:
    """
    error = False
    for e in edges_array:
        err1 = e['source'] not in all_node_ids
        err2 = e['target'] not in all_node_ids
        if err1:
            logger('Graph.lib', 'Source of {} is not valid'.format(e))
            # logger('Graph.lib', '__sanity_check_of_d3_data', '{} is not in dict of all node ids'.format(e['source']))
        if err2:
            logger('Graph.lib', 'Target of {} is not valid'.format(e))
            # logger('Graph.lib', '__sanity_check_of_d3_data', '{} is not in dict of all node ids'.format(e['target']))
        error = error or err1 or err2
    if error:
        logger('Graph.lib', 'At least one edge has invalid source or target!', error=True)
        logger('Graph.lib', 'List of all node ids: ' + str(all_node_ids))
        return True
    else:
        logger('Graph.lib', 'All nodes are connected well')
        return False


def __get_author_of_statement(uid):
    """

    :param uid:
    :return:
    """
    db_tv = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(
        TextVersion.uid.asc()).first()  # TODO #432
    db_author = DBDiscussionSession.query(User).get(db_tv.author_uid)
    gravatar = get_profile_picture(db_author, 40)
    name = db_author.get_global_nickname()
    return {'name': name, 'gravatar_url': gravatar}


def __get_editor_of_statement(uid):
    """

    :param uid:
    :return:
    """
    db_statement = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(
        TextVersion.uid.desc()).first()  # TODO #432
    db_editor = DBDiscussionSession.query(User).get(db_statement.author_uid)
    gravatar = get_profile_picture(db_editor, 40)
    name = db_editor.get_global_nickname()
    return {'name': name, 'gravatar': gravatar}


def __get_node_dict(uid, label, node_type='', author=None, editor=None, edge_source=None, edge_target=None,
                    timestamp=''):
    """
    Create node dict for D3

    :param uid:
    :param label:
    :param node_type:
    :param author:
    :param editor:
    :param edge_source:
    :param edge_target:
    :param timestamp:
    :return: dict()
    """
    if author is None:
        author = dict()
    if editor is None:
        editor = dict()

    return {'id': uid,
            'label': label,
            'type': node_type,
            'author': author,
            'editor': editor,
            # for virtual nodes
            'edge_source': edge_source,
            'edge_target': edge_target,
            'timestamp': timestamp}


def __get_edge_dict(uid, source, target, color, edge_type):
    """
    Create dictionary for edges

    :param uid:
    :param source:
    :param target:
    :param color:
    :param edge_type:
    :return:
    """
    return {'id': uid,
            'source': source,
            'target': target,
            'color': color,
            'edge_type': edge_type}


def __get_extras_dict(statement):
    """

    :param statement:
    :return:
    """
    db_textversion_author = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement.uid). \
        order_by(TextVersion.uid.asc()).first()  # TODO #432
    db_textversion_modifier = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement.uid). \
        order_by(TextVersion.uid.desc()).first()  # TODO #432

    db_author = DBDiscussionSession.query(User).get(db_textversion_author.author_uid)
    db_modifier = DBDiscussionSession.query(User).get(db_textversion_modifier.author_uid)

    db_votes = DBDiscussionSession.query(ClickedStatement).filter(ClickedStatement.statement_uid == statement.uid,
                                                                  ClickedStatement.is_up_vote == True,
                                                                  ClickedStatement.is_valid == True).all()

    return_dict = {
        'text': db_textversion_author.content,
        'author': db_author.get_global_nickname(),
        'author_gravatar': get_profile_picture(db_author, 20),
        'votes': len(db_votes),
        'was_modified': 'false'
    }

    if db_modifier.uid != db_author.uid:
        return_dict.update({
            'modifier': db_modifier.get_global_nickname(),
            'modifier_gravatar': get_profile_picture(db_modifier, 20),
            'was_modified': 'true'
        })

    return return_dict
