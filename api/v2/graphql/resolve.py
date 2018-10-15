"""
Namespace for functions used to resolve Queries on the database for GraphQL.
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
    query = __default(query, args, 'is_disabled', False)

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


def __default(query, args, key, default_value):
    """
    Filters a query by a value provided in args or the default given.
    Does nothing if `key` is not in args.

    :param query: The query to filter
    :param args: Arguments for querying. These are not applied yet!
    :param key: A key to look for in the query model
    :param default_value: The value 'key' gets if there is no value in args
    :return:
    """
    # just apply the filter to the ones who actually have a 'is_disabled' column
    if key in dir(query.column_descriptions[0]['entity']):
        disabled = args[key] if key in args else default_value  # this enables querying for disabled rows
        query = query.filter_by(**{key: disabled})

    return query
