from typing import List

from api.models import DataOrigin, DataAuthor
from api.origins import add_origin_for_list_of_statements
from dbas.database.discussion_model import StatementOrigins
from dbas.tests.utils import TestCaseWithConfig


class TestAssignmentOfOriginsToStatements(TestCaseWithConfig):
    origin = DataOrigin(aggregate_id="foobar", entity_id="1000", version=1000,
                        author=DataAuthor(nickname="anonymous", is_dgep_native=True, uid=1))

    def test_single_statement_and_origin_are_fine(self):
        statementorigins: List[StatementOrigins] = add_origin_for_list_of_statements(self.origin,
                                                                                     [self.first_position_cat_or_dog])
        self.assertIsInstance(statementorigins, list)

    def test_add_origin_for_multiple_statements(self):
        statementorigins: List[StatementOrigins] = add_origin_for_list_of_statements(self.origin,
                                                                                     [self.first_position_cat_or_dog,
                                                                                      self.second_position_cat_or_dog])
        self.assertIsInstance(statementorigins, list)
        self.assertEqual(len(statementorigins), 2)
