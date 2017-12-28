"""
Namespace for functions used to resolve Queries on the database for GraphQL.

.. sectionauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""


def resolve_list_query(args, context, graph):
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
    if args:
        query = query.filter_by(**args)
    return query.all()


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
