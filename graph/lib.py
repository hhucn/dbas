# Common library for Graph Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

import requests
import json

from sqlalchemy import and_
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, TextVersion, Premise, Issue, User, VoteStatement, Statement, \
    StatementSeenBy
from dbas.lib import get_profile_picture
from dbas.query_wrapper import get_not_disabled_arguments_as_query, get_not_disabled_statement_as_query
from dbas.database.initializedb import nick_of_anonymous_user


def get_d3_data(issue, nickname):
    """
    Given an issue, create an dictionary and return it

    :param issue: Current uid of issue
    :return: dictionary
    """
    logger('GraphLib', 'get_d3_data', 'main')
    db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

    # default values
    x = 0
    y = 0
    node_size = 6
    position_size = 6
    issue_size = 8
    edge_size = 90
    edge_size_on_virtual_nodes = 45
    edge_type = 'arrow'

    nodes_array = []
    edges_array = []
    extras_dict = {}
    db_issue = DBDiscussionSession.query(Issue).filter_by(uid=issue).first()
    if not db_issue:
        return {}

    logger('GraphLib', 'get_d3_data', 'issue: ' + db_issue.info)

    db_textversions = DBDiscussionSession.query(TextVersion).all()
    db_statements = get_not_disabled_statement_as_query().filter_by(issue_uid=issue).all()
    db_arguments = get_not_disabled_arguments_as_query().filter_by(issue_uid=issue).all()

    # issue
    node_dict = __get_node_dict(id='issue',
                                label=db_issue.info,
                                size=issue_size,
                                x=x,
                                y=y,
                                type='issue')
    x = (x + 1) % 10
    y += (1 if x == 0 else 0)
    nodes_array.append(node_dict)
    all_node_ids = ['issue']

    # for each statement a node will be added
    all_ids, nodes, edges, extras = __prepare_statements_for_d3_data(db_user, db_statements, db_textversions, x, y,
                                                                     node_size, position_size, edge_size, edge_type)
    all_node_ids += all_ids
    nodes_array += nodes
    edges_array += edges
    extras_dict.update(extras)

    # for each argument edges will be added as well as the premises
    all_ids, nodes, edges, extras = __prepare_arguments_for_d3_data(db_arguments, x, y, edge_size_on_virtual_nodes,
                                                                    edge_size, edge_type)
    all_node_ids += all_ids
    nodes_array += nodes
    edges_array += edges
    extras_dict.update(extras)

    __sanity_check_of_d3_data(all_node_ids, edges_array)

    d3_dict = {'nodes': nodes_array, 'edges': edges_array, 'extras': extras_dict}
    return d3_dict


def get_opinion_data(issue):
    """

    :param issue:
    :return:
    """
    db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
    db_all_seen = DBDiscussionSession.query(StatementSeenBy)
    db_all_votes = DBDiscussionSession.query(VoteStatement)
    ret_dict = dict()
    for statement in db_statements:
        db_seen = len(db_all_seen.filter_by(statement_uid=statement.uid).all())
        db_votes = len(db_all_votes.filter(and_(VoteStatement.statement_uid == statement.uid,
                                                VoteStatement.is_up_vote == True,
                                                VoteStatement.is_valid == True)).all())
        ret_dict[str(statement.uid)] = db_votes / db_seen

    return ret_dict


def get_doj_data(issue):
    """

    :param issue:
    :return:
    """
    logger('GraphLib', 'get_doj_data', 'main')
    url = 'http://localhost:5101/evaluate/dojs?issue=' + str(issue)
    try:
        resp = requests.get(url)
    except Exception as e:
        logger('Graph.lib', 'get_doj_data', 'Error: ' + str(e), error=True)
        return {}

    if resp.status_code == 200:
        doj = json.loads(resp.text)
        return doj['dojs'] if 'dojs' in doj else {}
    else:
        logger('GraphLib', 'get_doj_data', 'status ' + str(resp.status_code), error=True)
        return {}


def __prepare_statements_for_d3_data(db_user, db_statements, db_textversions, x, y, node_size, position_size, edge_size, edge_type):
    all_ids = []
    nodes = []
    edges = []
    extras = {}
    for statement in db_statements:
        text = next((tv for tv in db_textversions if tv.uid == statement.textversion_uid), None)
        text = text.content if text else 'None'
        node_dict = __get_node_dict(id='statement_' + str(statement.uid),
                                    label=text,
                                    size=position_size if statement.is_startpoint else node_size,
                                    x=x,
                                    y=y,
                                    type='position' if statement.is_startpoint else 'statement',
                                    author=__get_author_of_statement(statement.uid, db_user),
                                    editor=__get_editor_of_statement(statement.uid, db_user))
        extras[node_dict['id']] = node_dict
        all_ids.append('statement_' + str(statement.uid))
        x = (x + 1) % 10
        y += (1 if x == 0 else 0)
        nodes.append(node_dict)
        if statement.is_startpoint:
            edge_dict = __get_edge_dict(id='edge_' + str(statement.uid) + '_issue',
                                        source='statement_' + str(statement.uid),
                                        target='issue',
                                        is_attacking='none',
                                        size=edge_size,
                                        edge_type=edge_type)
            edges.append(edge_dict)

    return all_ids, nodes, edges, extras


