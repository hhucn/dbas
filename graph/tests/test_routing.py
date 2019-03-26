from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig
from graph.views import get_d3_complete_dump, get_d3_partial_dump


class ViewTest(TestCaseWithConfig):
    def test_get_d3_complete_dump(self):
        request = construct_dummy_request()
        ret_dict = get_d3_complete_dump(request)
        self.assertEqual(400, ret_dict.status_code)

        request = construct_dummy_request({'issue': 0})
        ret_dict = get_d3_complete_dump(request)
        self.assertEqual(400, ret_dict.status_code)

        request = construct_dummy_request({'issue': 4})
        ret_dict = get_d3_complete_dump(request)
        self.assertEqual(0, len(ret_dict.get('error', '')))

    def test_get_d3_partial_dump(self):
        request = construct_dummy_request()
        ret_dict = get_d3_partial_dump(request)
        self.assertEqual(400, ret_dict.status_code)

        request = construct_dummy_request({'issue': 2, 'uid': 2})
        ret_dict = get_d3_partial_dump(request)
        self.assertEqual(400, ret_dict.status_code)

        request = construct_dummy_request({'issue': 2, 'uid': 2, 'is_argument': False})
        ret_dict = get_d3_partial_dump(request)
        self.assertEqual(400, ret_dict.status_code)

        request = construct_dummy_request({'issue': 2, 'uid': 2, 'is_argument': False, 'path': ''})
        ret_dict = get_d3_partial_dump(request)
        self.assertEqual('', ret_dict.get('error', 'X'))

        request = construct_dummy_request({'issue': 2, 'uid': 12, 'is_argument': True, 'path': ''})
        ret_dict = get_d3_partial_dump(request)
        self.assertEqual('', ret_dict.get('error', 'X'))
