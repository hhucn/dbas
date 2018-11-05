from typing import List

from api.models import DataOrigin
from api.origins import add_origin_for_list_of_statements
from dbas.database.discussion_model import StatementOrigins
from dbas.tests.utils import TestCaseWithConfig


class TestAssignmentOfOriginsToStatements(TestCaseWithConfig):
    origin = DataOrigin(aggregate_id="foobar", entity_id="1000", author="i am groot", version=1000)

    def test_single_statement_and_origin_are_fine(self):
        statementorigins: List[StatementOrigins] = add_origin_for_list_of_statements(self.origin, [1])
        self.assertIsInstance(statementorigins, list)

    def test_add_origin_for_multiple_statements(self):
        statementorigins: List[StatementOrigins] = add_origin_for_list_of_statements(self.origin, [1, 2])
        self.assertIsInstance(statementorigins, list)
        self.assertEqual(len(statementorigins), 2)
