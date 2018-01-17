"""
Namespace for functions used to resolve Queries on the database for GraphQL.

.. sectionauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""
from typing import Dict


def resolve_list_query(args: Dict, context, graph):
    """
    Query a list of objects based on the provided graph / model.
    Removes disabled items and adds all additional arguments as a filter for sqlalchemy.

    :param args: Arguments provided by the GraphQL query
    :param context: retrieve current session
    :param graph: reduced database model
    :return: list of objects matching the criterias
    :rtype: list
    """
    query = graph.get_query(context)

    # just apply the filter to the ones who actually have a 'is_disabled' column
    if any([column == 'is_disabled' for column in dir(query.column_descriptions[0]['entity'])]):
        disabled = args['is_disabled'] if 'is_disabled' in args else False  # this enables querying for disabled rows
        query = query.filter_by(is_disabled=disabled)

    return query.filter_by(**args).all()


def resolve_field_query(args, context, graph):
    """
    Query database fields based on fields.

    :param args:
    :param context:
    :param graph:
    :param fields:
    :return: objects
    """
    query = graph.get_query(context)
    if "uid" in args:
        query = query.get(args.get("uid"))
    else:
        query = query.filter_by(**args).first()
    return query
