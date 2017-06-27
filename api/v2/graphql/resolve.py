"""
Namespace for functions used to resolve Queries on the database for GraphQL.

.. sectionauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""


def resolve_statements_query(args, context, graph, model):
    query = graph.get_query(context).filter(model.is_disabled == False)
    if args.get("is_startpoint"):
        query = query.filter(model.is_startpoint)
    return query.all()


def resolve_list_query(args, context, graph, model):
    query = graph.get_query(context).filter(model.is_disabled == False)
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
    if query and not query.is_disabled:
        return query
