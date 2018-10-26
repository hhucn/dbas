"""
GraphQL Core. Here are the models listed, which can be queried by GraphQl.

.. sectionauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

import arrow
import graphene
from arrow import Arrow
from graphene import Scalar
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.converter import convert_sqlalchemy_type
from graphql.language import ast
from sqlalchemy_utils import ArrowType

from api.v2.graphql.resolve import resolve_field_query, resolve_list_query
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Issue, TextVersion, User, Language, StatementReferences, \
    StatementOrigins, PremiseGroup, Premise, Argument


class ArrowTypeScalar(Scalar):
    """
    ArrowType Scalar Description
    """

    @staticmethod
    def serialize(a):
        assert isinstance(a, Arrow), (
            'Received not compatible arrowtype "{}"'.format(repr(a))
        )
        return a.format()

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return arrow.get(node.value)

    @staticmethod
    def parse_value(value):
        return arrow.get(value)


@convert_sqlalchemy_type.register(ArrowType)
def convert_column_to_arrow(ttype, column, registry=None):
    return ArrowTypeScalar(description=getattr(column, 'doc', None),
                           required=not (getattr(column, 'nullable', True)))


# -----------------------------------------------------------------------------
# Specify database models which should be able to be queried by GraphQL
class TextVersionGraph(SQLAlchemyObjectType):
    class Meta:
        model = TextVersion
        exclude_fields = "timestamp"


class ArgumentGraph(SQLAlchemyObjectType):
    class Meta:
        model = Argument

    @staticmethod
    def singular():
        return graphene.Field(ArgumentGraph, uid=graphene.Int(), issue_uid=graphene.Int(),
                              is_supportive=graphene.Boolean(), is_disabled=graphene.Boolean())

    @staticmethod
    def plural():
        return graphene.List(ArgumentGraph, issue_uid=graphene.Int(), is_supportive=graphene.Boolean(),
                             is_disabled=graphene.Boolean())


class StatementGraph(SQLAlchemyObjectType):
    text = graphene.String()
    textversions = graphene.Field(TextVersionGraph)
    arguments = ArgumentGraph.plural()
    supports = ArgumentGraph.plural()
    rebuts = ArgumentGraph.plural()
    undercuts = ArgumentGraph.plural()

    def resolve_textversions(self, info, **kwargs):
        return resolve_field_query({**kwargs, "statement_uid": self.uid}, info, TextVersionGraph)

    def resolve_text(self, info, **kwargs):
        return DBDiscussionSession.query(TextVersion).filter(TextVersion.statement_uid == self.uid).order_by(
            TextVersion.timestamp.desc()).first().content

    def resolve_arguments(self, info, **kwargs):
        return resolve_list_query({**kwargs, "conclusion_uid": self.uid}, info, ArgumentGraph)

    def resolve_supports(self, info, **kwargs):
        return resolve_list_query({**kwargs, "is_supportive": True, "conclusion_uid": self.uid}, info, ArgumentGraph)

    def resolve_rebuts(self, info, **kwargs):
        return resolve_list_query({**kwargs, "is_supportive": False, "conclusion_uid": self.uid}, info, ArgumentGraph)

    def resolve_undercuts(self, info, **kwargs):
        # Query for all arguments attacking / supporting this statement
        sq = DBDiscussionSession.query(Argument.uid) \
            .filter(Argument.conclusion_uid == self.uid,
                    Argument.is_disabled == False) \
            .subquery()

        # Query for all arguments, which are attacking the arguments from the query above.
        return ArgumentGraph.get_query(info) \
            .filter_by(**kwargs) \
            .filter(
            Argument.is_disabled == False,
            Argument.argument_uid.in_(sq)
        )

    class Meta:
        model = Statement

    @staticmethod
    def singular():
        return graphene.Field(StatementGraph, uid=graphene.Int(), is_position=graphene.Boolean(),
                              is_disabled=graphene.Boolean())

    @staticmethod
    def plural():
        return graphene.List(StatementGraph, is_position=graphene.Boolean(), is_disabled=graphene.Boolean())


class StatementReferencesGraph(SQLAlchemyObjectType):
    class Meta:
        model = StatementReferences


class StatementOriginsGraph(SQLAlchemyObjectType):
    class Meta:
        model = StatementOrigins
        exclude_fields = "created"


class IssueGraph(SQLAlchemyObjectType):
    position = StatementGraph.singular()
    arguments = ArgumentGraph.plural()

    def resolve_position(self, info, **kwargs):
        return resolve_field_query(kwargs, info, StatementGraph)

    def resolve_arguments(self, info, **kwargs):
        return resolve_list_query({**kwargs, "issue_uid": self.uid}, info, ArgumentGraph)

    class Meta:
        model = Issue

    @staticmethod
    def singular():
        return graphene.Field(IssueGraph, uid=graphene.Int(), slug=graphene.String(), title=graphene.String(),
                              is_disabled=graphene.Boolean())

    @staticmethod
    def plural():
        return graphene.List(IssueGraph, slug=graphene.String(), title=graphene.String(),
                             is_disabled=graphene.Boolean())


class UserGraph(SQLAlchemyObjectType):
    class Meta:
        model = User
        only_fields = ["uid", "public_nickname", "last_action", "registered", "last_login"]


class LanguageGraph(SQLAlchemyObjectType):
    class Meta:
        model = Language


class PremiseGroupGraph(SQLAlchemyObjectType):
    statements = StatementGraph.plural()

    def resolve_statements(self, info, **kwargs):
        premises = DBDiscussionSession.query(Premise).filter(Premise.premisegroup_uid == self.uid).all()
        uids = set([premise.statement_uid for premise in premises])
        query = StatementGraph.get_query(info)

        return query.filter_by(**kwargs).filter(Statement.uid.in_(uids))

    class Meta:
        model = PremiseGroup


class PremiseGraph(SQLAlchemyObjectType):
    class Meta:
        model = Premise


# -----------------------------------------------------------------------------
# Query-Definition

class Query(graphene.ObjectType):
    """
    Main entrypoint for GraphQL. Specifies which fields are accessible via the
    API and which fields from the database are queryable.

    :param graphene.ObjectType: Generic ObjectType for GraphQL
    """

    statement = StatementGraph.singular()
    statements = StatementGraph.plural()
    argument = ArgumentGraph.singular()
    arguments = ArgumentGraph.plural()
    statement_reference = graphene.Field(StatementReferencesGraph, uid=graphene.Int())
    statement_references = graphene.List(StatementReferencesGraph)
    statement_origin = graphene.Field(StatementOriginsGraph, uid=graphene.Int(), statement_uid=graphene.Int())
    issue = IssueGraph.singular()
    issues = IssueGraph.plural()
    premise = graphene.Field(PremiseGraph, uid=graphene.Int())
    premises = graphene.List(PremiseGraph, premisegroup_uid=graphene.Int())
    premisegroup = graphene.Field(PremiseGroupGraph, uid=graphene.Int())
    premisegroups = graphene.List(PremiseGroupGraph)
    user = graphene.Field(UserGraph)
    textversions = graphene.List(TextVersionGraph)

    def resolve_statement(self, info, **kwargs):
        return resolve_field_query(kwargs, info, StatementGraph)

    def resolve_statements(self, info, **kwargs):
        return resolve_list_query(kwargs, info, StatementGraph)

    def resolve_argument(self, info, **kwargs):
        return resolve_field_query(kwargs, info, ArgumentGraph)

    def resolve_arguments(self, info, **kwargs):
        return resolve_list_query(kwargs, info, ArgumentGraph)

    def resolve_statement_reference(self, info, **kwargs):
        return resolve_field_query(kwargs, info, StatementReferencesGraph)

    def resolve_statement_references(self, info, **kwargs):
        return StatementReferencesGraph.get_query(info).all()

    def resolve_statement_origin(self, info, **kwargs):
        return resolve_field_query(kwargs, info,  StatementOriginsGraph)

    def resolve_issue(self, info, **kwargs):
        return resolve_field_query(kwargs, info, IssueGraph)

    def resolve_issues(self, info, **kwargs):
        return resolve_list_query(kwargs, info, IssueGraph)

    def resolve_premise(self, info, **kwargs):
        return resolve_field_query(kwargs, info, PremiseGraph)

    def resolve_premises(self, info, **kwargs):
        return resolve_list_query(kwargs, info, PremiseGraph)

    def resolve_premisegroup(self, info, **kwargs):
        return resolve_field_query(kwargs, info, PremiseGroupGraph)

    def resolve_premisegroups(self, info, **kwargs):
        return PremiseGroupGraph.get_query(info).all()

    def resolve_user(self, info, **kwargs):
        return resolve_field_query(kwargs, info, UserGraph)

    def resolve_users(self, info):
        return None

    def resolve_textversions(self, info, **kwargs):
        return resolve_field_query(kwargs, info, TextVersionGraph)
