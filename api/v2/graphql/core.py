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
class TextVersionGraph(SQLAlchemyObjectType):
    class Meta:
        model = TextVersion
        exclude_fields = "timestamp"


class StatementGraph(SQLAlchemyObjectType):
    textversions = graphene.Field(TextVersionGraph)

    def resolve_textversions(self, info):
        return resolve_field_query({"statement_uid": self.uid}, info, TextVersionGraph)

    class Meta:
        model = Statement

    @staticmethod
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

    def resolve_statements(self, info):
        return resolve_list_query({"issue_uid": self.uid}, info, StatementGraph, Statement)

    class Meta:
        model = Issue
        exclude_fields = "date"


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
    argument = graphene.Field(ArgumentGraph, uid=graphene.Int(), issue_uid=graphene.Int(), is_supportive=graphene.Boolean())
    arguments = graphene.List(ArgumentGraph, issue_uid=graphene.Int(), is_supportive=graphene.Boolean())
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

    def resolve_statement(self, info, **kwargs):
        return resolve_field_query(kwargs, info, StatementGraph)

    def resolve_statements(self, info, **kwargs):
        return resolve_list_query(kwargs, info, StatementGraph, Statement)

    def resolve_argument(self, info, **kwargs):
        return resolve_field_query(kwargs, info, ArgumentGraph)

    def resolve_arguments(self, info, **kwargs):
        return resolve_list_query(kwargs, info, ArgumentGraph, Argument)

    def resolve_statement_reference(self, info, **kwargs):
        return resolve_field_query(kwargs, info, StatementReferencesGraph)

    def resolve_statement_references(self, info):
        return StatementReferencesGraph.get_query(info).all()

    def resolve_issue(self, info, **kwargs):
        return resolve_field_query(kwargs, info, IssueGraph)

    def resolve_issues(self, info):
        return IssueGraph.get_query(info).all()

    def resolve_premise(self, info, **kwargs):
        return resolve_field_query(kwargs, info, PremiseGraph)

    def resolve_premises(self, info, **kwargs):
        return resolve_list_query(kwargs, info, PremiseGraph, Premise)

    def resolve_premisegroup(self, info, **kwargs):
        return resolve_field_query(kwargs, info, PremiseGroupGraph)

    def resolve_premisegroups(self, info):
        return PremiseGroupGraph.get_query(info).all()

    def resolve_user(self, info, **kwargs):
        return resolve_field_query(kwargs, info, UserGraph)

    def resolve_users(self, info):
        return None

    def resolve_textversions(self, info, **kwargs):
        return resolve_field_query(kwargs, info, TextVersionGraph)
