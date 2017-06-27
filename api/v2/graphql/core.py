import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

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
    issue = graphene.Field(IssueGraph, uid=graphene.Int(), title=graphene.String(), slug=graphene.String())
    issues = graphene.List(IssueGraph)
    textversions = graphene.List(TextVersionGraph)

    def resolve_statement(self, args, context, info):
        query = StatementGraph.get_query(context)
        query = query.get(args.get("uid"))
        if not query.is_disabled:
            return query

    def resolve_statements(self, args, context, info):
        query = StatementGraph.get_query(context).filter(Statement.is_disabled == False)
        if args.get("is_startpoint"):
            query = query.filter(Statement.is_startpoint)
        return query.all()

    def resolve_issue(self, args, context, info):
        query = IssueGraph.get_query(context).filter(Issue.is_disabled == False)

        return query

    def resolve_issues(self, args, context, info):
        return IssueGraph.get_query(context).all()

    def resolve_textversions(self, args, context, info):
        return TextVersionGraph.get_query(context).all()
