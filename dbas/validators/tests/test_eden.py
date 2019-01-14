import hypothesis.strategies as st
from hypothesis import given

from dbas.tests.utils import TestCaseWithConfig, construct_dummy_request
from dbas.validators.eden import valid_optional_origin


class ValidOptionalOriginTest(TestCaseWithConfig):
    def test_no_origin_no_problem(self):
        request = construct_dummy_request()
        is_valid = valid_optional_origin(request)
        self.assertTrue(is_valid)
        self.assertIsNone(request.validated["origin"])

    def test_malformed_origin_is_a_bad_request(self):
        request = construct_dummy_request(json_body={
            "origin": {
                "¯\\_(ツ)_/¯": 42
            }
        })
        is_valid = valid_optional_origin(request)
        self.assertFalse(is_valid)

    def test_if_one_required_key_is_present(self):
        request = construct_dummy_request(json_body={
            "origin": {
                "entity-id": 42,
                "aggregate-id": "example.com",
                "author": {
                    "dgep-native": True,
                    "name": "anonymous",
                    "id": 1,
                },
            }
        })
        is_valid = valid_optional_origin(request)
        self.assertFalse(is_valid)

    def test_valid_origin_with_string_version_is_valid(self):
        request = construct_dummy_request(json_body={
            "origin": {
                "entity-id": 42,
                "aggregate-id": "example.com",
                "version": "1000",
                "author": {
                    "dgep-native": True,
                    "name": "anonymous",
                    "id": 1,
                },
            }
        })
        is_valid = valid_optional_origin(request)
        self.assertTrue(is_valid)

    def test_valid_origin_with_int_version_is_valid(self):
        request = construct_dummy_request(json_body={
            "origin": {
                "entity-id": 42,
                "aggregate-id": "example.com",
                "author": {
                    "dgep-native": True,
                    "name": "anonymous",
                    "id": 1,
                },
                "version": 1000
            }
        })
        is_valid = valid_optional_origin(request)
        self.assertTrue(is_valid)

    def test_valid_origin_with_non_number_version_is_invalid(self):
        request = construct_dummy_request(json_body={
            "origin": {
                "entity-id": 42,
                "aggregate-id": "example.com",
                "version": "not a number",
                "author": {
                    "dgep-native": True,
                    "name": "anonymous",
                    "id": 1,
                },
            }
        })
        is_valid = valid_optional_origin(request)
        self.assertFalse(is_valid)

    @given(entity_id=st.text(), aggregate_id=st.text(), version=st.integers())
    def test_all_texts_and_integer_should_be_allowed(self, entity_id, aggregate_id, version):
        if not entity_id or not aggregate_id:
            return
        request = construct_dummy_request(json_body={
            "origin": {
                "entity-id": entity_id,
                "aggregate-id": aggregate_id,
                "version": version,
                "author": {
                    "dgep-native": True,
                    "name": "anonymous",
                    "id": 1,
                },
            }
        })
        is_valid = valid_optional_origin(request)
        self.assertTrue(is_valid)
