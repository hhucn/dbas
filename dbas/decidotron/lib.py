from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import DecisionProcess, Statement, Issue, PositionCost
from dbas.lib import LOG


def add_associated_cost(db_issue: Issue, statement: Statement, cost: int) -> None:
    decision_process = DecisionProcess.by_id(db_issue.uid)
    if cost <= decision_process.budget and not decision_process.positions_end:
        associated_cost = PositionCost(statement, cost)
        LOG.debug("Add Cost to position %d. Cost: %d", statement.get_text(), associated_cost.cost)
        DBDiscussionSession.add(associated_cost)


def to_cents(euro: float) -> int:
    return int(euro * 100)
