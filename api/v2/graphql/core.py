import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.v2.graphql.resolve import resolve_statements_query, resolve_field_query
from dbas.database.discussion_model import Statement, Issue, TextVersion


# -----------------------------------------------------------------------------
# Specify database models which should be able to be queried by GraphQL

class StatementGraph(SQLAlchemyObjectType):
    class Meta:
        model = Statement


class IssueGraph(SQLAlchemyObjectType):
    class Meta:
        model = Issue
        exclude_fields = 'date'


class TextVersionGraph(SQLAlchemyObjectType):
    class Meta:
        model = TextVersion
        exclude_fields = 'timestamp'


# -----------------------------------------------------------------------------
# Query-Definition

class Query(graphene.ObjectType):
    statement = graphene.Field(StatementGraph, uid=graphene.Int())
    statements = graphene.List(StatementGraph, is_startpoint=graphene.Boolean())
    issue = graphene.Field(IssueGraph, uid=graphene.Int(), slug=graphene.String(), title=graphene.String())
    issues = graphene.List(IssueGraph)
    textversions = graphene.List(TextVersionGraph)

    def resolve_statement(self, args, context, info):
        return resolve_field_query(args, context, StatementGraph)

    def resolve_statements(self, args, context, info):
        return resolve_statements_query(args, context, StatementGraph, Statement)

    def resolve_issue(self, args, context, info):
        return resolve_field_query(args, context, IssueGraph)

    def resolve_issues(self, args, context, info):
        return IssueGraph.get_query(context).all()

    def resolve_textversions(self, args, context, info):
        return TextVersionGraph.get_query(context).all()
