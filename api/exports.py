from dataclasses import dataclass
from datetime import datetime
from typing import List, Set, Dict, Callable, Union

from cornice import Service
from cornice.resource import resource
from dateutil import parser
from pyramid.httpexceptions import HTTPConflict, HTTPCreated, HTTPUnauthorized
from pyramid.request import Request
from pyramid.response import Response

from api.login import valid_token
from api.views import LOG, cors_policy
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Statement, Argument, Issue, Language, User, TextVersion, PremiseGroup, \
    GraphNode, Premise
from dbas.validators.core import validate, has_keywords_in_path
from dbas.validators.discussion import valid_issue_by_slug
from graph.lib import get_graph_nodes


@dataclass(frozen=True)
class AIFEdge:
    edgeID: str
    toID: str
    fromID: str

    def to_dot(self) -> str:
        return f"{self.fromID} -> {self.toID};"

    def __json__(self, _request=None):
        return self.__dict__


def aif_edges(argument: Argument) -> List[AIFEdge]:
    # first the outgoing edge
    edges = [
        AIFEdge(
            edgeID=f"argument_{argument.uid}_edge_out",
            toID=f"statement_{argument.conclusion_uid}" if argument.conclusion else f"argument_{argument.argument_uid}",
            fromID=f"argument_{argument.uid}"
        )
    ]
    # then all incoming edges (multiple because of premise groups)
    for premise in argument.premises:
        edges.append(
            AIFEdge(
                edgeID=f"argument_{argument.uid}_edge_in_from_{premise.statement.uid}",
                toID=f"argument_{argument.uid}",
                fromID=f"statement_{premise.statement.uid}"
            )
        )

    return edges


def statement_node_to_dot(node: Statement) -> str:
    return f'{node.aif_node()["nodeID"]} [label="{node.get_text()}"];'


def argument_node_to_dot(node: Argument) -> str:
    color = "green" if node.is_supportive else "red"

    return f"{node.aif_node()['nodeID']} [shape=diamond,color=\"{color}\"];"


def aif_export_dict(nodes: Set[GraphNode]) -> Dict[str, List[Dict[str, str]]]:
    return {
        "nodes": [node.aif_node() for node in nodes],
        "edges": sum([aif_edges(node) for node in nodes if isinstance(node, Argument)], [])  # apply concat list
    }


def is_statement(node) -> bool:
    return node["type"] == "I"


def is_argument(node) -> bool:
    return node["type"] in {"CA", "RA"}


def group_by(f: Callable[[any], any], coll, mod=None) -> Dict[any, List[any]]:
    output = {}

    for element in coll:
        key = f(element)
        element = element if not mod else mod(element)
        if key in output:
            output[key].append(element)
        else:
            output[key] = [element]

    return output


class AIFContext:
    author: User
    issue: Issue
    aif: dict
    to_from_map: Dict[str, List[any]]
    indexed_aif: Dict[str, dict]
    statements: Dict[any, Statement]

    def __init__(self, author: User, issue: Issue, aif: dict):
        self.author = author
        self.issue = issue
        self.aif = aif
        self.to_from_map = group_by(lambda edge: edge["toID"], self.aif["edges"], mod=lambda edge: edge["fromID"])
        self.indexed_aif = {node["nodeID"]: node for node in self.aif["nodes"]}
        self.statements = {}

    def import_aif(self):
        i_nodes = filter(is_statement, self.aif["nodes"])

        def is_position(i_node) -> bool:
            return i_node["nodeID"] not in [edge["fromID"] for edge in self.aif["edges"]]

        positions = [i_node for i_node in i_nodes if is_position(i_node)]

        new_positions: List[Statement] = [self.add_statement(i_node, is_position=True) for i_node in positions]
        self.issue.positions.extend(new_positions)

    def add_statement(self, i_node, is_position=False) -> Statement:
        statement_id = i_node["nodeID"]

        if statement_id in self.statements:
            return self.statements[statement_id]

        timestamp = parser.parse(i_node["timestamp"])

        new_statement = Statement(is_position)
        self.issue.statements.append(new_statement)

        new_tv = TextVersion(content=i_node["text"],
                             author=self.author,
                             date=timestamp or datetime.now(),
                             statement=new_statement)

        DBDiscussionSession.add(new_tv)

        for argument_id in self.to_from_map.get(statement_id, []):
            argument_node = self.indexed_aif[argument_id]
            self.add_argument(argument_node, new_statement)

        self.statements[statement_id] = new_statement

        return new_statement

    def add_argument(self, argument_node: dict, conclusion: Union[Statement, Argument]) -> Argument:
        new_pg = PremiseGroup(author=self.author)

        is_supportive = argument_node["type"] == "RA"
        new_argument = Argument(premisegroup=new_pg,
                                is_supportive=is_supportive,
                                author=self.author,
                                issue=self.issue,
                                timestamp=parser.parse(argument_node['timestamp']),
                                conclusion=conclusion)

        DBDiscussionSession.add(new_argument)

        aif_premise_ids = self.to_from_map[argument_node["nodeID"]]
        nodes = [self.indexed_aif[premise_id] for premise_id in aif_premise_ids]

        for node in nodes:
            if is_statement(node):
                new_statement = self.add_statement(node)
                new_premise = Premise(new_pg, new_statement, False, author=self.author, issue=self.issue)
                DBDiscussionSession.add(new_premise)
            else:
                self.add_argument(node, conclusion=new_argument)

        return new_argument


aif_endpoint = Service(name='aif_endpoint',
                       path=r'{slug}/aif',
                       description='Discussion Attitude',
                       cors_policy=cors_policy)


@aif_endpoint.get()
@validate(valid_issue_by_slug)
def export_aif(request):
    issue: Issue = request.validated['issue']
    nodes = get_graph_nodes(issue)

    return aif_export_dict(nodes)


@aif_endpoint.post(require_csrf=False)
@validate(valid_token, has_keywords_in_path(("title", str), ("lang", str), location="params"))
def import_aif(request):
    slug: str = request.matchdict["slug"]
    title: str = request.params["title"]
    lang: Language = Language.by_locale(request.params["lang"])
    LOG.debug(f"Import with slug: {slug}")

    user = request.validated["user"]
    if not user.is_admin():
        return HTTPUnauthorized(explanation="Only Admins are allowed to import issues")

    if Issue.by_slug(slug):
        return HTTPConflict(explanation="Issue already exists. Please choose another slug.")

    new_issue = Issue(title, "", "", user, lang, slug=slug)
    DBDiscussionSession.add(new_issue)

    AIFContext(user, new_issue, request.json_body).import_aif()

    return HTTPCreated()


def dot_export_string(nodes: Set[GraphNode]) -> str:
    return "\n".join(
        [statement_node_to_dot(node) for node in nodes if isinstance(node, Statement)] +
        [argument_node_to_dot(node) for node in nodes if isinstance(node, Argument)] +
        [aif_edge.to_dot() for aif_edge in
         sum([aif_edges(node) for node in nodes if isinstance(node, Argument)], [])]
    )


@resource(path=r'{slug}/dot')
class Dot():
    def __init__(self, request, context=None):
        valid_issue_by_slug(request)
        self.issue: Issue = request.validated['issue']
        self.request: Request = request

    def get(self):
        nodes = get_graph_nodes(self.issue)

        response: Response = self.request.response
        response.text = f"digraph G {{\n{dot_export_string(nodes)}\n}}"
        response.content_type = "text/vnd.graphviz"

        return response
