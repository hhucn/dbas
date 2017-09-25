"""
GraphQL Core. Here are the models listed, which can be queried by GraphQl.

.. sectionauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.v2.graphql.resolve import resolve_field_query, resolve_list_query
from dbas.database.discussion_model import Statement, Issue, TextVersion, User, Language, StatementReferences, \
    PremiseGroup, Premise, Argument


# -----------------------------------------------------------------------------
# Specify database models which should be able to be queried by GraphQL

class StatementGraph(SQLAlchemyObjectType):
    class Meta:
        model = Statement

    def plural():
        return graphene.List(StatementGraph, is_startpoint=graphene.Boolean(), issue_uid=graphene.Int())


class ArgumentGraph(SQLAlchemyObjectType):
    class Meta:
        model = Argument
        exclude_fields = "timestamp"


class StatementReferencesGraph(SQLAlchemyObjectType):
    class Meta:
        model = StatementReferences
        exclude_fields = "created"


class IssueGraph(SQLAlchemyObjectType):
    statements = StatementGraph.plural()

    def resolve_statements(self, args, context, info):
        return resolve_list_query({**args, "issue_uid": self.uid}, context, StatementGraph, Statement)

    class Meta:
        model = Issue
        exclude_fields = "date"


class TextVersionGraph(SQLAlchemyObjectType):
    class Meta:
        model = TextVersion
        exclude_fields = "timestamp"


class UserGraph(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ["last_action", "last_login", "registered", "token", "token_timestamp", "password", "nickname",
                          "firstname", "surname", "gender", "email", "group_uid", "groups"]


class LanguageGraph(SQLAlchemyObjectType):
    class Meta:
        model = Language


class PremiseGroupGraph(SQLAlchemyObjectType):
    class Meta:
        model = PremiseGroup


class PremiseGraph(SQLAlchemyObjectType):
    class Meta:
        model = Premise
        exclude_fields = ["timestamp"]


# -----------------------------------------------------------------------------
# Query-Definition

class Query(graphene.ObjectType):
    """
    Main entrypoint for GraphQL. Specifies which fields are accessible via the
    API and which fields from the database are queryable.

    :param graphene.ObjectType: Generic ObjectType for GraphQL
    """

    statement = graphene.Field(StatementGraph, uid=graphene.Int(), is_startpoint=graphene.Boolean())
    statements = StatementGraph.plural()
    argument = graphene.Field(ArgumentGraph, uid=graphene.Int(), is_supportive=graphene.Boolean())
    arguments = graphene.List(ArgumentGraph, is_supportive=graphene.Boolean())
    statement_reference = graphene.Field(StatementReferencesGraph, uid=graphene.Int())
    statement_references = graphene.List(StatementReferencesGraph)
    issue = graphene.Field(IssueGraph, uid=graphene.Int(), slug=graphene.String(), title=graphene.String())
    issues = graphene.List(IssueGraph, slug=graphene.String(), title=graphene.String())
    premise = graphene.Field(PremiseGraph, uid=graphene.Int())
    premises = graphene.List(PremiseGraph, premisesgroup_uid=graphene.Int())
    premisegroup = graphene.Field(PremiseGroupGraph, uid=graphene.Int())
    premisegroups = graphene.List(PremiseGroupGraph)
    user = graphene.Field(UserGraph)
    textversions = graphene.List(TextVersionGraph)

    def resolve_statement(self, args, context, info):
        return resolve_field_query(args, context, StatementGraph)

    def resolve_statements(self, args, context, info):
        return resolve_list_query(args, context, StatementGraph, Statement)

    def resolve_argument(self, args, context, info):
        return resolve_field_query(args, context, ArgumentGraph)

    def resolve_arguments(self, args, context, info):
        return resolve_list_query(args, context, ArgumentGraph, Argument)

    def resolve_statement_reference(self, args, context, info):
        return resolve_field_query(args, context, StatementReferencesGraph)

    def resolve_statement_references(self, args, context, info):
        return StatementReferencesGraph.get_query(context).all()

    def resolve_issue(self, args, context, info):
        return resolve_field_query(args, context, IssueGraph)

    def resolve_issues(self, args, context, info):
        return resolve_list_query(args, context, IssueGraph, Issue)

    def resolve_premise(self, args, context, info):
        return resolve_field_query(args, context, PremiseGraph)

    def resolve_premises(self, args, context, info):
        return resolve_list_query(args, context, PremiseGraph, Premise)

    def resolve_premisegroup(self, args, context, info):
        return resolve_field_query(args, context, PremiseGroupGraph)

    def resolve_premisegroups(self, args, context, info):
        return PremiseGroupGraph.get_query(context).all()

    def resolve_user(self, args, context, info):
        return resolve_field_query(args, context, UserGraph)

    def resolve_users(self, args, context, info):
        return None

    def resolve_textversions(self, args, context, info):
        return TextVersionGraph.get_query(context).all()
