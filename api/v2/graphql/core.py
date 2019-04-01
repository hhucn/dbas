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
from dbas.database.discussion_model import Statement, Issue, TextVersion, User, Language, StatementReference, \
    StatementOrigins, PremiseGroup, Premise, Argument, ClickedArgument, ClickedStatement
from dbas.lib import get_profile_picture
from graph.lib import get_d3_data


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
    class Meta:
        model = Statement

    text = graphene.String()
    textversions = graphene.Field(TextVersionGraph)
    supports = ArgumentGraph.plural()
    rebuts = ArgumentGraph.plural()
    undercuts = ArgumentGraph.plural()

    def resolve_textversions(self, info, **kwargs):
        return resolve_field_query({**kwargs, "statement_uid": self.uid}, info, TextVersionGraph)

    def resolve_text(self: Statement, info):
        return self.get_text()

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

    @staticmethod
    def singular():
        return graphene.Field(StatementGraph, uid=graphene.Int(), is_position=graphene.Boolean(),
                              is_disabled=graphene.Boolean())

    @staticmethod
    def plural():
        return graphene.List(StatementGraph, is_position=graphene.Boolean(), is_disabled=graphene.Boolean())

    flat_statements_below = graphene.Dynamic(lambda: graphene.NonNull(StatementGraph.plural(),
                                                                      description="Returns all texts from the statements in the tree below this statement"))

    def resolve_flat_statements_below(self: Statement, _info):
        return self.flat_statements_below()


class ClickedArgumentNode(SQLAlchemyObjectType):
    class Meta:
        model = ClickedArgument


class ClickedStatementNode(SQLAlchemyObjectType):
    class Meta:
        model = ClickedStatement


class UserGraph(SQLAlchemyObjectType):
    profile_picture = graphene.Field(graphene.String, size=graphene.Int(),
                                     description="The profile picture of the user")
    clicked_statements = graphene.List(ClickedStatementNode, is_valid=graphene.Boolean(), is_up_vote=graphene.Boolean(),
                                       statement_uid=graphene.Int())

    def resolve_profile_picture(self, info, **kwargs):
        return get_profile_picture(self, **kwargs)

    def resolve_clicked_statements(self: User, info, **kwargs):
        return resolve_list_query({**kwargs, "author_uid": self.uid}, info, ClickedStatementNode)

    class Meta:
        model = User
        only_fields = ["uid", "public_nickname", "last_action", "registered", "last_login", "clicked_statements"]


class StatementOriginsGraph(SQLAlchemyObjectType):
    class Meta:
        model = StatementOrigins
        exclude_fields = "created"


class IssueGraph(SQLAlchemyObjectType):
    position = StatementGraph.singular()
    arguments = ArgumentGraph.plural()
    complete_graph = graphene.Field(graphene.JSONString,
                                    description="Returns the data for the whole graph-view as a JSON-String")
    complete_graph_cypher = graphene.Field(graphene.String,
                                           description="Return the graph data as Cypher CREATE statements for Neo4j.",
                                           default_value={})

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

    def resolve_complete_graph(self, info, **kwargs):
        graph, _ = get_d3_data(DBDiscussionSession.query(Issue).get(self.uid))
        return graph

    def resolve_complete_graph_cypher(self, info, **kwargs) -> str:
        def dict2cypher(d: dict) -> str:
            data = ["{key}: \"{data}\"".format(key=key, data=d[key]) for key in d.keys()]
            return "{" + ",".join(data) + "}"

        def node_to_cypher(node: dict) -> str:
            data = {
                'text': node['label'],
                'time': node['timestamp'],
                'author': node['author'].get('name', 'unknown')
            }
            t = node['type'] if node['type'] != "" else "argument"
            return f"CREATE ({node['id']}:{t} {dict2cypher(data)})"

        def edge_to_cypher(edge: dict) -> str:
            if edge['source'].startswith('statement') and edge['target'].startswith('statement'):
                rtype = "support" if edge["color"] == "greene" else "rebut"
                return f"CREATE ({edge['source']})-[:{rtype}]->(:argument)-[:conclusion]->({edge['target']})"
            else:
                if edge['target'].startswith('argument'):
                    if edge['color'] == "red":
                        if edge['edge_type'] == "arrow":
                            rtype = "undercut"
                        else:
                            rtype = "undermine"
                    else:
                        rtype = "support"
                else:
                    rtype = "conclusion"

            return f"CREATE ({edge['source']})-[:{rtype}]->({edge['target']})"

        graph, _ = get_d3_data(DBDiscussionSession.query(Issue).get(self.uid))

        cypher_nodes = [node_to_cypher(node) for node in graph['nodes']]
        cypher_edges = [edge_to_cypher(edge) for edge in graph['edges']]

        return " ".join(cypher_nodes + cypher_edges)


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


class StatementReferenceGraph(SQLAlchemyObjectType):
    class Meta:
        model = StatementReference

    # for legacy support
    users = graphene.Field(UserGraph, deprecation_reason="Use `author` instead")
    issues = graphene.Field(IssueGraph, deprecation_reason="Use `issue` instead")
    statements = graphene.Field(StatementGraph, deprecation_reason="Use `statement` instead")

    def resolve_users(self: StatementReference, info):
        return resolve_field_query({"uid": self.author_uid}, info, UserGraph)

    def resolve_issues(self: StatementReference, info):
        return resolve_field_query({"uid": self.issue_uid}, info, IssueGraph)

    def resolve_statements(self: StatementReference, info):
        return resolve_field_query({"uid": self.statement_uid}, info, StatementGraph)


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
    statement_reference = graphene.Field(StatementReferenceGraph, uid=graphene.Int())
    statement_references = graphene.List(StatementReferenceGraph)
    statement_origin = graphene.Field(StatementOriginsGraph, uid=graphene.Int(), statement_uid=graphene.Int())
    issue = IssueGraph.singular()
    issues = IssueGraph.plural()
    premise = graphene.Field(PremiseGraph, uid=graphene.Int())
    premises = graphene.List(PremiseGraph, premisegroup_uid=graphene.Int())
    premisegroup = graphene.Field(PremiseGroupGraph, uid=graphene.Int())
    premisegroups = graphene.List(PremiseGroupGraph)
    user = graphene.Field(UserGraph, uid=graphene.Int())
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
        return resolve_field_query(kwargs, info, StatementReferenceGraph)

    def resolve_statement_references(self, info, **kwargs):
        return StatementReferenceGraph.get_query(info).all()

    def resolve_statement_origin(self, info, **kwargs):
        return resolve_field_query(kwargs, info, StatementOriginsGraph)

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
