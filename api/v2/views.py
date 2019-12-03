import graphene
from cornice import Service

from api.v2.query.core import Query
from dbas.database import DBDiscussionSession

#
# CORS configuration
#
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
                   origins=('*',),
                   credentials=True,  # TODO: how can i use this?
                   max_age=42)

# -----------------------------------------------------------------------------
# Route Definitions

query = Service(name='query',
                path='/query',
                description="Query database",
                cors_policy=cors_policy)


# -----------------------------------------------------------------------------
# Routes

@query.get()
def query_route(request):
    r"""
    Query database based on Facebook's GraphQL Library.
    Parameters must be coded into a "q" GET parameter, e.g.
    `curl "localhost:4284/api/v2/query?q=query\{statements\{uid,isStartpoint\}\}"`

    :return: JSON containing queried data
    """
    q = request.params.get("q")
    if q:
        schema = graphene.Schema(query=Query)
        result = schema.execute(q, context_value={'session': DBDiscussionSession})
        if result.errors:
            return {"errors": {"message": "Not all requested parameters could be queried. Some fields are not "
                                          "allowed, e.g. the password.",
                               "exception": str(result.errors)}}
        return result.data
    return {"errors": {"message": "No valid query provided."}}