def __prepare_arguments_for_d3_data(db_arguments, x, y, edge_size_on_virtual_nodes, edge_size, edge_type):
    all_ids = []
    nodes = []
    edges = []
    extras = {}
    for argument in db_arguments:
        counter = 1
        # add invisible point in the middle of the edge (to enable pgroups and undercuts)
        node_dict = __get_node_dict(id='argument_' + str(argument.uid),
                                    label='',
                                    size=0,
                                    x=x,
                                    y=y)
        x = (x + 1) % 10
        y += 1 if x == 0 else 0
        nodes.append(node_dict)
        all_ids.append('argument_' + str(argument.uid))

        # we have an argument with:
        # 1) with one premise and no undercut is done on this argument
        # 2) with at least two premises  one conclusion or an undercut is done on this argument
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
        db_undercuts = DBDiscussionSession.query(Argument).filter_by(argument_uid=argument.uid).all()

        # target of the edge (case 1) or last edge (case 2)
        if argument.conclusion_uid is not None:
            target = 'statement_' + str(argument.conclusion_uid)
        else:
            target = 'argument_' + str(argument.argument_uid)

        if len(db_premises) == 1 and len(db_undercuts) == 0:
            edge_dict = __get_edge_dict(id='edge_' + str(argument.uid) + '_' + str(counter),
                                        source='statement_' + str(db_premises[0].statement_uid),
                                        target=target,
                                        is_attacking=argument.is_supportive,
                                        size=edge_size,
                                        edge_type=edge_type)
            edges.append(edge_dict)

        else:
            # edge from premisegroup to the middle point
            for premise in db_premises:
                edge_dict = __get_edge_dict(id='edge_' + str(argument.uid) + '_' + str(counter),
                                            source='statement_' + str(premise.statement_uid),
                                            target='argument_' + str(argument.uid),
                                            is_attacking=argument.is_supportive,
                                            size=edge_size_on_virtual_nodes,
                                            edge_type='')
                edges.append(edge_dict)
                counter += 1

            # edge from the middle point to the conclusion/argument
            edge_dict = __get_edge_dict(id='edge_' + str(argument.uid) + '_0',
                                        source='argument_' + str(argument.uid),
                                        target=target,
                                        is_attacking=argument.is_supportive,
                                        size=edge_size_on_virtual_nodes,
                                        edge_type=edge_type)
            edges.append(edge_dict)

    return all_ids, nodes, edges, extras


def __sanity_check_of_d3_data(all_node_ids, edges_array):
    """

    :param all_node_ids:
    :param edges_array:
    :return:
    """
    error = False
    for edge in edges_array:
        error = error or edge['source'] not in all_node_ids or edge['target'] not in all_node_ids
    if error:
        logger('GraphLib', 'get_d3_data', 'At least one edge has invalid source or target!', error=True)
    else:
        logger('GraphLib', 'get_d3_data', 'All nodes are connected well')


def __get_author_of_statement(uid, db_user):
    """

    :param uid:
    :param main_page:
    :return:
    """
    if not db_user:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    db_statement = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(TextVersion.uid.asc()).first()
    db_author = DBDiscussionSession.query(User).filter_by(uid=db_statement.author_uid).first()
    gravatar = get_profile_picture(db_author, 40)
    name = db_author.get_global_nickname() if db_user.uid != db_author.uid else db_user.nickname
    return {'name': name, 'gravatar_url': gravatar}


def __get_editor_of_statement(uid, db_user):
    """

    :param uid:
    :param main_page:
    :return:
    """
    if not db_user:
        db_user = DBDiscussionSession.query(User).filter_by(nickname=nick_of_anonymous_user).first()
    db_statement = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=uid).order_by(TextVersion.uid.desc()).first()
    db_editor = DBDiscussionSession.query(User).filter_by(uid=db_statement.author_uid).first()
    gravatar = get_profile_picture(db_editor, 40)
    name = db_editor.get_global_nickname() if db_user.uid != db_editor.uid else db_user.nickname
    return {'name': name, 'gravatar': gravatar}


def __get_node_dict(id, label, size, x, y, type='', author=dict(), editor=dict()):
    """
    Create dictionary for nodes

    :param id:
    :param label:
    :param size:
    :param x:
    :param y:
    :param type:
    :param author:
    :param editor:
    :return:
    """
    return {'id': id,
            'label': label,
            'color': '',
            'size': size,
            'x': x,
            'y': y,
            'type': type,
            'author': author,
            'editor': editor}


def __get_edge_dict(id, source, target, is_attacking, size, edge_type):
    """
    Create dictionary for edges

    :param id:
    :param source:
    :param target:
    :param is_attacking:
    :param size:
    :param edge_type:
    :return:
    """
    return {'id': id,
            'source': source,
            'target': target,
            'is_attacking': is_attacking,
            'size': size,
            'edge_type': edge_type}


def __get_extras_dict(statement):
    """

    :param statement:
    :return:
    """
    db_textversion_author = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement.uid).order_by(TextVersion.uid.asc()).first()
    db_textversion_modifier = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement.uid).order_by(TextVersion.uid.desc()).first()

    db_author   = DBDiscussionSession.query(User).filter_by(uid=db_textversion_author.author_uid).first()
    db_modifier = DBDiscussionSession.query(User).filter_by(uid=db_textversion_modifier.author_uid).first()

    db_votes = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement.uid,
                                                                    VoteStatement.is_up_vote == True,
                                                                    VoteStatement.is_valid == True)).all()

    return_dict = {'text': db_textversion_author.content,
                   'author': db_author.get_global_nickname(),
                   'author_gravatar': get_profile_picture(db_author, 20),
                   'votes': len(db_votes),
                   'was_modified': 'false'}

    if db_modifier.uid != db_author.uid:
        return_dict.update({'modifier': db_modifier.get_global_nickname(),
                            'modifier_gravatar': get_profile_picture(db_modifier, 20),
                            'was_modified': 'true'})

    return return_dict
