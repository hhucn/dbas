import graphene
from cornice import Service
from graphene_sqlalchemy import SQLAlchemyObjectType

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement as StatementModel

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
# GraphQL

class Statement(SQLAlchemyObjectType):
    class Meta:
        model = StatementModel


class Query(graphene.ObjectType):
    statements = graphene.List(Statement)

    def resolve_statements(self, args, context, info):
        query = Statement.get_query(context)  # SQLAlchemy query
        return query.all()


schema = graphene.Schema(query=Query)


# -----------------------------------------------------------------------------
# Routes

@query.get()
def query_route(request):
    """
    Query database based on Facebook's GraphQL Library.
    Parameters must be coded into a "q" GET parameter, e.g.
    `curl "localhost:4284/api/v2/query?q=query\{statements\{uid,isStartpoint\}\}"`

    :return: JSON containing queried data
    """
    q = request.params.get("q")
    if q:
        result = schema.execute(q, context_value={'session': DBDiscussionSession})
        return result.data
    return {"errors": {"message": "No valid query provided."}}
