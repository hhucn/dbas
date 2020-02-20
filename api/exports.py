from typing import List, Set, Dict

from cornice.resource import resource
from pyramid.request import Request
from pyramid.response import Response

from dbas.database.discussion_model import Statement, Argument, Issue, GraphNode
from dbas.validators.discussion import valid_issue_by_slug
from graph.lib import get_graph_nodes


def aif_edges(argument: Argument) -> List[dict]:
    edges = [
        # first the single outgoing edge
        {
            "edgeID": f"argument_edge_out_{argument.uid}",
            "toID": f"statement_{argument.conclusion_uid}" if argument.conclusion else f"argument_{argument.argument_uid}",
            "fromID": f"argument_{argument.uid}"
        }
    ]
    # then all incoming edges (multiple because of premise groups)
    for premise in argument.premises:
        edges.append(
            {
                "edgeID": f"argument_edge_in_{argument.uid}_from_{premise.statement.uid}",
                "toID": f"argument_{argument.uid}",
                "fromID": f"statement_{premise.statement.uid}"
            }
        )

    return edges


def statement_node_to_dot(node: Statement) -> str:
    return f'{node.aif_node()["nodeID"]} [label="{node.get_text()}"];'


def argument_node_to_dot(node: Argument) -> str:
    color = "green" if node.is_supportive else "red"
    return f"{node.aif_node()['nodeID']} [shape=diamond,color=\"{color}\"];"


def aif_edge_to_dot(aif_edge: dict) -> str:
    return f"{aif_edge['fromID']} -> {aif_edge['toID']};"


def aif_export_dict(nodes: Set[GraphNode]) -> Dict[str, List[Dict[str, str]]]:
    return {
        "nodes": [node.aif_node() for node in nodes],
        "edges": sum([aif_edges(node) for node in nodes if isinstance(node, Argument)], [])  # apply concat list
    }


@resource(path=r'{slug}/aif')
class AIF():
    def __init__(self, request, context=None):
        valid_issue_by_slug(request)
        self.issue: Issue = request.validated['issue']
        self.request: Request = request

    def get(self):
        nodes = get_graph_nodes(self.issue)

        return aif_export_dict(nodes)


def dot_export_string(nodes: Set[GraphNode]) -> str:
    return "\n".join(
        [statement_node_to_dot(node) for node in nodes if isinstance(node, Statement)] +
        [argument_node_to_dot(node) for node in nodes if isinstance(node, Argument)] +
        [aif_edge_to_dot(aif_edge) for aif_edge in
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
