# Common library for Graph Component
#
# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de

from sqlalchemy import and_
from dbas.logger import logger
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, TextVersion, Premise, Issue, User, VoteStatement
from dbas.user_management import get_public_profile_picture


grey = '#9E9E9E'
red = '#F44336'
green = '#8BC34A'
blue = '#2196F3'
dark_grey = '#616161'
dark_red = '#D32F2F'
dark_green = '#689F38'
dark_blue = '#1976D2'


def get_d3_data(issue):
    """
    Given an issue, create an dictionary and return it

    :param issue: 
    :return: dictionary
    """
    logger('GraphLib', 'get_d3_data', 'main')

    x = 0
    y = 0
    node_size = 6
    position_size = 6
    issue_size = 8
    edge_size = 2
    edge_type = 'arrow'

    nodes_array = []
    edges_array = []
    extras_dict = {}
    db_issue = DBDiscussionSession.query(Issue).filter_by(uid=issue).first()

    logger('GraphLib', 'get_d3_data', 'issue: ' + db_issue.info)

    db_textversions = DBDiscussionSession.query(TextVersion).all()
    db_statements = DBDiscussionSession.query(Statement).filter_by(issue_uid=issue).all()
    db_arguments = DBDiscussionSession.query(Argument).filter_by(issue_uid=issue).all()

    # issue
    node_dict = __get_node_dict(id='issue',
                                label=db_issue.info,
                                color=blue,
                                size=issue_size,
                                x=x,
                                y=y)
    x = (x + 1) % 10
    y += (1 if x == 0 else 0)
    nodes_array.append(node_dict)
    all_node_ids = ['issue']

    # for each statement a node will be added
    for statement in db_statements:
        text = next((tv for tv in db_textversions if tv.uid == statement.textversion_uid), None)
        text = text.content if text else 'None'
        node_dict = __get_node_dict(id='statement_' + str(statement.uid),
                                    label=text,
                                    color=blue if statement.is_startpoint else grey,
                                    size=position_size if statement.is_startpoint else node_size,
                                    x=x,
                                    y=y)
        extras_dict[node_dict['id']] = node_dict
        all_node_ids.append('statement_' + str(statement.uid))
        x = (x + 1) % 10
        y += (1 if x == 0 else 0)
        nodes_array.append(node_dict)
        if statement.is_startpoint:
            edge_dict = __get_edge_dict(id='edge_' + str(statement.uid) + '_issue',
                                        source='statement_' + str(statement.uid),
                                        target='issue',
                                        color=grey,
                                        size=edge_size,
                                        edge_type=edge_type)
            edges_array.append(edge_dict)

    # for each argument edges will be added as well as the premises
    for argument in db_arguments:
        counter = 1
        # add invisible point in the middle of the edge (to enable pgroups and undercuts)
        node_dict = __get_node_dict(id='argument_' + str(argument.uid),
                                    label='',
                                    color=green if argument.is_supportive else red,
                                    size=0.5,
                                    x=x,
                                    y=y)
        all_node_ids.append('argument_' + str(argument.uid))
        x = (x + 1) % 10
        y += (1 if x == 0 else 0)
        nodes_array.append(node_dict)

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
                                        color=green if argument.is_supportive else red,
                                        size=edge_size,
                                        edge_type=edge_type)
            edges_array.append(edge_dict)
        else:
            # edge from premisegroup to the middle point
            for premise in db_premises:
                edge_dict = __get_edge_dict(id='edge_' + str(argument.uid) + '_' + str(counter),
                                            source='statement_' + str(premise.statement_uid),
                                            target='argument_' + str(argument.uid),
                                            color=green if argument.is_supportive else red,
                                            size=edge_size,
                                            edge_type='')
                edges_array.append(edge_dict)
                counter += 1

            # edge from the middle point to the conclusion/argument
            edge_dict = __get_edge_dict(id='edge_' + str(argument.uid) + '_0',
                                        source='argument_' + str(argument.uid),
                                        target=target,
                                        color=green if argument.is_supportive else red,
                                        size=edge_size,
                                        edge_type=edge_type)
            edges_array.append(edge_dict)

    error = False
    for edge in edges_array:
        error = error or (edge['source'] not in all_node_ids) or (edge['target'] not in all_node_ids)
    if error:
        logger('GraphLib', 'get_d3_data', 'At least one edge has invalid source or target!', error=True)
    else:
        logger('GraphLib', 'get_d3_data', 'All nodes are connected well')

    d3_dict = {'nodes': nodes_array, 'edges': edges_array, 'extras': extras_dict}
    return d3_dict


def __get_node_dict(id, label, color, size, x, y):
    """
    Create dictionary for nodes

    :param id:
    :param label:
    :param color:
    :param size:
    :param x:
    :param y:
    :return:
    """
    return {'id': id,
            'label': label,
            'color': color,
            'size': size,
            'x': x,
            'y': y}


def __get_edge_dict(id, source, target, color, size, edge_type):
    """
    Create dictionary for edges

    :param id:
    :param source:
    :param target:
    :param color:
    :param size:
    :param edge_type:
    :return:
    """
    return {'id': id,
            'source': source,
            'target': target,
            'color': color,
            'size': size,
            'type': edge_type}


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
                   'author': db_author.public_nickname,
                   'author_gravatar': get_public_profile_picture(db_author, 20),
                   'votes': len(db_votes),
                   'was_modified': 'false'}

    if db_modifier.uid != db_author.uid:
        return_dict.update({'modifier': db_modifier.public_nickname,
                            'modifier_gravatar': get_public_profile_picture(db_modifier, 20),
                            'was_modified': 'true'})

    return return_dict
