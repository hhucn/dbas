from api.references import store_reference
from dbas.tests.utils import TestCaseWithConfig


class TestStoreReference(TestCaseWithConfig):
    def test_valid_reference_should_be_stored(self):
        ref_text = "foo"
        ref = store_reference(ref_text, "kangar.oo", "/schnapspralinen", self.user_christian, self.statement_town,
                              self.issue_town)
        self.assertTrue(ref)
        self.assertEqual(ref.text, ref_text)
        self.assertEqual(self.statement_town.uid, ref.statement_uid)
        self.assertEqual(self.user_christian.uid, ref.author_uid)
