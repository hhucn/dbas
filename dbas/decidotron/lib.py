from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import DecisionProcess, Statement, Issue, PositionCost
from dbas.lib import LOG


def add_associated_cost(db_issue: Issue, statement: Statement, cost: int) -> None:
    decision_process = DecisionProcess.by_id(db_issue.uid)

    if cost < decision_process.min_position_cost:
        raise ValueError(f'The costs of {cost} are lower then the {decision_process.min_position_cost} allowed.')

    if (decision_process.max_position_cost or decision_process.budget) < cost:
        raise ValueError(
            f'The costs of {cost} are higher then the {decision_process.max_position_cost or decision_process.budget} allowed.')

    if decision_process.position_ended():
        raise ValueError('The phase to add positions has ended!')

    associated_cost = PositionCost(statement, cost)
    LOG.debug(f"Add Cost to position {statement.get_text()}. Cost: {associated_cost.cost}")
    DBDiscussionSession.add(associated_cost)


def to_cents(euro: float) -> int:
    return int(euro * 100)
