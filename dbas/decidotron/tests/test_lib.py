from dbas.decidotron.lib import to_cents
from dbas.tests.utils import TestCaseWithConfig


class TestToCents(TestCaseWithConfig):
    def test_euro_only(self):
        input = 4000
        self.assertEqual(to_cents(input), 4000_00, )

    def test_cents_with_dot(self):
        input = 4000.99
        self.assertEqual(to_cents(input), 4000_99)

    def test_cents_with_1_digit(self):
        input = 4000.9
        self.assertEqual(to_cents(input), 4000_90, "one digit cents should be padded with 0.")

    def test_cents_with_3_digits(self):
        input = 4000.999
        self.assertEqual(to_cents(input), 4000_99, "three digit cents should be cut off.")
